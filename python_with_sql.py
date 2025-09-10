import pandas as pd
# Load dataset
df = pd.read_excel("District_Level_Data.xlsx")

print("Shape:",df.shape)
#  -------------------------1) dim_state  -------------------------
dim_state = df[['State Code', 'State Name']].drop_duplicates()

dim_district = df[['Dist Code', 'Dist Name', 'State Code']].drop_duplicates()
fact_crop_yearly = df.drop(columns=['State Name', 'Dist Name'])

print(dim_state.shape)
print(dim_district.shape)
print(fact_crop_yearly.shape)

# Identify ID columns
id_vars = ["Dist Code", "Year", "State Code"]

# All other columns are crop-related
value_vars = [c for c in df.columns if c not in id_vars]

# Melt into long format
df_long = df.melt(id_vars=id_vars, value_vars=value_vars,
                  var_name="Crop_Metric", value_name="Value")

# Split 'Crop_Metric' into Crop + Metric
df_long["Metric"] = df_long["Crop_Metric"].str.extract(r"(AREA|PRODUCTION|YIELD)")
df_long["Crop"] = df_long["Crop_Metric"].str.replace(r"\s+(AREA|PRODUCTION|YIELD).*", "", regex=True)

# Pivot so we get Area, Production, Yield in separate columns
fact_crop_yearly_long = df_long.pivot_table(index=["Dist Code", "Year", "State Code", "Crop"],
                                            columns="Metric", values="Value").reset_index()


# --- Rename columns to match SQL schema ---
dim_state = dim_state.rename(columns={
    "State Code": "state_code",
    "State Name": "state_name"
})

dim_district = dim_district.rename(columns={
    "Dist Code": "dist_code",
    "Dist Name": "dist_name",
    "State Code": "state_code"
})

fact_crop_yearly_long = fact_crop_yearly_long.rename(columns={
    "Dist Code": "dist_code",
    "Year": "year",
    "State Code": "state_code",
    "Crop": "crop",
    "AREA": "Area_1000_ha",
    "PRODUCTION": "Production_1000_t",
    "YIELD": "Yield_kg_ha"
})

# --- Setup ---
import matplotlib.pyplot as plt
from sqlalchemy import create_engine, text

# Connection string 
engine = create_engine("mysql+mysqlconnector://root:new_password@localhost/agriculture_db")

# Push to SQL
#dim_state.to_sql("dim_state", con=engine, if_exists="append", index=False)
#dim_district.to_sql("dim_district", con=engine, if_exists="append", index=False)
#fact_crop_yearly_long.to_sql("fact_crop_yearly_long", con=engine, if_exists="append", index=False)

print("Data successfully loaded into SQL database!")


def run_sql(q: str) -> pd.DataFrame:
    return pd.read_sql(text(q), con=engine)

# 1) Year-wise Trend of Rice Production Across States (Top 3 each year)
q1 = """
WITH rice_prod AS (
    SELECT 
        f.year,
        f.state_code,
        s.state_name,
        SUM(f.production_1000_t) AS total_rice_production
    FROM fact_crop_yearly_long f
    JOIN dim_state s ON f.state_code = s.state_code
    WHERE f.crop = 'RICE'
    GROUP BY f.year, f.state_code, s.state_name
),
ranked AS (
    SELECT 
        year,
        state_name,
        total_rice_production,
        RANK() OVER (PARTITION BY year ORDER BY total_rice_production DESC) AS rank_in_year
    FROM rice_prod
)
SELECT year, state_name, total_rice_production
FROM ranked
WHERE rank_in_year <= 3
ORDER BY year, rank_in_year, state_name;
"""
df1 = run_sql(q1)
print("1) Top 3 rice-producing states each year")
print(df1.head(10))
pivot1 = df1.pivot(index="year", columns="state_name", values="total_rice_production")
pivot1.plot(marker="o"); 
plt.title("Rice Production (Top 3 per Year)"); 
plt.xlabel("Year"); 
plt.ylabel("Production (000 Tonnes)"); 
plt.legend(title="State"); 
plt.show()

# 2) Top 5 Districts by Wheat Yield Increase Over the Last 5 Years
q2 = """
WITH year_range AS (
    SELECT MAX(year) AS max_year
    FROM fact_crop_yearly_long
    WHERE crop = 'WHEAT'
),
wheat_yield AS (
    SELECT 
        f.dist_code,
        d.dist_name,
        f.year,
        f.yield_kg_ha
    FROM fact_crop_yearly_long f
    JOIN dim_district d ON f.dist_code = d.dist_code
    WHERE f.crop = 'WHEAT'
),
compare AS (
    SELECT 
        w1.dist_code,
        w1.dist_name,
        ROUND((w1.yield_kg_ha - w2.yield_kg_ha), 2) AS yield_increase
    FROM wheat_yield w1
    JOIN wheat_yield w2 ON w1.dist_code = w2.dist_code
    JOIN year_range yr ON 1=1
    WHERE w1.year = yr.max_year
      AND w2.year = yr.max_year - 5
)
SELECT dist_name, yield_increase
FROM compare
ORDER BY yield_increase DESC
LIMIT 5;
"""
df2 = run_sql(q2)
print("\n2) Top 5 districts by wheat yield increase (last 5 years)")
print(df2)
df2.set_index("dist_name")["yield_increase"].plot(kind="bar"); 
plt.title("Wheat Yield Increase (kg/ha) - Top 5 Districts"); 
plt.xlabel(""); 
plt.ylabel("Increase (kg/ha)"); 
plt.show()

