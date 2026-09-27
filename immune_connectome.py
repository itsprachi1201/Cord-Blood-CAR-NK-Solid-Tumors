# Immunological Connectome: Cord Blood CAR-NK vs Tumor Microenvironment
# All relationships below are qualitative (not numerically weighted) and are
# based on real, cited sources. No values in this script were invented.

import networkx as nx
import matplotlib.pyplot as plt

# 1. Create a directed graph
immune_network = nx.DiGraph()

# 2. Add nodes — receptors and factors are grouped by role
# Activating receptors (naturally LOW in cord blood NK cells)
activating_receptors = ['CD16', 'DNAM_1', 'NKG2C', 'Granzyme_B']

# Inhibitory receptor (naturally HIGH in cord blood NK cells)
inhibitory_receptors = ['NKG2A']

# Engineering additions
engineering = ['CAR_construct', 'IL_15']

# Tumor microenvironment suppressive factors
tme_factors = ['TGF_Beta', 'PD_L1', 'ECM_Barrier']

# Physical barrier components (distinct from biochemical suppression)
physical_barrier = ['LOX']

# Engineering solution for the physical barrier
mmp_solution = ['MMP_Engineering']

# Core cell and target
core = ['UCB_NK_cell', 'Tumor_cell']

all_nodes = activating_receptors + inhibitory_receptors + engineering + mmp_solution + tme_factors + physical_barrier + core
for node in all_nodes:
    immune_network.add_node(node)

# 3. Add edges — each has a plain-word "effect" label, NOT a numeric weight,
# and a citation in the comment showing where the claim comes from.

edges_with_evidence = [
    # Source, Target, effect label, citation
    ('CD16', 'UCB_NK_cell', 'weak_baseline_activation',
     'Sarvaria et al. 2017, Front Immunol — UCB-NK cells show decreased CD16 expression vs peripheral blood NK cells'),

    ('DNAM_1', 'UCB_NK_cell', 'weak_baseline_activation',
     'Sarvaria et al. 2017, Front Immunol — lower DNAM-1 expression in UCB-NK cells, indicating immaturity'),

    ('NKG2C', 'UCB_NK_cell', 'weak_baseline_activation',
     'Sarvaria et al. 2017, Front Immunol — lower NKG2C expression in UCB-NK cells vs peripheral blood'),

    ('Granzyme_B', 'UCB_NK_cell', 'weak_baseline_cytotoxicity',
     'Sarvaria et al. 2017, Front Immunol — decreased perforin and granzyme B expression in UCB-NK cells'),

    ('NKG2A', 'UCB_NK_cell', 'inhibits',
     'Sarvaria et al. 2017, Front Immunol — UCB-NK cells show higher expression of inhibitory receptor NKG2A'),

    ('IL_15', 'UCB_NK_cell', 'restores_cytotoxicity',
     'Sarvaria et al. 2017, Front Immunol — IL-15 (alone or with IL-2) restored/enhanced UCB-NK cytotoxicity toward peripheral-blood NK cell levels'),

    ('CAR_construct', 'UCB_NK_cell', 'adds_targeted_recognition',
     'Kim et al. 2025, Cancer Immunol Immunother — anti-ErbB3 CAR-NK cells showed increased cytotoxicity against ErbB3-positive breast cancer cells'),

    ('UCB_NK_cell', 'Tumor_cell', 'attacks',
     'General CAR-NK mechanism — engineered cell targets and attempts to kill tumor cell'),

    ('TGF_Beta', 'UCB_NK_cell', 'suppresses',
     'Established TME immunosuppression mechanism — TGF-beta is a well-documented suppressor of NK cell cytotoxic function in the tumor microenvironment'),

    ('PD_L1', 'UCB_NK_cell', 'suppresses',
     'Established TME immunosuppression mechanism — PD-L1/checkpoint signaling suppresses immune cell activity in solid tumors'),

    ('LOX', 'ECM_Barrier', 'builds_physical_barrier',
     'Frontiers in Immunology, 2026, "Research progress on tumor extracellular matrix stiffness and immunosuppression" — LOX-driven collagen cross-linking stiffens the tumor ECM, creating a dense physical barrier'),

    ('ECM_Barrier', 'UCB_NK_cell', 'blocks_infiltration',
     'Frontiers in Immunology, 2026 (same source) — a dense ECM is the primary physical obstacle to NK cell infiltration; NK cells present near fibrotic tumors show severely restricted invasion depth'),

    ('MMP_Engineering', 'ECM_Barrier', 'degrades_barrier',
     'Frontiers in Immunology, 2026 (same source) — direct enzymatic cleavage of ECM components (e.g. via MMPs) can rapidly disrupt the physical barrier and enhance immune cell infiltration'),
]

for source, target, effect, citation in edges_with_evidence:
    immune_network.add_edge(source, target, effect=effect, citation=citation)

