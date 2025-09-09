# AgriData-Explorer-India

A Python + SQL + Power BI project that cleans, analyzes, and visualizes Indian agricultural data, providing insights into crop production, yield, and cultivation trends to help **farmers, policymakers, and researchers** make data-driven decisions.

---

## Project Overview

This project is an **Agricultural Data Analysis and Dashboard** initiative. It automates the process of **cleaning, storing, analyzing, and visualizing** district-level agricultural datasets.
The dashboard highlights **state/crop-wise production trends, yields, and growth rates**, enabling smarter agricultural planning and policymaking.

---

## Steps Done in the Project

### 1. Data Cleaning (Python)

* Loaded district-level crop dataset (ICRISAT).
* Handled missing values and standardized units (tons, hectares, kg/ha).
* Split dataset into **fact and dimension tables** (star schema).
* Reshaped data into long format for crop-metric analysis.
* Exported cleaned dataset for database storage.

---

### 2. Database Integration (MySQL)

* Designed relational schema:

  * **dim\_state** – State codes & names.
  * **dim\_district** – District codes, names, linked to states.
  * **fact\_crop\_yearly\_long** – Area, production, yield by crop and year.
* Inserted cleaned data into MySQL using SQLAlchemy.
* Wrote **10+ SQL queries** to extract insights, e.g.:

  * Top 3 rice-producing states per year.
  * Wheat yield growth by district.
  * States with highest oilseed production growth.
  * Cotton production trends in top 5 states.

---

### 3. Dashboard Development (Power BI)

* Connected MySQL database to Power BI.
* Built **interactive dashboards** with slicers for Crop, State, and Year.
* Created KPIs and visualizations:

  * **Total Area, Production, Avg Yield** (cards).
  * **State-wise Area vs Production vs Yield** (bar chart).
  * **Crop-wise Area, Production, Yield** (donut/pie).
  * **Trends over 50 years** (line charts).
  * **Geographic heatmaps** (state-level yield/production).

---

### 4. Data Analysis & Insights

* **Rice & Wheat** dominate cultivated area and production.
* **Oilseeds** show the highest **growth rate in the last 5 years**.
* **Uttar Pradesh, Punjab, and West Bengal** lead in staple crop production.
* **Sugarcane** shows continuous long-term growth.
* District-level analysis reveals yield disparities across regions.

---

### 5. Metrics & Visualization

* **KPIs**: Total cultivated area, total production, average yield.
* **Trends**: Production vs yield growth over decades.
* **Comparisons**: Crop-wise share of area & production.
* **Geographic breakdown**: State and district-level differences.

---

## Real-Life Problem Solved

* **Farmers**: Identify profitable crops and optimize crop planning.
* **Policymakers**: Allocate subsidies, track productivity, and design crop insurance policies.
* **Researchers**: Analyze long-term agricultural patterns and climate/yield impact.
* **National Planning**: Support strategies for food security and resource allocati
