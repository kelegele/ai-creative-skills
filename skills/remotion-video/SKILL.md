---
name: remotion-video
description: Remotion 视频创作工作流。前置检查清单 + 分镜拆解 + 资产清单 + 代码生成 + 自检交付。当用户用 Remotion 做视频、生成视频代码、做产品发布/数据报告/短视频动画时使用。触发词:Remotion, 做视频, 视频创作, 视频代码, 分镜, video generation。
version: 0.1.0
author: Kelegele
license: MIT
metadata:
  tags: [video, remotion, react, typescript, animation, motion-graphics]
---

# Remotion 视频创作

用 Remotion(React 写视频)创作可程序化渲染的视频。AI 按**前置检查清单**逐项确认后,再拆分镜、列资产、生成代码。

## 工具链(和仓库 Python/uv 主线不同,注意)

- Remotion 是 **Node 生态**:用 `npx` / `npm`,不用 uv
- 新工程:`npx create-video@latest`(官方脚手架)
- 预览:`npx remotion studio`(本地起 Studio,浏览器里逐帧预览)
- 渲染:`npx remotion render src/Video.tsx <CompositionID> out/video.mp4`
- 渲染耗时与时长/分辨率正相关,**先低清小样(720p)确认节奏,再出正片**

## 第0步:运行参数(开工前必做,问用户存运行变量)

- **PROJECT_DIR** — Remotion 工程目录(新建还是已有?)
- **OUTPUT_DIR** — 成片输出到哪
- **视频规格** — 时长 / 分辨率 / 帧率 / 输出格式(默认 1080×1920 竖屏 30fps MP4,按平台定)
- **素材来源** — 用户提供 / 从素材库取(见「配合 skill」)/ AI 生成 / 占位符

## 主流程(7步)

每步用户确认后才进下一步。

1. **需求确认** — 视频目标(产品发布/数据报告/短视频/宣传片)、时长、分辨率、帧率、输出格式、风格参考
2. **前置检查** — 对照 `references/checklist.md` 逐项过,未确认项标"待补充",**不得跳过**
3. **分镜拆解** — 按秒/帧切独立场景,每场景输出:开始帧、结束帧、画面描述、所需组件、动效参数、转场类型和时长。**逐场景给用户审**
4. **资产清单** — 列出所有图片/视频/字体/音频/SVG,标注来源(用户提供/素材库/AI生成/占位符),确认路径和引用方式
5. **代码生成** — 按以下结构:
   1. `src/Video.tsx` — 主 Composition 配置
   2. `src/scenes/Scene*.tsx` — 分镜组件(每场景独立文件)
   3. `src/components/` — 可复用动效组件
   4. `src/constants.ts` — 颜色、字体、动画参数常量
   5. `remotion.config.ts` — 渲染配置
6. **自检** — TypeScript 类型、帧范围不越界、资产路径、色彩空间、输出格式
7. **交付** — 渲染命令、占位资产替换说明、动画参数调整说明

## 关键规则(必读)

- **所有时间描述转换为帧数**,不写"2秒后"这种模糊表达
- 动画优先 `spring()` 和 `interpolate()`,避免线性僵硬;默认缓动 `spring({stiffness: 100, damping: 15})`
- 资产放 `public/` 目录,用 `staticFile()` 引用;字体用 `@remotion/google-fonts` 或本地加载
- 组件原子化拆分(可复用、可调试),参数外置到 props 或 constants
- `useCurrentFrame()` 返回值必须在 `0` 到 `durationInFrames-1` 范围内
- 可替换区域加标记注释:`// ASSET: 替换为实际产品图`
- **基准场景先行**:先做第 1 个场景渲染小样确认风格,再批量做其余场景(同 text-to-card 基准卡原则)
- 快速决策(转场/缓动/音频层级/信息呈现/色彩空间默认值)见 `references/checklist.md` 第五节

## 配合 skill

- **video-asset-library** — 素材库管理。做视频前先查库里有没有可复用的转场/动效/音频/组件,别从零造;项目结束后把可复用素材回收入库
- 素材库本体(二进制)不进 git,位置见 video-asset-library SKILL.md

## References

- `references/checklist.md` — 前置检查清单(可见层/隐形层/技术层 14 项)+ 快速决策卡
