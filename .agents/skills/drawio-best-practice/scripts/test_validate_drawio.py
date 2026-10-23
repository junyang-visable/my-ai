#!/usr/bin/env python3
"""validate_drawio.py 的单元测试。

运行: python3 scripts/test_validate_drawio.py
"""
import os
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import validate_drawio  # noqa: E402


def write_tmp(xml):
    fd, path = tempfile.mkstemp(suffix=".drawio")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(xml)
    return path


SKELETON = """<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net" version="24.7.6">
  <diagram id="main" name="Page-1">
    <mxGraphModel dx="1600" dy="1400" page="0" pageWidth="1600" pageHeight="1400">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        {body}
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
"""


class ValidateFileTest(unittest.TestCase):
    def validate(self, xml):
        path = write_tmp(xml)
        try:
            return validate_drawio.validate_file(path)
        finally:
            os.unlink(path)

    def errors(self, xml):
        errs, _ = self.validate(xml)
        return errs

    def warnings(self, xml):
        _, warns = self.validate(xml)
        return warns

    def test_valid_minimal_passes(self):
        xml = SKELETON.format(body="")
        self.assertEqual(self.errors(xml), [])

    def test_valid_vertex_and_edge_passes(self):
        body = (
            '<mxCell id="a" value="A" style="rounded=1;html=1;" vertex="1" parent="1">'
            '<mxGeometry x="10" y="10" width="100" height="40" as="geometry"/></mxCell>'
            '<mxCell id="b" value="B" style="rounded=1;html=1;" vertex="1" parent="1">'
            '<mxGeometry x="200" y="10" width="100" height="40" as="geometry"/></mxCell>'
            '<mxCell id="e1" style="edgeStyle=orthogonalEdgeStyle;" edge="1" parent="1" '
            'source="a" target="b">'
            '<mxGeometry relative="1" as="geometry"><Array as="points">'
            '<mxPoint x="150" y="30"/></Array></mxGeometry></mxCell>'
        )
        xml = SKELETON.format(body=body)
        errs, warns = self.validate(xml)
        self.assertEqual(errs, [])
        self.assertEqual(warns, [])

    def test_malformed_xml_is_error(self):
        errs = self.errors("<mxfile><diagram><root>")
        self.assertTrue(len(errs) == 1, errs)
        self.assertIn("XML", errs[0])

    def test_missing_structure_is_error(self):
        errs = self.errors('<?xml version="1.0"?><unrelated/>')
        joined = " ".join(errs)
        self.assertIn("mxfile", joined)

    def test_missing_reserved_cells_is_error(self):
        xml = SKELETON.format(body="")
        xml = xml.replace('<mxCell id="0"/>', "").replace('<mxCell id="1" parent="0"/>', "")
        joined = " ".join(self.errors(xml))
        self.assertIn("id=\"0\"", joined)
        self.assertIn("id=\"1\"", joined)

    def test_duplicate_id_is_error(self):
        body = (
            '<mxCell id="dup" value="A" style="html=1;" vertex="1" parent="1">'
            '<mxGeometry x="0" y="0" width="10" height="10" as="geometry"/></mxCell>'
            '<mxCell id="dup" value="B" style="html=1;" vertex="1" parent="1">'
            '<mxGeometry x="20" y="0" width="10" height="10" as="geometry"/></mxCell>'
        )
        joined = " ".join(self.errors(SKELETON.format(body=body)))
        self.assertIn("dup", joined)
        self.assertIn("重复", joined)

    def test_same_id_across_pages_is_legal(self):
        page = (
            '<diagram id="p{n}" name="P{n}"><mxGraphModel page="0"><root>'
            '<mxCell id="0"/><mxCell id="1" parent="0"/>'
            '<mxCell id="same" value="X" style="html=1;" vertex="1" parent="1">'
            '<mxGeometry x="0" y="0" width="10" height="10" as="geometry"/></mxCell>'
            "</root></mxGraphModel></diagram>"
        )
        xml = '<?xml version="1.0"?><mxfile>' + page.format(n=1) + page.format(n=2) + "</mxfile>"
        self.assertEqual(self.errors(xml), [])

    def test_dangling_target_is_error(self):
        body = (
            '<mxCell id="a" value="A" style="html=1;" vertex="1" parent="1">'
            '<mxGeometry x="0" y="0" width="10" height="10" as="geometry"/></mxCell>'
            '<mxCell id="e1" edge="1" parent="1" source="a" target="ghost">'
            '<mxGeometry relative="1" as="geometry"/></mxCell>'
        )
        joined = " ".join(self.errors(SKELETON.format(body=body)))
        self.assertIn("ghost", joined)

    def test_dangling_parent_is_error(self):
        body = (
            '<mxCell id="a" value="A" style="html=1;" vertex="1" parent="nope">'
            '<mxGeometry x="0" y="0" width="10" height="10" as="geometry"/></mxCell>'
        )
        joined = " ".join(self.errors(SKELETON.format(body=body)))
        self.assertIn("nope", joined)

    def test_vertex_without_geometry_is_error(self):
        body = '<mxCell id="a" value="A" style="html=1;" vertex="1" parent="1"/>'
        joined = " ".join(self.errors(SKELETON.format(body=body)))
        self.assertIn("a", joined)
        self.assertIn("mxGeometry", joined)

    def test_vertex_geometry_without_size_is_error(self):
        body = (
            '<mxCell id="a" value="A" style="html=1;" vertex="1" parent="1">'
            '<mxGeometry x="0" y="0" as="geometry"/></mxCell>'
        )
        joined = " ".join(self.errors(SKELETON.format(body=body)))
        self.assertIn("宽高", joined)

    def test_edge_without_source_is_error(self):
        body = (
            '<mxCell id="a" value="A" style="html=1;" vertex="1" parent="1">'
            '<mxGeometry x="0" y="0" width="10" height="10" as="geometry"/></mxCell>'
            '<mxCell id="e1" edge="1" parent="1" target="a">'
            '<mxGeometry relative="1" as="geometry"/></mxCell>'
        )
        joined = " ".join(self.errors(SKELETON.format(body=body)))
        self.assertIn("e1", joined)
        self.assertIn("source", joined)

    def test_floating_edge_with_endpoints_passes(self):
        body = (
            '<mxCell id="e1" edge="1" parent="1">'
            '<mxGeometry relative="1" as="geometry">'
            '<mxPoint x="0" y="0" as="sourcePoint"/>'
            '<mxPoint x="100" y="100" as="targetPoint"/>'
            "</mxGeometry></mxCell>"
        )
        self.assertEqual(self.errors(SKELETON.format(body=body)), [])

    def test_html_value_without_html1_is_error(self):
        body = (
            '<mxCell id="a" value="第一行&lt;br&gt;第二行" style="rounded=1;" vertex="1" parent="1">'
            '<mxGeometry x="0" y="0" width="10" height="10" as="geometry"/></mxCell>'
        )
        joined = " ".join(self.errors(SKELETON.format(body=body)))
        self.assertIn("html=1", joined)

    def test_entity_encoded_html_also_detected(self):
        # value 以 &lt;b&gt; 转义写入：真实解析后应同样检出
        body = (
            '<mxCell id="a" value="&amp;lt;b&amp;gt;x&amp;lt;/b&amp;gt;" style="rounded=1;" '
            'vertex="1" parent="1">'
            '<mxGeometry x="0" y="0" width="10" height="10" as="geometry"/></mxCell>'
        )
        self.assertEqual(self.errors(SKELETON.format(body=body)), [])

    def test_shape_table_style_is_error(self):
        body = (
            '<mxCell id="a" value="x" style="shape=table;html=1;" vertex="1" parent="1">'
            '<mxGeometry x="0" y="0" width="10" height="10" as="geometry"/></mxCell>'
        )
        joined = " ".join(self.errors(SKELETON.format(body=body)))
        self.assertIn("shape=table", joined)

    def test_markdown_table_in_value_is_error(self):
        body = (
            '<mxCell id="a" value="| a | b |&#10;|---|---|&#10;| 1 | 2 |" style="html=1;" '
            'vertex="1" parent="1">'
            '<mxGeometry x="0" y="0" width="10" height="10" as="geometry"/></mxCell>'
        )
        joined = " ".join(self.errors(SKELETON.format(body=body)))
        self.assertIn("markdown", joined)

    def test_userobject_wrapped_cell_passes(self):
        body = (
            '<UserObject label="DRG-1234" link="https://example.com" id="card1">'
            '<mxCell style="rounded=1;html=1;" vertex="1" parent="1">'
            '<mxGeometry x="0" y="0" width="100" height="30" as="geometry"/></mxCell>'
            "</UserObject>"
            '<mxCell id="e1" edge="1" parent="1" source="card1" target="card1">'
            '<mxGeometry relative="1" as="geometry"/></mxCell>'
        )
        self.assertEqual(self.errors(SKELETON.format(body=body)), [])

    def test_duplicate_id_between_userobject_and_cell_is_error(self):
        body = (
            '<UserObject label="X" id="dup">'
            '<mxCell style="html=1;" vertex="1" parent="1">'
            '<mxGeometry x="0" y="0" width="10" height="10" as="geometry"/></mxCell>'
            "</UserObject>"
            '<mxCell id="dup" value="Y" style="html=1;" vertex="1" parent="1">'
            '<mxGeometry x="20" y="0" width="10" height="10" as="geometry"/></mxCell>'
        )
        joined = " ".join(self.errors(SKELETON.format(body=body)))
        self.assertIn("重复", joined)

    def test_pageheight_overflow_warning(self):
        body = (
            '<mxCell id="a" value="A" style="html=1;" vertex="1" parent="1">'
            '<mxGeometry x="0" y="1350" width="100" height="100" as="geometry"/></mxCell>'
        )
        xml = SKELETON.format(body=body).replace('page="0"', 'page="1"')
        warns = self.warnings(xml)
        self.assertTrue(any("pageHeight" in w for w in warns), warns)

    def test_page_0_never_warns_pageheight(self):
        body = (
            '<mxCell id="a" value="A" style="html=1;" vertex="1" parent="1">'
            '<mxGeometry x="0" y="99999" width="100" height="100" as="geometry"/></mxCell>'
        )
        xml = SKELETON.format(body=body)
        self.assertEqual(self.warnings(xml), [])

    def test_table_column_overflow_warning(self):
        # 3 列 td px 宽共 300，cell 宽 300：300 + 9*3 + 4 > 300 → 警告
        value = (
            "&lt;table style='width:100%;table-layout:fixed;'&gt;"
            "&lt;tr&gt;&lt;td style='width:100px;'&gt;a&lt;/td&gt;"
            "&lt;td style='width:100px;'&gt;b&lt;/td&gt;"
            "&lt;td style='width:100px;'&gt;c&lt;/td&gt;&lt;/tr&gt;&lt;/table&gt;"
        )
        body = (
            f'<mxCell id="t1" value="{value}" '
            'style="rounded=0;whiteSpace=wrap;html=1;overflow=fill;verticalAlign=top;" '
            'vertex="1" parent="1">'
            '<mxGeometry x="50" y="100" width="300" height="80" as="geometry"/></mxCell>'
        )
        warns = self.warnings(SKELETON.format(body=body))
        self.assertTrue(any("列宽" in w for w in warns), warns)

    def test_table_with_slack_no_warning(self):
        value = (
            "&lt;table style='width:100%;table-layout:fixed;'&gt;"
            "&lt;tr&gt;&lt;td style='width:80px;'&gt;a&lt;/td&gt;"
            "&lt;td style='width:80px;'&gt;b&lt;/td&gt;&lt;/tr&gt;&lt;/table&gt;"
        )
        body = (
            f'<mxCell id="t1" value="{value}" '
            'style="rounded=0;whiteSpace=wrap;html=1;overflow=fill;verticalAlign=top;" '
            'vertex="1" parent="1">'
            '<mxGeometry x="50" y="100" width="300" height="80" as="geometry"/></mxCell>'
        )
        self.assertEqual(self.warnings(SKELETON.format(body=body)), [])


