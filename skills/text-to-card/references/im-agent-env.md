# IM 对话型 Agent 环境适配

面向 **Hermes / OpenClaw / QwenPaw** 等"基于 IM 对话的 agent"的环境特定操作。这些 agent 通过聊天(IM)与用户交互,因此预览/发图/取图/成品存放有共性能力,各 agent 路径不同。

主 SKILL.md 的创作流程是通用的;本文件只补充这类环境特有的交付机制。非 IM 对话型 agent(如 Claude Code、Codex CLI)通常不需要这些——直接给文件路径即可。

## 文件服务器预览(HTTP)

多卡片时,启动 HTTP 服务器让用户在手机浏览器看 HTML 源码 / 下载 zip。

```bash
# 用软链接引用成品目录(不要 cp 成品到 /tmp,避免两份不同步)
mkdir -p /tmp/cards-preview && cd /tmp/cards-preview
ln -sf <OUTPUT_DIR> output
python3 -m http.server 8899
```

**启动前必须验证端口 + 工作目录**(血泪教训:用户打开链接 404,根因是工作目录不对):
1. `lsof -ti:8899` 检查残留进程 → 有先 kill
2. 启动后验证工作目录:`ls -la /proc/$(lsof -ti:8899)/cwd` 确认指向项目目录
3. `curl -s -o /dev/null -w "%{http_code}" http://localhost:8899/card-01.html` 验证 200
4. 全部通过才告诉用户链接可用

**公网 IP**:远程 VPS 用 `curl -s4 https://api.ipify.org`,不要用 `hostname -I`(内网 IP)。用完关:`kill $(lsof -ti:8899)`。

**中文文件名**:http.server 目录含中文文件名(如 `Agent技巧-card-03.html`)→ 浏览器 404。✅ 成品用 ASCII 命名(`card-01.html`),中文只在目录/zip 名。

## IM 发图(MEDIA 机制)

通过 agent 的发图机制(如 `MEDIA:<path>`)发图给用户。

- **中文/长路径会静默失败**(API 返回 success 但用户收不到)。✅ 先 `cp` 到 `/tmp/` 纯 ASCII 名再发:`MEDIA:/tmp/card-03.png`
- 发图前检查路径,有中文就走 copy → /tmp → send
- **失败时 API 仍返回 success**,必须通过用户确认"收到了吗?"验证
- **限流**:连发 3-4 张触发限流。每张 sleep 15-30s,或改用文件服务器链接交付。最佳:发 2-3 张抽样 + zip 链接,不逐张发

## image_cache 取图

用户在 IM 发的图缓存在固定目录,直接 `cp` 到目标:
- Hermes: `/root/.hermes/image_cache/img_xxx.jpg`

用户重发截图(定版丢失恢复)时,从 image_cache `cp` 到 OUTPUT_DIR。注意手机截图是 JPG,比原始 PNG 分辨率低。

## 成品路径(按 agent)

| Agent | 成品主目录 | 备注 |
|-------|-----------|------|
| Hermes | `~/.hermes/skills/creative/text-to-card/output/YYYYMMDD-主题/` | skill output = 主目录 |
| OpenClaw | `~/.openclaw/workspace/output/` | 历史备份位,**不是主目录** |
| QwenPaw | `TODO:待补充` | 实施时确认 |

**Hermes 特有告诫**(Hermes 用户注意,其他 agent 忽略):成品放 skill output 目录,**不要放 openclaw workspace**——openclaw 与 Hermes 无关,只是归档副本。HTML + PNG 都存成品主目录。

## 版本管理

- output 下按 `YYYYMMDD-主题/` 分目录,废弃项目放 `archive/`
- 若环境对成品目录做 git 管理,遵循该环境的 git 工作流(skill 不绑定特定远程仓库)

## 多版本找定版

存在多个版本目录时:skill output 目录 = 最新(按日期);/tmp = 临时会丢;openclaw workspace = 废弃位。用户说"这版不是最新"→ 直接问哪个是定版,别翻遍目录 + vision 分析。
