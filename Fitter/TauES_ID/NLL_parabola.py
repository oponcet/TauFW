#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
quick_nll_plot.py   –   minimal ΔNLL curve from a Combine MultiDimFit file.

Usage
  python quick_nll_plot.py <rootfile> [poi_branch]

If poi_branch is omitted the script uses the first branch that starts with 'tes_'.
"""

import sys, pathlib, numpy as np, ROOT, matplotlib.pyplot as plt

if len(sys.argv) not in (2, 3):
    sys.exit("Usage: python quick_nll_plot.py <file.root> [poi]")

rootfile = pathlib.Path(sys.argv[1]).resolve()
if not rootfile.exists():
    sys.exit(f"File not found: {rootfile}")

f = ROOT.TFile.Open(str(rootfile))
tree = f.Get("limit")
if not tree:
    sys.exit("TTree 'limit' not found")

# pick POI branch
if len(sys.argv) == 3:
    poi_name = sys.argv[2]
else:
    poi_name = next(b.GetName() for b in tree.GetListOfBranches() if b.GetName().startswith("tes_"))

print("Using POI branch:", poi_name)
poi, nll = [], []
for e in tree:
    # if e.quantileExpected < 0:      # only nominal scan points
        poi.append(getattr(e, poi_name))
        nll.append(2 * e.deltaNLL)  # Combine stores ΔNLL; convert to –2ΔNLL

print(f"poi values: {poi}")
print(f"nll values: {nll}")

poi, nll = np.array(poi), np.array(nll)
order = np.argsort(poi)
poi, nll = poi[order], nll[order] - nll.min()   # shift minimum to 0

# plain-text table (optional)
np.savetxt(rootfile.with_suffix(".scan.txt"),
           np.column_stack([poi, nll]),
           header=f"{poi_name}   minus2DeltaNLL")

# simple Matplotlib plot
plt.plot(poi, nll, "o-")
plt.xlabel(poi_name)
plt.ylabel(r"$-2\,\Delta\mathrm{NLL}$")
plt.title(rootfile.name, fontsize=8)
plt.grid(True, ls=":")
plt.tight_layout()
outfile = rootfile.with_suffix(".scan.png")
plt.savefig(outfile, dpi=150)
print(f"Saved plot → {outfile}")
