#!/usr/bin/env python3
"""drawio-best-practice 文件校验器。

用法:
    python3 validate_drawio.py <file.drawio> [<file2.drawio> ...]

退出码: 0=通过, 1=存在 error 或文件不可读, 2=用法错误。
warning 不影响退出码，但应逐条确认。

仅依赖 Python 3 标准库。真实解析 XML（非正则），因此能检出
实体转义后仍缺 html=1 的场景；不检查 style 尾分号、自闭合空格
等 drawio 本身兼容的写法。
"""
import os
import re
import sys
import xml.etree.ElementTree as ET

RED = "\x1b[31m"
YELLOW = "\x1b[33m"
GREEN = "\x1b[32m"
DIM = "\x1b[2m"
RESET = "\x1b[0m"

HTML_TAG_RE = re.compile(r"<\s*(br|div|b|i|u|font|hr|span|p|table|tr|td)\b", re.I)
MARKDOWN_TABLE_RE = re.compile(r"\|\s*:?-{3,}")
TD_PX_WIDTH_RE = re.compile(r"<td[^>]*?width:(\d+)px", re.I)

# mxGraphModel pageHeight 缺省值（drawio 默认 A4 纵向）
DEFAULT_PAGE_HEIGHT = 1169


def _geometry_of(cell):
    for child in cell:
        if child.tag == "mxGeometry":
            return child
    return None


def _is_floating_edge(cell):
    geo = _geometry_of(cell)
    if geo is None:
        return False
    kinds = {
        p.get("as", "") for p in geo if p.tag == "mxPoint"
    }
    return "sourcePoint" in kinds and "targetPoint" in kinds


def _cell_label(cell):
    cid = cell.get("id")
    if cid:
        return f'id="{cid}"'
    value = cell.get("value")
    if value:
        shown = value if len(value) <= 20 else value[:17] + "..."
        return f'value="{shown}"'
    style = cell.get("style")
    if style:
        shown = style if len(style) <= 24 else style[:21] + "..."
        return f'style="{shown}"'
    return "(无 id 的 cell)"


def _iter_ints(*values):
    for v in values:
        try:
            yield int(v)
        except (TypeError, ValueError):
            continue


