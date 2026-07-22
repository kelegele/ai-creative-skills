# 素材库规范(分类 / 元数据 / 命名 / 调用)

## 一、建库价值判断

### ✅ 可以建库(高复用性、标准化)

| 素材类型 | 建库价值 | 复用场景 | 管理维度 |
|----------|----------|----------|----------|
| **镜头片段(B-Roll / 空镜)** | 极高 | 多项目共用城市/自然/办公场景 | 场景类型、色调、时长、分辨率 |
| **转场预设** | 高 | 同风格项目快速套用 | 转场类型、时长、缓动参数 |
| **动效组件(Motion Graphics)** | 极高 | 标题卡、数据图、Logo 动画复用 | 功能类型、风格、可配置参数 |
| **音效(SFX)** | 高 | whoosh、UI点击、环境音通用 | 类别、情绪、时长、采样率 |
| **音乐/BGM** | 高 | 同调性项目复用 | 情绪标签、BPM、时长、调性 |
| **字体** | 极高 | 品牌一致性 | 字重、语言支持、商用授权 |
| **调色预设(LUT)** | 高 | 同风格项目一键套用 | 风格名、色彩空间、适用场景 |
| **图标/矢量图形** | 极高 | UI、信息图、装饰元素 | 风格、主题、可编辑性 |
| **字幕模板** | 高 | 多语言版本、系列视频 | 语言、位置、字体、安全框 |
| **代码片段(Remotion 组件)** | 极高 | 同类型动画快速复用 | 功能、参数接口、版本兼容 |

### ⚠️ 谨慎建库(项目特异性强)

| 素材类型 | 原因 | 建议做法 |
|----------|------|----------|
| **完整镜头(带表演)** | 每项目演员/场景不同 | 按项目归档,不进入通用库 |
| **对白/旁白音频** | 项目专属内容 | 项目内管理,提取通用音效 |
| **完整脚本** | 叙事逻辑不可复用 | 提取"结构模板"入库(起承转合节奏) |
| **特定产品图** | 品牌专属 | 项目归档,提取通用展示动效入库 |

### ❌ 不建议建库(一次性/强关联)

| 素材类型 | 原因 |
|----------|------|
| **粗剪时间线** | 项目专属,无复用价值 |
| **精剪决策记录** | 与具体表演/节奏强绑定 |
| **单项目调色方案** | 除非提炼为通用 LUT |
| **临时代理文件** | 可自动重建,无需保存 |

---

## 二、分类体系(一级目录)

```
📁 video-assets-library/
├── 📁 footage/              # 镜头素材
│   ├── 📁 b-roll/           # 空镜/通用场景
│   │   ├── 📁 city/         # 城市
│   │   ├── 📁 nature/       # 自然
│   │   ├── 📁 office/       # 办公
│   │   └── 📁 abstract/     # 抽象/纹理
│   └── 📁 product/          # 产品展示(通用角度)
│
├── 📁 transitions/          # 转场预设
│   ├── 📁 hard-cut/         # 硬切参数模板
│   ├── 📁 dissolve/         # 叠化参数模板
│   ├── 📁 match-cut/        # 匹配剪辑模板
│   └── 📁 effect/           # 特效转场(光斑/故障等)
│
├── 📁 motion-graphics/      # 动效组件
│   ├── 📁 titles/           # 标题动画
│   ├── 📁 lower-thirds/     # 人名条/字幕条
│   ├── 📁 data-viz/         # 数据可视化
│   ├── 📁 logo-reveal/      # Logo 展示
│   └── 📁 icons/            # 图标动效
│
├── 📁 audio/                # 音频
│   ├── 📁 sfx/              # 音效
│   │   ├── 📁 ui/           # UI 交互音
│   │   ├── 📁 whoosh/       # 转场音效
│   │   ├── 📁 ambient/      # 环境音
│   │   └── 📁 foley/        # 拟音
│   ├── 📁 music/            # 音乐
│   │   ├── 📁 upbeat/       # 轻快
│   │   ├── 📁 dramatic/     # 戏剧性
│   │   ├── 📁 corporate/    # 商务
│   │   └── 📁 minimal/      # 极简
│   └── 📁 voice/            # 人声模板(语气参考)
│
├── 📁 fonts/                # 字体
│   ├── 📁 sans-serif/       # 无衬线
│   ├── 📁 serif/            # 衬线
│   ├── 📁 display/          # 展示字体
│   └── 📁 monospace/        # 等宽
│
├── 📁 color/                # 色彩资产
│   ├── 📁 luts/             # 调色预设
│   ├── 📁 palettes/         # 配色方案
│   └── 📁 gradients/        # 渐变预设
│
├── 📁 graphics/             # 图形资产
│   ├── 📁 icons/            # 图标(SVG)
│   ├── 📁 illustrations/    # 插画
│   ├── 📁 shapes/           # 几何形状
│   └── 📁 patterns/         # 纹理/图案
│
├── 📁 code-components/      # Remotion 代码组件
│   ├── 📁 animations/       # 通用动画逻辑
│   ├── 📁 compositions/     # 完整合成模板
│   └── 📁 hooks/            # 自定义 Hooks
│
└── 📁 templates/            # 项目模板
    ├── 📁 product-launch/   # 产品发布
    ├── 📁 data-report/      # 数据报告
    ├── 📁 short-video/      # 短视频
    └── 📁 documentary/      # 纪录片
```

