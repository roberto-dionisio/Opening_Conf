"""Figures for the StaND4LQ opening talk.

    python3 figures/make_figures.py

Two figures, one visual language (figures/talkstyle.py):

    BULK   dark teal   precision / Euclidean lattice QCD   -- the state of the art
    DEFECT orange      sampling, flows, generative models   -- the bridge
    EASY   steel blue  quantum simulation & many-body       -- the new directions
    TARGET crimson     what is still walled off             -- the problem

The same three colors label the talks in fig_programme, so by the time the
audience sees the timetable they have already learned what the colors mean.
"""

import math
from pathlib import Path

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

import talkstyle as ts

ts.use()

HERE = Path(__file__).parent


# =============================================================================
# fig_reach -- what lattice field theory can reach, and what still blocks it
# =============================================================================
def fig_reach():
    fig, ax = plt.subplots(figsize=(11.0, 3.95))
    ax.set_xlim(0, 10)
    ax.set_ylim(0.95, 4.35)
    ax.axis("off")

    y0, h = 2.62, 1.00  # the band of "what we can compute"
    wx0, ww = 4.60, 0.56  # the wall

    # --- the reading of the picture, along the top ---------------------------
    ax.annotate("", xy=(9.85, 4.02), xytext=(0.15, 4.02),
                arrowprops=dict(arrowstyle="-|>,head_width=0.20,head_length=0.40",
                                color=ts.FAINT, linewidth=1.6,
                                shrinkA=0, shrinkB=0), zorder=1)
    ax.text(0.15, 4.14, "STATE OF THE ART", ha="left", va="bottom",
            color=ts.BULK, fontsize=13, zorder=3)
    ax.text(9.85, 4.14, "NEW DIRECTIONS", ha="right", va="bottom",
            color=ts.EASY_TEXT, fontsize=13, zorder=3)

    # --- solid ground: the Euclidean, equilibrium, zero-density regime --------
    ax.add_patch(mpatches.FancyBboxPatch(
        (0.15, y0), 4.30, h, boxstyle="round,pad=0,rounding_size=0.07",
        facecolor=ts.BULK, edgecolor="none", zorder=2))
    ax.text(2.30, y0 + h * 0.62, "Euclidean  ·  equilibrium  ·  $\\mu = 0$",
            ha="center", va="center", color="white", fontsize=14, zorder=3)
    ax.text(2.30, y0 + h * 0.25, "precision at the per-mille level",
            ha="center", va="center", color="#d3dcdd", fontsize=11.5,
            style="italic", zorder=3)

    # --- the wall: taller than the band, so it plainly interrupts it ----------
    ax.add_patch(mpatches.Rectangle(
        (wx0, y0 - 0.18), ww, h + 0.36, facecolor=_tint(ts.TARGET, 0.16),
        edgecolor=ts.TARGET, linewidth=1.4, hatch="////", zorder=2))
    ax.text(wx0 + ww / 2, y0 - 0.34, "the wall", ha="center", va="top",
            color=ts.TARGET, fontsize=12.5, zorder=3)

    # --- the far side: still out of reach ------------------------------------
    ax.add_patch(mpatches.FancyBboxPatch(
        (5.40, y0), 4.45, h, boxstyle="round,pad=0,rounding_size=0.07",
        facecolor="none", edgecolor=ts.MUTED, linewidth=1.3,
        linestyle=(0, (5, 4)), zorder=2))
    for label, dy in [("real-time dynamics", 0.76),
                      ("finite density", 0.50),
                      ("large entanglement", 0.24)]:
        ax.text(7.62, y0 + h * dy, label, ha="center", va="center",
                color=ts.MUTED, fontsize=12.5, zorder=3)

    # --- the three routes, each spanning the stretch of ground it buys -------
    # Their left-to-right order is the argument: flows make the reachable region
    # cheaper, tensor networks and neural states reach the wall itself, quantum
    # hardware works on the far side. Same three colors as the programme legend.
    # arrows keep the bright brand value; their labels take the readable twin
    TEXT_TWIN = {ts.DEFECT: ts.DEFECT_TEXT, ts.EASY: ts.EASY_TEXT}
    y_arr = y0 - 0.72
    routes = [
        (0.20, 4.40, "generative models\n& normalizing flows", ts.DEFECT),
        (4.55, 6.10, "tensor networks\n& neural states", ts.EASY),
        (6.30, 9.80, "quantum hardware", ts.EASY),
    ]
    for xa, xb, label, color in routes:
        ax.annotate("", xy=(xb, y_arr), xytext=(xa, y_arr),
                    arrowprops=dict(arrowstyle="-|>,head_width=0.20,head_length=0.38",
                                    color=color, linewidth=2.2,
                                    shrinkA=0, shrinkB=0), zorder=4)
        ax.text((xa + xb) / 2, y_arr - 0.20, label, ha="center", va="top",
                color=TEXT_TWIN[color], fontsize=12, linespacing=1.35, zorder=4)

    ts.save(fig, "fig_reach")


