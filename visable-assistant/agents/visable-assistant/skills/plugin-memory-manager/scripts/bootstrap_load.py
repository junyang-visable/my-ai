"""
一次性加载所有前置记忆数据 + 生命周期检查。（支持多供应商）

替代以下多次独立工具调用：
  - read: GLOBAL_PREFERENCES.json
  - read: GLOBAL_RULES.json
  - read: suppliers/INDEX.json
  - read: suppliers/<supplier_id>/SUPPLIER_PROFILE.json
  - read: suppliers/<supplier_id>/LEARNED_RULES.json
  - bash: memory_manager.py read <skill>
  - bash: linker.py context <skill>
  - read: last_dream_ts
  - bash: skill_lifecycle.py before <skill> "<query>"

用法:
  python scripts/bootstrap_load.py <skill_name> "<user_query>" [supplier_id]

  supplier_id 可选：
    - 提供时：加载指定供应商数据
    - 未提供时：从 INDEX.json 读取 lastActiveId 自动选择

输出 JSON:
  {
    "global_preferences": {...} | null,
    "global_rules": {...} | null,
    "supplier_index": {...} | null,
    "supplier_id": "supplier-001" | null,
    "supplier_profile": {...} | null,
    "supplier_rules": {...} | null,
    "memory": {"entries": {}, "version": "1.0", "window_days": 30},
    "context": [...] | null,
    "dream_needed": true | false,
    "lifecycle": {"action": "proceed" | "jit", ...}
  }
"""
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent
SKILLS_DIR = SCRIPTS_DIR.parent.parent
AGENT_CORE = SKILLS_DIR.parent
MEMORY_DIR = AGENT_CORE / "memory"
SUPPLIERS_DIR = MEMORY_DIR / "suppliers"

if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))


def _load_json_file(fpath):
    """安全加载 JSON 文件，不存在或损坏时返回 None。"""
    if not fpath.exists():
        return None
    try:
        with open(fpath, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError, OSError):
        return None


def _load_global_data():
    """加载全局偏好和规则。"""
    return {
        "global_preferences": _load_json_file(MEMORY_DIR / "GLOBAL_PREFERENCES.json"),
        "global_rules": _load_json_file(MEMORY_DIR / "GLOBAL_RULES.json"),
    }


def _resolve_supplier_id(requested_id=None):
    """解析当前活跃的供应商 ID。"""
    index = _load_json_file(SUPPLIERS_DIR / "INDEX.json")
    if not index:
        return None, None

    suppliers = index.get("suppliers", {})
    if not suppliers:
        return None, index

    # 如果明确传入了 supplier_id，优先使用
    if requested_id and requested_id in suppliers:
        return requested_id, index

    # 否则使用 lastActiveId
    last_active = index.get("lastActiveId")
    if last_active and last_active in suppliers:
        return last_active, index

    # 最后兜底：取第一个
    return next(iter(suppliers)), index


def _load_supplier_data(supplier_id):
    """加载指定供应商的画像和规则。"""
    if not supplier_id:
        return {"supplier_profile": None, "supplier_rules": None}

    supplier_dir = SUPPLIERS_DIR / supplier_id
    return {
        "supplier_profile": _load_json_file(supplier_dir / "SUPPLIER_PROFILE.json"),
        "supplier_rules": _load_json_file(supplier_dir / "LEARNED_RULES.json"),
    }


def _load_memory(skill_name):
    """加载追问记忆并自动压缩。"""
    try:
        import memory_manager
        data = memory_manager._load(skill_name)
        data = memory_manager._compress(data)
        memory_manager._save(skill_name, data)
        return data
    except Exception as e:
        print(f"[warn] 加载追问记忆失败 ({skill_name}): {e}", file=sys.stderr)
        return {"version": "1.0", "window_days": 30, "entries": {}}


def _load_context(skill_name):
    """加载关联技能上下文。"""
    try:
        import linker
        links = linker.LINK_MAP.get(skill_name, [])
        if not links:
            return None

        context_parts = []
        for linked_skill, purpose in links:
            outcome = linker._load_latest_outcome(linked_skill)
            if outcome and outcome.get("summary"):
                context_parts.append({
                    "source_skill": linked_skill,
                    "purpose": purpose,
                    "summary": outcome["summary"],
                    "timestamp": outcome.get("timestamp", "unknown"),
                    "alerts": outcome.get("alerts", []),
                    "opportunities": outcome.get("opportunities", []),
                })
        return context_parts if context_parts else None
    except Exception as e:
        print(f"[warn] 加载关联上下文失败 ({skill_name}): {e}", file=sys.stderr)
        return None


def _check_dream_needed():
    """检查是否需要执行记忆整理（距上次整理 ≥ 24h 或从未整理过）。"""
    dream_ts_path = MEMORY_DIR / "last_dream_ts"
    if not dream_ts_path.exists():
        return True
    try:
        ts_str = dream_ts_path.read_text(encoding="utf-8").strip()
        if not ts_str:
            return True
        last_dream = datetime.fromisoformat(ts_str)
        return (datetime.now() - last_dream) >= timedelta(hours=24)
    except (ValueError, IOError, OSError):
        return True


def _run_lifecycle_before(skill_name, user_query):
    """执行生命周期前置检查（JIT 判断等）。"""
    try:
        import skill_lifecycle
        import io
        import contextlib

        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            skill_lifecycle.cmd_before(skill_name, user_query)

        output = buf.getvalue().strip()
        if output:
            return json.loads(output)
        return {"action": "proceed"}
    except Exception as e:
        print(f"[warn] 生命周期前置检查失败 ({skill_name}): {e}", file=sys.stderr)
        return {"action": "proceed", "error": str(e)}


def main():
    if len(sys.argv) < 2:
        print(__doc__, file=sys.stderr)
        sys.exit(1)

    skill_name = sys.argv[1]
    user_query = sys.argv[2] if len(sys.argv) > 2 else ""
    requested_supplier_id = sys.argv[3] if len(sys.argv) > 3 else None

    result = {}

    # 1. 全局数据
    global_data = _load_global_data()
    result.update(global_data)

    # 2. 供应商数据
    supplier_id, supplier_index = _resolve_supplier_id(requested_supplier_id)
    result["supplier_index"] = supplier_index
    result["supplier_id"] = supplier_id
    supplier_data = _load_supplier_data(supplier_id)
    result.update(supplier_data)

    # 3. 追问记忆（按供应商隔离：skill_name + supplier_id）
    effective_skill = f"{skill_name}_{supplier_id}" if supplier_id else skill_name
    result["memory"] = _load_memory(effective_skill)

    # 4. 关联上下文
    result["context"] = _load_context(skill_name)

    # 5. Dream 检查
    result["dream_needed"] = _check_dream_needed()

    # 6. 生命周期前置检查
    result["lifecycle"] = _run_lifecycle_before(skill_name, user_query)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
