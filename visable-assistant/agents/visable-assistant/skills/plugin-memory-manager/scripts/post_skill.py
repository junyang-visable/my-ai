"""
技能执行后：一次性完成所有写入操作。（支持多供应商）

替代以下多次独立工具调用：
  - bash: memory_manager.py update <skill> "<query>"
  - bash: skill_lifecycle.py after <skill> '<outcome_json>'
  - write/edit: GLOBAL_PREFERENCES.json
  - write/edit: GLOBAL_RULES.json
  - write/edit: suppliers/INDEX.json（更新 lastActiveId / lastActiveAt）
  - write/edit: suppliers/<id>/SUPPLIER_PROFILE.json
  - write/edit: suppliers/<id>/LEARNED_RULES.json
  - write: last_dream_ts

用法:
  python scripts/post_skill.py <skill_name> '<json>'

JSON 入参（均为可选，按需填写）：
  {
    "supplier_id": "supplier-001",        ← 本次操作的供应商 ID（可选，有则更新活跃状态）
    "memory_query": "店铺信息完整度如何",   ← 用户追问（去掉口语前缀）
    "outcome": {                           ← 技能执行结果摘要
      "summary": "店铺健康度72分，缺公司认证",
      "alerts": ["公司认证未填写"]
    },
    "profile_updates": {                  ← 本轮发现的信息更新
      "global_preferences": {"output_format": "table"},
      "global_rules": "商品描述不超过200字",
      "supplier_profile": {"categories": "五金工具"},
      "supplier_rules": "该供应商不做液体类产品"
    },
    "dream_executed": true                ← 本轮是否执行了记忆整理
  }

输出: {"status": "ok", "written": [...]}
"""
import json
import sys
from datetime import datetime
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent
SKILLS_DIR = SCRIPTS_DIR.parent.parent
AGENT_CORE = SKILLS_DIR.parent
MEMORY_DIR = AGENT_CORE / "memory"
SUPPLIERS_DIR = MEMORY_DIR / "suppliers"

if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))


