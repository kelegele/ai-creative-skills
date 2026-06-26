#!/usr/bin/env python3
"""标点全角化:把中文语境的半角标点转中文全角。

保护(不改):
- HTML:  <style> 块、标签属性(style="...")、HTML 注释
- Markdown: frontmatter YAML 键(title: 的冒号)、图片/链接语法(![]() []())、URL(https://)
- 通用:  代码块(```...```)、inline code(`...`)—— 若存在则遮罩保护

映射:, : ? ! ; ( )  →  ， ： ？ ！ ； （ ）

用法:
  uv run python punct_normalize.py <file.md|file.html>

退出码 0 = 处理完成。
"""
import re
import sys
from functools import reduce
from pathlib import Path

MAPPING = {
    ',': '，', ':': '：', '?': '？', '!': '！', ';': '；',
    '(': '（', ')': '）',
}


def conv(s: str) -> str:
    """逐字符替换半角标点为全角。"""
    return ''.join(MAPPING.get(c, c) for c in s)


def normalize_markdown(text: str) -> str:
    # 分离 frontmatter(首个 ---...--- 块)
    fm_match = re.match(r'^(---\n.*?\n---\n)(.*)$', text, re.DOTALL)
    if fm_match:
        fm, body = fm_match.group(1), fm_match.group(2)
    else:
        fm, body = '', text

    # frontmatter:只改 value,键和分隔冒号不动(title: ← 这个冒号保留)
    if fm:
        new_lines = []
        for line in fm.split('\n'):
            km = re.match(r'^([a-zA-Z_]+)(:)(\s?)(.*)$', line)
            if km:
                k, c, sp, v = km.groups()
                new_lines.append(k + c + sp + conv(v))
            else:
                new_lines.append(line)  # --- 分隔行 / 空行原样
        fm = '\n'.join(new_lines)

    # body:遮罩图片 / 链接 / URL / 代码块 → 全角化 → 还原
    placeholders: dict[str, str] = {}

    def hide(m):
        key = '\x00%d\x00' % len(placeholders)
        placeholders[key] = m.group(0)
        return key

    body = re.sub(r'```.*?```', hide, body, flags=re.DOTALL)  # 代码块
    body = re.sub(r'`[^`]*`', hide, body)                      # inline code
    body = re.sub(r'!\[[^\]]*\]\([^)]*\)', hide, body)         # 图片
    body = re.sub(r'\[[^\]]*\]\([^)]*\)', hide, body)          # 链接
    body = re.sub(r'https?://\S+', hide, body)                 # 裸 URL

    body = conv(body)
    body = reduce(lambda s, kv: s.replace(kv[0], kv[1]), placeholders.items(), body)
    return fm + body


def normalize_html(text: str) -> str:
    # 只处理 <body>...</body>(避开 head 的 <style> / <title>)
    bs = text.find('<body>')
    be = text.find('</body>')
    if bs == -1 or be == -1:
        return text  # 无 body 结构,不动(避免误伤)
    head, body, tail = text[:bs], text[bs:be], text[be:]
    # 正则 >文本< 只命中文本节点;标签属性(style="...")和 <style> 块天然在 < > 之间,碰不到
    body = re.sub(r'>([^<]*)<', lambda m: '>' + conv(m.group(1)) + '<', body)
    return head + body + tail


def main():
    if len(sys.argv) < 2:
        print('用法: uv run python punct_normalize.py <file.md|file.html>', file=sys.stderr)
        sys.exit(1)
    path = Path(sys.argv[1])
    if not path.exists():
        print(f'文件不存在: {path}', file=sys.stderr)
        sys.exit(1)
    text = path.read_text(encoding='utf-8')
    new = normalize_html(text) if path.suffix == '.html' else normalize_markdown(text)
    path.write_text(new, encoding='utf-8')
    print(f'done: {path}')


if __name__ == '__main__':
    main()
