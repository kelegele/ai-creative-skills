# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml"]
# ///
"""扫描视频素材库,生成静态橱窗 gallery.html(数据内联,file:// 直接打开,不起 server)。

用法:
    uv run build_gallery.py <LIBRARY_ROOT> [-o OUTPUT.html]

约定:
    - 文件素材:同目录旁挂 `<文件名>.metadata.yaml`
    - 目录素材(如 Remotion 组件目录):目录内放 `metadata.yaml`
    - gallery.html 默认生成到 LIBRARY_ROOT 下,媒体预览用相对路径(file:// 可播放)
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
<title>视频素材库 · __COUNT__ 件</title>
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  body { font-family:-apple-system,"PingFang SC","Noto Sans SC",sans-serif; background:#F6F6F1; color:#111827; padding:32px; }
  header { max-width:1200px; margin:0 auto 24px; }
  h1 { font-size:24px; margin-bottom:4px; }
  .sub { color:#6B7280; font-size:13px; }
  .bar { max-width:1200px; margin:0 auto 24px; display:flex; gap:12px; flex-wrap:wrap; }
  input,select { padding:10px 14px; border:1px solid #E5E2DA; border-radius:10px; font-size:14px; background:#fff; }
  input { flex:1; min-width:220px; }
  .grid { max-width:1200px; margin:0 auto; display:grid; grid-template-columns:repeat(auto-fill,minmax(280px,1fr)); gap:16px; }
  .card { background:#fff; border-radius:14px; padding:16px; box-shadow:0 1px 3px rgba(0,0,0,.06); display:flex; flex-direction:column; gap:8px; }
  .card h3 { font-size:15px; word-break:break-all; }
  .path { font-family:ui-monospace,Menlo,monospace; font-size:11px; color:#9CA3AF; word-break:break-all; }
  .tags { display:flex; gap:6px; flex-wrap:wrap; }
  .tag { font-size:11px; padding:2px 8px; border-radius:99px; background:#F3F4F6; color:#374151; }
  .tag.cat { background:#FF5701; color:#fff; }
  .tag.lic { background:#FEF3C7; color:#92400E; }
  .meta { font-size:12px; color:#6B7280; display:grid; grid-template-columns:auto 1fr; gap:2px 8px; }
  .meta b { color:#374151; font-weight:600; }
  video,audio,img { width:100%; border-radius:8px; background:#111; max-height:160px; object-fit:contain; }
  details { font-size:12px; color:#6B7280; }
  summary { cursor:pointer; color:#FF5701; }
  pre { background:#F9FAFB; padding:8px; border-radius:8px; overflow:auto; font-size:11px; margin-top:6px; }
  .empty { max-width:1200px; margin:60px auto; text-align:center; color:#9CA3AF; }
</style>
</head>
<body>
<header>
  <h1>🎬 视频素材库</h1>
  <div class="sub">__COUNT__ 件素材 · 生成时间 __TIME__ · 静态橱窗,入库/修改请走 video-asset-library skill</div>
</header>
<div class="bar">
  <input id="q" placeholder="搜索名称 / 路径 / 元数据…" oninput="render()">
  <select id="cat" onchange="render()"><option value="">全部分类</option></select>
  <select id="kind" onchange="render()">
    <option value="">全部形态</option>
    <option value="video">视频</option><option value="audio">音频</option>
    <option value="image">图片</option><option value="dir">组件/目录</option><option value="file">其他文件</option>
  </select>
</div>
<div class="grid" id="grid"></div>
<script>
const ITEMS = __DATA__;
const HIDE = ["id","name","type","license","source","project"];
const esc = s => String(s??"").replace(/[&<>"]/g, c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const cats = [...new Set(ITEMS.map(i=>i.category))].sort();
for (const c of cats) document.getElementById("cat").insertAdjacentHTML("beforeend", `<option>${esc(c)}</option>`);
function preview(i){
  if (i.kind==="video") return `<video src="${esc(i.path)}" controls preload="metadata"></video>`;
  if (i.kind==="audio") return `<audio src="${esc(i.path)}" controls></audio>`;
  if (i.kind==="image") return `<img src="${esc(i.path)}" loading="lazy">`;
  return "";
}
function render(){
  const q = document.getElementById("q").value.trim().toLowerCase();
  const cat = document.getElementById("cat").value;
  const kind = document.getElementById("kind").value;
  const list = ITEMS.filter(i =>
    (!cat || i.category===cat) && (!kind || i.kind===kind) &&
    (!q || JSON.stringify(i).toLowerCase().includes(q)));
  document.getElementById("grid").innerHTML = list.length ? list.map(i=>{
    const rows = Object.entries(i.meta||{}).filter(([k])=>!HIDE.includes(k))
      .map(([k,v])=>`<b>${esc(k)}</b><span>${esc(Array.isArray(v)?v.join(", "):v)}</span>`).join("");
    return `<div class="card">
      ${preview(i)}
      <h3>${esc(i.name)}</h3>
      <div class="path">${esc(i.path)}</div>
      <div class="tags">
        <span class="tag cat">${esc(i.category)}</span>
        ${i.type?`<span class="tag">${esc(i.type)}</span>`:""}
        ${i.license?`<span class="tag lic">${esc(i.license)}</span>`:""}
        ${i.source?`<span class="tag">${esc(i.source)}</span>`:""}
      </div>
      ${rows?`<div class="meta">${rows}</div>`:""}
      <details><summary>原始元数据</summary><pre>${esc(JSON.stringify(i.meta,null,2))}</pre></details>
    </div>`;
  }).join("") : `<div class="empty">没有匹配的素材</div>`;
}
render();
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
