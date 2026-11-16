# CodePaint-Engine

**可扩展、可复用的动画制作引擎。** 以时间驱动场景，由可替换的渲染器生成画面，再统一处理预览、视频与声音。

目前已接入的技术来自 Rainroji 的两部莫奈题材短片，其中程序化笔触渲染是已实现的**一个后端**。引擎的设计面向不同画风、二维/三维场景、不同渲染技术及未来的实时运行环境。

## 已实现

| 部分 | 当前能力 | 位置 |
| --- | --- | --- |
| 通用调度 | 帧率、时间采样、场景与后端解耦 | `src/anim/core.py` |
| 时间轴 | 关键帧插值、变速播放 | `src/anim/time.py` |
| 相机 | 二维视差、三维透视投影 | `src/anim/camera.py` |
| 平面后端 | 基础图形绘制，可用于普通二维动画 | `src/anim/backends/flat.py` |
| 笔触后端 | 24 种油画笔刷、颜料厚度、布纹与光照 | `src/anim/paint/` |
| 三维笔触世界 | 场景组、角色、动态场、细节层级、风与倒影 | `src/anim/paint/world3.py` |
| 声音工具 | 解码、声像、音效放置、淡化、WAV | `src/anim/audio.py` |
| 输出 | PNG、H.264 MP4、外部音轨封装 | `src/anim/output.py` |
| 验证 | 平面、二维笔触和三维笔触示例、单元测试、GitHub Actions | `examples/`、`tests/` |

这个仓库是可维护的引擎基础，不存放两部成片的视频。影片场景、镜头表、音效编排仍保存在各自的原作品分支，可作为具体制作方案的参考。

## 开始使用

建议 Python 3.11。视频输出另外安装 [FFmpeg](https://ffmpeg.org/) 并加入系统 PATH。

```bash
git clone https://github.com/yiggeror/CodePaint-Engine.git
cd CodePaint-Engine
python -m pip install -e ".[all,dev]"

# 生成两类后端的静帧
python examples/flat.py
python examples/paint.py
python examples/world3.py

# 需要完整测试或小段动画
python -m pytest -q
python examples/flat.py --video
python examples/paint.py --video
python examples/world3.py --video
```

默认输出到 `out/`。纯二维功能可以只安装 `.[flat]`，笔触功能使用 `.[paint]`；完整开发环境使用 `.[all,dev]`。

## 结构

```text
src/anim/
  core.py            统一运行与后端协议
  time.py            时间轴与变速
  camera.py          二维、三维相机
  audio.py           声音工具
  output.py          导出与音画合成
  backends/flat.py   平面绘制后端
  paint/
    adapter.py       通用接口到笔触数据的转换
    engine.py        原作复用的笔触光栅引擎
    world3.py        三维笔触世界与动态场
    light.py         画面光照参数插值
examples/             可运行示例
tests/                测试
docs/                 中文技术资料
```

## 文档导航

- [技术架构与模块接口](docs/DESIGN.md)
- [技术栈与依赖](docs/STACK.md)
- [标准制作流程](docs/FLOW.md)
- [复用情况与迁移建议](docs/REUSE.md)
- [原项目与来源索引](docs/REFS.md)
- [测试和日常维护](docs/DEV.md)
- [后续扩展路线](docs/NEXT.md)

## 分支管理

当前为基础建设阶段，**直接维护 `main`**。当后续引入大型后端、进行不兼容重构、开展实验性画风时，再创建短期功能分支，通过测试后合并。两个 Rainroji 原作分支继续原样保留。

## 技术定位

既可以使用现有的程序化笔触系统，也可以接入像素、矢量、传统二维、三维、WebGL 等其他风格和渲染实现。统一的是时间、场景、镜头、音频和输出协作方式；绘画形式始终可以替换。
