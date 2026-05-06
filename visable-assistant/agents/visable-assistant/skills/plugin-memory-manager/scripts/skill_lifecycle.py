"""
Skill 生命周期管理器。
agents.md 在 skill 执行前后各调一次，本脚本读取 jit_config.json 决定做什么。

用法:
  python scripts/skill_lifecycle.py before <skill_name> "<user_query>"
  python scripts/skill_lifecycle.py after  <skill_name> "<outcome_json>"

before 阶段：检查 JIT、联动上下文。
after 阶段：写入 outcome + 更新 snapshot。
"""
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent
CONFIG_FILE = SCRIPTS_DIR.parent / "jit_config.json"
SKILLS_DIR = SCRIPTS_DIR.parent.parent
MEMORY_DIR = SKILLS_DIR.parent / "memory"

SNAPSHOT_SKILLS = [
    "visable-business-insight",
    "visable-supplier-diagnostics",
    "visable-product-opt",
]


def _load_config():
    if not CONFIG_FILE.exists():
        return None
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, KeyError):
        return None


def _load_snapshot():
    snapshot_path = MEMORY_DIR / "state_snapshot.json"
    if not snapshot_path.exists():
        return None
    try:
        with open(snapshot_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, KeyError):
        return None


def _load_latest_outcome(skill_name):
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
    except (json.JSONDecodeError, KeyError):
        return None


def _build_snapshot():
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
                "detail": alert if isinstance(alert, str) else str(alert),
                "detected_at": outcome.get("timestamp", ""),
            })
        for opp in outcome.get("opportunities", []):
            snapshot["opportunities"].append({
                "source": skill_name,
                "detail": opp if isinstance(opp, str) else str(opp),
                "detected_at": outcome.get("timestamp", ""),
            })
        if skill_name == "visable-business-insight":
            snapshot["metrics"] = outcome.get("metrics", {})
    return snapshot


def _check_jit_match(user_query, jit_config):
    query_lower = user_query.lower()
    for phrase in jit_config.get("full_report_phrases", []):
        if phrase in query_lower:
            return "full"
    for phrase in jit_config.get("trigger_phrases", []):
        if phrase in query_lower:
            return "jit"
    return "jit"


def _render_jit_brief(snapshot, age_hours):
    lines = []
    metrics = snapshot.get("metrics", {})

    if metrics:
        lines.append("📊 **店铺经营速览**")
        lines.append(f"> 数据来源：上次完整查询（{_format_age(age_hours)}前）\n")
        lines.append("| 指标 | 数值 | 环比 |")
        lines.append("|------|------|------|")
        metric_labels = {
            "orders_30d": "30天订单",
            "visitors_30d": "30天访客",
            "conversion_rate": "转化率",
            "avg_order_value": "客单价",
        }
        for key, label in metric_labels.items():
            m = metrics.get(key)
            if m is None:
                continue
            if isinstance(m, dict):
                val = m.get("value", "-")
                crc = m.get("cycleCRC", "-")
                emoji = "🟢" if isinstance(crc, str) and crc.startswith("+") else "🔴" if isinstance(crc, str) and crc.startswith("-") else "🟡"
                lines.append(f"| {label} | {val} | {emoji} {crc} |")
            else:
                lines.append(f"| {label} | {m} | - |")
        lines.append("")

    alerts = snapshot.get("alerts", [])
    if alerts:
        lines.append("⚠️ **需关注**")
        for a in alerts[:5]:
            detail = a.get("detail", a) if isinstance(a, dict) else a
            lines.append(f"- 🔴 {detail}")
        lines.append("")

    opps = snapshot.get("opportunities", [])
    if opps:
        lines.append("💡 **积极信号**")
        for o in opps[:3]:
            detail = o.get("detail", o) if isinstance(o, dict) else o
            lines.append(f"- 🟢 {detail}")
        lines.append("")

    lines.append("---")
    lines.append("回复「详细分析」获取完整数据查询，或直接追问具体指标。")
    return "\n".join(lines)


def _format_age(hours):
    if hours < 1:
        return f"{int(hours * 60)}分钟"
    elif hours < 24:
        return f"{hours:.0f}小时"
    else:
        return f"{hours / 24:.1f}天"