def _check_page(diagram, page_name, errors, warnings):
    model = diagram.find("mxGraphModel")
    if model is None:
        errors.append(f"页 [{page_name}] 缺少 <mxGraphModel>")
        return
    root = model.find("root")
    if root is None:
        errors.append(f"页 [{page_name}] 缺少 <root>")
        return

    cells = list(root.iter("mxCell"))
    user_objects = list(root.iter("UserObject"))

    ids = {}
    for el in (*cells, *user_objects):
        cid = el.get("id")
        if cid:
            ids.setdefault(cid, []).append(el.tag)

    # 保留节点
    if "0" not in ids:
        errors.append('页 [{}] 缺少保留节点 <mxCell id="0"/>'.format(page_name))
    if "1" not in ids:
        errors.append('页 [{}] 缺少保留 layer <mxCell id="1" parent="0"/>'.format(page_name))

    # 页内重复 id（跨页同名合法）
    for cid, tags in ids.items():
        if len(tags) > 1:
            errors.append(
                f"页 [{page_name}] id 重复: id=\"{cid}\" 被 {len(tags)} 个元素使用"
                "（引用会指向错误对象）"
            )

    # 悬空引用
    for cell in cells:
        label = _cell_label(cell)
        for attr in ("parent", "source", "target"):
            ref = cell.get(attr)
            if ref and ref not in ids:
                errors.append(
                    f"页 [{page_name}] cell {label}: {attr}=\"{ref}\" 指向不存在的 id"
                )

    max_bottom = None
    for cell in cells:
        label = _cell_label(cell)
        style = cell.get("style") or ""
        value = cell.get("value") or ""

        if style and "shape=table" in style:
            errors.append(
                f"页 [{page_name}] cell {label}: style 含 shape=table"
                "（与 HTML 表格双引擎冲突导致裁切），改用 overflow=fill"
            )

        if value:
            if MARKDOWN_TABLE_RE.search(value):
                errors.append(
                    f"页 [{page_name}] cell {label}: value 含 markdown 表格语法"
                    "（drawio 不渲染 markdown），改用 HTML <table>"
                )
            if HTML_TAG_RE.search(value) and "html=1" not in style:
                errors.append(
                    f"页 [{page_name}] cell {label}: value 含 HTML 标签但 style 缺 html=1，"
                    "HTML 不会被渲染"
                )

        if cell.get("vertex") == "1":
            geo = _geometry_of(cell)
            if geo is None:
                errors.append(f"页 [{page_name}] vertex {label}: 缺少 <mxGeometry>")
            else:
                w, h = geo.get("width"), geo.get("height")
                if w is None or h is None:
                    errors.append(
                        f"页 [{page_name}] vertex {label}: <mxGeometry> 缺少宽高"
                    )
                else:
                    nums = list(_iter_ints(geo.get("x"), geo.get("y"), w, h))
                    if len(nums) == 4:
                        bottom = nums[1] + nums[3]
                        max_bottom = (
                            bottom if max_bottom is None else max(max_bottom, bottom)
                        )
                if "<table" in value.lower():
                    px_widths = [int(m) for m in TD_PX_WIDTH_RE.findall(value)]
                    try:
                        cell_w = int(geo.get("width", ""))
                    except ValueError:
                        cell_w = None
                    if cell_w and len(px_widths) >= 2:
                        need = sum(px_widths) + 9 * len(px_widths) + 4
                        if need > cell_w:
                            warnings.append(
                                f"页 [{page_name}] cell {label}: 表格列宽总和"
                                f" {sum(px_widths)}px + 开销 {9 * len(px_widths) + 4}px"
                                f" > cell 宽 {cell_w}px，最右列可能被裁剪"
                                "（规则：cell 宽 ≥ Σ(td 宽) + 9×列数 + 4px）"
                            )

        if cell.get("edge") == "1":
            missing = [
                attr for attr in ("source", "target") if not cell.get(attr)
            ]
            if missing and not _is_floating_edge(cell):
                errors.append(
                    f"页 [{page_name}] edge {label}: 缺少 {'/'.join(missing)}"
                    "（浮动连线需同时有 sourcePoint/targetPoint）"
                )

    # 页面高度（page=0 时不限制）
    page_attr = model.get("page", "1")
    if page_attr != "0" and max_bottom is not None:
        try:
            page_height = int(model.get("pageHeight", DEFAULT_PAGE_HEIGHT))
        except ValueError:
            page_height = DEFAULT_PAGE_HEIGHT
        if max_bottom > page_height:
            warnings.append(
                f"页 [{page_name}] 内容最低点 y={max_bottom} 超过 pageHeight={page_height}，"
                "分页/打印时会被裁切（page=0 或调大 pageHeight）"
            )


def validate_file(path):
    """校验单个文件，返回 (errors, warnings)，消息均为字符串。"""
    errors, warnings = [], []
    if not os.path.exists(path):
        errors.append(f"文件不存在: {path}")
        return errors, warnings
    try:
        tree = ET.parse(path)
    except ET.ParseError as e:
        errors.append(f"XML 解析失败: {e}")
        return errors, warnings
    except OSError as e:
        errors.append(f"文件不可读: {e}")
        return errors, warnings

    root_el = tree.getroot()
    diagrams = []
    if root_el.tag == "mxfile":
        diagrams = root_el.findall("diagram")
        if not diagrams:
            errors.append("缺少 <diagram> 元素")
    elif root_el.tag == "diagram":
        diagrams = [root_el]
    else:
        errors.append("缺少 <mxfile> 根元素（drawio 文件必须以 mxfile 开头）")

    for idx, diagram in enumerate(diagrams, 1):
        page_name = diagram.get("name") or f"Page-{idx}"
        _check_page(diagram, page_name, errors, warnings)

    return errors, warnings


def main(argv):
    if len(argv) < 2:
        print("用法: python3 validate_drawio.py <file.drawio> [<file2.drawio> ...]")
        return 2

    exit_code = 0
    for path in argv[1:]:
        errors, warnings = validate_file(path)
        print(f"\n{DIM}── {path} ──{RESET}")
        if not errors and not warnings:
            print(f"{GREEN}✓ 通过{RESET}")
            continue
        for e in errors:
            print(f"{RED}✗ {e}{RESET}")
        for w in warnings:
            print(f"{YELLOW}⚠ {w}{RESET}")
        print(
            f"{DIM}error={len(errors)} warning={len(warnings)}"
            f"（error 必须修复；warning 逐条确认）{RESET}"
        )
        if errors:
            exit_code = 1
    return exit_code


if __name__ == "__main__":
    sys.exit(main(sys.argv))
