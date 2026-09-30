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
     'Lee et al. 2025, Cancer Immunol Immunother (Kim S, Dong-A University, senior author) — anti-ErbB3 CAR-NK cells showed increased cytotoxicity against ErbB3-positive breast cancer cells'),

    ('UCB_NK_cell', 'Tumor_cell', 'attacks',
     'General CAR-NK mechanism — engineered cell targets and attempts to kill tumor cell'),

    ('TGF_Beta', 'UCB_NK_cell', 'suppresses',
     'Established TME immunosuppression mechanism — TGF-beta is a well-documented suppressor of NK cell cytotoxic function in the tumor microenvironment'),

    ('PD_L1', 'UCB_NK_cell', 'suppresses',
     'Established TME immunosuppression mechanism — PD-L1/checkpoint signaling suppresses immune cell activity in solid tumors'),

    ('LOX', 'ECM_Barrier', 'builds_physical_barrier',
     'Wu et al. 2026, Frontiers in Immunology, "Research progress on tumor extracellular matrix stiffness and immunosuppression" — LOX-driven collagen cross-linking stiffens the tumor ECM, creating a dense physical barrier'),

    ('ECM_Barrier', 'UCB_NK_cell', 'blocks_infiltration',
     'Wu et al. 2026 (same source) — a dense ECM is the primary physical obstacle to NK cell infiltration; NK cells present near fibrotic tumors show severely restricted invasion depth'),

    ('MMP_Engineering', 'ECM_Barrier', 'degrades_barrier',
     'Wu et al. 2026 (same source) — direct enzymatic cleavage of ECM components (e.g. via MMPs) can rapidly disrupt the physical barrier and enhance immune cell infiltration'),
]

for source, target, effect, citation in edges_with_evidence:
    immune_network.add_edge(source, target, effect=effect, citation=citation)

# 4. Draw the network
# Column layout: the three problem "layers" from the README each get their own
# labeled column on the left, feeding into the NK cell in the center. Interventions
# (CAR, IL-15, MMP engineering) sit in their own column on the right, since they are
# solutions, not part of the problem. Tumor_cell sits at the far right as the final target.

pos = {}

# Layer 1: Baseline immaturity (leftmost column)
layer1_nodes = ['NKG2C', 'CD16', 'DNAM_1', 'Granzyme_B', 'NKG2A']
layer1_x = -5.0
for i, node in enumerate(layer1_nodes):
    pos[node] = (layer1_x, 2.4 - i * 1.2)

# Layer 2: Biochemical TME suppression (second column)
layer2_nodes = ['TGF_Beta', 'PD_L1']
layer2_x = -3.2
for i, node in enumerate(layer2_nodes):
    pos[node] = (layer2_x, 0.7 - i * 1.4)

# Layer 3: Physical barrier (third column) — LOX feeds ECM_Barrier, which feeds the NK cell
layer3_x = -1.4
pos['LOX'] = (layer3_x - 0.9, 1.2)
pos['ECM_Barrier'] = (layer3_x, 0.0)

# Hub: the NK cell itself, center
pos['UCB_NK_cell'] = (0.6, 0.0)

# Target: the tumor cell, far right (what the NK cell is trying to reach and kill)
pos['Tumor_cell'] = (4.5, 0.0)

# Interventions column: solutions, kept visually separate on the right
interventions_x = 2.6
pos['CAR_construct'] = (interventions_x, 2.2)
pos['IL_15'] = (interventions_x, 1.0)
pos['MMP_Engineering'] = (interventions_x, -1.8)

# Column header labels, drawn directly onto the figure
column_headers = [
    (layer1_x, 3.3, "Layer 1:\nBaseline Immaturity"),
    (layer2_x, 2.0, "Layer 2:\nBiochemical Suppression"),
    (layer3_x - 0.4, 2.2, "Layer 3:\nPhysical Barrier"),
    (interventions_x, 3.3, "Interventions"),
]

# Color nodes by category for clarity
plt.figure(figsize=(13, 9))
node_colors = []
node_sizes = []
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
    elif node == 'Tumor_cell':
        node_colors.append('#3d0000')       # dark maroon = tumor cell, deliberately distinct from the grey NK cell
    else:
        node_colors.append('#7f7f7f')       # grey = the NK cell itself (only node this color now)
    # Bigger nodes for longer labels (Granzyme_B, CAR_construct, MMP_Engineering) so text doesn't overflow
    if node in ['Granzyme_B', 'CAR_construct', 'MMP_Engineering', 'ECM_Barrier', 'UCB_NK_cell']:
        node_sizes.append(4200)
    else:
        node_sizes.append(3000)

nx.draw_networkx_nodes(immune_network, pos, node_color=node_colors, node_size=node_sizes)
nx.draw_networkx_labels(immune_network, pos, font_size=7.5, font_weight='bold')

# Draw column headers
for x, y, text in column_headers:
    plt.text(x, y, text, fontsize=9.5, fontweight='bold', ha='center', va='center', color='#333333')

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

nx.draw_networkx_edges(immune_network, pos, edgelist=pos_edges, edge_color='green', width=2, arrowsize=18, arrows=True, arrowstyle='-|>', node_size=node_sizes)
nx.draw_networkx_edges(immune_network, pos, edgelist=weak_edges, edge_color='#d4a017', style='dotted', width=2, arrowsize=18, arrows=True, arrowstyle='-|>', node_size=node_sizes)  # amber dotted = weak, not suppressed
nx.draw_networkx_edges(immune_network, pos, edgelist=neg_edges, edge_color='red', style='dashed', width=2, arrowsize=18, arrows=True, arrowstyle='-|>', node_size=node_sizes)      # red dashed = actively suppresses
nx.draw_networkx_edges(immune_network, pos, edgelist=structural_edges, edge_color='#8b4513', style='solid', width=2, arrowsize=18, arrows=True, arrowstyle='-|>', node_size=node_sizes)  # brown solid = builds structural barrier

# Legend explaining every color/style so the diagram is readable without needing the README
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], color='green', lw=2, label='Helps NK cell act against tumor'),
    Line2D([0], [0], color='#d4a017', lw=2, linestyle='dotted', label='Naturally weak at baseline (not blocked)'),
    Line2D([0], [0], color='red', lw=2, linestyle='dashed', label='Actively suppresses / blocks'),
    Line2D([0], [0], color='#8b4513', lw=2, label='Builds physical barrier'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor='#2ca02c', markersize=10, label='Activating receptor'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor='#9467bd', markersize=10, label='Inhibitory receptor'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor='#d62728', markersize=10, label='TME suppressive factor'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor='#8b4513', markersize=10, label='Physical barrier component'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor='#1f77b4', markersize=10, label='Engineered intervention'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor='#3d0000', markersize=10, label='Tumor cell (target)'),
]
plt.legend(handles=legend_elements, loc='lower center', bbox_to_anchor=(0.5, -0.22), ncol=3, fontsize=7.5, frameon=True)

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
