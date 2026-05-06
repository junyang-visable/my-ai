"""
Plugin 级 Memory 管理器。
按 Skill 隔离追踪用户追问过的原始问题，支持 30 天窗口自动压缩。
memory 文件存放在每个 skill 自身目录下的 memory/ 文件夹中。

用法:
  python scripts/memory_manager.py read <skill_name>              # 读取（自动压缩过期条目）
  python scripts/memory_manager.py update <skill_name> "<query>"  # 记录用户追问的原始问题
  python scripts/memory_manager.py compress <skill_name>          # 手动压缩
  python scripts/memory_manager.py top <skill_name> [N]           # 返回频次最高的 N 条
  python scripts/memory_manager.py distill <skill_name>           # 从高频 query 蒸馏出 skill 格式行为指导
"""
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

# scripts/ -> plugin-memory-manager/ -> skills/
SKILLS_DIR = Path(__file__).parent.parent.parent
WINDOW_DAYS = 30


def _memory_file(skill_name):
    """返回指定 Skill 的 memory 文件路径: skills/<skill_name>/memory/queries.json"""
    return SKILLS_DIR / skill_name / "memory" / "queries.json"


def _default_data():
    """返回空的 memory 数据结构。"""
    return {"version": "1.0", "window_days": WINDOW_DAYS, "entries": {}}


def _load(skill_name):
    """加载指定 Skill 的 memory 文件，不存在或损坏时返回空结构。"""
    fpath = _memory_file(skill_name)
    if not fpath.exists():
        return _default_data()
    try:
        with open(fpath, "r", encoding="utf-8") as f:
            data = json.load(f)
        if "entries" not in data:
            data["entries"] = {}
        return data
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        print(f"[warn] memory 文件损坏，已重置 ({skill_name}): {e}", file=sys.stderr)
        return _default_data()


def _save(skill_name, data):
    """原子写入：先写临时文件再重命名。自动创建 memory/ 目录。"""
    fpath = _memory_file(skill_name)
    fpath.parent.mkdir(parents=True, exist_ok=True)
    tmp_file = fpath.with_suffix(".tmp")
    with open(tmp_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    tmp_file.replace(fpath)


def _compress(data):
    """删除 last_asked 超过 WINDOW_DAYS 天的条目。"""
    cutoff = datetime.now() - timedelta(days=WINDOW_DAYS)
    expired_keys = []
    for key, entry in data["entries"].items():
        try:
            last = datetime.fromisoformat(entry["last_asked"])
            if last < cutoff:
                expired_keys.append(key)
        except (KeyError, ValueError):
            expired_keys.append(key)
    for key in expired_keys:
        del data["entries"][key]
    return data


def cmd_read(skill_name):
    """读取 memory，自动压缩后输出 JSON。"""
    data = _load(skill_name)
    data = _compress(data)
    _save(skill_name, data)
    print(json.dumps(data, ensure_ascii=False, indent=2))


def cmd_update(skill_name, query):
    """记录用户追问的原始问题。相同 query 累加频次。"""
    data = _load(skill_name)
    now = datetime.now().isoformat(timespec="seconds")
    if query in data["entries"]:
        entry = data["entries"][query]
        entry["frequency"] = entry.get("frequency", 0) + 1
        entry["last_asked"] = now
    else:
        data["entries"][query] = {
            "query": query,
            "frequency": 1,
            "first_asked": now,
            "last_asked": now,
        }
    _save(skill_name, data)
    print(json.dumps({
        "status": "ok",
        "query": query,
        "frequency": data["entries"][query]["frequency"],
    }, ensure_ascii=False))


def cmd_compress(skill_name):
    """手动压缩。"""
    data = _load(skill_name)
    before = len(data["entries"])
    data = _compress(data)
    after = len(data["entries"])
    _save(skill_name, data)
    print(json.dumps({
        "status": "ok",
        "removed": before - after,
        "remaining": after,
    }, ensure_ascii=False))


def cmd_top(skill_name, n):
    """返回频次最高的 N 条。"""
    data = _load(skill_name)
    data = _compress(data)
    _save(skill_name, data)
    sorted_entries = sorted(
        data["entries"].values(),
        key=lambda x: x.get("frequency", 0),
        reverse=True,
    )[:n]
    print(json.dumps(sorted_entries, ensure_ascii=False, indent=2))


def _query_to_skill(query, entry):
    """将一条高频 query 转换为 skill 格式的行为指导对象。"""
    frequency = entry.get("frequency", 0)
    first_asked = entry.get("first_asked", "")[:10]
    last_asked = entry.get("last_asked", "")[:10]
    return {
        "name": f"优先关注{query}",
        "principle": f"该商家高频关注「{query}」（共 {frequency} 次），"
                     f"在相关场景中优先展示此维度的数据和分析",
        "when_to_apply": f"当执行与「{query}」相关的任务时",
        "source": f"用户 {frequency} 次追问「{query}」"
                  f"（{first_asked} ~ {last_asked}）",
    }


def cmd_distill(skill_name):
    """从高频 query（frequency >= 3）蒸馏出 skill 格式的行为指导，输出 JSON 到 stdout。"""
    fpath = _memory_file(skill_name)
    if not fpath.exists():
        print(f"[warn] memory 文件不存在: {fpath}", file=sys.stderr)
        print(json.dumps({"skills": []}, ensure_ascii=False))
        return

    try:
        with open(fpath, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict) or "entries" not in data:
            raise ValueError("缺少 entries 字段")
    except (json.JSONDecodeError, ValueError, TypeError) as e:
        print(f"[warn] memory 文件损坏 ({skill_name}): {e}", file=sys.stderr)
        print(json.dumps({"skills": []}, ensure_ascii=False))
        return

    skills = []
    for query, entry in data["entries"].items():
        if not isinstance(entry, dict):
            continue
        freq = entry.get("frequency", 0)
        if isinstance(freq, (int, float)) and freq >= 3:
            skills.append(_query_to_skill(query, entry))

    print(json.dumps({"skills": skills}, ensure_ascii=False))


def main():
    if len(sys.argv) < 3:
        print(__doc__, file=sys.stderr)
        sys.exit(1)

    cmd = sys.argv[1]
    skill_name = sys.argv[2]

    if cmd == "read":
        cmd_read(skill_name)
    elif cmd == "update":
        if len(sys.argv) < 4:
            print("用法: python scripts/memory_manager.py update <skill_name> \"<query>\"",
                  file=sys.stderr)
            sys.exit(1)
        cmd_update(skill_name, sys.argv[3])
    elif cmd == "compress":
        cmd_compress(skill_name)
    elif cmd == "top":
        n = int(sys.argv[3]) if len(sys.argv) > 3 else 5
        cmd_top(skill_name, n)
    elif cmd == "distill":
        cmd_distill(skill_name)
    else:
        print(f"未知命令: {cmd}", file=sys.stderr)
        print(__doc__, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
