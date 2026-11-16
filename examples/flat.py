"""非油画示例：用关键帧制作简单的平面几何动画。"""
import argparse
import math
from anim import Config, Engine, Key, sample
from anim.backends.flat import Flat, FlatFrame
from anim.output import png, video


class Scene:
    def sample(self, t):
        x = sample([Key(0, 60), Key(2.0, 580)], min(t, 2.0))
        y = 165 + 45 * math.sin(t * 4)
        return FlatFrame(
            background=(24, 32, 54),
            shapes=[
                {"kind": "rect", "box": (0, 280, 640, 360), "color": (48, 90, 90)},
                {"kind": "circle", "x": x, "y": y, "r": 32, "color": (255, 186, 92)},
                {"kind": "line", "points": [(30, 275), (610, 275)], "width": 3, "color": (180, 224, 218)},
            ],
        )


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="平面动画示例")
    ap.add_argument("--video", action="store_true", help="渲染完整 MP4")
    args = ap.parse_args()
    eng = Engine(Config(640, 360, 30, 2.0), Scene(), Flat())
    out = video(eng, "out/flat.mp4") if args.video else png(eng, "out/flat.png", 15)
    print(out)
