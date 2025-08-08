import matplotlib.pyplot as plt

#trying to replicate the figure 1 from article, proton flux day 143 of 1992
# energy midpoints of channels in MeV, calculated from table 1 in article
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
flux_values = [
    1.46E+04, #p1_fx
    4.04E+03, #p2_fx
    5.98E+02, #p3_fx
    3.35E+01, #p4_fx
    2.65E-01, #p5_fx
    2.62E-03, #p7_fx , why are we missing for channel6? will it affect results?
    3.98E-03, #p8_fx
    1.69E-03, #p9_fx
    1.04E-03, #p10_fx
    8.82E-04 ] # p11_fx

plt.figure(figsize=(6, 8))
plt.plot(energy_channels, flux_values, marker='o', linestyle='-', color='b')

plt.xscale('log')
plt.yscale('log')
plt.xlim(1e-01, 1e+03)
plt.ylim(1e-04, 1e+05)

plt.xlabel('Energy (MeV)', fontsize=14)
plt.ylabel('Proton Flux (counts/sr-cm²-sec-MeV/nuc)', fontsize=14)
plt.title('Figure 1.', fontsize=16)
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.show()