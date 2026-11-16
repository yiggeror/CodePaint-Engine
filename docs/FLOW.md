# 制作流程

此流程用于新作品；现有两部 Rainroji 短片的具体实现与时间点详见 [REFS.md](REFS.md)。

## 1. 确定作品与艺术方案

写清时长、分辨率、帧率、视觉参考、场景顺序、人物动作和声音方向。决定采用二维、三维、笔触渲染或新建后端。

## 2. 选择已有模块

先查 [REUSE.md](REUSE.md)。优先使用 `Engine`、`Config`、时间轴、相机和输出工具。风格相关的模块按需选择，不将独有场景直接塞入引擎核心。

## 3. 先做关键静帧

创建 `Scene.sample(t)`，对开头、转场、高潮及结尾分别渲染静帧，重点确认构图、颜色、比例、层次与画面质感。

示例：

```bash
python examples/flat.py
python examples/paint.py
```

对复杂作品可编写自己的联系表脚本，按时间点排列预览，参考 Rainroji 两部的 `render.py` 与 `sheet.py`。

## 4. 动作与相机

确定时间关键点，按需要引入风场、骨骼动作、物理变化及相机路径。建议单独验证：

- 人物姿态、关节、接触关系与物体尺度；
- 相机路径的平滑性、透视与穿模；
- 水面、倒影、云影和地表细节的一致性；
- 物体在镜头运动中是否漂移、闪烁、突变；
- 转场是否连续，角色和动态元素是否保持同一时钟。

## 5. 声音设计

优先记录声音素材的来源与授权。音乐、环境、动作音效分轨安排，按场景时间、角色动作或相机距离设置音量与声像。现有 `audio.py` 提供通用工具，作品级同步编排可参考《Berceuse》的 `audio_mix.py`。

## 6. 片段渲染与审查

先低分辨率抽样，再渲染短片段，最后输出完整画面。检查常见问题：闪烁、锯齿、接缝、重复帧、停顿、瞬间位置跳变、错误遮挡、过曝与色彩闪动。

当前输出接口：

```python
from anim.output import png, video, mux
# png(engine, "out/test.png", index=30)
# video(engine, "out/segment.mp4", start=0, stop=90, crf=18)
# mux("out/segment.mp4", "out/mix.wav", "out/final.mp4")
```

完整长片优先分段渲染。分段边界必须使用相同的固定帧号、随机种子、时间映射与场景状态。

## 7. 最终制作与归档

- 输出目标分辨率、帧率、视频格式与音频编码。
- 查看成片首尾、各场景交界处、动作密集处与音画同步点。
- 保存源代码、依赖、声音素材信息、参数、渲染命令、最终版本与已知问题。
- 在作品目录记录引用的引擎版本或 Git 提交 SHA。

## 两部原片的构建线索

《Un jour de lumière》：`render.py` → `renderseg.sh`（按段交给 FFmpeg 编码）→ `audio_mix.py`。

《Berceuse》：`render.py` → `renderseg.sh` → `audio/get_sfx.sh` 与 `audio/music_edit.py` → `audio_mix.py` → FFmpeg 封装。

原作品的声音文件需按 `CREDITS.md` 准备。第二部的音乐剪辑脚本使用原始音频中间文件，重建时应同步完成相应格式转换。
