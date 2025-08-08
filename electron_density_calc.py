import math
import pandas as pd
from datetime import datetime, timedelta
#table 1, energy channel parameters
energy_channels = [
    (0.29 + 0.5)/2, #p1
    (0.50 +0.96)/2,#p2
    (.96+2)/2,#p3
    (2.00+ 4.60)/2, #p4
    (4.6+ 15.0)/2,#p5
    (15+ 25.0)/2, #p7
    (25+48.0)/2, #p8
    (48+96.0)/2, #p9
    (96+145.0)/2, #p10
    (145+440)/2] #p11

#table 2: altitude : avg equivv. sealvl thickness (km : cm)
slabs_altitude = {
     115: 0.0122, 
     110: 0.0247, 
     105: 0.0533, 
     100: 0.119,  
     95: 0.286,
     90: 0.737,  
     85: 1.94,    
     80: 4.76,   
     75: 10.6,   
     70: 22.1,
     65: 43.5,   
     60: 82.4,   
     55: 152,    
     50: 278,    
     45: 530,
     40: 1070,   
     35: 2250,    
     30: 4840,   
     25: 10600,  
     20: 23600}

flux_cols = ['p1_fx', 'p2_fx', 'p3_fx', 'p4_fx', 'p5_fx', 'p6_fx', 'p8_fx', 'p9_fx', 
             'p10_fx', 'p11_fx']

#table 3
neutral_data = {
    115: {'temperature': 380.6, 'density': 5.772E+11},
    110: {'temperature': 317.1, 'density': 1.076E+12},
    105: {'temperature': 265.5, 'density': 2.182E+12},
    100: {'temperature': 228.0, 'density': 4.768E+12},
    95: {'temperature': 203.5, 'density': 1.125E+13},
    90: {'temperature': 190.3, 'density': 2.808E+13},
    85: {'temperature': 183.8, 'density': 7.087E+13},
    80: {'temperature': 185.1, 'density': 1.736E+14},
    75: {'temperature': 195.0, 'density': 3.964E+14},
    70: {'temperature': 205.0, 'density': 8.696E+14},
    65: {'temperature': 216.2, 'density': 1.822E+15},
    60: {'temperature': 232.7, 'density': 3.568E+15},
    55: {'temperature': 249.3, 'density': 6.669E+15},
    50: {'temperature': 263.9, 'density': 1.210E+16},
    45: {'temperature': 271.6, 'density': 2.198E+16},
    40: {'temperature': 267.7, 'density': 4.148E+16},
    35: {'temperature': 255.3, 'density': 8.265E+16},
    30: {'temperature': 241.5, 'density': 1.722E+17},
    25: {'temperature': 230.7, 'density': 3.690E+17},
    20: {'temperature': 221.7, 'density': 8.111E+17}
    }

#eq 4, computes energy lost per cm sea lvl air
#important notes : Ep is proton energy in MeV
#return energy loss in keV/cm
def energy_loss(E):
    a0 = -.0316
    a1 = .229
    a2 = -.229
    a3 = .0907
    logEp = math.log10(E)
    correction = 1 + (a3* logEp**3) + (a2* logEp**2) + (a1*logEp) + a0
    return 287* (E**(-.757) ) * correction

#https://www.sciencedirect.com/topics/engineering/solar-declination
# 𝛿=23.45°sin[360°365(284+𝑁)],(2.1) 
def solar_declination(day_of_year):
    declination = 23.44 * math.sin(math.radians(360/365*(day_of_year + 284)))  
    return declination

#sza for south pole
def calculate_sza(lat, day_of_year, year_col):
    latitude = lat  # 90°s
    #solar declination
    δ = solar_declination(day_of_year)

    #local solar time = time based on the position of the Sun relative to the local meridian
    #eot: https://www.pveducation.org/pvcdrom/properties-of-sunlight/solar-time 
    #assume lstm is 0 since south pole doesnt have fixed latitude
    base = datetime(int(year_col), 1, 1)
    b = (360/365) * (day_of_year-81)
    eot = 9.87*math.sin(math.radians(2 * b)) - 7.53* math.cos(math.radians(b)) - 1.5 * math.sin(math.radians(b))
    date = base + timedelta(day_of_year-1)
    lst =date.hour + date.minute / 60 + date.second / 3600  + eot/60

    #hour angle, local solar time
    H = 15 * (lst - 12)  

    #cos(SZA) = sin(δ) * sin(latitude) + cos(δ) * cos(latitude) * cos(H)
    latitude_rad = math.radians(latitude)
    declination_rad = math.radians(δ)
    hour_angle_rad = math.radians(H)

    cos_sza = math.sin(declination_rad) * math.sin(latitude_rad) + math.cos(declination_rad) * math.cos(latitude_rad) * math.cos(hour_angle_rad)
    sza = math.degrees(math.acos(cos_sza))  
    return sza

