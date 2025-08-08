# Polar Cap Absorption Model Reproduction
**Author:** Tiffany Cai
**Date:** Summer 2025

This repository contains Python scripts developed to reproduce the Polar Cap Absorption (PCA) model presented in:

> Patterson, J. D., T. P. Armstrong, C. M. Laird, D. L. Detrick, and A. T. Weatherwax (2001), Correlation of solar energetic protons and polar cap absorption, J. Geophys. Res., 106(A1), 149–163, doi:10.1029/2000JA002006.       
> > [Link to article](https://agupubs.onlinelibrary.wiley.com/doi/epdf/10.1029/2000JA002006)  

The project replicates figures, calculations, and statistical comparisons from the study, using proton flux and riometer absorption datasets.

---

## Table of Contents
- [Repository Structure](#repository-structure)  
- [Datasets](#datasets)  
- [Installation](#installation)  
- [Usage](#usage)  
- [Notes](#notes)  

---

## Repository Structure

| File | Description |
|------|-------------|
| `absorption_calc.py` | Calculates theoretical absorption values based on proton flux and model parameters. |
| `avg_measured_absorption.py` | Processes measured riometer data and computes daily average absorption values. |
| `electron_density_calc.py` | Computes electron density profiles using ion production rates and recombination coefficients. |
| `fig1.py` | Replicates Figure 1 from the paper. |
| `fig3.py` | Replicates Figure 3 (electron density contour plots). |
| `fig4.py` | Replicates Figure 4 (absorption efficiency curves). |
| `.gitignore` | Specifies files to ignore in version control. |
| `README.md` | This file. |

---

## Datasets 

### 1. Proton Flux Data (IMP-8 CPME-PET instrument)  
- **Source:** [http://sd-www.jhuapl.edu/IMP/data/imp8/cpme/cpme_1d/protons/flux/](http://sd-www.jhuapl.edu/IMP/data/imp8/cpme/cpme_1d/protons/flux/)  

### 2. Measured Cosmic Radio Noise Absorption Data (South Pole Riometer)  
- **Source:** [https://vmo.igpp.ucla.edu/data1/ICESTAR/](https://vmo.igpp.ucla.edu/data1/ICESTAR/)  

> **Note:**  
> Both datasets must be **converted to CSV format** before running scripts.

 **Google Colab Notebook:**  
[Download South Pole Riometer Data (1986–1994) – Google Colab](https://colab.research.google.com/drive/15T7bC8leUwYcN0Hqre1i4bV5hNRjy9kx?usp=sharing)  
*This notebook shows how `.rio` files were downloaded, stripped of headers, and saved as `.txt` for later conversion to CSV.  
It can also be used for future absorption calculations (not yet implemented in this repository).*


---

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/tiffaxyc/PCA-RESEARCH-SUMMER-2025.git
   cd PCA-RESEARCH-SUMMER-2025 
2. Install dependencies: 
    ```bash
    pip install numpy pandas matplotlib

---

## Usage

1. Download [Datasets](#datasets)  
2. Convert raw data to .csv format before use.
3. Place CSV files inside a data/directory in the repository.
- Note: Make sure to change input file path.
4. Run scripts:
    ```bash
    python fig1.py
    python fig3.py
    python fig4.py
    python absorption_calc.py
    python avg_measured_absorption.py
    python electron_density_calc.py
5. View results in the output/directory.

---

## Notes

- Data gaps: Missing measured absorption data for 20.5 MHz and 38.2 MHz will affect correlation values and completeness of figures.

- Daily averages: Calculations use daily averaged proton flux and absorption, matching the method in Patterson et al.

- Figures: The scripts replicate Figures 1, 3, 4 from the study; Figures 5–12 require complete measured datasets.

## Next Steps

To fully reproduce the results of **Patterson et al. (2001)**, the following needs to be completed:

1. **Fill Missing Measured Absorption Data**
   - Find complete South Pole riometer datasets (1986–1994) for **20.5 MHz** and **38.2 MHz**.

2. **Reproduce Remaining Figures & Tables**
   - **Figure 5:** Generate crossplots for all four frequencies once measured data is complete.
   - **Table 4:** Recalculate correlation coefficients (p²) and χ² for A > 1.0 dB and A < 1.0 dB.
   - **Figure 6:** Create full time series plots for 1986–1994 at each frequency.
   - **Figures 7–10:** Model absorption vs. proton energy & frequency; validate against study’s curves.
   - **Figures 11–12 & Table 5:** Compare recombination coefficient models.
   - **Table 6:** Calculate fractional absorption by altitude for sampled PCA events.

3. **Verify with Paper’s Results**


4. **Improve Script Flexibility**
   - Parameterize input file paths, date ranges, and frequencies.


---
