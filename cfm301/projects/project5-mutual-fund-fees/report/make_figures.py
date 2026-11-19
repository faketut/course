"""Figures for Project 5 report. Run from the project root."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams.update({"font.size": 9, "axes.spines.top": False,
                     "axes.spines.right": False})

alphas = pd.read_csv("outputs/table_alphas.csv")
car = alphas[alphas["model"] == "Carhart"].pivot(index="ticker", columns="basis",
                                                values="alpha_ann_pct")
info = pd.read_csv("data/fund_info.csv", index_col="ticker")
order = ["FCNTX", "FMAGX", "AGTHX", "PRGFX", "TRBCX"]

# Fig 1: net vs gross Carhart alpha, with the expense ratio as a marker.
fig, ax = plt.subplots(figsize=(6.6, 2.6))
x = range(len(order))
w = 0.36
ax.bar([i - w / 2 for i in x], [car.loc[t, "net"] for t in order], w,
       label="Net alpha", color="#1f4e79")
ax.bar([i + w / 2 for i in x], [car.loc[t, "gross"] for t in order], w,
       label="Gross alpha", color="#8ea9c1")
for i, t in enumerate(order):
    ax.plot([i - w, i + w], [info.loc[t, "fee_pct"]] * 2, color="#c0392b",
            lw=1.2, ls="--")
ax.plot([], [], color="#c0392b", ls="--", label="Expense ratio")
ax.axhline(0, color="black", lw=0.8)
ax.set_xticks(list(x))
ax.set_xticklabels(order)
ax.set_ylabel("Carhart alpha (%/yr)")
ax.set_title("Net vs gross Carhart alpha, 1994-2024 (dashed = expense ratio)")
ax.legend(frameon=False, ncols=3, loc="upper right")
ax.set_ylim(-1.2, 3.6)
fig.tight_layout()
fig.savefig("outputs/fig_alpha_net_gross.png", dpi=200)
plt.close(fig)

# Fig 2: rolling 36-month Carhart net alphas.
fig, ax = plt.subplots(figsize=(6.6, 2.8))
for t in order:
    r = pd.read_csv(f"outputs/rolling_alpha_{t}.csv", index_col=0, parse_dates=True)
    ax.plot(r.index, r["alpha_ann_pct"], lw=1.1, label=t)
ax.axhline(0, color="black", lw=0.8)
ax.set_ylabel("36-month Carhart alpha (%/yr)")
ax.set_title("Rolling 36-month net Carhart alpha (each point = past 36 months)")
ax.legend(frameon=False, ncols=5, loc="upper left")
ax.set_ylim(-10, 18)
fig.tight_layout()
fig.savefig("outputs/fig_rolling_alpha.png", dpi=200)
plt.close(fig)
print("figures written")
