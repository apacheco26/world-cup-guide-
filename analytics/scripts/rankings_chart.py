"""
FIFA World Cup 2026 - Rankings Lollipop Chart
Run: python3 analytics/scripts/rankings_chart.py
Output: frontend/assets/images/rankings.png
"""

import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.ticker import MultipleLocator

# Edit pts (FIFA points) and wr (world rank) here as rankings update.
# host=True highlights the team in blue. Top 3 are automatic (first 3 rows).
data = [
    dict(name="France", flag="🇫🇷", pts=1854, wr=1),
    dict(name="Spain", flag="🇪🇸", pts=1838, wr=2),
    dict(name="Argentina", flag="🇦🇷", pts=1820, wr=3),
    dict(name="England", flag="🏴󠁧󠁢󠁥󠁮󠁧󠁿", pts=1805, wr=4),
    dict(name="Portugal", flag="🇵🇹", pts=1773, wr=5),
    dict(name="Brazil", flag="🇧🇷", pts=1760, wr=6),
    dict(name="Netherlands", flag="🇳🇱", pts=1754, wr=7),
    dict(name="Morocco", flag="🇲🇦", pts=1710, wr=8),
    dict(name="Belgium", flag="🇧🇪", pts=1733, wr=9),
    dict(name="Germany", flag="🇩🇪", pts=1722, wr=10),
    dict(name="Croatia", flag="🇭🇷", pts=1700, wr=11),
    dict(name="Colombia", flag="🇨🇴", pts=1691, wr=13),
    dict(name="Senegal", flag="🇸🇳", pts=1648, wr=14),
    dict(name="Mexico", flag="🇲🇽", pts=1640, wr=15, host=True),
    dict(name="USA", flag="🇺🇸", pts=1607, wr=16, host=True),
    dict(name="Uruguay", flag="🇺🇾", pts=1590, wr=17),
    dict(name="Japan", flag="🇯🇵", pts=1580, wr=18),
    dict(name="Switzerland", flag="🇨🇭", pts=1570, wr=19),
    dict(name="Iran", flag="🇮🇷", pts=1540, wr=21),
    dict(name="Turkiye", flag="🇹🇷", pts=1530, wr=22),
    dict(name="Ecuador", flag="🇪🇨", pts=1520, wr=23),
    dict(name="Austria", flag="🇦🇹", pts=1510, wr=24),
    dict(name="South Korea", flag="🇰🇷", pts=1500, wr=25),
    dict(name="Australia", flag="🇦🇺", pts=1470, wr=27),
    dict(name="Algeria", flag="🇩🇿", pts=1460, wr=28),
    dict(name="Egypt", flag="🇪🇬", pts=1450, wr=29),
    dict(name="Canada", flag="🇨🇦", pts=1440, wr=30, host=True),
    dict(name="Norway", flag="🇳🇴", pts=1430, wr=31),
    dict(name="Panama", flag="🇵🇦", pts=1410, wr=33),
    dict(name="Côte d'Ivoire", flag="🇨🇮", pts=1400, wr=34),
    dict(name="Sweden", flag="🇸🇪", pts=1370, wr=38),
    dict(name="Paraguay", flag="🇵🇾", pts=1350, wr=40),
    dict(name="Scotland", flag="🏴󠁧󠁢󠁳󠁣󠁴󠁿", pts=1330, wr=43),
    dict(name="Tunisia", flag="🇹🇳", pts=1320, wr=44),
    dict(name="Czechia", flag="🇨🇿", pts=1310, wr=45),
    dict(name="Congo DR", flag="🇨🇩", pts=1300, wr=46),
    dict(name="Uzbekistan", flag="🇺🇿", pts=1280, wr=50),
    dict(name="Qatar", flag="🇶🇦", pts=1240, wr=55),
    dict(name="Saudi Arabia", flag="🇸🇦", pts=1230, wr=56),
    dict(name="Iraq", flag="🇮🇶", pts=1220, wr=57),
    dict(name="New Zealand", flag="🇳🇿", pts=1210, wr=58),
    dict(name="South Africa", flag="🇿🇦", pts=1180, wr=65),
    dict(name="Ghana", flag="🇬🇭", pts=1170, wr=66),
    dict(name="Haiti", flag="🇭🇹", pts=1140, wr=70),
    dict(name="Bosnia & Herzegovina", flag="🇧🇦", pts=1100, wr=75),
    dict(name="Cabo Verde", flag="🇨🇻", pts=1090, wr=76),
    dict(name="Curaçao", flag="🇨🇼", pts=1060, wr=80),
    dict(name="Jordan", flag="🇯🇴", pts=1020, wr=87),
]

