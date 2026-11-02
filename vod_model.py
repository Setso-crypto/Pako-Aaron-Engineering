import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# =================================================================
# 1. BERA 2026/27 REAL-WORLD REGULATORY TARIFF RATES (TOU 8)
# =================================================================
BPC_PEAK_TARIFF_KWH = 2.28       # BWP per kWh during peak hours
BPC_OFF_PEAK_TARIFF_KWH = 1.15   # BWP per kWh during off-peak hours
BPC_DEMAND_CHARGE_KVA = 210.00   # BWP per kVA statutory monthly demand fee

POWER_FACTOR = 0.88              # Standard industrial motor power factor (cos phi)
BASE_FAN_POWER_KW = 450.0        # Auxiliary ventilation network capacity load

# Simulating 24-Hour Mining Shift Profile
hours = list(range(24))
shift_profile = [
    0,0,0,0,0,0,                 # Early Morning Empty Mine
    1,1,1,1,1,1,1,1,             # Day Shift Production
    2,                           # Shift-change Blasting / Toxic gas flush
    1,1,1,1,1,1,1,               # Night Shift Production
    2,2                          # Main Blasting Clearance
]

bpc_peak_hours = {7, 8, 9, 18, 19, 20}  # Peak hours for BPC TOU tariff
tariff_schedule = [1 if hour in bpc_peak_hours else 0 for hour in hours]

df = pd.DataFrame({
    'Hour': hours,
    'Activity_Type': shift_profile,
    'Is_Peak_Hour': tariff_schedule
})

# =================================================================
# 2. VENTILATION ON DEMAND (VoD) MECHANICAL MODELING
# =================================================================
def determine_flow_ratio(activity):
    if activity == 0: return 0.45   # Maintain 45% safe airflow for structural integrity
    if activity == 1: return 1.00   # 100% statutory required baseline airflow
    if activity == 2: return 1.10   # 125% overdrive to clear post-blast diesel particles fast
    return 1.00

df['Flow_Target'] = df['Activity_Type'].apply(determine_flow_ratio)

# Fluid Mechanics: Fan Affinity Law (Required Power scales cubically with Flow Volume)
df['Traditional_Load_kW'] = BASE_FAN_POWER_KW
df['VoD_Load_kW'] = BASE_FAN_POWER_KW * (df['Flow_Target'] ** 3)

# Convert active working loads to apparent energy indicators (kVA)
df['Traditional_Apparent_kVA'] = df['Traditional_Load_kW'] / POWER_FACTOR
df['VoD_Apparent_kVA'] = df['VoD_Load_kW'] / POWER_FACTOR

# =================================================================
# 3. REGULATORY METRIC COST ANALYSIS
# =================================================================
def calculate_consumption_cost(row, load_col):
    tariff = BPC_PEAK_TARIFF_KWH if row['Is_Peak_Hour'] == 1 else BPC_OFF_PEAK_TARIFF_KWH
    return row[load_col] * 1.0 * tariff

df['Trad_Energy_Cost'] = df.apply(lambda r: calculate_consumption_cost(r, 'Traditional_Load_kW'), axis=1)
df['VoD_Energy_Cost'] = df.apply(lambda r: calculate_consumption_cost(r, 'VoD_Load_kW'), axis=1)

daily_trad_opex = df['Trad_Energy_Cost'].sum()
daily_vod_opex = df['VoD_Energy_Cost'].sum()
daily_savings = daily_trad_opex - daily_vod_opex

# =================================================================
# 4. MAXIMUM DEMAND & POWER FACTOR PENALTY ANALYSIS
# =================================================================
peak_traditional_kva = df['Traditional_Apparent_kVA'].max()
peak_vod_kva = df['VoD_Apparent_kVA'].max()

monthly_trad_demand_fee = peak_traditional_kva * BPC_DEMAND_CHARGE_KVA
monthly_vod_demand_fee = peak_vod_kva * BPC_DEMAND_CHARGE_KVA
monthly_demand_savings = monthly_trad_demand_fee - monthly_vod_demand_fee

