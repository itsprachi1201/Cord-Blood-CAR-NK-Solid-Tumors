"""
Immunological Connectome: Cord Blood CAR-NK vs Tumor Microenvironment
----------------------------------------------------------------------
Draws the three-layer diagram described in README.md and prints an
edge-to-source table so every arrow can be traced to a cited paper.

Run:  python immune_connectome.py        (needs matplotlib only)
Out:  immune_connectome.png

Design rules in this version
  * Receptors and cytotoxic molecules sit INSIDE the NK cell (they are on the cell).
  * Edges are drawn under nodes and routed so none passes behind another node.
  * Every arrow has its own arrival point (no piled-up arrowheads).
  * Each intervention points at the layer it addresses; Layer 2 has none because
    the cited sources do not cover one.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, FancyArrowPatch
from matplotlib.lines import Line2D

# ---------- colours ----------
GREEN, AMBER, RED, BROWN = "#2ca02c", "#d4a017", "#d62728", "#8b5a2b"
PURPLE, BLUE, DARK, GREY = "#a569d6", "#1f77b4", "#3e0000", "#808080"
MAGENTA = "#c2185b"

PPU = 0.84 * 72  # points per data unit (figure is sized so 1 unit ~ 0.85 inch)

fig = plt.figure(figsize=(16, 12.0))
ax = fig.add_axes([0.01, 0.13, 0.98, 0.86])
ax.set_xlim(0, 18.4)
ax.set_ylim(-1.45, 10.9)
ax.set_aspect("equal", adjustable="box")
ax.axis("off")

nodes = {}


def band(x, y, w, h, color, alpha=0.10, ls="-", ec=None, z=0):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.3",
                                fc=color, ec=ec or color, alpha=alpha if ec is None else 1,
                                lw=1.2, ls=ls, zorder=z))


def node(key, x, y, color, label, r=0.66, ring=None, ring_w=4.2, fs=8.5, tc="black"):
    nodes[key] = (x, y, r)
    ax.add_patch(Circle((x, y), r, fc=color, ec=ring or "white", lw=ring_w if ring else 1.5, zorder=4))
    ax.text(x, y, label, ha="center", va="center", fontsize=fs, fontweight="bold", color=tc, zorder=5)


def arrow(a, b, color, style="-", lw=2.4, rad=0.0, to_point=None, shrink_b=None):
    """Arrow from node a to node b (or to an explicit point), under the nodes."""
    xa, ya, ra = nodes[a]
    if to_point is not None:
        xb, yb = to_point
        sb = shrink_b if shrink_b is not None else 2
    else:
        xb, yb, rb = nodes[b]
        sb = rb * PPU + 3
    ax.add_patch(FancyArrowPatch((xa, ya), (xb, yb), arrowstyle="-|>", mutation_scale=20,
                                 lw=lw, color=color, linestyle=style,
                                 connectionstyle=f"arc3,rad={rad}",
                                 shrinkA=ra * PPU + 3, shrinkB=sb, zorder=2))


def label(x, y, text, fs=8, ha="center", color="#222", italic=False):
    ax.text(x, y, text, ha=ha, va="center", fontsize=fs, color=color, zorder=6,
            style="italic" if italic else "normal",
            bbox=dict(fc="white", ec="none", alpha=0.85, pad=1.5))


# ---------- title ----------
ax.text(9.2, 10.6, "Cord Blood CAR-NK vs Tumor Microenvironment",
        ha="center", va="center", fontsize=17, fontweight="bold")

# ---------- layer bands ----------
band(0.15, 0.9, 5.1, 8.5, BROWN)          # Layer 3
band(5.75, 0.9, 3.3, 8.5, RED)            # Layer 2
band(10.8, 2.0, 4.6, 6.6, GREY, alpha=0.14)  # NK cell (Layer 1)
ax.text(2.7, 9.75, "Layer 3: Physical barrier", ha="center", fontsize=12, fontweight="bold", color="#333")
ax.text(7.4, 9.75, "Layer 2: Biochemical suppression", ha="center", fontsize=12, fontweight="bold", color="#333")
ax.text(13.1, 9.15, "Cord blood NK cell (UCB-NK)", ha="center", fontsize=12, fontweight="bold", color="#333")
ax.text(13.1, 8.7, "Layer 1: baseline immaturity", ha="center", fontsize=10, color="#333")
ax.text(13.1, 8.32, "amber ring = under-expressed  |  red ring = over-expressed", ha="center", fontsize=7.3, color="#555", style="italic")

# ---------- Layer 3 nodes (stromal / barrier) ----------
node("CAF", 3.6, 8.2, BROWN, "CAF", tc="white")
node("LOXL2", 3.6, 5.9, BROWN, "LOXL2\nPLOD2", tc="white")
node("ECM", 3.6, 3.3, "#6d4c41", "Stiff ECM\nbarrier", r=0.8, tc="white")

# ---------- Layer 3 interventions ----------
node("LOXi", 1.0, 5.9, BLUE, "LOX/LOXL2\ninhibitor*", r=0.78, fs=8)
node("ECMenz", 1.0, 3.3, BLUE, "ECM-degrading\nenzyme†", r=0.82, fs=8)

# ---------- Layer 2 nodes ----------
node("TGFb", 7.4, 7.3, RED, "TGF-β\n(TME)")
node("PDL1", 7.4, 4.5, RED, "PD-L1\n(tumor cells)", r=0.75, fs=8)
band(6.0, 1.0, 2.8, 1.15, "white", ec="#999", ls="--", z=1)
ax.text(7.4, 1.58, "No intervention covered\nby the cited sources", ha="center", va="center",
        fontsize=8.5, color="#555", style="italic", zorder=6)

# ---------- Layer 1 nodes (inside the NK cell) ----------
node("CD16", 12.0, 6.7, GREEN, "CD16", ring=AMBER)
node("DNAM1", 14.2, 6.7, GREEN, "DNAM-1", ring=AMBER)
node("NKG2C", 12.0, 5.1, GREEN, "NKG2C", ring=AMBER)
node("GZMB", 14.2, 5.1, GREEN, "Granzyme B", ring=AMBER, fs=7.5)
node("PRF", 12.0, 3.5, GREEN, "Perforin", ring=AMBER, fs=8)
node("NKG2A", 14.2, 3.5, PURPLE, "NKG2A", ring=RED)

# ---------- tumour + CAR + IL-15 ----------
node("TUM", 17.45, 5.4, DARK, "Tumor\ncell", r=0.85, tc="white", fs=9)
node("CAR", 16.3, 8.4, BLUE, "CAR\nconstruct", r=0.72)
node("IL15", 13.1, 0.85, BLUE, "IL-15", r=0.68)

# ---------- edges: Layer 3 loop ----------
arrow("CAF", "LOXL2", BROWN)
label(3.0, 7.05, "secretes\ncross-linkers", ha="right")
arrow("LOXL2", "ECM", BROWN)
label(3.0, 4.6, "stiffens", ha="right")
arrow("ECM", "CAF", BROWN, style="--", rad=0.4)        # feedback loop bulging to the right
label(5.45, 6.1, "stiffness\nactivates CAFs", fs=8.3, ha="center")

# ---------- edges: Layer 3 -> NK, Layer 2 -> NK ----------
arrow("ECM", None, RED, style="--", to_point=(10.8, 3.2), shrink_b=0)
label(8.3, 3.2, "impairs NK cells (CD44 anchoring,\nlost cytotoxicity, glycocalyx)", fs=8.3)
arrow("TGFb", None, RED, style="--", to_point=(10.8, 7.3), shrink_b=0)
arrow("PDL1", None, RED, style="--", to_point=(10.8, 4.5), shrink_b=0)

# stiffness -> PD-L1 (upregulation in tumour cells)
arrow("ECM", "PDL1", MAGENTA, style="-.", rad=0.15)
label(5.55, 4.45, "upregulates\n(tumor cells)", fs=8.3, color=MAGENTA)

# ---------- edges: NK -> tumour, interventions ----------
ax.add_patch(FancyArrowPatch((15.4, 5.4), (16.58, 5.4), arrowstyle="-|>", mutation_scale=20,
                             lw=2.6, color=GREEN, shrinkA=0, shrinkB=0, zorder=2))
label(16.0, 4.85, "kills", fs=8)
arrow("CAR", None, BLUE, to_point=(16.3, 5.72), shrink_b=0)
label(17.35, 7.1, "gives tumor\nspecificity", fs=7.5)

arrow("IL15", None, BLUE, to_point=(13.1, 2.0), shrink_b=0)
label(15.8, 1.1, "restores cytotoxicity (priming)\nand supports persistence (armoring)", fs=7.5)

arrow("LOXi", "LOXL2", BLUE)
label(2.3, 6.45, "inhibits", fs=7.5)
arrow("ECMenz", "ECM", BLUE)
label(2.3, 3.85, "degrades", fs=7.5)

# ---------- footnotes ----------
foot = [
    "* Benefit shown for T cells in the reviewed work; any NK benefit is an extrapolation.   "
    "† Example: hyaluronidase improved NK-92 infiltration in a pancreatic cancer model.",
    "Amber ring = under-expressed in cord blood NK vs adult NK; red ring = over-expressed.   "
    "Simplified: NKG2A acts via HLA-E and PD-L1 via PD-1 (not drawn).",
    "An ECM → TGF-β link is not drawn: it is supported only in other tumor types. "
    "ECM/NK evidence comes mostly from other tumors and NK cells generally.",
]
for i, t in enumerate(foot):
    ax.text(0.2, -0.35 - 0.42 * i, t, fontsize=8, color="#444", ha="left", va="center")

# ---------- legend ----------
handles = [
    Line2D([0], [0], color=GREEN, lw=2.6, label="Helps the NK cell act against the tumor"),
    Line2D([0], [0], color=RED, lw=2.6, ls="--", label="Actively suppresses / blocks"),
    Line2D([0], [0], color=BROWN, lw=2.6, label="Builds / stiffens the physical barrier"),
    Line2D([0], [0], color=BROWN, lw=2.6, ls="--", label="Feedback: stiffness activates CAFs"),
    Line2D([0], [0], color=MAGENTA, lw=2.6, ls="-.", label="Upregulates (PD-L1 in tumor cells)"),
    Line2D([0], [0], color=BLUE, lw=2.6, label="Intervention acts on"),
    Line2D([0], [0], marker="o", color="w", mfc=GREEN, mec=AMBER, mew=3, ms=12, label="Activating receptor / cytotoxic molecule"),
    Line2D([0], [0], marker="o", color="w", mfc=PURPLE, mec=RED, mew=3, ms=12, label="Inhibitory receptor"),
    Line2D([0], [0], marker="o", color="w", mfc=RED, ms=12, label="TME suppressive factor"),
    Line2D([0], [0], marker="o", color="w", mfc=BROWN, ms=12, label="Stromal / barrier component"),
    Line2D([0], [0], marker="o", color="w", mfc=BLUE, ms=12, label="Engineered / pharmacological intervention"),
    Line2D([0], [0], marker="o", color="w", mfc=DARK, ms=12, label="Tumor cell (target)"),
]
fig.legend(handles=handles, loc="lower center", ncol=3, fontsize=9, frameon=True,
           bbox_to_anchor=(0.5, 0.005))

fig.savefig("immune_connectome.png", dpi=150, facecolor="white")
print("Saved immune_connectome.png\n")

# ---------- edge-to-source table (printed so every arrow is traceable) ----------
TABLE = [
    ("Layer 1 nodes (CD16, DNAM-1, NKG2C, granzyme B, perforin low; NKG2A high)",
     "Sarvaria et al., 2017", "cord blood NK immaturity phenotype"),
    ("IL-15 -> NK cell", "Sarvaria et al., 2017 (priming); Lee et al., 2025 (armoring)",
     "confirmed: Lee describes IL-15-secreting CAR-NK cells built for persistence"),
    ("CAR construct -> tumor targeting", "Lee et al., 2025",
     "confirmed: anti-ErbB3 CAR-NK cells show increased cytotoxicity specifically against ErbB3+ breast cancer cells"),
    ("TGF-b -> NK cell", "Viel et al., 2016, Sci Signal",
     "confirmed NK-specific: TGF-b represses mTOR activation and reduces NK cell activity/function directly"),
    ("PD-L1 -> NK cell", "Hsu et al., 2018, J Clin Invest",
     "confirmed NK-specific: PD-1 on NK cells engaged by PD-L1+ tumor cells suppresses NK-mediated antitumor immunity"),
    ("Stiff ECM -> NK cell", "Wu et al., 2026, Sec. 2.2.4",
     "CD44 anchoring; ECM shifts NK from killing to cytokines; glycocalyx (other tumor models)"),
    ("CAF -> LOXL2/PLOD2 -> stiff ECM", "Wu et al., 2026, Sec. 3.1", "CAFs stiffen matrix"),
    ("Stiff ECM -> CAF (feedback)", "Wu et al., 2026, Sec. 3.1", "stiffness activates CAFs"),
    ("Stiff ECM -> PD-L1 (tumor cells)", "Wu et al., 2026, Sec. 3.2", "stiffness upregulates PD-L1"),
    ("ECM-degrading enzyme -> ECM", "Wu et al., 2026, Sec. 4.1.1", "hyaluronidase, NK-92, pancreatic model"),
    ("LOX/LOXL2 inhibitor -> LOXL2", "Wu et al., 2026, Sec. 4.1.2", "T cell evidence; NK extrapolated"),
]
print("EDGE -> SOURCE TABLE")
print("-" * 100)
for edge, src, note in TABLE:
    print(f"{edge}\n    source: {src}\n    note:   {note}")