# Colors
CREAM = "#F5F0E6"
INK = "#1A1916"
INK_SOFT = "#4A4844"
MUTED = "#8A8580"
GOLD = "#C4992E"
HOST_BLUE = "#3E6E9A"
LINE_MID = "#D6D0C4"

df = pd.DataFrame(data)
df["host"] = df["host"].fillna(False) if "host" in df.columns else False
df["top3"] = df.index < 3

def row_color(row):
    if row["top3"]:
        return GOLD
    if row["host"]:
        return HOST_BLUE
    return INK

df["color"] = df.apply(row_color, axis=1)

RK_MIN = 900
RK_MAX = 1950
N = len(df)

fig_h = max(10, N * 0.32)
fig, ax = plt.subplots(figsize=(9, fig_h), facecolor=CREAM)
ax.set_facecolor(CREAM)

for i, (_, row) in enumerate(df.iterrows()):
    y = N - 1 - i
    c = row["color"]
    lw = 1.8 if (row["top3"] or row["host"]) else 1.2
    ax.hlines(y, RK_MIN, row["pts"], color=c, linewidth=lw, zorder=2)
    ms = 8 if (row["top3"] or row["host"]) else 6
    ax.plot(row["pts"], y, "o", color=c, markersize=ms, zorder=3)
    ax.text(
        RK_MAX + 12, y,
        f"#{row['wr']}",
        va="center", ha="left",
        fontsize=7,
        color=MUTED if not (row["top3"] or row["host"]) else INK,
        fontfamily="monospace",
        fontweight="600" if (row["top3"] or row["host"]) else "normal",
    )

ax.set_yticks(list(range(N)))
labels = [df.iloc[N - 1 - i]["name"] for i in range(N)]
ax.set_yticklabels(labels, fontsize=8.5, fontfamily="sans-serif", color=INK)
for i, lbl in enumerate(ax.get_yticklabels()):
    row = df.iloc[N - 1 - i]
    if row["top3"]:
        lbl.set_color(INK)
        lbl.set_fontweight("600")
    elif row["host"]:
        lbl.set_color(HOST_BLUE)
        lbl.set_fontweight("500")
    else:
        lbl.set_color(INK_SOFT)

ax.set_xlim(RK_MIN, RK_MAX + 60)
ax.set_ylim(-0.8, N - 0.2)
ax.xaxis.set_major_locator(MultipleLocator(200))
ax.tick_params(axis="x", colors=MUTED, labelsize=7)
ax.tick_params(axis="y", length=0, pad=6)

ax.grid(axis="x", color=LINE_MID, linewidth=0.5, zorder=0)
for spine in ax.spines.values():
    spine.set_visible(False)
ax.spines["bottom"].set_visible(True)
ax.spines["bottom"].set_color(LINE_MID)
ax.spines["bottom"].set_linewidth(0.8)

fig.text(0.13, 0.985, "FIFA Points (pre-tournament)", ha="left", va="top",
         fontsize=7.5, color=MUTED, fontfamily="monospace", transform=fig.transFigure)

legend_patches = [
    mpatches.Patch(color=GOLD, label="Top 3"),
    mpatches.Patch(color=HOST_BLUE, label="Host nation"),
    mpatches.Patch(color=INK_SOFT, label="Qualified"),
]
ax.legend(handles=legend_patches, loc="lower right", frameon=False, fontsize=7, labelcolor=INK_SOFT)

plt.tight_layout(rect=[0, 0, 1, 0.985])

out_dir = os.path.join(os.path.dirname(__file__), "../../frontend/assets/images")
out_path = os.path.normpath(os.path.join(out_dir, "rankings.png"))
os.makedirs(os.path.dirname(out_path), exist_ok=True)
fig.savefig(out_path, dpi=160, bbox_inches="tight", facecolor=CREAM)
print(f"Saved → {out_path}")
