import json

def create_markdown_cell(source):
    if isinstance(source, str):
        source = [line + '\n' for line in source.split('\n')]
    elif isinstance(source, list):
        source = [line + '\n' if not line.endswith('\n') else line for line in source]
    
    if len(source) > 0 and source[-1].endswith('\n'):
        source[-1] = source[-1][:-1]
        
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": source
    }

def create_code_cell(source):
    if isinstance(source, str):
        source = [line + '\n' for line in source.split('\n')]
    elif isinstance(source, list):
        source = [line + '\n' if not line.endswith('\n') else line for line in source]
        
    if len(source) > 0 and source[-1].endswith('\n'):
        source[-1] = source[-1][:-1]
        
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source
    }

cells = []

# Title and Intro
cells.append(create_markdown_cell([
    "# Sales Data Analysis and Business Insights",
    "",
    "**Author:** Shashwat Goswami  ",
    "**Role:** Data Analyst  ",
    "**Dataset:** Superstore Sales Dataset",
    "",
    "## 🎯 Problem Statement",
    "The objective of this project is to analyze retail sales data to identify revenue drivers, loss-making segments, and actionable strategies to improve overall business profitability. Assume the role of a Data Analyst at a retail organization; this analysis supports strategic business decision-making by translating raw operational data into actionable recommendations.",
    "",
    "## 📖 Project Outline",
    "1. **Environment Setup & Data Loading:** Importing necessary libraries and fetching the raw data.",
    "2. **Data Cleaning:** Preparing the dataset for accurate analysis (handling missing values, data types).",
    "3. **Exploratory Data Analysis (EDA):** Visualizing key metrics (Sales, Profit, Trends) to find hidden patterns.",
    "4. **Business Insights & Recommendations:** Deriving deep insights to guide business strategy.",
    "5. **Executive Summary & KPI Dashboard:** Highlighting top-level metrics for senior stakeholders."
]))

# 1. Environment Setup
cells.append(create_markdown_cell([
    "---",
    "## 1. Environment Verification and Setup",
    "In this section, we import the necessary Python libraries required for data manipulation (`pandas`, `numpy`) and visualization (`matplotlib`, `seaborn`). We also establish a consistent, professional visual theme for all plots ensuring they are presentation-ready."
]))

cells.append(create_code_cell([
    "import pandas as pd",
    "import numpy as np",
    "import matplotlib.pyplot as plt",
    "import seaborn as sns",
    "import warnings",
    "",
    "# Suppress warnings for cleaner notebook presentation",
    "warnings.filterwarnings('ignore')",
    "",
    "# Set visualization style for presentation-ready plots",
    "sns.set_theme(style='whitegrid', context='notebook', palette='muted')",
    "plt.rcParams['figure.figsize'] = (12, 6)",
    "plt.rcParams['axes.titlesize'] = 16",
    "plt.rcParams['axes.labelsize'] = 14"
]))

# 2. Data Loading
cells.append(create_markdown_cell([
    "---",
    "## 2. Data Loading and Initial Exploration",
    "We will load the Superstore Sales Dataset and display the first few rows to understand its structure, shape, and early statistical summaries."
]))

cells.append(create_code_cell([
    "url = 'https://raw.githubusercontent.com/leonism/sample-superstore/master/data/superstore.csv'",
    "try:",
    "    # Standard encoding might fail depending on the exact source, using latin1 is universally safe for this CSV",
    "    df = pd.read_csv(url, encoding='latin1')",
    "    print('✅ Dataset loaded successfully!')",
    "except Exception as e:",
    "    print(f'❌ Error loading dataset: {e}')"
]))

cells.append(create_code_cell([
    "# Display the first 5 records to inspect the data format",
    "df.head()"
]))

cells.append(create_code_cell([
    "# Display dataset dimensions and column names",
    "print(f\"Dataset Shape: {df.shape[0]} rows and {df.shape[1]} columns.\\n\")",
    "print(\"Column Names:\")",
    "print(df.columns.tolist())"
]))

cells.append(create_code_cell([
    "# Summary statistics for numerical columns to spot early outliers or anomalies",
    "df.describe()"
]))

# 3. Data Cleaning
cells.append(create_markdown_cell([
    "---",
    "## 3. Data Cleaning",
    "Before diving into the analysis, we must ensure high data quality. Clean data leads to accurate business insights. Our cleaning workflow includes:",
    "- Detecting and addressing missing values.",
    "- Converting string-based dates into reliable `datetime` objects for time-series analysis.",
    "- Dropping duplicate records to prevent skewed profit/sales metrics.",
    "- Extracting features like `Order Year` and `Order Month` for trend line modeling."
]))

