#!/usr/bin/env python3
"""甘特式 roadmap drawio 坐标断言脚本

用法:
    python3 verify_roadmap.py <drawio文件> <起始日期YYYY-MM-DD>

自动断言:
  1. 日期网格序列完整且相邻格 gap=14 无缺口
  2. 月份表头宽 = 当月天数×14 且首尾衔接
  3. 周末背景列坐标集合 == 日期网格中周末格坐标集合
  4. 无甘特区元素超出时间轴右缘
输出 PASS/FAIL；FAIL 时逐条列出问题 cell。
"""
import sys
import datetime as dt
import xml.etree.ElementTree as ET

DAY_W = 14


def parse(path):
    # 每次新建 parser（不可复用）；本地可信文件，无需额外加固
    return ET.parse(path)


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    path, start = sys.argv[1], sys.argv[2]
    start_date = dt.date.fromisoformat(start)

    geom = {}  # id -> (x, y, w, value)
    for c in parse(path).getroot().iter('mxCell'):
        g = c.find('mxGeometry')
        if g is None or g.get('x') is None or g.get('width') is None:
            continue
        geom[c.get('id')] = (float(g.get('x')), float(g.get('y')),
                             float(g.get('width')), c.get('value') or '')

    # 日期行 (y=142): 推断 X0 与日期映射
    date_cells = sorted((x, w, v, cid) for cid, (x, y, w, v) in geom.items() if y == 142)
    X0 = date_cells[0][0]
    total_days = len(date_cells)
    errors = []

    # 1) gap=14 且序列与自然日一致
    expect_dates = [start_date + dt.timedelta(days=i) for i in range(total_days)]
    for i, (x, w, v, cid) in enumerate(date_cells):
        if x != X0 + i * DAY_W:
            errors.append(f'日期格 {cid}({v}) x={x} 期望 {X0 + i * DAY_W}')
        if v != str(expect_dates[i].day):
            errors.append(f'日期格 {cid} 值 {v} 期望 {expect_dates[i].day}（{expect_dates[i]}）')
    right_edge = X0 + total_days * DAY_W

    # 2) 月表头（蓝条 #1565C0）：宽=当月天数×14 且按月衔接（需读 style）
    headers = []
    for c in parse(path).getroot().iter('mxCell'):
        g = c.find('mxGeometry')
        if g is None or g.get('y') != '104':
            continue
        st = c.get('style') or ''
        if '#1565C0' in st and c.get('value', '').startswith('20'):
            headers.append((float(g.get('x')), float(g.get('width')), c.get('value')))
    headers.sort()
    end_date = expect_dates[-1]
    for i, (x, w, v) in enumerate(headers):
        year, month = int(v.split('-')[0]), int(v.split('-')[1])
        first = max(dt.date(year, month, 1), start_date)  # 截断月：轴内首日
        last = min((dt.date(year + month // 12, month % 12 + 1, 1) - dt.timedelta(days=1)), end_date)
        days_in = (last - first).days + 1  # 该月在时间轴内的天数
        if w != days_in * DAY_W:
            errors.append(f'表头 {v} 宽 {w} 期望 {days_in * DAY_W}（轴内 {first} ~ {last}）')
        if x != X0 + (first - start_date).days * DAY_W:
            errors.append(f'表头 {v} x={x} 起点错位')

    # 3) 周末背景列 == 周末日期格
    # 周末格: y=142 且值与周末日期匹配 -> x；周末列: y=首行y(158) w=14 无边框 EFEFEF
    wk_date_xs = {X0 + i * DAY_W for i, d in enumerate(expect_dates) if d.weekday() >= 5}
    # 周末背景列（EFEFEF 宽 14）
    wk_cols = set()
    for c in parse(path).getroot().iter('mxCell'):
        st = c.get('style') or ''
        if 'fillColor=#EFEFEF' not in st:
            continue
        g = c.find('mxGeometry')
        if g is not None and g.get('width') == '14':
            x = float(g.get('x'))
            if X0 <= x < right_edge:
                wk_cols.add(x)
    if wk_cols != wk_date_xs:
        errors.append(f'周末列错位: 多余 {sorted(wk_cols - wk_date_xs)} 缺失 {sorted(wk_date_xs - wk_cols)}')

    # 4) 右缘溢出（甘特区元素 x>=X0）
    for cid, (x, y, w, v) in geom.items():
        if x >= X0 and x + w > right_edge + 0.5:
            errors.append(f'{cid}({v[:10]}) 右缘 {x + w} 超出 {right_edge}')

    print(f'网格: {total_days} 天 {start_date} ~ {expect_dates[-1]} | X0={X0} 右缘={right_edge}')
    print(f'表头: {len(headers)} 个月条 | 周末列: {len(wk_cols)} 根')
    if errors:
        print('FAIL:')
        for e in errors:
            print(' -', e)
        sys.exit(1)
    print('PASS')


if __name__ == '__main__':
    main()
