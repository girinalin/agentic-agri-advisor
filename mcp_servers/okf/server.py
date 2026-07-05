import os

import yaml
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("OKF-Knowledge-Graph")

BASE_OKF = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../okf"))


@mcp.tool()
async def read_okf_concept(concept_path: str) -> dict:
    """Read a specific OKF concept markdown file and return its properties.

    Args:
        concept_path: Relative path to the concept (e.g. 'crops/placeholder.md' or 'soil/nutrients/placeholder.md').
    """
    full_path = os.path.join(BASE_OKF, concept_path)
    if not os.path.exists(full_path):
        return {
            "status": "error",
            "message": f"Concept path {concept_path} not found at {full_path}.",
        }

    try:
        with open(full_path, encoding="utf-8") as f:
            content = f.read()

        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                metadata = yaml.safe_load(parts[1])
                body = parts[2].strip()
                return {"status": "success", "metadata": metadata, "body": body}
        return {"status": "success", "body": content}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def write_okf_concept(
    concept_path: str,
    type_name: str,
    name: str,
    description: str,
    properties: dict = None,
) -> dict:
    """Write or update an OKF concept markdown file.

    Args:
        concept_path: Relative path to the concept (e.g., 'crops/corn.md').
        type_name: Schema type (e.g. 'Crop', 'Soil', 'Pest').
        name: Common name of the entity.
        description: Description of the entity.
        properties: Optional dictionary of attributes.
    """
    full_path = os.path.join(BASE_OKF, concept_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    meta = {
        "id": os.path.splitext(os.path.basename(concept_path))[0],
        "type": type_name,
        "name": name,
        "description": description,
        "properties": properties or {},
    }

    yaml_str = yaml.dump(meta, sort_keys=False)
    content = f"---\n{yaml_str}---\n\n# {name}\n\n{description}\n"

    try:
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        return {
            "status": "success",
            "message": f"Concept successfully written to {concept_path}",
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
