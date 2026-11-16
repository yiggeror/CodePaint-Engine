"""验证音轨混合、剪裁和渐变处理。"""
import numpy as np
from anim.audio import place, fade


def test_place_and_pan():
    mix = np.zeros((100, 2), dtype=np.float32)
    clip = np.ones((30, 2), dtype=np.float32)
    place(mix, clip, 0.02, sr=100, gain=0.5, pan=-1)
    np.testing.assert_allclose(mix[2:32, 0], 0.5)
    np.testing.assert_allclose(mix[2:32, 1], 0.0)


def test_negative_clip_and_fade():
    mix = np.zeros((20, 2), dtype=np.float32)
    place(mix, np.ones((12, 2), np.float32), -0.05, sr=100)
    assert mix[:7].sum() == 14
    out = fade(np.ones((100, 2), np.float32), 0.1, 0.1, sr=100)
    assert np.all(out[0] == 0) and np.all(out[-1] == 0)