class MainTest(unittest.TestCase):
    def run_main(self, *args):
        return validate_drawio.main(["validate_drawio.py", *args])

    def test_exit_0_for_valid_file(self):
        path = write_tmp(SKELETON.format(body=""))
        try:
            self.assertEqual(self.run_main(path), 0)
        finally:
            os.unlink(path)

    def test_exit_1_for_error_file(self):
        path = write_tmp("<mxfile><diagram><root></root></diagram></mxfile>")
        try:
            self.assertEqual(self.run_main(path), 1)
        finally:
            os.unlink(path)

    def test_exit_2_without_args(self):
        self.assertEqual(self.run_main(), 2)

    def test_exit_1_for_missing_file(self):
        self.assertEqual(self.run_main("/nonexistent.drawio"), 1)

    def test_output_contains_cell_details(self):
        body = (
            '<mxCell id="a" value="A" style="html=1;" vertex="1" parent="ghost">'
            '<mxGeometry x="0" y="0" width="10" height="10" as="geometry"/></mxCell>'
        )
        path = write_tmp(SKELETON.format(body=body))
        try:
            buf = sys.stdout
            from io import StringIO

            out = StringIO()
            sys.stdout = out
            try:
                code = self.run_main(path)
            finally:
                sys.stdout = buf
            self.assertEqual(code, 1)
            self.assertIn("ghost", out.getvalue())
        finally:
            os.unlink(path)


class RealWorldRegressionTest(unittest.TestCase):
    """仓库内存量文件回归：已有规范产出的文件必须 0 error。"""

    REPO_ROOT = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "..", "..")
    )

    def test_repo_existing_files_pass(self):
        kb = os.path.join(self.REPO_ROOT, "knowledge-base")
        files = [
            os.path.join(kb, "V-Frontend-Monitor-告警能力清单.drawio"),
            os.path.join(kb, "extreme-scenario-alert-config.drawio"),
            os.path.join(kb, "monitoring-alert-补全计划.drawio"),
        ]
        for f in files:
            with self.subTest(file=f):
                self.assertTrue(os.path.exists(f), f"缺少回归样本: {f}")
                errs, _ = validate_drawio.validate_file(f)
                self.assertEqual(errs, [], f"{f} 存在 error")


if __name__ == "__main__":
    unittest.main(verbosity=2)