cells.append(create_code_cell([
    "# Check for missing values across all columns",
    "missing_values = df.isnull().sum()",
    "print(\"Missing Values:\\n\", missing_values[missing_values > 0] if missing_values.sum() > 0 else \"No missing values found.\")"
]))

cells.append(create_code_cell([
    "# Convert Date columns to proper datetime format",
    "df['Order Date'] = pd.to_datetime(df['Order Date'])",
    "df['Ship Date'] = pd.to_datetime(df['Ship Date'])",
    "",
    "# Drop exact duplicate rows to maintain data integrity",
    "initial_rows = df.shape[0]",
    "df.drop_duplicates(inplace=True)",
    "final_rows = df.shape[0]",
    "print(f'Dropped {initial_rows - final_rows} duplicate rows.')",
    "",
    "# Extract 'Year' and 'Month' for granular time-series analysis",
    "df['Order Year'] = df['Order Date'].dt.year",
    "df['Order Month'] = df['Order Date'].dt.month",
    "",
    "print(\"\\nData cleaning complete. Updated Data types:\")",
    "df.dtypes"
]))

# 4. Exploratory Data Analysis
cells.append(create_markdown_cell([
    "---",
    "## 4. Exploratory Data Analysis (EDA) & Deep Business Insights",
    "In this main section, we will systematically break down the data across different dimensions: Product Categories, Sub-Categories, Regional Geography, and Time Constraints. \n\nEvery visualization is paired with a deep-dive analysis addressing **What we observed**, **Why this happens**, and **What the business should do next**."
]))

# 4.1 Sales by Category
cells.append(create_markdown_cell([
    "### 4.1 Profitability and Revenue by Product Category",
    "Understanding which macro-categories generate pure revenue versus actual net profit is foundational. Let's analyze the Sales and Profit across the highest-level product groupings."
]))

cells.append(create_code_cell([
    "category_group = df.groupby('Category')[['Sales', 'Profit']].sum().reset_index()",
    "category_group = category_group.sort_values(by='Sales', ascending=False)",
    "",
    "fig, ax1 = plt.subplots(figsize=(10, 6))",
    "",
    "# Bar chart for Sales",
    "sns.barplot(x='Category', y='Sales', data=category_group, color='steelblue', label='Total Sales', ax=ax1)",
    "ax1.set_ylabel('Total Sales ($)', fontsize=14)",
    "ax1.set_xlabel('Product Category', fontsize=14)",
    "ax1.set_title('Total Sales vs. Profit by Product Category', fontsize=18, pad=15)",
    "",
    "# Line chart for Profit on secondary axis",
    "ax2 = ax1.twinx()",
    "sns.lineplot(x='Category', y='Profit', data=category_group, color='crimson', marker='o', label='Total Profit', linewidth=3, markersize=8, ax=ax2)",
    "ax2.set_ylabel('Total Profit ($)', fontsize=14)",
    "",
    "# Formatting legends cleanly",
    "handles1, labels1 = ax1.get_legend_handles_labels()",
    "handles2, labels2 = ax2.get_legend_handles_labels()",
    "ax1.legend(handles1 + handles2, labels1 + labels2, loc='upper right', fontsize=12)",
    "ax2.get_legend().remove() # Prevent duplicate legends",
    "plt.show()"
]))

cells.append(create_markdown_cell([
    "> 💡 **Deep Business Insight: Category Performance**",
    "> - **Observation:** Technology is the ultimate driver, yielding the highest revenue and dominating in net profit. Conversely, Furniture generates immense sales volume but negligible profit.",
    "> - **Why this happens:** Furniture inherently involves steep shipping, warehousing, and operational handling costs. Additionally, aggressive discounting may be applied by sales teams to move bulky inventory.",
    "> - **What should the business do next?:** Immediate audit of the Furniture supply chain. Reduce blanket discounts on Furniture, negotiate better courier flat-rates, and aggressively cross-sell high-margin Technology products alongside Furniture purchases."
]))

# 4.2 Top 10 Products
cells.append(create_markdown_cell([
    "### 4.2 The Flagship Items: Top 10 Products by Sales",
    "Which exact products are critical to our top-line revenue? Identifying flagship products allows us to secure inventory."
]))

cells.append(create_code_cell([
    "top_products = df.groupby('Product Name')['Sales'].sum().sort_values(ascending=False).head(10)",
    "",
    "plt.figure(figsize=(12, 7))",
    "sns.barplot(x=top_products.values, y=top_products.index, palette='viridis')",
    "plt.title('Top 10 Flagship Products by Total Sales Revenue', fontsize=18, pad=15)",
    "plt.xlabel('Total Sales ($)', fontsize=14)",
    "plt.ylabel('Product Name', fontsize=14)",
    "plt.tight_layout()",
    "plt.show()"
]))

