"""Helpers for inspecting imported Pandapower networks."""


NETWORK_TABLES = (
    ("bus", "Buses"),
    ("line", "Lines"),
    ("trafo", "Transformers"),
    ("trafo3w", "Three-winding transformers"),
    ("load", "Loads"),
    ("sgen", "Static generators"),
    ("gen", "Generators"),
    ("ext_grid", "External grids"),
    ("switch", "Switches"),
    ("shunt", "Shunts"),
    ("impedance", "Impedances"),
    ("storage", "Storage units"),
)


def summarize_network(network):
    """Return a compact element-count summary for a Pandapower network."""
    lines = []
    for table_name, label in NETWORK_TABLES:
        table = network.get(table_name)
        count = len(table) if table is not None else 0
        if count:
            lines.append("{}: {}".format(label, count))
    if not lines:
        return "The imported network contains no recognized elements."
    return "\n".join(lines)