# =============================================================================
# fig_programme -- the three days, colored by what each talk is about
# =============================================================================
# (start, end, kind, who, what)
#   kind: "inv" invited | "con" contributed | "brk" break | "spc" plenary moment
QCD, ML, QT = "qcd", "ml", "qt"

DAYS = [
    ("Wed 30 Sep", [
        (8.50, 9.00, "brk", None, "Registration", None),
        (9.00, 9.25, "spc", None, "Welcome", None),
        (9.25, 10.08, "inv", "Bonanno", "axion phenomenology", QCD),
        (10.08, 10.58, "con", "Francesconi", "topology at finite $T$", QCD),
        (10.58, 11.08, "brk", None, "Coffee", None),
        (11.08, 11.92, "inv", "Gagliardi", "flavour physics", QCD),
        (11.92, 12.42, "con", "Margari", "smeared $R$-ratio", QCD),
        (12.42, 12.92, "con", "Tavella", "QCD+QED vs RM123", QCD),
        (12.92, 14.75, "brk", None, "Lunch", None),
        (14.75, 15.58, "inv", "Nada", "generative approaches", ML),
        (15.58, 16.08, "con", "Verzichelli", "stochastic norm. flows", ML),
        (16.08, 16.58, "con", "Cellini", "Jarzynski $\\leftrightarrow$ RG", ML),
        (16.58, 17.08, "brk", None, "Coffee", None),
    ]),
    ("Thu 1 Oct", [
        (9.00, 9.83, "inv", "Butti", "sampling by transport", ML),
        (9.83, 10.33, "con", "Liturri", "flows for 2D QED", ML),
        (10.33, 10.83, "brk", None, "Coffee", None),
        (10.83, 11.33, "con", "Gu", "QCD magnetometer", QCD),
        (11.33, 12.17, "inv", "Romiti", "neural states as PINNs", QT),
        (12.17, 13.50, "spc", None, "Discussion Session", None),
        (13.50, 15.00, "brk", None, "Lunch", None),
        (15.00, 15.83, "inv", "Fontana", "", QT),
        (15.83, 16.67, "inv", "Wauters", "discrete non-Abelian LGT", QT),
        (16.67, 17.25, "brk", None, "Coffee", None),
        (17.25, 18.08, "inv", "Chakraborty", "", QT),
    ]),
    ("Fri 2 Oct", [
        (9.00, 9.83, "inv", "Piccitto", "Ising quantum Otto engine", QT),
        (9.83, 10.33, "con", "Arezzo", "optimal control", QT),
        (10.33, 10.83, "con", "De Simone", "entanglement on graphs", QT),
        (10.83, 11.33, "brk", None, "Coffee", None),
        (11.33, 11.58, "spc", None, "Conclusions", None),
    ]),
]

THEME = {QCD: ts.BULK, ML: ts.DEFECT, QT: ts.EASY}
BG = "#f1f1f1"  # the slide background the SVG sits on


def _tint(color, amount):
    """Blend `color` toward the slide background -- a real tint, not alpha, so a
    contributed talk keeps its hue instead of turning grey."""
    import matplotlib.colors as mc
    c, b = mc.to_rgb(color), mc.to_rgb(BG)
    return tuple(c[i] * amount + b[i] * (1 - amount) for i in range(3))


