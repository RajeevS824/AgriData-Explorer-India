import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_excel("District_Level_Data.xlsx")
print("Shape:", df.shape)

# Prepare dimension tables (state, district) and fact table
dim_state = df[['State Code', 'State Name']].drop_duplicates()
dim_district = df[['Dist Code', 'Dist Name', 'State Code']].drop_duplicates()
fact_crop_yearly = df.drop(columns=['State Name', 'Dist Name'])

# Identify ID columns vs crop-related columns
id_vars = ["Dist Code", "Year", "State Code"]
value_vars = [c for c in df.columns if c not in id_vars]

# Reshape dataset into long format (Crop + Metric separated)
df_long = df.melt(id_vars=id_vars, value_vars=value_vars,
                  var_name="Crop_Metric", value_name="Value")
df_long["Metric"] = df_long["Crop_Metric"].str.extract(r"(AREA|PRODUCTION|YIELD)")
df_long["Crop"] = df_long["Crop_Metric"].str.replace(r"\s+(AREA|PRODUCTION|YIELD).*", "", regex=True)

# Pivot into fact table with Area, Production, Yield
fact_crop_yearly_long = df_long.pivot_table(
    index=["Dist Code", "Year", "State Code", "Crop"],
    columns="Metric",
    values="Value"
).reset_index()

# Rename columns for clarity
fact_crop_yearly_long = fact_crop_yearly_long.rename(columns={
    "AREA": "Area_1000_ha",
    "PRODUCTION": "Production_1000_t",
    "YIELD": "Yield_kg_ha"
})

# ---- Rice Production: Top 7 states (Bar Plot)
rice_data = fact_crop_yearly_long.merge(dim_state, on="State Code", how="left")
rice_data = rice_data[rice_data["Crop"] == "RICE"]
rice_production = rice_data.groupby("State Name")["Production_1000_t"].sum().reset_index().sort_values("Production_1000_t", ascending=False)
top7_rice = rice_production.head(7)
print(top7_rice)

plt.figure(figsize=(10,6))
plt.bar(top7_rice["State Name"], top7_rice["Production_1000_t"])
plt.xticks(rotation=45, ha="right")
plt.ylabel("Rice Production (1000 tons)")
plt.title("Top 7 States in Rice Production")
plt.show()

# ---- Wheat Production: Top 5 states (Bar + Pie)
wheat_data = fact_crop_yearly_long.merge(dim_state, on="State Code", how="left")
wheat_data = wheat_data[wheat_data["Crop"] == "WHEAT"]
wheat_production = wheat_data.groupby("State Name")["Production_1000_t"].sum().reset_index().sort_values("Production_1000_t", ascending=False)
top5_wheat = wheat_production.head(5)
print(top5_wheat)

plt.figure(figsize=(10,6))
plt.bar(top5_wheat["State Name"], top5_wheat["Production_1000_t"], color="skyblue")
plt.xticks(rotation=45, ha="right")
plt.ylabel("Wheat Production (1000 tons)")
plt.title("Top 5 Wheat Producing States")
plt.show()

plt.figure(figsize=(8,8))
plt.pie(top5_wheat["Production_1000_t"], labels=top5_wheat["State Name"], autopct="%1.1f%%", startangle=140)
plt.title("Top 5 Wheat Producing States - Percentage Share")
plt.show()

# ---- Oilseeds Production: Top 5 states
oilseed_data = fact_crop_yearly_long.merge(dim_state, on="State Code", how="left")
oilseed_data = oilseed_data[oilseed_data["Crop"] == "OILSEEDS"]
oilseed_production = oilseed_data.groupby("State Name")["Production_1000_t"].sum().reset_index().sort_values("Production_1000_t", ascending=False)
top5_oilseeds = oilseed_production.head(5)
print(top5_oilseeds)

plt.figure(figsize=(10,6))
plt.bar(top5_oilseeds["State Name"], top5_oilseeds["Production_1000_t"], color="red")
plt.xticks(rotation=45, ha="right")
plt.ylabel("Oilseeds Production (1000 tons)")
plt.title("Top 5 Oilseeds Producing States")
plt.show()

# ---- Sunflower Production: Top 7 states
sunflower_data = fact_crop_yearly_long.merge(dim_state, on="State Code", how="left")
sunflower_data = sunflower_data[sunflower_data["Crop"] == "SUNFLOWER"]
sunflower_production = sunflower_data.groupby("State Name")["Production_1000_t"].sum().reset_index().sort_values("Production_1000_t", ascending=False)
top7_sunflower = sunflower_production.head(7)
print(top7_sunflower)

plt.figure(figsize=(10,6))
plt.bar(top7_sunflower["State Name"], top7_sunflower["Production_1000_t"], color="gold")
plt.xticks(rotation=45, ha="right")
plt.ylabel("Sunflower Production (1000 tons)")
plt.title("Top 7 Sunflower Producing States")
plt.show()

# ---- Sugarcane Production Trend: Last 50 years
sugarcane_data = fact_crop_yearly_long[fact_crop_yearly_long["Crop"] == "SUGARCANE"]
sugarcane_trend = sugarcane_data.groupby("Year")["Production_1000_t"].sum().reset_index().sort_values("Year")
last_50_years = sugarcane_trend.tail(50)
print(last_50_years.head())

