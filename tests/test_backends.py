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
