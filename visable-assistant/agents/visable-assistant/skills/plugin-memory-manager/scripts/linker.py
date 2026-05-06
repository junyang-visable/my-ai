"""
Skill 信息联动器。
在 Skill 执行前，读取关联 Skill 的最新 outcomes，生成注入上下文。
在 Skill 执行后，聚合各 Skill outcomes 生成全局 state_snapshot。

用法:
  python scripts/linker.py context <skill_name>
  python scripts/linker.py snapshot
  python scripts/linker.py snapshot --read
"""
import json
import sys
from datetime import datetime
from pathlib import Path

SKILLS_DIR = Path(__file__).parent.parent.parent
MEMORY_DIR = SKILLS_DIR.parent / "memory"

# 联动关系映射：当前 skill → 需要查看哪些 skill 的 outcomes
LINK_MAP = {
    "store-diagnostics": [
        ("business-insight", "最近运营数据，结合数据判断店铺问题"),
    ],
    "product-optimization": [
        ("business-insight", "运营数据，识别曝光/转化低的商品，指导优化方向"),
        ("store-diagnostics", "店铺诊断结果，关联商品层面的问题"),
    ],
    "business-insight": [
        ("store-diagnostics", "店铺诊断结果，结合数据判断整体健康度"),
        ("product-optimization", "最近优化的商品，追踪优化效果"),
    ],
}

# 快照聚合时关注的 skill 列表（按优先级）
SNAPSHOT_SKILLS = [
    "business-insight",
    "store-diagnostics",
    "product-optimization",
]


def _load_latest_outcome(skill_name):
    """加载指定 skill 的最新一条未过期 outcome。"""
    fpath = SKILLS_DIR / skill_name / "memory" / "outcomes.json"
    if not fpath.exists():
        return None
    try:
        with open(fpath, "r", encoding="utf-8") as f:
            data = json.load(f)
        entries = data.get("entries", [])
        if not entries:
            return None
        now = datetime.now()
        for entry in entries:
            try:
                expires = datetime.fromisoformat(entry["expires_at"])
                if expires > now:
                    return entry
            except (KeyError, ValueError):
                return entry
        return None
    except (json.JSONDecodeError, KeyError, TypeError):
        return None


def cmd_context(skill_name):
    """获取关联 skill 的上下文注入内容。"""
    links = LINK_MAP.get(skill_name, [])
    if not links:
        print(json.dumps({"context": None, "message": "无关联 skill"}, ensure_ascii=False))
        return

    context_parts = []
    for linked_skill, purpose in links:
        outcome = _load_latest_outcome(linked_skill)
        if outcome and outcome.get("summary"):
            context_parts.append({
                "source_skill": linked_skill,
                "purpose": purpose,
                "summary": outcome["summary"],
                "timestamp": outcome.get("timestamp", "unknown"),
                "alerts": outcome.get("alerts", []),
                "opportunities": outcome.get("opportunities", []),
            })

    if context_parts:
        print(json.dumps({
            "context": context_parts,
            "count": len(context_parts),
        }, ensure_ascii=False, indent=2))
    else:
        print(json.dumps({"context": None, "message": "关联 skill 暂无执行记录"}, ensure_ascii=False))


def cmd_snapshot(read_only=False):
    """聚合各 skill 的 outcomes 生成全局快照。"""
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    snapshot_path = MEMORY_DIR / "state_snapshot.json"

    if read_only:
        if snapshot_path.exists():
            with open(snapshot_path, "r", encoding="utf-8") as f:
                print(f.read())
        else:
            print(json.dumps({"snapshot": None, "message": "暂无快照"}, ensure_ascii=False))
        return

    now = datetime.now()
    snapshot = {
        "snapshot_ts": now.isoformat(timespec="seconds"),
        "metrics": {},
        "alerts": [],
        "opportunities": [],
        "skill_summaries": {},
    }

    for skill_name in SNAPSHOT_SKILLS:
        outcome = _load_latest_outcome(skill_name)
        if not outcome:
            continue

        snapshot["skill_summaries"][skill_name] = {
            "summary": outcome.get("summary", ""),
            "timestamp": outcome.get("timestamp", ""),
        }

        for alert in outcome.get("alerts", []):
            snapshot["alerts"].append({
                "source": skill_name,
                "detail": alert,
                "detected_at": outcome.get("timestamp", ""),
            })
        for opp in outcome.get("opportunities", []):
            snapshot["opportunities"].append({
                "source": skill_name,
                "detail": opp,
                "detected_at": outcome.get("timestamp", ""),
            })

        if skill_name == "business-insight":
            snapshot["metrics"] = outcome.get("metrics", {})

    tmp = snapshot_path.with_suffix(".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, ensure_ascii=False, indent=2)
    tmp.replace(snapshot_path)

    print(json.dumps({
        "status": "ok",
        "alerts_count": len(snapshot["alerts"]),
        "opportunities_count": len(snapshot["opportunities"]),
        "skills_with_data": list(snapshot["skill_summaries"].keys()),
    }, ensure_ascii=False, indent=2))


def main():
    if len(sys.argv) < 2:
        print(__doc__, file=sys.stderr)
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "context":
        if len(sys.argv) < 3:
            print("用法: python scripts/linker.py context <skill_name>", file=sys.stderr)
            sys.exit(1)
        cmd_context(sys.argv[2])
    elif cmd == "snapshot":
        read_only = "--read" in sys.argv
        cmd_snapshot(read_only=read_only)
    else:
        print(f"未知命令: {cmd}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