def earth_shadow_height(sza):
    radius_earth = 6371  
    sza_rad = math.radians(sza)  
    height = radius_earth * (1 / math.cos(sza_rad) - 1)
    return height

#aeff
def aeff_day(z):
    return 0.501 * math.exp(-0.165 * z)

def aeff_night(z):
    return 652 * math.exp(-0.234 * z)

def aeff_high(z):
    return 2.5e-6 * math.exp(-0.0195 * z)

def get_mode(x_gse):
    if x_gse > 0:
        return "day"
    else:
        return "night"

def get_aeff(z, sza):
    if z > 85:
        return aeff_high(z)
    shadow_h = earth_shadow_height(sza)
    if z < shadow_h:
        return aeff_night(z)
    else:
        return aeff_day(z)

#loop thru each energy channel, compute energy loss + ionization
def calc_daily_q(flux_row):
    q_info = {}
    for alt in slabs_altitude:
        q_info[alt] = {}
        for E0 in energy_channels:
            q_info[alt][E0] = 0.0

   # date = flux_row.get('dec_year')
    # initialize q to 0 in each slab
   # q_by_altitude = {alt: 0.0 for alt in slabs_altitude} 

    for i in range(len(energy_channels)):
        E0 = energy_channels[i]
        flux_col = flux_cols[i]
        flux = float(flux_row.get(flux_col, 0.0)) #finds flux for the given energy channel i
        #if energy channel has 0 flux, skip
        if flux <= 0:
            continue
        E = E0
        #we want to loop thru each altitude
        for altitude, thickness in slabs_altitude.items():
            if E <= 0: # when proton lost all KE, stop
                break 
            #how much energy proton loses through one slab --> keV (keV/cm * cm)
            e_lost_in_slab = energy_loss(E) * thickness 
            #take min since if e can only lose as much energy it has, cant lose more than it has
            e_lost_conversion = min(E, e_lost_in_slab/1000) #kev --> mev (Pe is in mev)
            e_flux = e_lost_conversion*flux
            q = .12 *e_flux
            #cumulative here? but we also want to keep track of the q contributed
            # by each energy channel
          #  q_by_altitude[altitude] += q 
            #keep track of each contribution:
            q_info[altitude][E0] += q
            E-= e_lost_conversion
    return q_info
   # return [{"Date": date, "Altitude_km": alt, "Ionization_rate_q": q}
    #        for alt, q in q_by_altitude.items()]

def get_total_q(q_info):
    q_by_altitude = {}
    for alt in q_info:
        total_q= 0.0
        for q in q_info[alt].values():
            total_q += q
        q_by_altitude[alt] = total_q
    return q_by_altitude

def calc_electron_density(q_by_altitude, sza):
    ne_by_alt = {}
    for alt, q in q_by_altitude.items():
        aeff = get_aeff(alt, sza)
        ne = math.sqrt(q/aeff)
        ne_by_alt[alt] = ne
    return ne_by_alt

def process_flux_file(csv_path):
    #skip first row (header)
    flux_df = pd.read_csv(csv_path, skiprows=1)  
    all_results = []
   
#no need for index _,
    for _, row in flux_df.iterrows():
        year_col = row.get('dec_year')
        date = row.get('doy')
        sza = calculate_sza(90, date, year_col)  
        q_info = calc_daily_q(row)
        q_all = get_total_q(q_info)
        ne_density = calc_electron_density(q_all, sza)

        for alt in slabs_altitude:
            for E0 in energy_channels:
                all_results.append({
                    "Date": date,
                    "Mode": 'day' if sza < 90 else 'night',
                    "Altitude_km": alt,
                    "Energy_MeV": E0,
                    "q": q_info[alt][E0],
                    "Electron_density_cm3": ne_density[alt] 
                })

    return pd.DataFrame(all_results)

if __name__ == "__main__":
    input_path = "/Users/tiffanycai/Desktop/imp8_csvs/1990flux.csv" 
    #stores more info (energy channel)
    output_path = "1990_electron_density_output.csv"
    output_path_plot = "1990_electron_density_forgraph_output.csv"
    df = process_flux_file(input_path)

    df.to_csv(output_path, index=False)
    #for the contour plot, we see for electron density is the same for all energy channels of 
    # an altitude since we use the cumulative q which is added on from all energy channels
    #of corresponding h
    #so to get the plot, we only need altitude and associated electron density, we 
    #can generalize the electron density by using energy channel 1 (index 0)
    general_energy_channel = energy_channels[0]
    #filters dataframe to onmly include rows of energy channel 1
    filtered_df = df[df['Energy_MeV'] == general_energy_channel]
    #we dont need energy channel column, so filter it out
    df_clean = filtered_df[['Date', 'Mode', 'Altitude_km', 'Electron_density_cm3']].copy()
    df_clean.to_csv(output_path_plot, index=False)
