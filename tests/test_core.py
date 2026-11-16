"""验证通用框架的帧调度与时间映射。"""
import numpy as np
import pytest
from anim import Config, Engine, Key, sample, TimeWarp
from anim.camera import Camera2D, Camera3D


class S:
    def sample(self, t):
        return t


class B:
    def draw(self, val, cfg):
        return np.full((cfg.height, cfg.width, 3), int(val * 100), np.uint8)


def test_frames():
    eng = Engine(Config(16, 9, 10, 1.0), S(), B())
    assert eng.config.count == 10
    assert eng.frame(5)[0, 0, 0] == 50
    assert len(list(eng.frames(2, 4))) == 2
    with pytest.raises(IndexError):
        eng.frame(10)


def test_keys():
    assert sample([Key(0, 0), Key(1, 10)], 0.5) == 5.0
    np.testing.assert_allclose(sample([Key(0, (0, 2)), Key(1, (10, 12))], 0.5), [5, 7])
    with pytest.raises(ValueError):
        sample([], 0.5)


def test_warp():
    w = TimeWarp([(0, 1), (2, 2)], steps=2048)
    assert w.duration < 2
    assert abs(w.to_story(w.to_film(1.5)) - 1.5) < 0.01


def test_cameras():
    xy = Camera2D(x=10, y=0, cx=100, cy=50).project([[15, 2]], depth=0.5)
    np.testing.assert_allclose(xy[0], [102.5, 51])
    p = Camera3D((0, 1, 0), (0, 1, 1), width=1920, height=1080).project([[0, 1, 5]])
    np.testing.assert_allclose(p[0, :2], [960, 540])
    assert p[0, 2] == 5