# =================================================================
# 5. CORPORATE FINANCE LAYER: CAPITAL BUDGETING
# =================================================================
CAPEX = 650000.00             # Upfront investment cost for VSDs and sensor network (BWP)
ANNUAL_MAINTENANCE = 35000.00 # Annual operational upkeep cost
DISCOUNT_RATE = 0.12          # 12% Corporate Cost of Capital
PROJECT_LIFESPAN_YEARS = 5    # Assessment period

annual_energy_savings = (daily_savings * 365) + (monthly_demand_savings * 12)
annual_net_cash_flow = annual_energy_savings - ANNUAL_MAINTENANCE

print("============ BERA 2026/27 TOU MINING METRICS ============")
print(f"Traditional Strategy Daily Cost : BWP {daily_trad_opex:,.2f}")
print(f"Automated VoD Strategy Daily Cost: BWP {daily_vod_opex:,.2f}")
print(f"Net Daily Financial Savings      : BWP {daily_savings:,.2f}")
print(f"Estimated Monthly Energy Savings : BWP {(daily_savings * 30.5):,.2f}")
print("=========================================================")

print("\n============ BERA MAXIMUM DEMAND CHARGE SUMMARY ============")
print(f"Traditional Peak Demand Load    : {peak_traditional_kva:.1f} kVA")
print(f"Automated VoD Peak Demand Load : {peak_vod_kva:.1f} kVA")
print(f"Monthly Trad Demand Tariff Fee : BWP {monthly_trad_demand_fee:,.2f}")
print(f"Monthly VoD Demand Tariff Fee  : BWP {monthly_vod_demand_fee:,.2f}")
print(f"Net Monthly Demand Cost Savings: BWP {monthly_demand_savings:,.2f}")

print("\n============ PROJECT FINANCIAL FEASIBILITY ANALYSIS ============")
print(f"Initial Capital Investment (CapEx) : BWP {CAPEX:,.2f}")
print(f"Net Annual Operational Cash Inflow: BWP {annual_net_cash_flow:,.2f}")

npv = -CAPEX
for year in range(1, PROJECT_LIFESPAN_YEARS + 1):
    discounted_value = annual_net_cash_flow / ((1 + DISCOUNT_RATE) ** year)
    npv += discounted_value
    print(f"Year {year} Discounted Cash Flow     : BWP {discounted_value:,.2f}")

print(f"\nNet Present Value (NPV @ {DISCOUNT_RATE*100}%): BWP {npv:,.2f}")
months_to_payback = CAPEX / (annual_net_cash_flow / 12)
print(f"Estimated Investment Payback Period: {months_to_payback:.1f} Months")
print("==================================================================")

# =================================================================
# 6. PROFESSIONAL MATPLOTLIB GRAPHICS EXPORT MODULE
# =================================================================
plt.style.use('default')
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 7), sharex=True)

ax1.plot(df['Hour'], df['Traditional_Load_kW'], label='Traditional Strategy (Continuous 100%)', color='#d9534f', linestyle='--', linewidth=2)
ax1.step(df['Hour'], df['VoD_Load_kW'], label='Automated VoD Optimization Engine', color='#0275d8', where='mid', linewidth=2.5)
ax1.set_ylabel('Auxiliary Fan Draw (kW)', fontsize=11, fontweight='semibold')
ax1.set_title('Techno-Economic Modeling: Ventilation on Demand (VoD) Performance Dynamics', fontsize=13, fontweight='bold', pad=15)
ax1.legend(loc='upper right')

for start, end in [(7,9), (18,20)]:
    ax1.axvspan(start, end, color='#f0ad4e', alpha=0.15)

ax2.plot(df['Hour'], df['Trad_Energy_Cost'].cumsum(), label='Baseline Cumulative Cost', color='#d9534f', linewidth=2)
ax2.plot(df['Hour'], df['VoD_Energy_Cost'].cumsum(), label='VoD Cumulative Cost', color='#5cb85c', linewidth=2.5)
ax2.set_xlabel('24-Hour Mining Operational Shift Cycle (Hours)', fontsize=11, fontweight='semibold')
ax2.set_ylabel('Cumulative Cost (BWP)', fontsize=11, fontweight='semibold')
ax2.set_xticks(range(0, 24, 2))
ax2.legend(loc='upper left')

plt.tight_layout()
plt.savefig('vod_savings_chart.png', dpi=300)
print("\n[SUCCESS] Professional executive visualization charts exported cleanly as 'vod_savings_chart.png'")