# 4. Draw the network
# Manual circular layout: place every node that connects directly to UCB_NK_cell
# evenly around it, then push LOX and MMP_Engineering (which attach one hop further,
# via ECM_Barrier) out beyond the main circle at an offset angle. This guarantees
# no overlapping nodes or edges, unlike a force-directed layout which can vary run to run.
import math

hub = 'UCB_NK_cell'
spoke_order = ['NKG2C', 'CD16', 'DNAM_1', 'Granzyme_B', 'CAR_construct', 'IL_15',
               'NKG2A', 'TGF_Beta', 'PD_L1', 'ECM_Barrier', 'Tumor_cell']
radius = 1.3
pos = {hub: (0.0, 0.0)}
n = len(spoke_order)
for i, node in enumerate(spoke_order):
    angle = 2 * math.pi * i / n
    pos[node] = (radius * math.cos(angle), radius * math.sin(angle))

# ECM_Barrier's satellites: place them further out, offset to either side of its angle
ecm_index = spoke_order.index('ECM_Barrier')
ecm_angle = 2 * math.pi * ecm_index / n
outer_radius = 2.3
pos['LOX'] = (outer_radius * math.cos(ecm_angle - 0.3), outer_radius * math.sin(ecm_angle - 0.3))
pos['MMP_Engineering'] = (outer_radius * math.cos(ecm_angle + 0.3), outer_radius * math.sin(ecm_angle + 0.3))

# Color nodes by category for clarity
node_colors = []
for node in immune_network.nodes():
    if node in activating_receptors:
        node_colors.append('#2ca02c')       # green = activating
    elif node in inhibitory_receptors:
        node_colors.append('#9467bd')       # purple = inhibitory
    elif node in tme_factors:
        node_colors.append('#d62728')       # red = tumor suppression
    elif node in physical_barrier:
        node_colors.append('#8b4513')       # brown = physical/structural barrier
    elif node in mmp_solution:
        node_colors.append('#1f77b4')       # blue = engineered addition (same as other solutions)
    elif node in engineering:
        node_colors.append('#1f77b4')       # blue = engineered addition
    else:
        node_colors.append('#7f7f7f')       # grey = core cell/tumor

nx.draw_networkx_nodes(immune_network, pos, node_color=node_colors, node_size=2000)
nx.draw_networkx_labels(immune_network, pos, font_size=8, font_weight='bold')

# Split edges into three honest categories, not just positive/negative:
# - positive: helps the NK cell act against the tumor
# - weak_baseline: the receptor is present but naturally under-expressed (not "suppressed", just weak)
# - suppresses: something is actively working against the NK cell's function
positive_effects = ['restores_cytotoxicity', 'adds_targeted_recognition', 'attacks', 'degrades_barrier']
weak_baseline_effects = ['weak_baseline_activation', 'weak_baseline_cytotoxicity']
suppress_effects = ['inhibits', 'suppresses', 'blocks_infiltration']
structural_effects = ['builds_physical_barrier']

pos_edges = [(u, v) for u, v, d in immune_network.edges(data=True) if d['effect'] in positive_effects]
weak_edges = [(u, v) for u, v, d in immune_network.edges(data=True) if d['effect'] in weak_baseline_effects]
neg_edges = [(u, v) for u, v, d in immune_network.edges(data=True) if d['effect'] in suppress_effects]
structural_edges = [(u, v) for u, v, d in immune_network.edges(data=True) if d['effect'] in structural_effects]

nx.draw_networkx_edges(immune_network, pos, edgelist=pos_edges, edge_color='green', width=2, arrowsize=20)
nx.draw_networkx_edges(immune_network, pos, edgelist=weak_edges, edge_color='#d4a017', style='dotted', width=2, arrowsize=20)  # amber dotted = weak, not suppressed
nx.draw_networkx_edges(immune_network, pos, edgelist=neg_edges, edge_color='red', style='dashed', width=2, arrowsize=20)      # red dashed = actively suppresses
nx.draw_networkx_edges(immune_network, pos, edgelist=structural_edges, edge_color='#8b4513', style='solid', width=2, arrowsize=20)  # brown solid = builds structural barrier

plt.title("Immunological Connectome:\nCord Blood CAR-NK vs Tumor Microenvironment", fontsize=13, fontweight='bold')
plt.axis('off')
plt.margins(0.15)  # adds breathing room around the outermost nodes so labels never get clipped
plt.tight_layout()
plt.savefig('immune_connectome.png', dpi=200, bbox_inches='tight')  # bbox_inches='tight' trims to content while keeping full labels
plt.show()

# 5. Print out the citation list so it's easy to copy into your references section
print("\n--- Citations used in this diagram ---")
seen = set()
for _, _, _, citation in edges_with_evidence:
    if citation not in seen:
        print("-", citation)
        seen.add(citation)
