import pandas as pd

df = pd.read_csv(
    "/Users/tiffanycai/Desktop/imp8_csvs/1990_absorption.csv",
    skiprows=10,
    names=["Time", "30_MHz", "51.4_MHz"]  
)

df = df.dropna()

avg_30mhz = df["30_MHz"].mean()
avg_51mhz = df["51.4_MHz"].mean()

print(f"Daily Average Absorption - 30 MHz: {avg_30mhz:.3f} dB")
print(f"Daily Average Absorption - 51.4 MHz: {avg_51mhz:.3f} dB")
