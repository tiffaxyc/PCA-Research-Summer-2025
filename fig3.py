import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#https://www.geeksforgeeks.org/python/contour-plot-using-matplotlib-python/'
#https://alexmiller.phd/posts/contour-plots-in-python-matplotlib-x-y-z/
data = pd.read_csv("1990_electron_density_forgraph_output.csv")

#x = days
#y= altitude
#z = electron density
#need to reshape data, create emptygrid of density values
#1 row for each altitude, 1 col for each day
days = np.sort(data["Date"].unique())
altitudes = np.sort(data["Altitude_km"].unique())
Z = np.zeros((len(altitudes), len(days)))
#fill in grid
for i, altitude in enumerate(altitudes):
    for j, day in enumerate(days):
        value = data[(data["Altitude_km"] == altitude) &
        (data["Date"] == day)]["Electron_density_cm3"]
        Z[i,j] = np.log10(value.values[0])

# Generate meshgrid
X, Y = np.meshgrid(days, altitudes)
#share axis, 3 rows, 1 col, returns a tuple of (figure, subplots)
grid = plt.subplots(3, 1, figsize=(10, 8), sharey=True)
whole_fig = grid[0] #figure
subplots = grid[1] #subplots
#3 plots, day rnges
ranges = [(0, 120), (120, 240), (240, 380)]

#loops thru each subplot, corresponding to each range
#subplt 1 : range 0-120
#subplt 2: range 120-240
#subplt 3 : range 240-380
for i in range(len(ranges)):
    each_plot = subplots[i]
    start, end = ranges[i]
    mask = (days >= start) & (days < end)
    day_subset = days[mask]

    X_sub, Y_sub = np.meshgrid(day_subset, altitudes)
    #sets altitude (all rows:) for only days where mask = true
    Z_sub = Z[:, mask]

    contour = each_plot.contour(X_sub, Y_sub, Z_sub, levels=range(1, 6), colors='black')
    each_plot.clabel(contour, fmt='%d', fontsize=8)
    each_plot.set_xlim(start, end)
    each_plot.set_ylabel("Altitude (km)")
    each_plot.grid(False)

subplots[-1].set_xlabel("Day of 1990")
whole_fig.suptitle("Figure 3", fontsize=14)
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()