def cmd_before(skill_name, user_query):
    config = _load_config()
    if not config:
        print(json.dumps({"action": "proceed", "reason": "无配置文件"}, ensure_ascii=False))
        return

    skill_config = config.get("skills", {}).get(skill_name, {})
    jit_config = skill_config.get("jit", {})
    linkage_config = skill_config.get("linkage", {})

    result = {
        "action": "proceed",
        "jit_mode": False,
        "snapshot": None,
        "context": [],
        "jit_supplement_tools": [],
    }

    # JIT 判断
    if jit_config.get("enabled", False):
        snapshot = _load_snapshot()
        if snapshot and snapshot.get("snapshot_ts"):
            try:
                snap_time = datetime.fromisoformat(snapshot["snapshot_ts"])
                age_hours = (datetime.now() - snap_time).total_seconds() / 3600
                max_age = jit_config.get("max_age_hours", 24)

                if age_hours <= max_age:
                    match_type = _check_jit_match(user_query, jit_config)
                    if match_type == "jit":
                        result["action"] = "jit"
                        result["jit_mode"] = True
                        result["snapshot"] = snapshot
                        result["snapshot_age_hours"] = round(age_hours, 1)
                        result["rendered_output"] = _render_jit_brief(snapshot, age_hours)
                    else:
                        result["snapshot"] = snapshot
                        result["snapshot_age_hours"] = round(age_hours, 1)
                else:
                    result["snapshot"] = snapshot
                    result["snapshot_age_hours"] = round(age_hours, 1)
                    result["snapshot_expired"] = True
            except (ValueError, TypeError):
                pass

    # 联动上下文
    if linkage_config.get("enabled", False):
        reads_from = linkage_config.get("reads_from", [])
        for linked_skill in reads_from:
            outcome = _load_latest_outcome(linked_skill)
            if outcome and outcome.get("summary"):
                result["context"].append({
                    "source_skill": linked_skill,
                    "summary": outcome["summary"],
                    "timestamp": outcome.get("timestamp", ""),
                    "alerts": outcome.get("alerts", []),
                    "opportunities": outcome.get("opportunities", []),
                })

    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_after(skill_name, outcome_json):
    config = _load_config()
    if not config:
        print(json.dumps({"status": "skip", "reason": "无配置文件"}, ensure_ascii=False))
        return

    skill_config = config.get("skills", {}).get(skill_name, {})
    outcome_config = skill_config.get("outcome", {})

    if not outcome_config.get("enabled", False):
        print(json.dumps({"status": "skip", "reason": f"{skill_name} 未启用 outcome"}, ensure_ascii=False))
        return

    try:
        outcome = json.loads(outcome_json)
    except json.JSONDecodeError as e:
        print(json.dumps({"status": "error", "message": f"JSON 解析失败: {e}"}, ensure_ascii=False))
        return

    now = datetime.now()
    ttl = outcome_config.get("ttl_days", 14)

    entry = {
        "timestamp": now.isoformat(timespec="seconds"),
        "expires_at": (now + timedelta(days=ttl)).isoformat(timespec="seconds"),
        "skill": skill_name,
        **outcome,
    }

    outcomes_file = SKILLS_DIR / skill_name / "memory" / "outcomes.json"
    outcomes_file.parent.mkdir(parents=True, exist_ok=True)

    data = {"version": "1.0", "entries": []}
    if outcomes_file.exists():
        try:
            with open(outcomes_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, KeyError):
            pass

    data.setdefault("entries", []).append(entry)
    valid = []
    for e in data["entries"]:
        try:
            if datetime.fromisoformat(e["expires_at"]) > now:
                valid.append(e)
        except (KeyError, ValueError):
            valid.append(e)
    valid.sort(key=lambda e: e.get("timestamp", ""), reverse=True)
    data["entries"] = valid[:20]

    tmp = outcomes_file.with_suffix(".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    tmp.replace(outcomes_file)

    snapshot = _build_snapshot()
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    snapshot_path = MEMORY_DIR / "state_snapshot.json"
    tmp = snapshot_path.with_suffix(".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, ensure_ascii=False, indent=2)
    tmp.replace(snapshot_path)

    print(json.dumps({"status": "ok", "skill": skill_name, "snapshot_updated": True}, ensure_ascii=False))


def main():
    if len(sys.argv) < 3:
        print(__doc__, file=sys.stderr)
        sys.exit(1)

    cmd = sys.argv[1]
    skill_name = sys.argv[2]

    if cmd == "before":
        user_query = sys.argv[3] if len(sys.argv) > 3 else ""
        cmd_before(skill_name, user_query)
    elif cmd == "after":
        if len(sys.argv) < 4:
            print("用法: python skill_lifecycle.py after <skill_name> '<outcome_json>'", file=sys.stderr)
            sys.exit(1)
        cmd_after(skill_name, sys.argv[3])
    else:
        print(f"未知命令: {cmd}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
