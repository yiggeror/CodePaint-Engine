"""关键帧插值与故事时间映射。"""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class Key:
    t: float
    value: object


def _ease(x: float, mode: str) -> float:
    if mode == "linear":
        return x
    if mode == "smooth":
        return x * x * (3 - 2 * x)
    if mode == "smoother":
        return x * x * x * (x * (x * 6 - 15) + 10)
    raise ValueError("未知插值模式")


def sample(keys: list[Key], t: float, mode: str = "smooth"):
    """对标量或同维数组插值，边界外保持首尾值。"""
    if not keys:
        raise ValueError("关键帧不能为空")
    ordered = sorted(keys, key=lambda k: k.t)
    times = [k.t for k in ordered]
    if len(set(times)) != len(times):
        raise ValueError("关键帧时间不能重复")
    if t <= times[0]:
        return ordered[0].value
    if t >= times[-1]:
        return ordered[-1].value
    idx = int(np.searchsorted(times, t)) - 1
    a, b = ordered[idx], ordered[idx + 1]
    u = _ease((t - a.t) / (b.t - a.t), mode)
    out = np.asarray(a.value, np.float64) * (1 - u) + np.asarray(b.value, np.float64) * u
    return float(out) if out.ndim == 0 else out


class TimeWarp:
    """把故事时间映射为播放时间；速度曲线允许局部快放或慢放。"""

    def __init__(self, speeds: list[tuple[float, float]], steps: int = 2048):
        if len(speeds) < 2 or steps < 2:
            raise ValueError("至少提供两个速度关键点")
        keys = sorted(speeds)
        xs = np.array([x for x, _ in keys], np.float64)
        vs = np.array([v for _, v in keys], np.float64)
        if xs[0] != 0 or np.any(np.diff(xs) <= 0) or np.any(vs <= 0):
            raise ValueError("速度关键点需要从零开始、时间递增、速度为正")
        self.story = np.linspace(0, xs[-1], steps + 1)
        v = np.interp(self.story[:-1], xs, vs)
        self.film = np.r_[0.0, np.cumsum(np.diff(self.story) / v)]
        self.duration = float(self.film[-1])

    def to_story(self, t: float) -> float:
        return float(np.interp(t, self.film, self.story))

    def to_film(self, story_t: float) -> float:
        return float(np.interp(story_t, self.story, self.film))