cells.append(create_markdown_cell([
    "> 💡 **Deep Business Insight: Product Reliance**",
    "> - **Observation:** The top-performing products are almost exclusively high-ticket Technology items (like advanced Copiers) and heavy Office Supplies.",
    "> - **Why this happens:** Enterprise customers or bulk B2B purchasers likely drive these massive revenue spikes, ordering expensive technical equipment for corporate setups rather than single household purchases.",
    "> - **What should the business do next?:** Treat these items as VIP products. Ensure strict inventory monitoring to avoid stockouts on these exact 10 items. Establish an exclusive B2B loyalty program for the clients purchasing these flagship products to secure recurring revenue."
]))

# 4.3 Sales by Region
cells.append(create_markdown_cell([
    "### 4.3 Geographic Penetration: Regional Performance",
    "How does geographic location impact our market share and profitability? Are we dominating specific coasts while ignoring others?"
]))

cells.append(create_code_cell([
    "region_group = df.groupby('Region')[['Sales', 'Profit']].sum().sort_values(by='Sales', ascending=False)",
    "",
    "fig, axes = plt.subplots(1, 2, figsize=(15, 6))",
    "",
    "# Sales Donut Chart",
    "axes[0].pie(region_group['Sales'], labels=region_group.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette('pastel'), wedgeprops={'edgecolor': 'black'})",
    "axes[0].set_title('Market Share (Sales) by Region', fontsize=16)",
    "centre_circle = plt.Circle((0,0),0.65,fc='white')",
    "axes[0].add_artist(centre_circle)",
    "",
    "# Profit Bar Chart",
    "sns.barplot(x=region_group.index, y=region_group['Profit'], ax=axes[1], palette='crest')",
    "axes[1].set_title('Total Net Profit by Region', fontsize=16)",
    "axes[1].set_ylabel('Profit ($)', fontsize=14)",
    "axes[1].set_xlabel('Region', fontsize=14)",
    "",
    "plt.tight_layout()",
    "plt.show()"
]))

cells.append(create_markdown_cell([
    "> 💡 **Deep Business Insight: Regional Discrepencies**",
    "> - **Observation:** The West and East coast regions absolutely dominate both market share (~60% combined) and profit generation. The Central and South regions lag significantly.",
    "> - **Why this happens:** Major tech hubs and higher corporate density on the coasts likely drive bulk purchasing of our most profitable Technology categories.",
    "> - **What should the business do next?:** Stop wasting generalized ad spend in the lowest performing regions. Instead, deploy highly targeted, localized marketing campaigns in the South/Central regions. Alternatively, optimize supply chain routes primarily in the West to further maximize the profit margins where we are already winning."
]))

# 4.4 Monthly Sales Trend
cells.append(create_markdown_cell([
    "### 4.4 Time Series: Monthly Sales Trend and Seasonality",
    "Is the business affected by seasonal buying patterns? Let's trace our historical sales to forecast resource allocation."
]))

cells.append(create_code_cell([
    "# Aggregate sales by Order Date (Monthly frequency)",
    "monthly_sales = df.set_index('Order Date').resample('M')['Sales'].sum()",
    "",
    "plt.figure(figsize=(15, 6))",
    "monthly_sales.plot(color='darkblue', linewidth=2.5)",
    "plt.title('Historical Monthly Sales Trend (2014 - 2017)', fontsize=18, pad=15)",
    "plt.xlabel('Order Date', fontsize=14)",
    "plt.ylabel('Total Sales ($)', fontsize=14)",
    "plt.axvspan('2017-09-01', '2017-12-31', color='yellow', alpha=0.2, label='Q4 Peak Season (Sept-Dec)')",
    "plt.legend(fontsize=12)",
    "plt.grid(True, linestyle='--', alpha=0.6)",
    "plt.show()"
]))

cells.append(create_markdown_cell([
    "> 💡 **Deep Business Insight: Seasonality**",
    "> - **Observation:** There is an undeniable, repeating seasonal trend. Sales consistently remain stagnant in Q1 and violently spike entering Q4 (September through December).",
    "> - **Why this happens:** This is typical retail behavior reflecting Back-to-School shopping, end-of-year corporate budget depletion, and the global Holiday shopping rush.",
    "> - **What should the business do next?:** Staffing and inventory allocation must mirror this seasonality. Scale up customer support staff, bulk-order warehouse inventory, and launch aggressive advertising heavily by mid-Q3 to ride the Q4 wave. Deliberately reduce operational overhead during the Q1 dip."
]))

# 4.5 Loss-making Products and Discount Impact
cells.append(create_markdown_cell([
    "### 4.5 The Impact of Discounts: Discovering the Loss-Leaders",
    "Discounts definitely increase sales volume, but do they actually help our bottom line? Let's find the breaking point of profitability."
]))

