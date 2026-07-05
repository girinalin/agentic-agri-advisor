#!/usr/bin/env python3
"""
Tool Call Validation Script — Pre-execution safety guard for agent tools.

Runs as a pre-tool-use hook. Validates that tool calls don't:
- Attempt to write to OKF knowledge graph (should be read-only at runtime)
- Bypass the safety kernel
- Execute dangerous system commands
- Access files outside the project directory

Based on secure-agent-lab's validate_tool_call.py pattern.
"""

import json
import os
import re
import sys

# Tools that should NEVER be called by the agent directly
BLOCKED_TOOLS = {
    "write_okf_concept",  # OKF is static knowledge — no runtime writes
}

# Tools that require safety kernel verification after execution
SAFETY_CRITICAL_TOOLS = {
    "analyze_crop_image",
    "get_treatment_safety",
    "query_knowledge_graph",
}

# Dangerous command patterns
DANGEROUS_PATTERNS = [
    r"rm\s+-rf\s+/",
    r"rm\s+-rf\s+\*",
    r"rm\s+-f\s+/",
    r"mkfs",
    r"dd\s+if=.*of=/dev/",
    r"wget\s+.*\|\s*sh",
    r"curl\s+.*\|\s*bash",
    r"sudo\s+",
    r"chmod\s+777",
    r"eval\s*\(",
]


def validate_tool_call(tool_name: str, tool_args: dict) -> dict:
    """Validate a tool call before execution.

    Returns:
        dict: {"allow": bool, "reason": str}
    """
    # Check if tool is blocked
    if tool_name in BLOCKED_TOOLS:
        return {
            "allow": False,
            "reason": f"Tool '{tool_name}' is blocked. OKF knowledge graph is read-only at runtime.",
        }

    # Check for dangerous patterns in string arguments
    for key, value in tool_args.items():
        if isinstance(value, str):
            for pattern in DANGEROUS_PATTERNS:
                if re.search(pattern, value, re.IGNORECASE):
                    return {
                        "allow": False,
                        "reason": f"Dangerous pattern in '{key}': blocked for safety.",
                    }

        # Check for path traversal in file-related arguments
        if key in ("image_path", "output_path", "concept_path", "file_path"):
            if isinstance(value, str):
                normalized = os.path.normpath(value)
                if ".." in normalized:
                    return {
                        "allow": False,
                        "reason": f"Path traversal detected in '{key}'. Only project paths allowed.",
                    }

    # Check for prompt injection in safety-critical tool arguments
    if tool_name in SAFETY_CRITICAL_TOOLS:
        for key, value in tool_args.items():
            if isinstance(value, str):
                injection_patterns = [
                    r"ignore.*instructions",
                    r"ignore.*safety",
                    r"bypass.*kernel",
                    r"you\s+are\s+now",
                    r"system\s+prompt",
                ]
                for pattern in injection_patterns:
                    if re.search(pattern, value, re.IGNORECASE):
                        return {
                            "allow": True,  # Allow but flag for safety kernel
                            "reason": f"WARNING: Possible prompt injection in '{key}'. Safety kernel will validate.",
                        }

    return {"allow": True, "reason": "OK"}


def main():
    """Main entry point for hook execution."""
    try:
        input_data = json.load(sys.stdin)
        tool_name = input_data.get("tool_name", "")
        tool_args = input_data.get("tool_args", {})

        result = validate_tool_call(tool_name, tool_args)

        if not result["allow"]:
            print(json.dumps({"action": "block", "message": result["reason"]}))
            sys.exit(1)
        else:
            print(json.dumps({"action": "allow", "message": result["reason"]}))
            sys.exit(0)
    except Exception as e:
        print(
            json.dumps(
                {"action": "allow", "message": f"Validation error (non-blocking): {e}"}
            )
        )
        sys.exit(0)


if __name__ == "__main__":
    main()
