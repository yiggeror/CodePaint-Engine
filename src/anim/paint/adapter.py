"""把独立笔触或三维场景的投影结果接入通用渲染接口。"""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from anim.core import Config
from . import engine


@dataclass(frozen=True)
class Brush:
    """设计坐标系为 1920×1080；RGB 颜色分量在 0 到 1 之间。"""
    x: float
    y: float
    length: float
    width: float
    rgb: tuple[float, float, float]
    angle: float = 0.0
    alpha: float = 1.0
    sprite: int = 0
    height: float = 0.5
    order: float = 0.0


def pack(brushes: list[Brush]) -> dict:
    """将笔触列表转换为按绘制顺序排序的列式数组。"""
    ordered = sorted(brushes, key=lambda item: item.order)
    return {
        "x": np.array([b.x for b in ordered], np.float32),
        "y": np.array([b.y for b in ordered], np.float32),
        "L": np.array([b.length for b in ordered], np.float32),
        "W": np.array([b.width for b in ordered], np.float32),
        "rgb": np.array([b.rgb for b in ordered], np.float32).reshape(-1, 3),
        "ang": np.array([b.angle for b in ordered], np.float32),
        "a": np.array([b.alpha for b in ordered], np.float32),
        "spr": np.array([b.sprite for b in ordered], np.int32),
        "hb": np.array([b.height for b in ordered], np.float32),
    }


class Paint:
    """程序化油画后端；允许输入 Brush 列表或 world3.compose 的列式数据。"""

    def __init__(self, **settings):
        self.settings = settings

    def draw(self, data, cfg: Config):
        if cfg.width * 9 != cfg.height * 16:
            raise ValueError("当前油画后端使用 16:9 设计画布；通用核心可使用其他尺寸")
        brushes = pack(data) if isinstance(data, (tuple, list)) else data
        return engine.render(brushes, cfg.height, **self.settings)
