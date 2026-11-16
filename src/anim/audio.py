"""音轨放置、基础声像与淡入淡出；源音频解码交由 FFmpeg 完成。"""
from __future__ import annotations
from pathlib import Path
import subprocess
import numpy as np


def load(path: str, sr: int = 48000) -> np.ndarray:
    """将任意 FFmpeg 支持的音频解码为双声道浮点采样。"""
    data = subprocess.check_output(["ffmpeg", "-loglevel", "error", "-i", path,
                                   "-f", "f32le", "-ac", "2", "-ar", str(sr), "-"])
    return np.frombuffer(data, dtype="<f4").reshape(-1, 2).copy()


def place(mix: np.ndarray, clip: np.ndarray, start: float, sr: int = 48000,
          gain: float = 1.0, pan: float = 0.0) -> None:
    """将音效放入时间轴；pan 取 -1 到 1，负数偏左。"""
    if mix.ndim != 2 or clip.ndim != 2 or mix.shape[1] != 2 or clip.shape[1] != 2:
        raise ValueError("音轨必须是 N×2 双声道数组")
    if not -1 <= pan <= 1:
        raise ValueError("声像范围应为 -1 到 1")
    begin = round(start * sr)
    src0 = max(0, -begin)
    dst0 = max(0, begin)
    size = min(len(clip) - src0, len(mix) - dst0)
    if size <= 0:
        return
    weights = np.array([min(1.0, 1.0 - pan), min(1.0, 1.0 + pan)], np.float32)
    mix[dst0:dst0 + size] += clip[src0:src0 + size] * weights * gain


def fade(clip: np.ndarray, first: float = 0.03, last: float = 0.08,
         sr: int = 48000) -> np.ndarray:
    """在已有录音两端施加短淡化，避免拼接爆音。"""
    out = np.asarray(clip, np.float32).copy()
    a = min(len(out), max(0, round(first * sr)))
    b = min(len(out), max(0, round(last * sr)))
    if a:
        out[:a] *= np.linspace(0, 1, a, dtype=np.float32)[:, None]
    if b:
        out[-b:] *= np.linspace(1, 0, b, dtype=np.float32)[:, None]
    return out


def wav(samples: np.ndarray, path: str, sr: int = 48000):
    """将 N×2 浮点采样保存为双声道 WAV。"""
    import wave
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    pcm = (np.clip(samples, -1, 1) * 32767).astype("<i2")
    with wave.open(str(out), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(pcm.tobytes())
    return out
