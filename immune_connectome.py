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
tme_factors = ['TGF_Beta', 'PD_L1']

# Core cell and target
core = ['UCB_NK_cell', 'Tumor_cell']

all_nodes = activating_receptors + inhibitory_receptors + engineering + tme_factors + core
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
]

for source, target, effect, citation in edges_with_evidence:
    immune_network.add_edge(source, target, effect=effect, citation=citation)

# 4. Draw the network
pos = nx.spring_layout(immune_network, seed=42)  # seed=42 just keeps the layout consistent each time you run it

# Color nodes by category for clarity
node_colors = []
for node in immune_network.nodes():
    if node in activating_receptors:
        node_colors.append('#2ca02c')       # green = activating
    elif node in inhibitory_receptors:
        node_colors.append('#9467bd')       # purple = inhibitory
    elif node in tme_factors:
        node_colors.append('#d62728')       # red = tumor suppression
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
positive_effects = ['restores_cytotoxicity', 'adds_targeted_recognition', 'attacks']
weak_baseline_effects = ['weak_baseline_activation', 'weak_baseline_cytotoxicity']
suppress_effects = ['inhibits', 'suppresses']

pos_edges = [(u, v) for u, v, d in immune_network.edges(data=True) if d['effect'] in positive_effects]
weak_edges = [(u, v) for u, v, d in immune_network.edges(data=True) if d['effect'] in weak_baseline_effects]
neg_edges = [(u, v) for u, v, d in immune_network.edges(data=True) if d['effect'] in suppress_effects]

nx.draw_networkx_edges(immune_network, pos, edgelist=pos_edges, edge_color='green', width=2, arrowsize=20)
nx.draw_networkx_edges(immune_network, pos, edgelist=weak_edges, edge_color='#d4a017', style='dotted', width=2, arrowsize=20)  # amber dotted = weak, not suppressed
nx.draw_networkx_edges(immune_network, pos, edgelist=neg_edges, edge_color='red', style='dashed', width=2, arrowsize=20)      # red dashed = actively suppresses

plt.title("Immunological Connectome:\nCord Blood CAR-NK vs Tumor Microenvironment", fontsize=13, fontweight='bold')
plt.axis('off')
plt.tight_layout()
plt.savefig('immune_connectome.png', dpi=200)
plt.show()

# 5. Print out the citation list so it's easy to copy into your references section
print("\n--- Citations used in this diagram ---")
seen = set()
for _, _, _, citation in edges_with_evidence:
    if citation not in seen:
        print("-", citation)
        seen.add(citation)