def fig_programme():
    fig, ax = plt.subplots(figsize=(11.6, 6.5))
    fig.subplots_adjust(left=0.055, right=0.995, top=0.925, bottom=0.085)
    t_top, t_bot = 8.42, 18.42
    ax.set_xlim(-0.34, 3.02)
    ax.set_ylim(t_bot, t_top)  # inverted: morning at the top
    ax.axis("off")

    # hour rules, so the eye can read the day without a tick axis
    for hh in range(9, 19):
        ax.plot([-0.04, 3.0], [hh, hh], color=ts.FAINT, linewidth=0.5,
                zorder=0, clip_on=False)
        ax.text(-0.12, hh, f"{hh}:00", ha="right", va="center",
                color=ts.MUTED, fontsize=9.2)

    for d, (day, blocks) in enumerate(DAYS):
        x0, w = d + 0.02, 0.96
        ax.text(x0 + w / 2, t_top - 0.10, day, ha="center", va="bottom",
                color=ts.BULK, fontsize=14.5, clip_on=False)

        for t0, t1, kind, who, what, theme in blocks:
            span, mid = t1 - t0, (t0 + t1) / 2
            tight = span < 0.45  # too short for two lines of text

            if kind == "brk":
                ax.add_patch(mpatches.Rectangle(
                    (x0, t0), w, span, facecolor=ts.FAINT, alpha=0.32,
                    edgecolor="none", zorder=1))
                ax.text(x0 + w / 2, mid, what, ha="center", va="center",
                        color=ts.MUTED, fontsize=9.6, zorder=2)
                continue

            if kind == "spc":
                # The 15-minute bookends (Welcome, Conclusions) are far too thin
                # for a dashed outline and 11pt type -- the label would spill into
                # the block above. Give those a flat tint and small caps instead,
                # and keep the dashed treatment for the long Discussion Session.
                slim = span < 0.4
                ax.add_patch(mpatches.FancyBboxPatch(
                    (x0 + 0.015, t0 + 0.02), w - 0.03, span - 0.04,
                    boxstyle="round,pad=0,rounding_size=0.02",
                    facecolor=_tint(ts.BULK, 0.10) if slim else "white",
                    edgecolor=_tint(ts.BULK, 0.45) if slim else ts.BULK,
                    linewidth=1.0 if slim else 1.3,
                    linestyle="solid" if slim else (0, (4, 3)), zorder=2))
                ax.text(x0 + w / 2, mid, what, ha="center", va="center",
                        color=ts.BULK, fontsize=8.4 if slim else 12, zorder=3)
                continue

            color = THEME[theme]
            invited = kind == "inv"
            ax.add_patch(mpatches.FancyBboxPatch(
                (x0 + 0.015, t0 + 0.03), w - 0.03, span - 0.06,
                boxstyle="round,pad=0,rounding_size=0.02",
                facecolor=color if invited else _tint(color, 0.28),
                edgecolor="none" if invited else _tint(color, 0.60),
                linewidth=0 if invited else 1.0, zorder=2))

            fg = "white" if invited else ts.INK
            if what and not tight:
                # A 30-minute block is only ~16pt tall on the slide, which will not
                # hold a 10.5pt name over an 8.6pt topic: step both down for the
                # short slots so nothing bleeds into the block below.
                short = span < 0.7
                fs_n, fs_s = (10.2, 8.1) if short else (11.5, 9.2)
                dy_n, dy_s = (-0.095, 0.135) if short else (-0.125, 0.175)
                ax.text(x0 + w / 2, mid + dy_n, who, ha="center", va="center",
                        color=fg, fontsize=fs_n, zorder=3)
                ax.text(x0 + w / 2, mid + dy_s, what, ha="center", va="center",
                        color=fg, fontsize=fs_s, alpha=0.93, zorder=3)
            else:
                ax.text(x0 + w / 2, mid, who, ha="center", va="center",
                        color=fg, fontsize=10.4 if tight else 11.5, zorder=3)

    # social dinner: the one thing that happens off the grid
    ax.add_patch(mpatches.FancyBboxPatch(
        (1.035, 18.04), 0.93, 0.26, boxstyle="round,pad=0,rounding_size=0.02",
        facecolor=_tint(ts.TARGET, 0.11), edgecolor=_tint(ts.TARGET, 0.5),
        linewidth=1.0, zorder=2))
    ax.text(1.50, 18.17, "Social dinner  ·  20:00  ·  La Grotta", ha="center",
            va="center", color=ts.TARGET, fontsize=9.6, zorder=3)

    # --- the legend is the argument, so it sits under the whole grid ---------
    key = [("precision lattice QCD", ts.BULK),
           ("sampling & generative ML", ts.DEFECT),
           ("quantum simulation & many-body", ts.EASY)]
    for i, (label, color) in enumerate(key):
        x = 0.085 + i * 0.295
        fig.patches.append(mpatches.Rectangle(
            (x, 0.022), 0.017, 0.030, facecolor=color, edgecolor="none",
            transform=fig.transFigure, zorder=5))
        fig.text(x + 0.026, 0.037, label, ha="left", va="center",
                 color=ts.INK, fontsize=10.2, zorder=5)

    # keep the margins set above: a "tight" bbox would re-crop and undo them.
    with plt.rc_context({"savefig.bbox": "standard"}):
        ts.save(fig, "fig_programme")


