# Underground Mine Ventilation on Demand (VoD) Techno-Economic Optimization Engine

## Project Overview
This repository contains a quantitative, data-driven software framework that models the integration of smart automation hardware within underground mine ventilation infrastructures. The system leverages physical fluid dynamics constraints and statutory utility regulations to optimize energy consumption patterns, reducing operational volatility and maximizing capital efficiency.

This model is configured using the **Botswana Energy Regulatory Authority (BERA) 2026/27 Time-of-Use (TOU 8)** industrial electricity pricing schedule to analyze the real financial impact of transitioning from static auxiliary fan deployment to programmatic Automated Control.

## Core Problem Statement
Deep underground mines face immense cost centers, with auxiliary ventilation accounts frequently consuming up to **40-50%** of an active mine site's total electrical baseline. Traditional operations run massive mechanical fans at 100% continuous output regardless of immediate shaft occupancy or production cycles, creating massive financial waste.

## Technical Architecture & Methodology

### 1. Fluid Dynamics Engine (Fan Affinity Laws)
The script maps airflow requirements cubically to power consumption coefficients. The structural fan efficiency profile dictates that required power scales with the cube of the shaft velocity ratio:

$$\frac{P_2}{P_1} = \left(\frac{Q_2}{Q_1}\right)^3$$

By dynamically shifting airflow output to **45% of peak capacity** during low-occupancy shifts, the optimization script drops fan draw requirements to just **~9.1% of continuous baseline output**, creating significant operational cash-flow variances.

### 2. Commercial Optimization Layer
* **Statutory Framework:** Modeled after BERA TOU 8 tariff classifications, factoring in regular regional industrial rate increases.
* **Capital Budgeting Metrics:** Upfront automated engineering deployment costs are systematically evaluated using high-level quantitative project metrics:
  * **Net Present Value (NPV):** Project outlays discounted over a 5-year mining lifecyle using a 12% Cost of Capital.
  * **Payback Period Estimation:** Calculates exact capital recovery horizons based on real cash-flow margins.
# =================================================================
# UPDATE: BERA STATUTORY MAXIMUM DEMAND & POWER FACTOR PENALTY ANALYSIS
# =================================================================
# 1. Isolate the absolute highest hourly kVA draw from the daily dataframe
peak_traditional_kva = df['Traditional_Apparent_kVA'].max()
peak_vod_kva = df['VoD_Apparent_kVA'].max()

# BERA calculates demand fees monthly based on the peak demand spike recorded
monthly_trad_demand_fee = peak_traditional_kva * BPC_DEMAND_CHARGE_KVA
monthly_vod_demand_fee = peak_vod_kva * BPC_DEMAND_CHARGE_KVA
monthly_demand_savings = monthly_trad_demand_fee - monthly_vod_demand_fee

# 2. Simulate the structural cost penalty of a degrading Power Factor (PF)
# Poor power factors draw higher current, heavily scaling up kVA penalties
volatile_pf_scenarios = [0.75, 0.82, 0.88, 0.95] # 0.75 is heavily penalized; 0.95 is ideal
pf_analysis_metrics = []

for simulated_pf in volatile_pf_scenarios:
    # Recalculate peak VoD kVA demand under differing power factor efficiencies
    simulated_peak_kva = BASE_FAN_POWER_KW / simulated_pf
    simulated_monthly_fee = simulated_peak_kva * BPC_DEMAND_CHARGE_KVA
    pf_analysis_metrics.append((simulated_pf, simulated_monthly_fee))

print("\n============ BERA MAXIMUM DEMAND CHARGE SUMMARY ============")
print(f"Traditional Peak Demand Load    : {peak_traditional_kva:.1f} kVA")
print(f"Automated VoD Peak Demand Load : {peak_vod_kva:.1f} kVA")
print(f"Monthly Trad Demand Tariff Fee : BWP {monthly_trad_demand_fee:,.2f}")
print(f"Monthly VoD Demand Tariff Fee  : BWP {monthly_vod_demand_fee:,.2f}")
print(f"Net Monthly Demand Cost Savings: BWP {monthly_demand_savings:,.2f}")

print("\n--- Power Factor Financial Sensitivity Analysis ---")
for pf, fee in pf_analysis_metrics:
    penalty_note = " (BERA Penalty Zone)" if pf < 0.85 else " (Compliant Zone)"
    print(f"Operating PF: {pf:.2f} -> Projected Monthly Demand Charge: BWP {fee:,.2f}{penalty_note}")
print("=============================================================")

# ⚠️ INTEGRATION ADJUSTMENT FOR YOUR FINANCE LAYER:
# To make your capital budgeting realistic, update your annual energy savings
# calculation to include the monthly demand tariff savings vector:
annual_energy_savings = (daily_savings * 365) + (monthly_demand_savings * 12)

## Performance Analysis & Visualizations
The model evaluates active mine shift profiles against peak and off-peak rate vectors, compiling detailed metrics shown below:

* **Baseline Traditional Opex:** BWP 15,471.00 / Day
* **Optimized VoD Opex Engine:** BWP 14,128.67 / Day
* **Net Annual Operational Cash Inflow:** ~BWP 454,950.56
* **Project Investment Payback Horizon:** ~17.1 Months
* **5-Year Asset Net Present Value (NPV @ 12%):** BWP 989,994.97

![VoD Performance Optimization Dynamics](vod_savings_chart.png)

## Deployment & Replication Steps
To execute the economic simulation model locally, clone the repository and run the setup commands through your terminal:

```bash
git clone https://github.com
cd Pako-Aaron-Engineering
python vod_model.py
```

## Licensing & IP Statement
Copyright (c) 2026. All rights reserved. Licensed under the GNU General Public License v3.0 (GPL-3.0). Code artifacts and quantitative asset optimization models are open to public evaluation and review for academic, recruitment, and corporate validation purposes.
