import json
from pathlib import Path
from pyvis.network import Network

ROOT_DIR = Path(__file__).resolve().parent.parent.parent


def _clean_str(value, default="Unknown"):
    """Safely converts any data type (None, list, dict, float) into a valid string."""
    if value is None:
        return default
    if isinstance(value, (list, tuple, set)):
        items = [_clean_str(x, "") for x in value if x is not None]
        cleaned = ", ".join(filter(None, items))
        return cleaned if cleaned else default
    val_str = str(value).strip()
    return val_str if val_str else default


def create_graph_html(graph_data):
    net = Network(
        height="400px",
        width="100%",
        bgcolor="#ffffff",
        font_color="#0f172a",
        cdn_resources="remote"
    )

    net.repulsion(
        node_distance=150,
        spring_length=120,
        damping=0.85
    )

    output_dir = ROOT_DIR / "frontend"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "graph.html"

    if not graph_data:
        net.save_graph(str(output_file))
        return str(output_file)

    if isinstance(graph_data, dict):
        graph_data = [graph_data]
    elif isinstance(graph_data, str):
        try:
            parsed = json.loads(graph_data)
            graph_data = [parsed] if isinstance(parsed, dict) else parsed
        except Exception:
            graph_data = []

    if not isinstance(graph_data, list):
        graph_data = []

    added_nodes = set()

    for item in graph_data:
        if not isinstance(item, dict):
            continue

        # Safely convert all values to string to satisfy PyVis assert
        scheme = _clean_str(item.get("scheme"), default="Scheme")
        beneficiary = _clean_str(item.get("beneficiary"), default="Farmer")
        benefit_type = _clean_str(item.get("benefit_type"), default="Benefit")
        funding = _clean_str(item.get("funding"), default="Funding")

        # Add Nodes safely (avoiding duplicate additions)
        nodes_to_add = [
            (beneficiary, "#16a34a", 24, f"Beneficiary: {beneficiary}"),
            (scheme, "#2563eb", 28, f"Scheme: {scheme}"),
            (benefit_type, "#f59e0b", 20, f"Benefit: {benefit_type}"),
            (funding, "#dc2626", 18, f"Funding: {funding}"),
        ]

        for node_id, color, size, title in nodes_to_add:
            if node_id not in added_nodes:
                net.add_node(
                    node_id,
                    label=node_id,
                    color=color,
                    size=size,
                    shape="dot",
                    title=title
                )
                added_nodes.add(node_id)

        # Add Edges
        net.add_edge(beneficiary, scheme)
        net.add_edge(scheme, benefit_type)
        net.add_edge(benefit_type, funding)

    net.save_graph(str(output_file))
    return str(output_file)