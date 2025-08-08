import numpy as np
import matplotlib.pyplot as plt
import math

altitudes = np.array([
    115, 110, 105, 100, 95, 90, 85, 80, 75, 70,
    65, 60, 55, 50, 45, 40, 35, 30, 25, 20])

# Table 3 data
neutral_temp = {
    115: 380.6,
    110: 317.1,
    105: 265.5,
    100: 228.0,
    95: 203.5,
    90: 190.3,
    85: 183.8,
    80: 185.1,
    75: 195.0,
    70: 205.0,
    65: 216.2,
    60: 232.7,
    55: 249.3,
    50: 263.9,
    45: 271.6,
    40: 267.7,
    35: 255.3,
    30: 241.5,
    25: 230.7,
    20: 221.7,
    }

neutral_density = {
    115: 5.772E+11,
    110: 1.076E+12,
    105: 2.182E+12,
    100: 4.768E+12,
    95: 1.125E+13,
    90: 2.808E+13,
    85: 7.087E+13,
    80: 1.736E+14,
    75: 3.964E+14,
    70: 8.696E+14,
    65: 1.822E+15,
    60: 3.568E+15,
    55: 6.669E+15,
    50: 1.210E+16,
    45: 2.198E+16,
    40: 4.148E+16,
    35: 8.265E+16,
    30: 1.722E+17,
    25: 3.690E+17,
    20: 8.111E+17
}

frequencies_mhz = [20.5, 30.0, 38.2, 51.4]

#eqn 10
def magnetoionic_integral(x):
    a_0 = 1.1630641
    a_1 = 16.901002
    a_2 = 6.6945939
    b_0 = 4.3605732
    b_1 = 64.093464
    b_2 = 68.920505
    b_3 = 35.355257
    b_4 = 6.6314497
    return (x**3 + (a_2 * x**2)+ (a_1 * x) + a_0)/(x**5 + (b_4 * x**4) + (b_3 * x**3)+ (b_2 * x**2) + (b_1*x)+ b_0)

#eqn 11
def coll_freq(h):
    n = neutral_density[h]
    T = neutral_temp[h]
    return 5.4e-10 * n * math.sqrt(T)

#unsure abt value of B
#gyrofreq = eB/m_e
def gyrofrequency(h_km):
    #earth_r = 6371
    #r = earth_r + h_km
    #B = 5e-5 * (earth_r / r) ** 3
    #magnetic field strenght of earth?
    B = 5e-5 
    return (1.602e-19 * B) / (9.109e-31)

plt.figure(figsize=(6, 8))
#k_abs(h,w) = 1.15e5/ve_n (c/ve_n)
for f_mhz in frequencies_mhz:
    #hz --> mhz
    f_hz = f_mhz * 1e6
    #w = 2pif
    omega = 2 * np.pi * f_hz
    kabs_vals = []
    for h in altitudes:
        nu_en = coll_freq(h)
        omega_e = gyrofrequency(h)
        x = (omega + omega_e) / nu_en 
        C = magnetoionic_integral(x)
        k_abs = (1.15e5/ nu_en) * C
        kabs_vals.append(k_abs)

    plt.plot(kabs_vals, altitudes, label=f"{f_mhz} MHz")

altitudes = np.arange(20, 121, 5)
plt.ylim(120, 20)
plt.yticks(np.arange(20, 121, 10))
plt.ylabel("Altitude (km)")
plt.xscale("log") 
plt.xlim(1e-9, 1e-3) 
plt.xlabel("Absorption Efficiency (dB/km-elec-cm³)")

plt.title("Figure 4.")
plt.legend()
#grid lines
plt.grid(True)
plt.gca().invert_yaxis()
plt.show()