# 3) States with Highest Growth in Oilseed Production (5-Year Growth Rate)
q3 = """
WITH year_range AS (
    SELECT MAX(year) AS max_year
    FROM fact_crop_yearly_long
    WHERE crop = 'OILSEEDS'
),
oilseed_data AS (
    SELECT 
        f.state_code,
        s.state_name,
        f.year,
        SUM(f.production_1000_t) AS total_production
    FROM fact_crop_yearly_long f
    JOIN dim_state s ON f.state_code = s.state_code
    WHERE f.crop = 'OILSEEDS'
    GROUP BY f.state_code, s.state_name, f.year
),
compare AS (
    SELECT 
        o1.state_name,
        o1.total_production AS latest_prod,
        o2.total_production AS past_prod,
        ROUND(((o1.total_production - o2.total_production) / NULLIF(o2.total_production,0)) * 100, 2) AS growth_rate
    FROM oilseed_data o1
    JOIN oilseed_data o2 ON o1.state_name = o2.state_name
    JOIN year_range yr ON 1=1
    WHERE o1.year = yr.max_year
      AND o2.year = yr.max_year - 5
)
SELECT state_name, latest_prod, past_prod, growth_rate
FROM compare
ORDER BY growth_rate DESC
LIMIT 5;
"""
df3 = run_sql(q3)
print("\n3) Highest 5-year growth in oilseed production (states)")
print(df3)
df3.set_index("state_name")["growth_rate"].plot(kind="bar"); 
plt.title("Oilseeds Production Growth Rate (5-Year)"); 
plt.xlabel(""); 
plt.ylabel("Growth (%)"); 
plt.show()

# 4) District-wise Correlation Between Area and Production for RICE, WHEAT, MAIZE
q4 = """
SELECT 
    f.dist_code,
    d.dist_name,
    f.crop,
    f.year,
    f.area_1000_ha,
    f.production_1000_t
FROM fact_crop_yearly_long f
JOIN dim_district d ON f.dist_code = d.dist_code
WHERE f.crop IN ('RICE', 'WHEAT', 'MAIZE');
"""
df4_raw = run_sql(q4)
def _corr(g):
    if g["area_1000_ha"].nunique() > 1 and g["production_1000_t"].nunique() > 1 and len(g)>=3:
        return g[["area_1000_ha","production_1000_t"]].corr().iloc[0,1]
    return None
corr_df = (
    df4_raw.groupby(["dist_name","crop"], as_index=False)
           .apply(lambda g: pd.Series({"pearson_corr": _corr(g)}), include_groups=False)
           .dropna()
           .sort_values("pearson_corr", ascending=False)
)
print("\n4) District-wise area vs production correlation (Rice/Wheat/Maize) - top 15")
print(corr_df.head(15))

# 5) Yearly Production of Cotton in Top 5 Cotton Producing States
q5 = """
WITH total_cotton AS (
    SELECT 
        f.state_code,
        s.state_name,
        SUM(f.production_1000_t) AS total_cotton_production
    FROM fact_crop_yearly_long f
    JOIN dim_state s ON f.state_code = s.state_code
    WHERE f.crop = 'COTTON'
    GROUP BY f.state_code, s.state_name
    ORDER BY total_cotton_production DESC
    LIMIT 5
),
cotton_yearly AS (
    SELECT 
        f.year,
        f.state_code,
        s.state_name,
        SUM(f.production_1000_t) AS yearly_production
    FROM fact_crop_yearly_long f
    JOIN dim_state s ON f.state_code = s.state_code
    WHERE f.crop = 'COTTON'
    GROUP BY f.year, f.state_code, s.state_name
)
SELECT 
    c.year,
    c.state_name,
    c.yearly_production
FROM cotton_yearly c
JOIN total_cotton t ON c.state_code = t.state_code
ORDER BY c.state_name, c.year;
"""
df5 = run_sql(q5)
print("\n5) Cotton yearly production in top 5 states")
print(df5.head(10))
pivot5 = df5.pivot(index="year", columns="state_name", values="yearly_production")
pivot5.plot(marker="o"); 
plt.title("Cotton Production - Top 5 States"); 
plt.xlabel("Year"); 
plt.ylabel("Production (000 Tonnes)"); 
plt.legend(title="State"); 
plt.show()