---

## 三、元数据 schema(每件素材旁边放 `metadata.yaml`)

```yaml
# 通用元数据(所有素材必填)
id: "唯一标识"
name: "素材名称"
type: "素材类型"
created: "创建日期"
updated: "最后更新"
source: "来源(原创/购买/免费)"
license: "授权类型"
project: "所属项目(通用留空)"

# 镜头素材特有
resolution: "1920x1080"
framerate: "30fps"
duration: "00:00:15"
color_space: "Rec.709"
scene_type: "城市/自然/办公"
lighting: "日光/夜景/室内"
camera_movement: "固定/推/拉/摇/移"

# 动效组件特有
function: "标题/数据/Logo"
style: "极简/科技/活泼/庄重"
configurable_params: ["text", "color", "duration", "easing"]
remotion_version: "4.x"
dependencies: ["@remotion/..."]

# 音频特有
category: "音效/音乐/人声"
mood: "紧张/轻松/激励/悲伤"
bpm: "120"
key: "C Major"
duration: "00:00:30"
loopable: true/false

# 字体特有
family: "Inter"
weights: [400, 600, 800]
languages: ["Latin", "CJK"]
license: "OFL/商业授权"
```

---

## 四、命名规范

### 4.1 镜头素材
```
[类型]_[场景]_[描述]_[版本]_[分辨率]_[时长]

示例:
BRoll_City_TrafficNight_v01_4K_15s.mp4
BRoll_Nature_ForestAerial_v02_1080p_30s.mp4
Product_Tech_PhoneRotate_v01_4K_10s.mp4
```

### 4.2 动效组件
```
[功能]_[风格]_[描述]_[版本]_[Remotion版本]

示例:
Title_Minimal_SlideIn_v01_R4.tsx
DataViz_Tech_BarChart_v02_R4.tsx
LogoReveal_Corporate_3DFlip_v01_R4.tsx
```

### 4.3 音频
```
[类型]_[情绪]_[描述]_[BPM]_[时长]_[版本]

示例:
SFX_UI_ClickSoft_v01_0bpm_1s.wav
Music_Upbeat_CorporateDrive_v01_120bpm_60s.mp3
Music_Dramatic_EpicBuild_v02_90bpm_120s.mp3
```

### 4.4 字体
```
[家族名]_[字重范围]_[语言支持]_[授权]

示例:
Inter_400-800_Latin_OFL.zip
NotoSansCJK_400-700_CJK_OFL.zip
```

---

## 五、Remotion 调用示例

### 5.1 组件级复用
```typescript
// 从素材库导入通用标题组件
import { TitleSlideIn } from "@assets-library/motion-graphics/titles";

// 使用时传入项目特定参数
<TitleSlideIn
  text="产品发布"
  color="#FFFFFF"
  durationInFrames={60}
  easing="spring"
/>
```

### 5.2 转场级复用
```typescript
// 从素材库导入转场预设
import { CrossDissolve } from "@assets-library/transitions";

// 在两段素材之间使用
<Sequence from={0} durationInFrames={120}>
  <Video src={staticFile("scene1.mp4")} />
</Sequence>
<CrossDissolve durationInFrames={8} />
<Sequence from={120} durationInFrames={180}>
  <Video src={staticFile("scene2.mp4")} />
</Sequence>
```

### 5.3 音频级复用
```typescript
// 从素材库导入音效
import { SFX_Click } from "@assets-library/audio/sfx";

// 在特定帧触发
const frame = useCurrentFrame();
const playSound = frame === 30; // 第30帧触发

// 实际播放逻辑(需配合音频库如 remotion-media-utils)
```
