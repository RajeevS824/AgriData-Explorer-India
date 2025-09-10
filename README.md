# 🌾 AgriData Explorer – Indian Agriculture Analysis

## 📌 Project Overview

India’s agricultural sector is vast and diverse, but analyzing its data is challenging due to fragmented sources and complexity.
This project aims to build an **end-to-end data pipeline and visualization system** that helps:

* **Farmers** → decide what crops to grow based on historical yields.
* **Policymakers** → identify low-yield regions and design subsidies or insurance.
* **Researchers** → study agricultural trends, crop performance, and innovations.

The project integrates **Python, SQL, and Power BI** to deliver insights into crop production, cultivated areas, and yield trends across states and districts of India.

---

## 🛠️ What I Did in This Project

### 1. **Data Preparation (Python + Pandas)**

* Collected and cleaned **district-level agricultural dataset**.
* Standardized units (area in `1000 ha`, production in `1000 tons`, yield in `kg/ha`).
* Reshaped dataset into a **star schema**:

  * `dim_state` → state details.
  * `dim_district` → district details.
  * `fact_crop_yearly_long` → yearly crop facts (area, production, yield).

---

### 2. **SQL Analysis (MySQL + SQLAlchemy)**

* Pushed cleaned tables into **MySQL database**.
* Wrote SQL queries to answer key questions:

  * Top 3 rice-producing states each year.
  * Wheat yield improvement in districts over 5 years.
  * Oilseed growth rates across states.
  * Cotton production in top states.
  * Rice vs Wheat production trend (last 10 years).
* Used **CTEs, window functions, and joins** for efficient analysis.

---

### 3. **Exploratory Data Analysis (Python + Matplotlib)**

* Visualized agricultural patterns through plots:

  * **Top states** → Rice, Wheat, Oilseeds, Sunflower, Groundnut, Soybean.
  * **Trends (50 years)** → Sugarcane, Millet, Sorghum, Rice vs Wheat.
  * **District level** → Rice in West Bengal, Wheat in UP.
  * **Scatter plots** → Area vs Production for Rice, Wheat, Maize.
  * **Efficiency** → Rice vs Wheat yield scatter, Soybean yield efficiency.

---

### 4. **Power BI Dashboards**

* Designed **interactive dashboards** with KPIs, slicers, and charts:

  * **Dashboard 1 – Agricultural Insights**

    * KPIs → Total Area, Production, Yield, States, Crops.
    * State-wise comparison of Area vs Production vs Yield.
    * Crop distribution (area, production, yield).
  * **Dashboard 2 – Agricultural Trends**

    * Time series of Cultivation Area, Production, and Yield.
    * Crop slicer for detailed analysis.
* Added interactivity (filters, tooltips, dynamic visuals).

---

## 🎯 Motive of the Project

* To simplify access to agricultural data for different stakeholders.
* To uncover **hidden trends and regional disparities**.
* To empower **data-driven decision making** in agriculture.

---

## 🌍 Real-Life Use Cases

* **Farmers**: Choose profitable crops for each season based on historical yield.
* **Government**: Allocate subsidies and crop insurance in regions with unstable productivity.
* **Researchers**: Study the effects of soil, irrigation, and climate on yields.
* **Agri-tech companies**: Build advisory services for crop planning and risk management.

---

## ✅ Conclusion

This project demonstrates how **Python, SQL, and Power BI** can work together to transform raw agricultural data into **actionable insights**.
By connecting data pipelines, statistical analysis, and interactive dashboards, the project builds a foundation for **smart agriculture and policy interventions** in India.