plt.figure(figsize=(12,6))
plt.plot(last_50_years["Year"], last_50_years["Production_1000_t"], marker="o", color="green")
plt.xlabel("Year")
plt.ylabel("Sugarcane Production (1000 tons)")
plt.title("India's Sugarcane Production (Last 50 Years)")
plt.grid(True, linestyle="--", alpha=0.6)
plt.show()

# ---- Rice vs Wheat Production: Last 50 years
rice_data = fact_crop_yearly_long[fact_crop_yearly_long["Crop"] == "RICE"]
wheat_data = fact_crop_yearly_long[fact_crop_yearly_long["Crop"] == "WHEAT"]
rice_trend = rice_data.groupby("Year")["Production_1000_t"].sum().reset_index().sort_values("Year")
wheat_trend = wheat_data.groupby("Year")["Production_1000_t"].sum().reset_index().sort_values("Year")
trend = rice_trend.merge(wheat_trend, on="Year", suffixes=("_Rice", "_Wheat"))
last_50_years = trend.tail(50)
print(last_50_years.head())

plt.figure(figsize=(12,6))
plt.plot(last_50_years["Year"], last_50_years["Production_1000_t_Rice"], label="Rice", color="blue", marker="o")
plt.plot(last_50_years["Year"], last_50_years["Production_1000_t_Wheat"], label="Wheat", color="brown", marker="s")
plt.xlabel("Year")
plt.ylabel("Production (1000 tons)")
plt.title("Rice vs Wheat Production in India (Last 50 Years)")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.6)
plt.show()

# ---- Rice Production by Districts in West Bengal
rice_data = fact_crop_yearly_long.merge(dim_state, on="State Code", how="left").merge(dim_district, on=["Dist Code", "State Code"], how="left")
rice_wb = rice_data[(rice_data["Crop"] == "RICE") & (rice_data["State Name"] == "West Bengal")]
rice_wb_districts = rice_wb.groupby("Dist Name")["Production_1000_t"].sum().reset_index().sort_values("Production_1000_t", ascending=False)
print(rice_wb_districts.head())

plt.figure(figsize=(12,6))
plt.bar(rice_wb_districts["Dist Name"], rice_wb_districts["Production_1000_t"], color="red")
plt.xticks(rotation=90)
plt.ylabel("Rice Production (1000 tons)")
plt.title("Rice Production by Districts in West Bengal")
plt.show()

# ---- Top 10 Wheat Production Years in Uttar Pradesh
wheat_data = fact_crop_yearly_long.merge(dim_state, on="State Code", how="left")
wheat_up = wheat_data[(wheat_data["Crop"] == "WHEAT") & (wheat_data["State Name"] == "Uttar Pradesh")]
wheat_up_years = wheat_up.groupby("Year")["Production_1000_t"].sum().reset_index().sort_values("Production_1000_t", ascending=False)
top10_wheat_up = wheat_up_years.head(10)
print(top10_wheat_up)

plt.figure(figsize=(10,6))
plt.bar(top10_wheat_up["Year"].astype(str), top10_wheat_up["Production_1000_t"], color="brown")
plt.xticks(rotation=45)
plt.ylabel("Wheat Production (1000 tons)")
plt.title("Top 10 Wheat Production Years in Uttar Pradesh")
plt.show()

# ---- Millet Production Trend: Last 50 years
millet_data = fact_crop_yearly_long[fact_crop_yearly_long["Crop"].isin(["PEARL MILLET", "FINGER MILLET"])]
millet_trend = millet_data.groupby("Year")["Production_1000_t"].sum().reset_index().sort_values("Year")
last_50_millet = millet_trend.tail(50)
print(last_50_millet.head())

plt.figure(figsize=(12,6))
plt.plot(last_50_millet["Year"], last_50_millet["Production_1000_t"], marker="o", color="purple")
plt.xlabel("Year")
plt.ylabel("Millet Production (1000 tons)")
plt.title("India's Millet (Pearl + Finger) Production (Last 50 Years)")
plt.grid(True, linestyle="--", alpha=0.6)
plt.show()

# ---- Sorghum Production (Kharif vs Rabi) by State
sorghum_data = fact_crop_yearly_long.merge(dim_state, on="State Code", how="left")
sorghum_data = sorghum_data[sorghum_data["Crop"].isin(["KHARIF SORGHUM", "RABI SORGHUM"])]
sorghum_by_state = sorghum_data.groupby(["State Name", "Crop"])["Production_1000_t"].sum().reset_index()
sorghum_pivot = sorghum_by_state.pivot(index="State Name", columns="Crop", values="Production_1000_t").fillna(0)
print(sorghum_pivot.head())

sorghum_pivot.plot(kind="bar", figsize=(14,6))
plt.ylabel("Production (1000 tons)")
plt.title("Sorghum Production (Kharif vs Rabi) by State")
plt.xticks(rotation=90)
plt.legend(title="Sorghum Type")
plt.tight_layout()
plt.show()

