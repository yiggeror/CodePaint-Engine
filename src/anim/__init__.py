"""通用动画引擎：分离时间、场景采样、渲染后端和视频输出。"""
from .core import Config, Engine, Backend, Scene
from .time import Key, sample, TimeWarp
__all__ = ["Config", "Engine", "Backend", "Scene", "Key", "sample", "TimeWarp"]
__version__ = "0.1.0"
