#!/usr/bin/env python3
"""test_wordcount.py — wordcount.py 单元测试(纯 stdlib unittest)。"""
import unittest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent))
from wordcount import count_words, check_structure


SAMPLE = """---
title: 测试标题
topic: test
wordcount: 0
status: draft
---

# 测试标题

这是一段正文，短句为主，**重点加粗**。

① 第一段要点。

② 第二段要点。

**核心观点**：一句话主张。

---

### 参考来源
1. [来源](https://example.com) — 一手

### 候选标题(未选用)
- 备选一
"""


class TestCountWords(unittest.TestCase):
    def test_counts_only_body_excludes_frontmatter_and_refs(self):
        n = count_words(SAMPLE)
        self.assertTrue(20 <= n <= 45, f"got {n}")

    def test_strips_markdown_symbols(self):
        n = count_words("# 标题\n\n**加粗**\n")
        self.assertEqual(n, 4)

    def test_empty_body(self):
        n = count_words("---\nt: x\n---\n")
        self.assertEqual(n, 0)


class TestCheckStructure(unittest.TestCase):
    def test_complete_article_passes(self):
        result = check_structure(SAMPLE)
        self.assertEqual(result, [])

    def test_missing_core_view_reports(self):
        bad = SAMPLE.replace("**核心观点**：一句话主张。", "")
        result = check_structure(bad)
        self.assertIn("核心观点", "".join(result))

    def test_missing_references_reports(self):
        bad = SAMPLE.replace("### 参考来源", "### 其他")
        result = check_structure(bad)
        self.assertIn("参考来源", "".join(result))

    def test_missing_candidate_titles_reports(self):
        bad = SAMPLE.replace("### 候选标题(未选用)", "### 其他")
        result = check_structure(bad)
        self.assertIn("候选标题", "".join(result))


if __name__ == "__main__":
    unittest.main()
