"""
Skill 执行结果管理器。
按 Skill 隔离存储每次执行的结果摘要，支持过期自动清理和跨 Skill 查询。
outcomes 文件存放在每个 skill 自身目录下的 memory/ 文件夹中。

用法:
  python scripts/outcome_manager.py write <skill_name> '<json摘要>'
  python scripts/outcome_manager.py read <skill_name>
  python scripts/outcome_manager.py read <skill_name> --latest
  python scripts/outcome_manager.py clean <skill_name>
"""
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

SKILLS_DIR = Path(__file__).parent.parent.parent
CONFIG_FILE = Path(__file__).parent.parent / "outcome_config.json"

DEFAULT_TTL_DAYS = {
    "store-diagnostics": 7,
    "visable-product-opt": 30,
    "business-insight": 7,
}
FALLBACK_TTL_DAYS = 14
MAX_ENTRIES = 20


def _outcome_file(skill_name):
    return SKILLS_DIR / skill_name / "memory" / "outcomes.json"


def _default_data():
    return {"version": "1.0", "entries": []}


def _load(skill_name):
    fpath = _outcome_file(skill_name)
    if not fpath.exists():
        return _default_data()
    try:
        with open(fpath, "r", encoding="utf-8") as f:
            data = json.load(f)
        if "entries" not in data:
            data["entries"] = []
        return data
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        print(f"[warn] outcomes 文件损坏，已重置 ({skill_name}): {e}", file=sys.stderr)
        return _default_data()


def _save(skill_name, data):
    fpath = _outcome_file(skill_name)
    fpath.parent.mkdir(parents=True, exist_ok=True)
    tmp = fpath.with_suffix(".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    tmp.replace(fpath)


def _clean_expired(data, skill_name):
    """删除过期条目，保留最多 MAX_ENTRIES 条。"""
    now = datetime.now()
    ttl = DEFAULT_TTL_DAYS.get(skill_name, FALLBACK_TTL_DAYS)
    valid = []
    for entry in data["entries"]:
        try:
            expires = datetime.fromisoformat(entry["expires_at"])
            if expires > now:
                valid.append(entry)
        except (KeyError, ValueError):
            try:
                ts = datetime.fromisoformat(entry["timestamp"])
                if (now - ts).days < ttl:
                    valid.append(entry)
            except (KeyError, ValueError):
                pass
    valid.sort(key=lambda e: e.get("timestamp", ""), reverse=True)
    data["entries"] = valid[:MAX_ENTRIES]
    return data


def cmd_write(skill_name, outcome_json):
    """写入一条执行结果。"""
    try:
        outcome = json.loads(outcome_json)
    except json.JSONDecodeError as e:
        print(json.dumps({"status": "error", "message": f"JSON 解析失败: {e}"}, ensure_ascii=False))
        sys.exit(1)

    now = datetime.now()
    ttl = DEFAULT_TTL_DAYS.get(skill_name, FALLBACK_TTL_DAYS)

    entry = {
        "timestamp": now.isoformat(timespec="seconds"),
        "expires_at": (now + timedelta(days=ttl)).isoformat(timespec="seconds"),
        "skill": skill_name,
        **outcome,
    }

    data = _load(skill_name)
    data["entries"].append(entry)
    data = _clean_expired(data, skill_name)
    _save(skill_name, data)

    print(json.dumps({"status": "ok", "skill": skill_name, "entries_count": len(data["entries"])}, ensure_ascii=False))


def cmd_read(skill_name, latest_only=False):
    """读取执行结果，自动清理过期条目。"""
    data = _load(skill_name)
    data = _clean_expired(data, skill_name)
    _save(skill_name, data)

    if latest_only and data["entries"]:
        print(json.dumps(data["entries"][0], ensure_ascii=False, indent=2))
    else:
        print(json.dumps(data, ensure_ascii=False, indent=2))


def cmd_clean(skill_name):
    """手动清理过期条目。"""
    data = _load(skill_name)
    before = len(data["entries"])
    data = _clean_expired(data, skill_name)
    after = len(data["entries"])
    _save(skill_name, data)
    print(json.dumps({"status": "ok", "removed": before - after, "remaining": after}, ensure_ascii=False))


def main():
    if len(sys.argv) < 3:
        print(__doc__, file=sys.stderr)
        sys.exit(1)

    cmd = sys.argv[1]
    skill_name = sys.argv[2]

    if cmd == "write":
        if len(sys.argv) < 4:
            print("用法: python scripts/outcome_manager.py write <skill_name> '<json>'", file=sys.stderr)
            sys.exit(1)
        cmd_write(skill_name, sys.argv[3])
    elif cmd == "read":
        latest = "--latest" in sys.argv
        cmd_read(skill_name, latest_only=latest)
    elif cmd == "clean":
        cmd_clean(skill_name)
    else:
        print(f"未知命令: {cmd}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