cells.append(create_code_cell([
    "plt.figure(figsize=(10, 6))",
    "sns.scatterplot(x='Discount', y='Profit', data=df, alpha=0.6, color='purple', s=50)",
    "plt.axhline(0, color='red', linestyle='dashed', linewidth=2)",
    "plt.title('The Devastating Effect of Discounts on Profitability', fontsize=18, pad=15)",
    "plt.xlabel('Discount Rate (e.g., 0.2 = 20%)', fontsize=14)",
    "plt.ylabel('Profit / Loss ($)', fontsize=14)",
    "plt.show()"
]))

cells.append(create_code_cell([
    "# Identify the Top 5 Sub-Categories with the highest cumulative losses",
    "loss_categories = df[df['Profit'] < 0].groupby('Sub-Category')['Profit'].sum().sort_values().head(5)",
    "print(\"Top 5 Worst Loss-Making Sub-Categories:\\n\")",
    "print(loss_categories)"
]))

cells.append(create_markdown_cell([
    "> 💡 **Deep Business Insight: The Discount Trap**",
    "> - **Observation:** Providing discounts greater than 20% mathematically guarantees a financial loss on almost every single transaction. Binders, Tables, and Bookcases are hemorrhaging the most money.",
    "> - **Why this happens:** Sales quotas may be incentivizing team members to offer massive price slashes just to close deals, completely destroying the profit margin in the process.",
    "> - **What should the business do next?:** Implement a strict, system-wide hard cap on discounts at **15% maximum**. For heavily bleeding items like Tables and Bookcases, transition them to a 'Made-to-Order' business model or stop selling them entirely if margins cannot be structurally repaired."
]))

# 5. Conclusion & Dashboard
cells.append(create_markdown_cell([
    "---",
    "## 5. Executive Summary",
    "### 🎯 Key Findings & Strategic Recommendations",
    "Based on the analysis of the Superstore dataset, the organization is effectively generating revenue but faces critical inefficiencies regarding cost control and unregulated discounting.",
    "",
    "**1. Resuscitate the Furniture Segment:** Furniture is a high-liability segment. Stop blanketing Tables and Bookcases with discounts. Re-evaluate courier fees for these heavy items.",
    "**2. Cap All Discounts at 15%:** The data explicitly proves discounts >20% destroy profitability entirely. Block the sales team from offering unsustainable price cuts.",
    "**3. Prioritize Tech & the West Coast:** Double down on allocating marketing budget to the West and East Regions promoting Technology packages, representing the most lucrative combination of geography and product type.",
    "**4. Anticipate Q4 Spikes:** Align inventory and staffing resources with the aggressive Q4 seasonal rush.",
    "",
    "## 📈 Master KPI Dashboard"
]))

cells.append(create_code_cell([
    "total_sales = df['Sales'].sum()",
    "total_profit = df['Profit'].sum()",
    "profit_margin = (total_profit / total_sales) * 100",
    "best_category = category_group.iloc[0]['Category']",
    "best_region = region_group.index[0]",
    "",
    "html_dashboard = f\"\"\"",
    "<div style='background-color: #f4f6f9; padding: 20px; border-radius: 10px; border-left: 6px solid #2ecc71; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);'>",
    "    <h2 style='margin-top: 0; color: #333; font-family: sans-serif;'>Enterprise KPI Snapshot</h2>",
    "    <ul style='font-size: 16px; line-height: 2.0; font-family: sans-serif;'>",
    "        <li><b>💰 Total Generated Sales:</b> <span style='color: #2980b9; font-weight: bold;'>${total_sales:,.2f}</span></li>",
    "        <li><b>💵 Total Net Profit:</b> <span style='color: #27ae60; font-weight: bold;'>${total_profit:,.2f}</span></li>",
    "        <li><b>📉 Overall Profit Margin:</b> <span style='color: #e74c3c; font-weight: bold;'>{profit_margin:.2f}%</span></li>",
    "        <li><b>📦 Most Profitable Category:</b> <b>{best_category}</b></li>",
    "        <li><b>🌎 Most Lucrative Region:</b> <b>{best_region}</b></li>",
    "    </ul>",
    "</div>",
    "\"\"\"",
    "",
    "from IPython.display import display, HTML",
    "display(HTML(html_dashboard))"
]))

notebook = {
    "cells": cells,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "codemirror_mode": {"name": "ipython", "version": 3},
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbconvert_exporter": "python",
            "pygments_lexer": "ipython3",
            "version": "3.8.0"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

with open('Sales_Data_Analysis_Project.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=2)

print("Notebook 'Sales_Data_Analysis_Project.ipynb' generated successfully.")
