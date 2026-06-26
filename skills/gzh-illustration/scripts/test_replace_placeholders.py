#!/usr/bin/env python3
"""test_replace_placeholders.py — replace_placeholders.py 单元测试(纯 stdlib)。"""
import unittest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent))
from replace_placeholders import parse_placeholders, replace_draft, replace_final


ARTICLE = """---
title: 测试
---

# 测试标题

正文一段。

> 🖼️ 【封面 · 900×383 · 生成】主视觉:两个邮箱并排,左灰暗右明亮。

> 🖼️ 【配图① · 1080×自由 · 生成】收件箱 500+ 未读,红点密布。

> 🖼️ 【配图② · 1080×自由 · 自供】images/inbox.png

结尾。
"""


class TestParse(unittest.TestCase):
    def test_parse_finds_three_placeholders(self):
        phs = parse_placeholders(ARTICLE)
        self.assertEqual(len(phs), 3)

    def test_parse_extracts_fields(self):
        phs = parse_placeholders(ARTICLE)
        self.assertEqual(phs[0]["seq"], "封面")
        self.assertEqual(phs[0]["size"], "900×383")
        self.assertEqual(phs[0]["source"], "生成")
        self.assertIn("主视觉", phs[0]["desc"])
        self.assertEqual(phs[1]["seq"], "配图①")
        self.assertEqual(phs[2]["source"], "自供")
        self.assertEqual(phs[2]["desc"], "images/inbox.png")

    def test_parse_default_source_is_generate(self):
        text = "> 🖼️ 【配图① · 1080×自由】描述。\n"
        phs = parse_placeholders(text)
        self.assertEqual(phs[0]["source"], "生成")


class TestDraftMode(unittest.TestCase):
    def test_draft_inserts_image_keeps_placeholder(self):
        result = replace_draft(ARTICLE, phs=parse_placeholders(ARTICLE))
        self.assertIn("🖼️ 【封面", result)
        self.assertIn("![封面](images/gzh-imaget-封面.png)", result)
        self.assertIn("![配图①](images/gzh-imaget-配图①.png)", result)
        self.assertIn("![images/inbox.png](images/inbox.png)", result)

    def test_draft_does_not_remove_original_text(self):
        result = replace_draft(ARTICLE, phs=parse_placeholders(ARTICLE))
        self.assertIn("结尾。", result)
        self.assertIn("正文一段。", result)


class TestFinalMode(unittest.TestCase):
    def test_final_removes_placeholders_keeps_images(self):
        draft = replace_draft(ARTICLE, phs=parse_placeholders(ARTICLE))
        final = replace_final(draft)
        self.assertNotIn("🖼️", final)
        self.assertIn("gzh-imaget-封面.png", final)
        self.assertIn("images/inbox.png", final)
        self.assertIn("结尾。", final)


if __name__ == "__main__":
    unittest.main()
