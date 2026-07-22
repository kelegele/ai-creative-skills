---
name: video-asset-library
description: 视频制作素材库管理。建立、分类、维护 Remotion 视频可复用资产(B-Roll/转场/动效/音频/字体/LUT/代码组件),skill 驱动入库和盘点,静态 web 橱窗查看。当用户管理视频素材、建素材库、素材入库、盘点素材、查看素材库时使用。触发词:素材库, 视频素材, 素材入库, 素材管理, asset library, B-Roll。
version: 0.1.0
author: Kelegele
license: MIT
metadata:
  tags: [video, asset-management, remotion, b-roll, motion-graphics, library]
---

# 视频制作素材库管理

系统化建立、分类、维护视频制作中的可复用资产,提升 Remotion 视频创作的效率和一致性。

## 核心原则(先记住)

- **素材库本体不进 git** —— 素材(字体/音频/B-Roll)和素材元信息(元数据 yaml、生成的索引、橱窗 HTML)都 git 不跟踪;git 里只有本 skill 的规范和 tools 里的查看器代码
- **skill 是唯一写入方** —— 入库、改元数据、盘点、维护都走本 skill 流程;web 橱窗只读
- **单一数据源** —— 文件系统目录 + 每件素材旁边的 `metadata.yaml`;索引和橱窗都是脚本重新生成的产物,可随时重建

## 路径约定(第0步问用户,存运行变量)

- **LIBRARY_ROOT** — 素材库根目录(默认 `<项目仓库>/.asset_library/`,隐藏目录、git 不跟踪;本地目录或网盘同步目录均可)
- 分类体系、元数据 schema、命名规范见 `references/library-spec.md`,不要自造分类

## 主流程(7步)

1. **需求分析** — 用途(个人/团队/商业交付)、主要视频类型、复用频率
2. **库结构设计** — 按 `references/library-spec.md` 分类体系生成目录;确认存储位置和命名规范
3. **现有资产盘点** — 扫描现有素材,按元数据 schema 分类标注,标记"可入库/需优化/废弃"
4. **缺失资产识别** — 对比目标库结构和现有资产,列缺失类别和优先级,给获取建议(自制/购买/免费资源站)
5. **入库操作** — 按命名规范重命名 → 写 `metadata.yaml`(schema 见 references)→ 生成缩略图/预览 → 放入对应目录
6. **索引与橱窗** — 跑查看器脚本重建索引和橱窗:
   ```bash
   cd <repo>/tools/asset-library-web && uv run build_gallery.py <LIBRARY_ROOT>
   ```
   生成 `gallery.html`(数据内联,双击 file:// 直接打开,不起 server)
7. **使用指南输出** — 快速索引表 + Remotion 代码引用示例(见 `references/library-spec.md` 第五节)

## 维护节奏

### 每项目结束
- [ ] 提取可复用素材补充入库
- [ ] 项目专属调色方案提炼为通用 LUT 入库
- [ ] 优化后的时间线结构 / 风格配置 / 配音配置提炼进"全案模板"(`templates/`,引用不复制)
- [ ] 项目专属素材归档(不入通用库,保留参考)

### 每季度
- [ ] 扫描冗余/过期素材,标记待清理
- [ ] 检查授权到期情况(字体/音乐/视频)
- [ ] 更新元数据标签
- [ ] 备份验证(抽查恢复测试)
- [ ] Remotion 升级后组件版本兼容性检查

## 配合

- **remotion-video** — 做视频时先从本库取可复用素材(转场/动效/音频/组件),项目结束回收可复用素材入库
- **查看器代码**:`tools/asset-library-web/`(本仓库,git 跟踪);**生成的索引/橱窗**:git 不跟踪

## References

- `references/library-spec.md` — 分类体系(目录树)、元数据 schema、命名规范、Remotion 调用示例、建库价值判断(哪些该入库/谨慎/不该)、全案模板(templates/)详解
