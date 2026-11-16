"""动画运行核心：管理帧率、时间采样和可替换的渲染后端。"""
from __future__ import annotations
from dataclasses import dataclass
import math
from typing import Any, Protocol
import numpy as np


@dataclass(frozen=True)
class Config:
    """作品的尺寸、帧率与时长，单位依次为像素、帧每秒、秒。"""
    width: int = 640
    height: int = 360
    fps: int = 30
    duration: float = 3.0

    def __post_init__(self):
        if self.width <= 0 or self.height <= 0 or self.fps <= 0 or self.duration <= 0:
            raise ValueError("画面尺寸、帧率与时长必须大于零")

    @property
    def count(self) -> int:
        """总帧数：末尾只保留小于作品总时长的采样帧。"""
        return int(math.ceil(self.duration * self.fps - 1e-9))


class Scene(Protocol):
    """场景协议：任意实现 sample(t) 的对象都可接入。"""
    def sample(self, t: float) -> Any: ...


class Backend(Protocol):
    """绘制协议：后端负责把场景采样转换为 RGB 数组。"""
    def draw(self, sample: Any, config: Config) -> np.ndarray: ...


class Engine:
    """统一逐帧调度器；无需绑定油画或特定三维渲染方式。"""

    def __init__(self, config: Config, scene: Scene, backend: Backend):
        self.config = config
        self.scene = scene
        self.backend = backend

    def at(self, t: float) -> np.ndarray:
        """计算指定秒数的图像。"""
        if not 0 <= t <= self.config.duration:
            raise ValueError("时间超出作品时长")
        data = self.scene.sample(float(t))
        rgb = np.asarray(self.backend.draw(data, self.config))
        if rgb.shape != (self.config.height, self.config.width, 3):
            raise ValueError("后端返回的 RGB 图像尺寸不正确")
        if rgb.dtype != np.uint8:
            raise TypeError("后端必须返回 uint8 RGB 图像")
        return np.ascontiguousarray(rgb)

    def frame(self, index: int) -> np.ndarray:
        """按帧号渲染，便于独立并行计算不同时间段。"""
        if not 0 <= index < self.config.count:
            raise IndexError("帧号超出范围")
        return self.at(index / self.config.fps)

    def frames(self, start: int = 0, stop: int | None = None):
        """按顺序输出一段帧，stop 为不包含的结束帧号。"""
        if stop is None:
            stop = self.config.count
        if not 0 <= start <= stop <= self.config.count:
            raise ValueError("帧范围无效")
        for i in range(start, stop):
            yield self.frame(i)
