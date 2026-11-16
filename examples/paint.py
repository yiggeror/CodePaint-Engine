"""程序化笔触示例：证明共用引擎可以在新项目中直接调用。"""
import argparse
import math
import numpy as np
from anim import Config, Engine
from anim.paint import Brush, Paint
from anim.output import png, video

rng = np.random.default_rng(1872)
# 由固定种子生成笔触布局，每次运行可重现。
points = np.column_stack((rng.uniform(0, 1920, 350), rng.uniform(0, 1080, 350)))
hues = rng.random((350, 3))


class Scene:
    def sample(self, t):
        result = []
        for (x, y), (r, g, b) in zip(points, hues):
            drift = 10.0 * math.sin(t * 1.2 + x * 0.003)
            rgb = (0.1 + 0.8 * r, 0.2 + 0.6 * g, 0.4 + 0.5 * b)
            result.append(Brush(x=x, y=y + drift, length=66, width=20,
                                rgb=rgb, angle=0.22 * math.sin(t + y * 0.005),
                                sprite=0, alpha=0.83))
        return result


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="程序化绘画示例")
    ap.add_argument("--video", action="store_true", help="渲染完整 MP4")
    args = ap.parse_args()
    eng = Engine(Config(640, 360, 15, 1.0), Scene(), Paint())
    out = video(eng, "out/paint.mp4") if args.video else png(eng, "out/paint.png", 0)
    print(out)
