"""独立于绘画风格的图像保存与 FFmpeg 视频输出。"""
from __future__ import annotations
from pathlib import Path
import shutil
import subprocess
from .core import Engine


def png(engine: Engine, path: str, index: int = 0):
    """保存指定帧为 PNG。"""
    from PIL import Image
    dst = Path(path)
    dst.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(engine.frame(index), "RGB").save(dst)
    return dst


def video(engine: Engine, path: str, start: int = 0, stop: int | None = None, crf: int = 18):
    """将 RGB 帧流送至 FFmpeg 编码为 H.264 MP4。可渲染独立片段。"""
    if shutil.which("ffmpeg") is None:
        raise RuntimeError("未找到 FFmpeg，请先安装并加入 PATH")
    cfg = engine.config
    if stop is None:
        stop = cfg.count
    if not 0 <= start < stop <= cfg.count:
        raise ValueError("帧范围无效")
    dst = Path(path)
    dst.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo",
           "-pix_fmt", "rgb24", "-s", f"{cfg.width}x{cfg.height}",
           "-r", str(cfg.fps), "-i", "-", "-an", "-c:v", "libx264",
           "-pix_fmt", "yuv420p", "-crf", str(crf), str(dst)]
    with subprocess.Popen(cmd, stdin=subprocess.PIPE) as proc:
        try:
            for im in engine.frames(start, stop):
                proc.stdin.write(im.tobytes())
        finally:
            proc.stdin.close()
        code = proc.wait()
    if code:
        raise RuntimeError(f"FFmpeg 编码失败，返回码 {code}")
    return dst


def mux(picture: str, audio: str, dest: str):
    """合并已有视频和音轨，保留视频码流并使用 AAC 音频。"""
    if shutil.which("ffmpeg") is None:
        raise RuntimeError("未找到 FFmpeg")
    out = Path(dest)
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                    "-i", picture, "-i", audio, "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "256k", "-shortest", str(out)], check=True)
    return out
