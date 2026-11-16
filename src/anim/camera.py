"""通用二维视差和三维透视相机。"""
from __future__ import annotations
from dataclasses import dataclass
import math
import numpy as np


@dataclass(frozen=True)
class Camera2D:
    x: float = 0.0
    y: float = 0.0
    zoom: float = 1.0
    cx: float = 960.0
    cy: float = 540.0

    def project(self, points, depth=1.0) -> np.ndarray:
        """二维投影，depth 较小的图层移动较慢。"""
        p = np.asarray(points, np.float64)
        if p.ndim != 2 or p.shape[1] != 2:
            raise ValueError("二维点坐标需要 N×2 数组")
        return (p - np.array([self.x, self.y])) * np.asarray(depth)[..., None] * self.zoom + [self.cx, self.cy]


@dataclass(frozen=True)
class Camera3D:
    position: tuple[float, float, float]
    target: tuple[float, float, float]
    fov: float = 55.0
    width: int = 1920
    height: int = 1080

    def project(self, points) -> np.ndarray:
        """透视投影；输出屏幕横纵坐标与前向距离，非正距离位于相机后方。"""
        p = np.asarray(points, np.float64)
        if p.ndim != 2 or p.shape[1] != 3:
            raise ValueError("三维点坐标需要 N×3 数组")
        pos = np.asarray(self.position, np.float64)
        forward = np.asarray(self.target, np.float64) - pos
        forward /= np.linalg.norm(forward)
        right = np.cross([0.0, 1.0, 0.0], forward)
        if np.linalg.norm(right) < 1e-9:
            raise ValueError("相机方向不能与世界竖直轴重合")
        right /= np.linalg.norm(right)
        up = np.cross(forward, right)
        d = p - pos
        z = d @ forward
        f = (self.width / 2) / math.tan(math.radians(self.fov) / 2)
        safe = np.where(np.abs(z) < 1e-9, 1e-9, z)
        return np.stack([self.width / 2 + f * (d @ right) / safe,
                         self.height / 2 - f * (d @ up) / safe, z], axis=1)