sorghum_pivot.plot(kind="bar", stacked=True, figsize=(14,6))
plt.ylabel("Production (1000 tons)")
plt.title("Total Sorghum Production by State (Kharif + Rabi)")
plt.xticks(rotation=90)
plt.legend(title="Sorghum Type")
plt.tight_layout()
plt.show()

# ---- Groundnut Production: Top 7 states
groundnut_data = fact_crop_yearly_long.merge(dim_state, on="State Code", how="left")
groundnut_data = groundnut_data[groundnut_data["Crop"] == "GROUNDNUT"]
groundnut_production = groundnut_data.groupby("State Name")["Production_1000_t"].sum().reset_index().sort_values("Production_1000_t", ascending=False)
top7_groundnut = groundnut_production.head(7)
print(top7_groundnut)

plt.figure(figsize=(10,6))
plt.bar(top7_groundnut["State Name"], top7_groundnut["Production_1000_t"], color="peru")
plt.xticks(rotation=45, ha="right")
plt.ylabel("Groundnut Production (1000 tons)")
plt.title("Top 7 States in Groundnut Production")
plt.show()

# ---- Soybean Production and Yield Efficiency
soy_data = fact_crop_yearly_long.merge(dim_state, on="State Code", how="left")
soy_data = soy_data[soy_data["Crop"] == "SOYABEAN"]
soy_state = soy_data.groupby("State Name")[["Area_1000_ha", "Production_1000_t"]].sum().reset_index()

def safe_yield(row):
    return (row["Production_1000_t"] * 1000) / (row["Area_1000_ha"] * 1000) if row["Area_1000_ha"] > 0 else 0

soy_state["Yield_t_per_ha"] = soy_state.apply(safe_yield, axis=1)
top5_soy = soy_state.sort_values("Production_1000_t", ascending=False).head(5)
print(top5_soy)

plt.figure(figsize=(10,6))
plt.bar(top5_soy["State Name"], top5_soy["Production_1000_t"], color="goldenrod")
plt.xticks(rotation=45, ha="right")
plt.ylabel("Soybean Production (1000 tons)")
plt.title("Top 5 Soybean Producing States")
plt.show()

plt.figure(figsize=(10,6))
plt.bar(top5_soy["State Name"], top5_soy["Yield_t_per_ha"], color="seagreen")
plt.xticks(rotation=45, ha="right")
plt.ylabel("Soybean Yield (tons per ha)")
plt.title("Yield Efficiency of Top 5 Soybean States")
plt.show()

# ---- Oilseed Production in Major States (Top 10)
oilseed_data = fact_crop_yearly_long.merge(dim_state, on="State Code", how="left")
oilseed_data = oilseed_data[oilseed_data["Crop"] == "OILSEEDS"]
oilseed_by_state = oilseed_data.groupby("State Name")["Production_1000_t"].sum().reset_index().sort_values("Production_1000_t", ascending=False)
print(oilseed_by_state.head(10))

plt.figure(figsize=(12,6))
plt.bar(oilseed_by_state["State Name"][:10], oilseed_by_state["Production_1000_t"][:10], color="orange")
plt.xticks(rotation=45, ha="right")
plt.ylabel("Oilseeds Production (1000 tons)")
plt.title("Oilseed Production in Major States (Top 10)")
plt.show()

# ---- Area vs Production (Rice, Wheat, Maize) scatter comparison
crops = {
    "RICE": ("RICE AREA (1000 ha)", "RICE PRODUCTION (1000 tons)"),
    "WHEAT": ("WHEAT AREA (1000 ha)", "WHEAT PRODUCTION (1000 tons)"),
    "MAIZE": ("MAIZE AREA (1000 ha)", "MAIZE PRODUCTION (1000 tons)")
}

plt.figure(figsize=(15, 5))
for i, (crop, (area_col, prod_col)) in enumerate(crops.items(), 1):
    plt.subplot(1, 3, i)
    plt.scatter(df[area_col], df[prod_col], alpha=0.5)
    plt.title(f"{crop}: Area vs Production")
    plt.xlabel("Area Cultivated (1000 ha)")
    plt.ylabel("Production (1000 tons)")
plt.tight_layout()
plt.show()

# ---- Rice vs Wheat Yield Across States (Scatter with labels)
state_yields = df.groupby("State Name")[["RICE YIELD (Kg per ha)", "WHEAT YIELD (Kg per ha)"]].mean().reset_index()

plt.figure(figsize=(12, 15))
plt.scatter(state_yields["RICE YIELD (Kg per ha)"], state_yields["WHEAT YIELD (Kg per ha)"], color="blue", alpha=0.7)
for i, row in state_yields.iterrows():
    plt.text(row["RICE YIELD (Kg per ha)"] + 10, row["WHEAT YIELD (Kg per ha)"] + 10, row["State Name"], fontsize=8)

plt.title("Rice vs. Wheat Yield Across States")
plt.xlabel("Rice Yield (Kg per ha)")
plt.ylabel("Wheat Yield (Kg per ha)")
plt.grid(True, linestyle="--", alpha=0.6)
plt.show()