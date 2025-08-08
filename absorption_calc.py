import math
import numpy as np
import pandas as pd
from electron_density_calc import slabs_altitude, calculate_sza, calc_daily_q, get_total_q, calc_electron_density, energy_channels
from scipy import integrate

#table 3
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

#frequency = [30.0, 51.4, 38.2, 20.5]

#c 2.5(x)
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

def coll_freq(h): 
    n = neutral_density.get(h)
    te = neutral_temp.get(h)
    return 5.4e-10 * n * math.sqrt(te)

#electron gyrofreq dependant on alt rad/s
def gyrofrequency(h_km):
    earth_r = 6371
    r = earth_r +h_km
    B = 5e-5 * (earth_r/r) **3
    return (1.602e-19*B)/9.109e-31
    
def calc_absorption(altitude, frequency, ne_dict):
    freq_hz = frequency *1e6
    #w = 2pif --> mhz -> rad/s
    ang_freq = 2*np.pi*freq_hz
    h_km = np.array(altitude)
    integrand = []

    for h in altitude:
        v_en = coll_freq(h)
        omega_e = gyrofrequency(h)  
        x = (ang_freq + omega_e) / v_en 
        C = magnetoionic_integral(x)
        k_abs = (1.15e5 / v_en) * C
        ne = ne_dict.get(h, 0)
        integrand.append(ne * k_abs)

    return np.trapezoid(integrand, h_km) 

def process_flux_and_absorption(csv_path):
    flux_df = pd.read_csv(csv_path, skiprows=1)
    all_results = []
   
    for _, row in flux_df.iterrows():
        year_col = row.get('dec_year')
        date = row.get('doy')
        sza = calculate_sza(90, date, year_col)  
        q_info = calc_daily_q(row)
        q_all = get_total_q(q_info)
        ne_density = calc_electron_density(q_all, sza)

        #freq should be [20.5, 30.0, 38.2, 51.4], but for comparative purposes,
        #we just use 30 and 51.4
        for frequency in [30.0, 51.4]:  
                    absorption = calc_absorption(
                    list(slabs_altitude.keys()), frequency, ne_density
                )
                    all_results.append({
                        "Date": date,
                        "Frequency": frequency,
                        "Absorption_dB": absorption
                    })

    return pd.DataFrame(all_results)

if __name__ == "__main__":
    input_path = "/Users/tiffanycai/Desktop/imp8_csvs/1990flux.csv" 
    #stores more info (energy channel)
    output_path = "1990_absorption.csv"
    df = process_flux_and_absorption(input_path)

    df.to_csv(output_path, index=False)
    #for the contour plot, we see for electron density is the same for all energy channels of 
    # an altitude since we use the cumulative q which is added on from all energy channels
    #of corresponding h
    #so to get the plot, we only need altitude and associated electron density, we 
    #can generalize the electron density by using energy channel 1 (index 0)
  