def _load_json(fpath):
    if not fpath.exists():
        return None
    try:
        with open(fpath, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return None


def _save_json(fpath, data):
    fpath.parent.mkdir(parents=True, exist_ok=True)
    tmp = fpath.with_suffix(".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    tmp.replace(fpath)


def _update_memory_query(skill_name, supplier_id, query):
    """更新追问记忆（按供应商隔离）。"""
    try:
        import memory_manager
        effective_skill = f"{skill_name}_{supplier_id}" if supplier_id else skill_name
        memory_manager.cmd_update(effective_skill, query)
        return True
    except Exception as e:
        print(f"[warn] 追问记忆更新失败: {e}", file=sys.stderr)
        return False


def _run_lifecycle_after(skill_name, outcome_json):
    """执行生命周期后置处理（写入 outcome + 更新 snapshot）。"""
    try:
        import skill_lifecycle
        import io
        import contextlib

        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            skill_lifecycle.cmd_after(skill_name, outcome_json)
        return True
    except Exception as e:
        print(f"[warn] 生命周期后置处理失败: {e}", file=sys.stderr)
        return False


def _update_supplier_index(supplier_id):
    """更新供应商索引的 lastActiveId 和 lastActiveAt。"""
    if not supplier_id:
        return False

    index_path = SUPPLIERS_DIR / "INDEX.json"
    index = _load_json(index_path) or {
        "version": "1.0",
        "lastUpdated": "",
        "lastActiveId": "",
        "suppliers": {},
    }

    now = datetime.now().isoformat(timespec="seconds")
    index["lastActiveId"] = supplier_id
    index["lastUpdated"] = now

    suppliers = index.setdefault("suppliers", {})
    if supplier_id not in suppliers:
        suppliers[supplier_id] = {}
    suppliers[supplier_id]["lastActiveAt"] = now

    _save_json(index_path, index)
    return True


def _deep_merge(base, updates):
    """递归合并 dict，保留已有字段。"""
    if not isinstance(base, dict) or not isinstance(updates, dict):
        return updates
    result = dict(base)
    for k, v in updates.items():
        if k in result and isinstance(result[k], dict) and isinstance(v, dict):
            result[k] = _deep_merge(result[k], v)
        else:
            result[k] = v
    return result


def _update_global_preferences(updates):
    """更新全局操作偏好。"""
    fpath = MEMORY_DIR / "GLOBAL_PREFERENCES.json"
    now = datetime.now().isoformat(timespec="seconds")
    data = _load_json(fpath) or {"version": "1.0", "lastUpdated": now}

    if isinstance(updates, dict):
        for category, fields in updates.items():
            if isinstance(fields, dict):
                data.setdefault(category, {})
                for field, value in fields.items():
                    if isinstance(value, dict):
                        data[category][field] = {**value, "updatedAt": now}
                    else:
                        data[category][field] = {
                            "value": value, "confidence": "explicit", "updatedAt": now
                        }
            else:
                data[category] = {"value": fields, "confidence": "explicit", "updatedAt": now}

    data["lastUpdated"] = now
    _save_json(fpath, data)
    return True


def _append_rule(rules_list, rule_text, context="all"):
    """向规则列表追加或强化一条规则。"""
    now = datetime.now().isoformat(timespec="seconds")
    for rule in rules_list:
        if rule.get("rule") == rule_text:
            rule["reinforceCount"] = rule.get("reinforceCount", 1) + 1
            rule["lastTriggeredAt"] = now
            return rules_list
    rules_list.append({
        "id": f"rule-{len(rules_list) + 1:03d}",
        "rule": rule_text,
        "context": context,
        "source": "用户纠正或指令",
        "createdAt": now,
        "reinforceCount": 1,
        "lastTriggeredAt": now,
    })
    return rules_list


def _update_global_rules(rule_text):
    """更新全局规则。"""
    fpath = MEMORY_DIR / "GLOBAL_RULES.json"
    now = datetime.now().isoformat(timespec="seconds")
    data = _load_json(fpath) or {"version": "1.0", "lastUpdated": now, "rules": []}
    data["rules"] = _append_rule(data.get("rules", []), rule_text)
    data["lastUpdated"] = now
    _save_json(fpath, data)
    return True


def _update_supplier_profile(supplier_id, updates):
    """更新指定供应商的画像。"""
    if not supplier_id:
        return False

    fpath = SUPPLIERS_DIR / supplier_id / "SUPPLIER_PROFILE.json"
    now = datetime.now().isoformat(timespec="seconds")
    data = _load_json(fpath) or {"version": "1.0", "lastUpdated": now, "slots": {}}

    if isinstance(updates, dict):
        slots = data.setdefault("slots", {})
        for key, value in updates.items():
            if isinstance(value, dict):
                slots[key] = {**value, "updatedAt": now}
            else:
                slots[key] = {
                    "label": key, "value": value,
                    "confidence": "explicit", "updatedAt": now, "source": "conversation"
                }

    data["lastUpdated"] = now
    _save_json(fpath, data)
    return True


def _update_supplier_rules(supplier_id, rule_text):
    """更新供应商专属规则。"""
    if not supplier_id:
        return False

    fpath = SUPPLIERS_DIR / supplier_id / "LEARNED_RULES.json"
    now = datetime.now().isoformat(timespec="seconds")
    data = _load_json(fpath) or {"version": "1.0", "lastUpdated": now, "rules": []}
    data["rules"] = _append_rule(data.get("rules", []), rule_text)
    data["lastUpdated"] = now
    _save_json(fpath, data)
    return True


def _update_dream_ts():
    """更新 last_dream_ts。"""
    ts_path = MEMORY_DIR / "last_dream_ts"
    ts_path.write_text(datetime.now().isoformat(timespec="seconds"), encoding="utf-8")
    return True


def main():
    if len(sys.argv) < 3:
        print(__doc__, file=sys.stderr)
        sys.exit(1)

    skill_name = sys.argv[1]
    try:
        payload = json.loads(sys.argv[2])
    except json.JSONDecodeError as e:
        print(json.dumps({"status": "error", "message": f"JSON 解析失败: {e}"}, ensure_ascii=False))
        sys.exit(1)

    supplier_id = payload.get("supplier_id")
    written = []

    # 1. 更新追问记忆
    if payload.get("memory_query"):
        if _update_memory_query(skill_name, supplier_id, payload["memory_query"]):
            written.append("memory")

    # 2. 写入技能执行结果 + 更新 snapshot
    if payload.get("outcome"):
        outcome_json = json.dumps(payload["outcome"], ensure_ascii=False)
        if _run_lifecycle_after(skill_name, outcome_json):
            written.append("outcome+snapshot")

    # 3. 更新供应商活跃状态
    if supplier_id:
        if _update_supplier_index(supplier_id):
            written.append("supplier_index")

    # 4. 处理 profile_updates
    profile_updates = payload.get("profile_updates", {})

    if profile_updates.get("global_preferences"):
        if _update_global_preferences(profile_updates["global_preferences"]):
            written.append("global_preferences")

    if profile_updates.get("global_rules"):
        if _update_global_rules(profile_updates["global_rules"]):
            written.append("global_rules")

    if profile_updates.get("supplier_profile") and supplier_id:
        if _update_supplier_profile(supplier_id, profile_updates["supplier_profile"]):
            written.append("supplier_profile")

    if profile_updates.get("supplier_rules") and supplier_id:
        if _update_supplier_rules(supplier_id, profile_updates["supplier_rules"]):
            written.append("supplier_rules")

    # 5. 更新 dream 时间戳
    if payload.get("dream_executed"):
        if _update_dream_ts():
            written.append("dream_ts")

    print(json.dumps({"status": "ok", "written": written}, ensure_ascii=False))


if __name__ == "__main__":
    main()