# =============================================================================
# fig_topics -- the 18 talks by area, as a donut whose wedges sweep in
# =============================================================================
# Written as inline SVG (not matplotlib) so each wedge can be a reveal fragment.
# The sweep reuses the .draw-line machinery already in theme.scss: the wedge is
# an arc *stroked* thickly rather than a filled pie slice, so animating
# stroke-dashoffset from its own length down to 0 draws it round the circle.
#
# theme.scss reads that length from `--len`. The Lattice deck set it with a
# getTotalLength() script on load, which had to be re-run on slidechanged
# because it reads 0 on a slide that was never visible. An arc's length is just
# R*dtheta, so we write the exact number into the markup and need no JS at all.

# (label, n talks, colour). Five areas, but only three hues: the two QCD areas
# share teal and the two quantum areas share blue, so the donut still reads as
# the three communities from the previous slides while naming real topics.
TOPICS = [
    ("Precision QCD &amp; flavour", 3, "#23373B"),
    ("Topology &amp; finite-<tspan font-style='italic'>T</tspan> QCD", 3, "#55787D"),
    ("Generative models &amp; sampling", 5, "#EB811B"),
    ("Quantum simulation of gauge theories", 4, "#3B7EA1"),
    ("Quantum many-body &amp; control", 3, "#82B3CB"),
]

CX, CY, R_MID, RING = 236.0, 238.0, 150.0, 58.0
GAP_DEG = 1.7          # half-gap trimmed off each end of every wedge
LEGEND_X, ROW_H = 500.0, 74.0


def _arc(a0, a1):
    """Stroked-arc path from angle a0 to a1 (degrees, 0 = 3 o'clock, clockwise
    on screen because SVG y points down), plus its length in user units."""
    p0 = (CX + R_MID * math.cos(math.radians(a0)),
          CY + R_MID * math.sin(math.radians(a0)))
    p1 = (CX + R_MID * math.cos(math.radians(a1)),
          CY + R_MID * math.sin(math.radians(a1)))
    large = 1 if (a1 - a0) > 180 else 0
    d = (f"M {p0[0]:.2f} {p0[1]:.2f} "
         f"A {R_MID:.2f} {R_MID:.2f} 0 {large} 1 {p1[0]:.2f} {p1[1]:.2f}")
    return d, R_MID * math.radians(a1 - a0)


def fig_topics():
    total = sum(n for _, n, _ in TOPICS)
    out = ['```{=html}',
           '<svg class="anim-fig topics-fig" viewBox="0 0 1000 470" '
           'xmlns="http://www.w3.org/2000/svg">']

    # the ring the wedges land on, so the shape reads before anything sweeps
    out.append(f'  <circle cx="{CX}" cy="{CY}" r="{R_MID}" fill="none" '
               f'stroke="#e3e6e6" stroke-width="{RING}"/>')

    angle = -90.0  # start at twelve o'clock, sweep clockwise
    for i, (label, n, color) in enumerate(TOPICS):
        span = 360.0 * n / total
        d, length = _arc(angle + GAP_DEG, angle + span - GAP_DEG)
        row_y = 95.0 + i * ROW_H

        out.append(f'  <g class="fragment draw-line" data-fragment-index="{i}" '
                   f'style="--len:{length:.2f}">')
        out.append(f'    <path d="{d}" fill="none" stroke="{color}" '
                   f'stroke-width="{RING}" stroke-linecap="butt"/>')
        out.append(f'    <rect x="{LEGEND_X}" y="{row_y - 15:.0f}" width="21" '
                   f'height="21" rx="4" fill="{color}"/>')
        out.append(f'    <text x="{LEGEND_X + 36:.0f}" y="{row_y:.0f}" '
                   f'font-size="26" fill="#33474B">{label}</text>')
        out.append(f'    <text x="{LEGEND_X + 36:.0f}" y="{row_y + 27:.0f}" '
                   f'font-size="21" fill="{ts.MUTED}">{n} talks  ·  '
                   f'{100.0 * n / total:.0f}%</text>')
        out.append('  </g>')
        angle += span

    # the total sits in the hole, present from the first moment
    out.append(f'  <text x="{CX}" y="{CY - 4:.0f}" text-anchor="middle" '
               f'font-size="62" fill="#23373B">{total}</text>')
    out.append(f'  <text x="{CX}" y="{CY + 30:.0f}" text-anchor="middle" '
               f'font-size="25" fill="{ts.MUTED}">talks</text>')
    out.append('</svg>')
    out.append('```')

    path = HERE / "_fig_topics.qmd"
    path.write_text("\n".join(out) + "\n")
    print(f"  wrote figures/{path.name}  ({len(TOPICS)} wedges, {total} talks)")


if __name__ == "__main__":
    print("building StaND4LQ opening figures")
    fig_reach()
    fig_programme()
    fig_topics()
    print("done")
