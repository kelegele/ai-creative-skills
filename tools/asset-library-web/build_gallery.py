# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml"]
# ///
"""扫描视频素材库,生成静态橱窗 gallery.html(数据内联,file:// 直接打开,不起 server)。

前端:antd v5 组件 + Tailwind 工具类 + Kimi 设计 token 调教(色彩/圆角/字体/动效),
CDN 加载(首次打开需联网)。数据内联,媒体用相对路径。

用法:
    uv run build_gallery.py <LIBRARY_ROOT> [-o OUTPUT.html]

约定:
    - 文件素材:同目录旁挂 `<原文件名>.metadata.yaml`
    - 目录素材(如 Remotion 组件目录):目录内放 `metadata.yaml`
    - gallery.html 默认生成到 LIBRARY_ROOT 下
    - LIBRARY_ROOT、metadata.yaml、gallery.html 均不进 git(见仓库 .gitignore)
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

MEDIA_PREVIEW = {
    ".mp4": "video", ".mov": "video", ".webm": "video",
    ".mp3": "audio", ".wav": "audio", ".aac": "audio", ".m4a": "audio",
    ".png": "image", ".jpg": "image", ".jpeg": "image", ".gif": "image",
    ".svg": "image", ".webp": "image",
}
META_SUFFIX = ".metadata.yaml"


def load_meta(path: Path) -> dict:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except Exception as e:  # noqa: BLE001
        print(f"⚠️  元数据解析失败 {path}: {e}", file=sys.stderr)
        return {}


def scan(root: Path) -> list[dict]:
    items: list[dict] = []
    consumed: set[Path] = set()

    # 目录素材:目录内 metadata.yaml
    for meta in sorted(root.rglob("metadata.yaml")):
        target = meta.parent
        items.append(build_item(root, target, load_meta(meta), is_dir=True))
        consumed.add(meta)

    # 文件素材:<原文件名>.metadata.yaml
    for meta in sorted(root.rglob(f"*{META_SUFFIX}")):
        if meta in consumed:
            continue
        asset = Path(str(meta)[: -len(META_SUFFIX)])
        if not asset.exists():
            print(f"⚠️  元数据无对应素材文件: {meta}", file=sys.stderr)
            continue
        items.append(build_item(root, asset, load_meta(meta), is_dir=False))
    return items


def build_item(root: Path, target: Path, meta: dict, is_dir: bool) -> dict:
    rel = target.relative_to(root).as_posix()
    kind = "dir" if is_dir else MEDIA_PREVIEW.get(target.suffix.lower(), "file")
    return {
        "path": rel,
        "category": rel.split("/")[0] if "/" in rel else "(root)",
        "kind": kind,
        "name": meta.get("name") or target.name,
        "type": meta.get("type", ""),
        "license": meta.get("license", ""),
        "source": meta.get("source", ""),
        "updated": str(meta.get("updated", "")),
        "meta": meta,
    }


TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>素材库橱窗 · __COUNT__ 件</title>
<script src="https://cdn.tailwindcss.com"></script>
<script>
/* Kimi tokens(color/radius/typography/spacing)→ Tailwind 映射
   来源:kimi-design-skill references/tokens.json */
tailwind.config = {
  theme: { extend: {
    colors: {
      kimiBlue:  { DEFAULT:'#1783ff', hover:'#167ff7', active:'#167cf2', bg10:'rgba(23,131,255,0.1)' },
      kimiOrange:{ DEFAULT:'#ff9500', bg10:'rgba(255,149,0,0.1)' },
      label: { primary:'rgba(0,0,0,0.9)', secondary:'rgba(0,0,0,0.6)', tertiary:'rgba(0,0,0,0.45)', quaternary:'rgba(0,0,0,0.3)' },
      fill:  { f1:'rgba(0,0,0,0.03)', f2:'rgba(0,0,0,0.05)', f3:'rgba(0,0,0,0.15)' },
      sep:   'rgba(0,0,0,0.13)',
      ground:'#f9fbfc',
      surface:'#ffffff',
    },
    borderRadius: { xxs:'4px', sm:'8px', md:'10px', lg:'12px', xl:'16px' },
    fontFamily: {
      sans:['PingFang SC','-apple-system','Helvetica Neue','Microsoft YaHei','sans-serif'],
      mono:['Geist Mono','ui-monospace','Menlo','monospace'],
    },
  }}
}
</script>
<style>
  body { background:#f9fbfc; }
  /* Purposeful Motion:hover 抬升 1.02 / 按压 0.97,150ms Kimi ease-out,只动 transform+shadow */
  .card { transition:transform 150ms cubic-bezier(0.23,1,0.32,1), box-shadow 150ms cubic-bezier(0.23,1,0.32,1); }
  @media (hover:hover) and (pointer:fine) {
    .card:hover { transform:scale(1.02); box-shadow:0 4px 16.4px rgba(0,0,0,0.1); }
  }
  .card:active { transform:scale(0.97); }
  *:focus-visible { outline:2px solid #1783ff; outline-offset:2px; border-radius:4px; }
  @media (prefers-reduced-motion:reduce) {
    * { animation-duration:0.01ms!important; transition-duration:0.01ms!important; }
  }
</style>
<script crossorigin src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
<script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
<script src="https://unpkg.com/dayjs@1/dayjs.min.js"></script>
<script src="https://unpkg.com/antd@5/dist/antd.min.js"></script>
<script src="https://unpkg.com/@babel/standalone@7/babel.min.js"></script>
</head>
<body>
<div id="root"></div>
<script type="text/babel" data-presets="react">
const { useState, useMemo } = React;
const { ConfigProvider, Input, Select, Tabs, Tag, Modal, Empty } = antd;

const ITEMS = __DATA__;
const HIDE = ["id","name","type","license","source","project"];
const KIND_LABEL = { video:"视频", audio:"音频", image:"图片", dir:"组件/目录", file:"其他文件" };
/* 一级目录名(英文,文件系统惯例)→ 界面显示(中文),未收录的目录名原样显示 */
const CAT_LABEL = {
  "footage":"镜头素材", "transitions":"转场预设", "motion-graphics":"动效组件",
  "audio":"音频", "fonts":"字体", "color":"色彩资产",
  "graphics":"图形资产", "code-components":"代码组件", "templates":"项目模板",
};
const catLabel = c => CAT_LABEL[c] || c;
/* Tab 顺序 = library-spec.md 目录树业务顺序(9 大类全展示,无素材为 0);枚举外目录排最后按字母序 */
const CAT_ORDER = Object.keys(CAT_LABEL);

/* 语义色:分类=kimiBlue(主层级),授权=kimiOrange(权益提示),来源=中性灰 */
function ItemTag({color, bg, children}) {
  return (
    <Tag bordered={false} style={{ marginInlineEnd:0, borderRadius:4, fontSize:12, lineHeight:'18px',
      color, background:bg, padding:'0 8px' }}>{children}</Tag>
  );
}

function Preview({ item }) {
  if (item.kind === 'video')
    return <video src={item.path} controls preload="metadata"
      className="w-full rounded-sm bg-black max-h-40 object-contain" />;
  if (item.kind === 'audio')
    return <audio src={item.path} controls className="w-full" />;
  if (item.kind === 'image')
    return <img src={item.path} loading="lazy"
      className="w-full rounded-sm bg-black max-h-40 object-contain" />;
  return null;
}

function AssetCard({ item, onOpenMeta }) {
  const rows = Object.entries(item.meta || {})
    .filter(([k]) => !HIDE.includes(k))
    .slice(0, 6);
  return (
    <div className="card bg-surface rounded-lg p-4 flex flex-col gap-2">
      <Preview item={item} />
      <div className="text-[15px] leading-[22px] font-medium text-label-primary break-all">{item.name}</div>
      <div className="font-mono text-[10px] leading-[14px] text-label-quaternary break-all">{item.path}</div>
      <div className="flex flex-wrap gap-1">
        <ItemTag color="#1783ff" bg="rgba(23,131,255,0.1)">{catLabel(item.category)}</ItemTag>
        {item.type && <ItemTag color="rgba(0,0,0,0.6)" bg="rgba(0,0,0,0.05)">{item.type}</ItemTag>}
        {item.license && <ItemTag color="#ff9500" bg="rgba(255,149,0,0.1)">{item.license}</ItemTag>}
        {item.source && <ItemTag color="rgba(0,0,0,0.45)" bg="rgba(0,0,0,0.03)">{item.source}</ItemTag>}
      </div>
      {rows.length > 0 && (
        <div className="grid grid-cols-[auto_1fr] gap-x-2 gap-y-0.5 text-[12px] leading-[18px]">
          {rows.map(([k, v]) => (
            <React.Fragment key={k}>
              <span className="text-label-tertiary">{k}</span>
              <span className="text-label-secondary break-all">{Array.isArray(v) ? v.join(', ') : String(v)}</span>
            </React.Fragment>
          ))}
        </div>
      )}
      <button onClick={() => onOpenMeta(item)}
        className="self-start text-[12px] leading-[18px] text-kimiBlue hover:text-kimiBlue-hover transition-colors">
        原始元数据 →
      </button>
    </div>
  );
}

function App() {
  const [q, setQ] = useState('');
  const [cat, setCat] = useState(null);
  const [kind, setKind] = useState(null);
  const [metaItem, setMetaItem] = useState(null);

  /* Tab 固定展示规范 9 大类(无素材的为 0),枚举外目录追加在最后 */
  const cats = useMemo(() => {
    const present = new Set(ITEMS.map(i => i.category));
    const extras = [...present].filter(c => !CAT_ORDER.includes(c)).sort();
    return [...CAT_ORDER, ...extras];
  }, []);
  const list = useMemo(() => {
    const kw = q.trim().toLowerCase();
    return ITEMS.filter(i =>
      (!cat || i.category === cat) &&
      (!kind || i.kind === kind) &&
      (!kw || JSON.stringify(i).toLowerCase().includes(kw)));
  }, [q, cat, kind]);

  return (
    <ConfigProvider theme={{
      token: {
        colorPrimary:'#1783ff', borderRadius:10,
        fontFamily:"PingFang SC, -apple-system, 'Helvetica Neue', 'Microsoft YaHei', sans-serif",
        colorText:'rgba(0,0,0,0.9)', colorTextSecondary:'rgba(0,0,0,0.6)',
        colorBorder:'rgba(0,0,0,0.13)', colorBgLayout:'#f9fbfc',
      },
      components: { Input:{ controlHeight:32 }, Select:{ controlHeight:32 } },
    }}>
      <div className="max-w-[1200px] mx-auto px-6 py-8">
        {/* 页头:大标题 20/600,说明 12px tertiary,Quiet Utility */}
        <header className="mb-6">
          <h1 className="text-[20px] leading-[30px] font-semibold text-label-primary">素材库橱窗</h1>
          <p className="text-[12px] leading-[18px] text-label-tertiary mt-1">
            __COUNT__ 件素材 · 生成于 __TIME__ · 只读橱窗,入库与维护走 video-asset-library skill
          </p>
        </header>

        {/* 工具栏:搜索 + 形态筛选,间距 12 */}
        <div className="flex flex-wrap gap-3">
          <Input allowClear placeholder="搜索名称 / 路径 / 元数据…"
            value={q} onChange={e => setQ(e.target.value)} style={{ flex:1, minWidth:220 }} />
          <Select allowClear placeholder="全部形态" value={kind} onChange={v => setKind(v ?? null)}
            style={{ minWidth:140 }}
            options={Object.entries(KIND_LABEL).map(([v, l]) => ({ value:v, label:l }))} />
        </div>

        {/* 分类 Tab:第一个「全部」,带数量;切换即筛选 */}
        <Tabs
          activeKey={cat ?? 'all'}
          onChange={k => setCat(k === 'all' ? null : k)}
          items={[
            { key:'all', label:`全部 ${ITEMS.length}` },
            ...cats.map(c => ({
              key:c,
              label:`${catLabel(c)} ${ITEMS.filter(i => i.category === c).length}`,
            })),
          ]}
        />

        {/* 卡片网格:卡片即框架对象,间距 16,白卡片 vs 浅灰页底=面对比不加描边 */}
        {list.length > 0 ? (
          <div className="grid gap-4 [grid-template-columns:repeat(auto-fill,minmax(280px,1fr))]">
            {list.map(i => <AssetCard key={i.path} item={i} onOpenMeta={setMetaItem} />)}
          </div>
        ) : (
          <Empty description="没有匹配的素材" style={{ margin:'60px auto' }} />
        )}

        <Modal open={!!metaItem} title={metaItem?.name} footer={null}
          onCancel={() => setMetaItem(null)} width={520}>
          <pre className="font-mono text-[12px] leading-[18px] bg-fill-f1 rounded-sm p-3 overflow-auto">
            {metaItem ? JSON.stringify(metaItem.meta, null, 2) : ''}
          </pre>
        </Modal>
      </div>
    </ConfigProvider>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
</script>
</body>
</html>
"""


def main() -> None:
    ap = argparse.ArgumentParser(description="视频素材库静态橱窗生成器")
    ap.add_argument("library_root", type=Path, help="素材库根目录 LIBRARY_ROOT")
    ap.add_argument("-o", "--output", type=Path, default=None,
                    help="输出路径(默认 <LIBRARY_ROOT>/gallery.html)")
    args = ap.parse_args()

    root = args.library_root.resolve()
    if not root.is_dir():
        sys.exit(f"❌ 素材库目录不存在: {root}")

    items = scan(root)
    out = args.output or (root / "gallery.html")
    from datetime import datetime
    page = (TEMPLATE
            .replace("__DATA__", json.dumps(items, ensure_ascii=False))
            .replace("__COUNT__", str(len(items)))
            .replace("__TIME__", datetime.now().strftime("%Y-%m-%d %H:%M")))
    out.write_text(page, encoding="utf-8")
    print(f"✅ {len(items)} 件素材 → {out}")
    if not items:
        print("ℹ️  没有找到任何 metadata.yaml / *.metadata.yaml,先入库素材再生成", file=sys.stderr)


if __name__ == "__main__":
    main()