# 6) Districts with Highest Groundnut Production in Latest Year
q6 = """
WITH latest_year AS (
    SELECT MAX(year) AS max_year
    FROM fact_crop_yearly_long
    WHERE crop = 'GROUNDNUT'
)
SELECT 
    d.dist_name,
    SUM(f.production_1000_t) AS production_latest
FROM fact_crop_yearly_long f
JOIN dim_district d ON f.dist_code = d.dist_code
JOIN latest_year y ON f.year = y.max_year
WHERE f.crop = 'GROUNDNUT'
GROUP BY d.dist_name
ORDER BY production_latest DESC
LIMIT 5;
"""
df6 = run_sql(q6)
print("\n6) Top 5 districts by groundnut production (latest year)")
print(df6)
df6.set_index("dist_name")["production_latest"].plot(kind="bar"); 
plt.title("Groundnut Production (Latest Year) - Top 5 Districts"); 
plt.xlabel(""); plt.ylabel("Production (000 Tonnes)"); 
plt.show()

# 7) Annual Average Maize Yield Across All States
q7 = """
SELECT 
    f.year,
    ROUND(AVG(f.yield_kg_ha), 2) AS avg_maize_yield
FROM fact_crop_yearly_long f
WHERE f.crop = 'MAIZE'
GROUP BY f.year
ORDER BY f.year;
"""
df7 = run_sql(q7)
print("\n7) Annual average maize yield")
print(df7)
df7.plot(x="year", y="avg_maize_yield", marker="o"); 
plt.title("Average Maize Yield Across All States"); 
plt.xlabel("Year"); plt.ylabel("Yield (kg/ha)"); 
plt.show()

# 8) Total Area Cultivated for Oilseeds in Each State
q8 = """
SELECT 
    s.state_name,
    ROUND(SUM(f.area_1000_ha), 2) AS total_oilseeds_area
FROM fact_crop_yearly_long f
JOIN dim_state s ON f.state_code = s.state_code
WHERE f.crop = 'OILSEEDS'
GROUP BY s.state_name
ORDER BY total_oilseeds_area DESC;
"""
df8 = run_sql(q8)
print("\n8) Total oilseeds area by state")
print(df8.head(10))
df8.set_index("state_name")["total_oilseeds_area"].plot(kind="bar"); 
plt.title("Total Area Cultivated for Oilseeds by State"); 
plt.xlabel(""); plt.ylabel("Area (000 ha)"); 
plt.show()

# 9) Districts with the Highest Rice Yield
q9 = """
SELECT 
    d.dist_name,
    ROUND(MAX(f.yield_kg_ha), 2) AS max_rice_yield
FROM fact_crop_yearly_long f
JOIN dim_district d ON f.dist_code = d.dist_code
WHERE f.crop = 'RICE'
GROUP BY d.dist_name
ORDER BY max_rice_yield DESC
LIMIT 10;
"""
df9 = run_sql(q9)
print("\n9) Top 10 districts by max rice yield")
print(df9)
df9.set_index("dist_name")["max_rice_yield"].plot(kind="bar"); 
plt.title("Max Rice Yield - Top 10 Districts"); 
plt.xlabel(""); plt.ylabel("Yield (kg/ha)"); 
plt.show()

# 10) Compare Production of Wheat and Rice for Top 5 States Over 10 Years
q10 = """
WITH top_states AS (
    SELECT 
        s.state_name,
        SUM(f.production_1000_t) AS total_prod
    FROM fact_crop_yearly_long f
    JOIN dim_state s ON f.state_code = s.state_code
    WHERE f.crop IN ('WHEAT', 'RICE')
    GROUP BY s.state_name
    ORDER BY total_prod DESC
    LIMIT 5
),
latest_10_years AS (
    SELECT DISTINCT year
    FROM fact_crop_yearly_long
    ORDER BY year DESC
    LIMIT 10
)
SELECT 
    f.year,
    s.state_name,
    f.crop,
    ROUND(SUM(f.production_1000_t), 2) AS production
FROM fact_crop_yearly_long f
JOIN dim_state s ON f.state_code = s.state_code
JOIN top_states t ON t.state_name = s.state_name
JOIN latest_10_years y ON f.year = y.year
WHERE f.crop IN ('WHEAT', 'RICE')
GROUP BY f.year, s.state_name, f.crop
ORDER BY f.year, s.state_name, f.crop;
"""
df10 = run_sql(q10)
print("\n10) Wheat vs Rice production for top 5 states (last 10 years)")
print(df10.head(12))

# Plot separately (one chart per crop)
for crop in ["WHEAT", "RICE"]:
    pivot10 = df10[df10["crop"]==crop].pivot(index="year", columns="state_name", values="production")
    pivot10.plot(marker="o"); 
    plt.title(f"{crop} Production - Top 5 States (Last 10 Years)"); 
    plt.xlabel("Year"); plt.ylabel("Production (000 Tonnes)"); 
    plt.legend(title="State"); 
    plt.show()
