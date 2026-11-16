"""验证非油画后端和油画后端可独立渲染。"""
import numpy as np
from anim import Config, Engine
from anim.backends.flat import Flat, FlatFrame


class FlatScene:
    def sample(self, t):
        return FlatFrame((0, 0, 0), [{"kind": "circle", "x": 12, "y": 12, "r": 4, "color": (255, 0, 0)}])


def test_flat():
    rgb = Engine(Config(32, 18, 10, 1.0), FlatScene(), Flat()).frame(0)
    assert rgb.shape == (18, 32, 3)
    np.testing.assert_equal(rgb[12, 12], [255, 0, 0])


def test_paint():
    from anim.paint import Paint, Brush
    class Painted:
        def sample(self, t):
            return [Brush(960, 540, 180, 80, (1, 0.2, 0.1))]
    rgb = Engine(Config(128, 72, 10, 1.0), Painted(), Paint()).frame(0)
    assert rgb.shape == (72, 128, 3)
    assert rgb.dtype == np.uint8
    assert np.any(rgb != rgb[0, 0])


def test_world3():
    from anim.paint.world3 import Path, Env
    from anim.paint.light import look
    keys = [(0, 0, 2, 0, 0, 2, 10, 55), (2, 0, 2, 1, 0, 2, 11, 55)]
    path = Path(keys, sigma=0.1)
    e = Env(1.0, path, look)
    assert e.project(np.array([[0.0, 2.0, 12.0]]))[2][0] > 0

def test_world3_shading():
    """真实经过三维世界、云影和笔触光栅路径。"""
    from anim.paint import Paint
    from anim.paint.world3 import Path, Env, SB, shade, compose
    from anim.paint.light import look
    rng = np.random.default_rng(3)
    brush = SB(rng)
    brush.add(np.array([[0, 2, 8], [0.7, 1.5, 9]], np.float32),
              D=(1, 0, 0), L=1.0, W=0.3, spr=0,
              csh=(0.3, 0.2, 0.4), cli=(0.9, 0.6, 0.2))
    group = brush.group(reflect=False)
    path = Path([(0, 0, 2, -5, 0, 2, 10, 55), (1, 0, 2, -5, 0, 2, 10, 55)])
    def lit(t):
        d = look(t)
        d["cloudsh"] = 0.5
        return d
    env = Env(0.5, path, lit)
    data = compose([shade(env, group.lod(env))])
    rgb = Paint().draw(data, Config(128, 72, 10, 1))
    assert rgb.shape == (72, 128, 3)
    assert np.any(rgb != rgb[0, 0])
