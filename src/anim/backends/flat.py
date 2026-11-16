"""平面图形绘制后端：用于非油画作品及简单场景验证。"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
import numpy as np
from anim.core import Config


@dataclass
class FlatFrame:
    background: tuple[int, int, int] = (16, 20, 34)
    shapes: list[dict[str, Any]] = field(default_factory=list)


class Flat:
    """基于 Pillow 的平面图形渲染器。"""

    def draw(self, data: FlatFrame, cfg: Config) -> np.ndarray:
        from PIL import Image, ImageDraw
        im = Image.new("RGB", (cfg.width, cfg.height), data.background)
        dr = ImageDraw.Draw(im)
        for shape in data.shapes:
            kind = shape["kind"]
            color = tuple(shape["color"])
            if kind == "rect":
                dr.rectangle(tuple(shape["box"]), fill=color)
            elif kind == "circle":
                x, y, r = shape["x"], shape["y"], shape["r"]
                dr.ellipse((x-r, y-r, x+r, y+r), fill=color)
            elif kind == "line":
                dr.line([tuple(p) for p in shape["points"]], fill=color, width=int(shape.get("width", 1)))
            elif kind == "poly":
                dr.polygon([tuple(p) for p in shape["points"]], fill=color)
            else:
                raise ValueError(f"未知图形类型：{kind}")
        return np.asarray(im, dtype=np.uint8)
