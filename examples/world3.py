"""三维笔触示例：利用真实世界坐标与三维相机投影，再交给笔触绘制器。"""
import argparse
import numpy as np
from anim import Config, Engine
from anim.paint import Paint
from anim.paint.world3 import Path, Env, SB, shade, compose
from anim.paint.light import look
from anim.output import png, video

rng = np.random.default_rng(2026)
points = np.column_stack((
    rng.uniform(-5.5, 5.5, 500),
    rng.uniform(0.1, 4.2, 500),
    rng.uniform(6.0, 15.0, 500),
))
brushes = SB(rng)
brushes.add(points, D=(0.7, 0.3, 0.0), L=0.45, W=0.11, spr=0,
            csh=(0.16, 0.30, 0.46), cli=(0.94, 0.70, 0.34),
            N=(0, 1, 0), flex=0.06)
group = brushes.group(reflect=False, name="悬浮笔触群")
path = Path([
    (0.0, -1.5, 2.1, -7.0, 0.0, 2.1, 12.0, 55.0),
    (1.0, 1.5, 2.1, -7.0, 0.0, 2.1, 12.0, 55.0),
], sigma=0.08)


def current_light(t):
    """启用云影以验证画面受光与风场的完整渲染路径。"""
    data = look(t)
    data["cloudsh"] = 0.4
    return data


class Scene:
    def sample(self, t):
        env = Env(t, path, current_light)
        if not group.visible(env):
            return None
        world_strokes = group.lod(env)
        return compose([shade(env, world_strokes, sway=True)])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="三维笔触示例")
    parser.add_argument("--video", action="store_true", help="输出 MP4")
    args = parser.parse_args()
    eng = Engine(Config(320, 180, 12, 1.0), Scene(), Paint())
    out = video(eng, "out/world3.mp4") if args.video else png(eng, "out/world3.png", 0)
    print(out)
