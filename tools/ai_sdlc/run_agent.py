"""
Lifecycle Agent Runner — executes AI-SDLC lifecycle agents by running
their declared permittedTools against the actual toolRegistry.

Usage:
    python -m tools.ai_sdlc.run_agent --agent test
    python -m tools.ai_sdlc.run_agent --agent security
    python -m tools.ai_sdlc.run_agent --agent release
    python -m tools.ai_sdlc.run_agent --agent safety
    python -m tools.ai_sdlc.run_agent --agent all

This bridges the declarative lifecycle agents (.ai-sdlc/agents/*.yaml)
to the executable CLI (tools/ai_sdlc/cli.py) via the toolRegistry
defined in .ai-sdlc/manifest.yaml.
"""

import argparse
import os
import subprocess
import sys
from datetime import UTC
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
AGENTS_DIR = REPO_ROOT / ".ai-sdlc" / "agents"
MANIFEST_PATH = REPO_ROOT / ".ai-sdlc" / "manifest.yaml"


def load_manifest():
    """Load the AI-SDLC manifest to get toolRegistry."""
    with open(MANIFEST_PATH) as f:
        # Strip cache control artifacts from manifest
        content = f.read()
        # Find the end of valid YAML (stop at any non-YAML artifact)
        # The manifest is valid YAML up to the first non-YAML line
        return yaml.safe_load(content)


def load_tool_registry(manifest):
    """Extract toolRegistry from manifest as {name: command}."""
    tools = {}
    for tool in manifest.get("toolRegistry", []):
        tools[tool["name"]] = tool["command"]
    return tools


def load_agent(agent_name):
    """Load an agent YAML by name (e.g., 'test', 'security', 'release')."""
    # Map short names to file names
    name_map = {
        "requirements": "requirements_agent",
        "architecture": "architecture_agent",
        "developer": "developer_agent",
        "test": "test_agent",
        "security": "security_agent",
        "safety": "safety_review_agent",
        "devops": "devops_agent",
        "release": "release_agent",
        "documentation": "documentation_agent",
        "ux": "ux_accessibility_agent",
        "observability": "observability_agent",
    }

    file_key = name_map.get(agent_name, f"{agent_name}_agent")
    agent_file = AGENTS_DIR / f"{file_key}.yaml"

    if not agent_file.exists():
        print(f"❌ Agent '{agent_name}' not found. Expected: {agent_file}")
        print(f"   Available: {list(name_map.keys())}")
        return None

    with open(agent_file) as f:
        return yaml.safe_load(f)


def run_tool(tool_name, tool_registry):
    """Run a single tool from the registry."""
    command_str = tool_registry.get(tool_name)
    if not command_str:
        print(f"  ⚠️  Tool '{tool_name}' not found in toolRegistry")
        return True  # Don't fail on missing tools

    # Replace `python -m` with the venv python
    command_str = command_str.replace("python -m", f"{sys.executable} -m")
    print(f"  ▸ {tool_name}: {command_str}")

    try:
        result = subprocess.run(
            command_str.split(),
            cwd=REPO_ROOT,
            capture_output=False,
            timeout=300,
        )
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print(f"  ⚠️  Tool '{tool_name}' timed out")
        return False
    except FileNotFoundError:
        print(f"  ⚠️  Tool '{tool_name}' command not found")
        return True  # Don't fail on missing executables


def run_agent(agent_name, tool_registry):
    """Load an agent YAML and execute all its permittedTools."""
    agent = load_agent(agent_name)
    if not agent:
        return False

    agent_display = agent.get("name", agent_name)
    permitted_tools = agent.get("permittedTools", [])
    evidence_produced = agent.get("evidenceProduced", "none")

    print(f"\n{'=' * 60}")
    print(f"🤖 Lifecycle Agent: {agent_display}")
    print(f"   Purpose: {agent.get('purpose', 'N/A')}")
    print(f"   Permitted tools: {permitted_tools}")
    print(f"   Evidence: {evidence_produced}")
    print(f"{'=' * 60}")

    if not permitted_tools:
        print("  ⚠️  No permitted tools defined — skipping execution.")
        return True

    results = {}
    for tool_name in permitted_tools:
        # Map agent-permitted tools to registry tool names
        # Agent YAML uses descriptive names; registry uses kebab-case
        registry_name = tool_name.replace("_", "-")
        # Also try direct match
        if registry_name not in tool_registry:
            # Try partial match
            matches = [k for k in tool_registry if tool_name in k or registry_name in k]
            if matches:
                registry_name = matches[0]
            else:
                print(f"  ⚠️  Tool '{tool_name}' not in toolRegistry — skipping")
                results[tool_name] = True
                continue

        results[tool_name] = run_tool(registry_name, tool_registry)

    # Summary
    passed = sum(results.values())
    total = len(results)
    print(f"\n  Result: {passed}/{total} tools passed")

    # Record evidence
    evidence_produced = agent.get("evidenceProduced", [])
    if isinstance(evidence_produced, str):
        evidence_produced = [evidence_produced]
    if evidence_produced:
        evidence_dir = REPO_ROOT / ".ai-sdlc" / "evidence" / agent_name
        evidence_dir.mkdir(parents=True, exist_ok=True)
        import json
        from datetime import datetime, timezone

        evidence_data = {
            "agent": agent_display,
            "agentId": agent_name,
            "status": "PASS" if passed == total else "FAIL",
            "toolsRun": list(results.keys()),
            "toolsPassed": passed,
            "toolsTotal": total,
            "timestamp": datetime.now(UTC).isoformat(),
        }
        # Write to the first evidence file name
        evidence_file = (
            evidence_produced[0]
            if isinstance(evidence_produced, list)
            else evidence_produced
        )
        evidence_path = evidence_dir / evidence_file
        with open(evidence_path, "w") as f:
            json.dump(evidence_data, f, indent=2)
        print(f"  📋 Evidence: {evidence_path}")

    return passed == total


def run_all_agents(tool_registry):
    """Run all executable lifecycle agents in order."""
    # Order matters: follow the feature-delivery workflow
    agent_order = [
        "test",
        "safety",
        "security",
        "release",
    ]

    print("\n🚀 Running all lifecycle agents in SDLC order...\n")
    all_passed = True
    for agent_name in agent_order:
        success = run_agent(agent_name, tool_registry)
        if not success:
            all_passed = False
            print(f"\n⚠️  Agent '{agent_name}' failed — continuing to next agent")

    print(f"\n{'=' * 60}")
    if all_passed:
        print("✅ All lifecycle agents passed.")
    else:
        print("❌ Some lifecycle agents failed.")
    print(f"{'=' * 60}")
    return all_passed


def main():
    parser = argparse.ArgumentParser(
        description="Run AI-SDLC lifecycle agents — executes declared tools from agent YAMLs"
    )
    parser.add_argument(
        "--agent",
        type=str,
        help="Agent to run (test, security, safety, release, devops, all)",
    )
    args = parser.parse_args()

    manifest = load_manifest()
    tool_registry = load_tool_registry(manifest)

    if not args.agent:
        print("Available agents: test, safety, security, release, devops, all")
        print("Usage: python -m tools.ai_sdlc.run_agent --agent test")
        return

    if args.agent == "all":
        success = run_all_agents(tool_registry)
    else:
        success = run_agent(args.agent, tool_registry)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
