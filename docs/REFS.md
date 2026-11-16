# 原项目索引与来源

## 主要来源：Rainroji

| 作品 | 原分支 | 核心文件 | 技术特点 |
| --- | --- | --- | --- |
| 《Un jour de lumière》 | [claude/laughing-volta-yn071i](https://github.com/yiggeror/Rainroji/tree/claude/laughing-volta-yn071i/monet) | [README](https://github.com/yiggeror/Rainroji/blob/claude/laughing-volta-yn071i/monet/README.md)、[engine.py](https://github.com/yiggeror/Rainroji/blob/claude/laughing-volta-yn071i/monet/engine.py)、[world.py](https://github.com/yiggeror/Rainroji/blob/claude/laughing-volta-yn071i/monet/world.py) | 102秒、2.5D多平面、20种笔刷 |
| 《Berceuse》 | [claude/practical-dijkstra-mwlyd8](https://github.com/yiggeror/Rainroji/tree/claude/practical-dijkstra-mwlyd8/berceuse) | [README](https://github.com/yiggeror/Rainroji/blob/claude/practical-dijkstra-mwlyd8/berceuse/README.md)、[engine.py](https://github.com/yiggeror/Rainroji/blob/claude/practical-dijkstra-mwlyd8/berceuse/engine.py)、[core.py](https://github.com/yiggeror/Rainroji/blob/claude/practical-dijkstra-mwlyd8/berceuse/core.py) | 171秒、三维笔触世界、四季渐变、24种笔刷 |

本仓库 `paint/engine.py`、`paint/world3.py`、`paint/light.py` 以《Berceuse》的对应模块为基础移植，保留核心算法并调整导入、文档和宿主接口。

### 源项目技术材料

- 第一部：[场景和流水线](https://github.com/yiggeror/Rainroji/blob/claude/laughing-volta-yn071i/monet/README.md)、[音乐与音效授权](https://github.com/yiggeror/Rainroji/blob/claude/laughing-volta-yn071i/monet/CREDITS.md)
- 第二部：[场景和构建命令](https://github.com/yiggeror/Rainroji/blob/claude/practical-dijkstra-mwlyd8/berceuse/README.md)、[素材与授权](https://github.com/yiggeror/Rainroji/blob/claude/practical-dijkstra-mwlyd8/berceuse/CREDITS.md)
- 第二部：[镜头、变速与光照](https://github.com/yiggeror/Rainroji/blob/claude/practical-dijkstra-mwlyd8/berceuse/shots.py)、[人物骨骼](https://github.com/yiggeror/Rainroji/blob/claude/practical-dijkstra-mwlyd8/berceuse/rig.py)、[划船动作](https://github.com/yiggeror/Rainroji/blob/claude/practical-dijkstra-mwlyd8/berceuse/boat.py)、[音画同步](https://github.com/yiggeror/Rainroji/blob/claude/practical-dijkstra-mwlyd8/berceuse/audio_mix.py)

## 其他可参考作品方向

以下仓库可作为后续扩展动画风格、浏览器渲染或影视流程时的考察入口，尚未移植到当前引擎：

- [Rainroji：日式雨景相关分支](https://github.com/yiggeror/Rainroji/tree/claude/rainy-japanese-street-scene-o63f0n)
- [animation-competition](https://github.com/yiggeror/animation-competition)
- [3am-bug](https://github.com/yiggeror/3am-bug)
- [toward-the-sea](https://github.com/yiggeror/toward-the-sea)

## 版权与复用

- 莫奈画作已进入公有领域；具体录音、字体、音效使用条件记录在原片 `CREDITS.md`。
- 当前引擎仓库以源代码与技术文档为主，不复制原片的音乐、环境录音与成片视频。
- 如果未来加入其他仓库中的第三方素材、依赖或源码，应逐项记录来源、版本、授权与所做修改。
- 后续公开发布可安装的正式引擎包时，再确定统一源码许可证。
