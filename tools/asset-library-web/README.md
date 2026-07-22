# asset-library-web · 视频素材库静态橱窗

扫描素材库,生成单文件 `gallery.html`(数据内联,双击 file:// 直接打开,**不起 server**)。

## 前端技术栈(改模板前必读)

- **antd v5 + Tailwind(均 CDN 加载)**,React 18 UMD;**首次打开需联网**
- **Kimi 设计体系调教**:色彩/圆角/字体/动效 token 来自 kimi-design-skill(`tokens.json`),映射在模板 `tailwind.config` 与 antd `ConfigProvider` 里
- **Babel 必须锁 v7**(`@babel/standalone@7`):v8 默认 automatic JSX runtime 会吐 `import` 语句,UMD 页面直接白屏
- 分类 Tab:9 大类全展示(含 0)、中文显示、按 `library-spec.md` 目录树业务顺序——**类目增改要同步模板里的 `CAT_LABEL` / `CAT_ORDER`**(spec 第二节也有联动提醒)

## 用法

```bash
uv run build_gallery.py <LIBRARY_ROOT>
# 默认输出 <LIBRARY_ROOT>/gallery.html,可用 -o 指定别处
```

## 约定

- **文件素材**:同目录旁挂元数据 `<原文件名>.metadata.yaml`(如 `BRoll_City_Traffic_v01.mp4.metadata.yaml`)
- **目录素材**(Remotion 组件等):目录内放 `metadata.yaml`
- 元数据 schema 见 `skills/video-asset-library/references/library-spec.md`
- gallery.html 生成在素材库根目录下,媒体预览用相对路径(file:// 可直接播放视频/音频/图片)

## git 边界

| 内容 | 是否进 git |
|------|-----------|
| `build_gallery.py` / 本 README | ✅ 跟踪 |
| LIBRARY_ROOT(素材本体) | ❌ 不跟踪 |
| `metadata.yaml` / 索引 / `gallery.html` | ❌ 不跟踪(生成物,可随时重建) |

入库、改元数据、盘点等**写操作走 `video-asset-library` skill**;本工具只读。
