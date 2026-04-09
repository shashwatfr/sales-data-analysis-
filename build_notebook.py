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
    "**Dataset:** Superstore Sales Dataset  ",
    "**Objective:** Perform an end-to-end exploratory data analysis (EDA) to uncover business insights regarding sales, profit, and growth opportunities. The actionable insights presented here can help drive strategic business decisions."
]))

# 1. Environment Setup
cells.append(create_markdown_cell([
    "## 1. Environment Verification and Setup",
    "In this section, we import the necessary libraries required for data manipulation and visualization."
]))

cells.append(create_code_cell([
    "import pandas as pd",
    "import numpy as np",
    "import matplotlib.pyplot as plt",
    "import seaborn as sns",
    "import warnings",
    "",
    "# Suppress warnings for cleaner output",
    "warnings.filterwarnings('ignore')",
    "",
    "# Set visualization style for professional looking plots",
    "sns.set_theme(style='whitegrid')",
    "plt.rcParams['figure.figsize'] = (10, 6)"
]))

# 2. Data Loading and Understanding
cells.append(create_markdown_cell([
    "## 2. Data Loading and Initial Exploration",
    "We will load the Superstore Sales Dataset using pandas and display the first few rows to understand its structure."
]))

cells.append(create_code_cell([
    "url = 'https://raw.githubusercontent.com/leonism/sample-superstore/master/data/superstore.csv'",
    "try:",
    "    # Standard encoding might fail depending on the exact source, using latin1 is safe for this CSV",
    "    df = pd.read_csv(url, encoding='latin1')",
    "    print('Dataset loaded successfully!')",
    "except Exception as e:",
    "    print(f'Error loading dataset: {e}')"
]))

cells.append(create_code_cell([
    "# Displaying the first 5 records",
    "df.head()"
]))

cells.append(create_code_cell([
    "# Display dataset dimensions and column names",
    "print(f\"Dataset Shape: {df.shape[0]} rows and {df.shape[1]} columns.\")",
    "print(\"\\nColumn Names:\")",
    "print(df.columns.tolist())"
]))

cells.append(create_code_cell([
    "# Summary statistics for numerical columns",
    "df.describe()"
]))

cells.append(create_code_cell([
    "# Check for missing values in all columns",
    "df.isnull().sum()"
]))

# 3. Data Cleaning
cells.append(create_markdown_cell([
    "## 3. Data Cleaning",
    "A crucial step before analysis is ensuring the data is clean. We will:",
    "- Impute or remove missing values if any are found.",
    "- Convert date-related columns (`Order Date`, `Ship Date`) to reliable datetime objects.",
    "- Drop duplicate records to prevent skewed metrics.",
    "- Ensure appropriate data types for metric calculations."
]))

cells.append(create_code_cell([
    "# Convert Date columns to datetime format",
    "# Note: The dataset has M/D/YYYY format usually",
    "df['Order Date'] = pd.to_datetime(df['Order Date'])",
    "df['Ship Date'] = pd.to_datetime(df['Ship Date'])",
    "",
    "# Drop exact duplicate rows if any exist",
    "initial_rows = df.shape[0]",
    "df.drop_duplicates(inplace=True)",
    "final_rows = df.shape[0]",
    "print(f'Dropped {initial_rows - final_rows} duplicate rows.')",
    "",
    "# Extract 'Year' and 'Month' from 'Order Date' for time-series analysis later",
    "df['Order Year'] = df['Order Date'].dt.year",
    "df['Order Month'] = df['Order Date'].dt.month",
    "",
    "df.info()"
]))

# 4. Exploratory Data Analysis & Business Insights
cells.append(create_markdown_cell([
    "## 4. Exploratory Data Analysis (EDA) and Business Insights",
    "In this section, we systematically explore the relationships between sales, profit, product categories, and geographical regions. For each visualization, we will highlight key **Business Insights**."
]))

# 4.1 Sales by Category
cells.append(create_markdown_cell([
    "### 4.1 Sales & Profit by Category",
    "Let's see which main product categories drive the most revenue and profit."
]))

cells.append(create_code_cell([
    "category_group = df.groupby('Category')[['Sales', 'Profit']].sum().reset_index()",
    "category_group = category_group.sort_values(by='Sales', ascending=False)",
    "",
    "fig, ax1 = plt.subplots(figsize=(10, 6))",
    "",
    "sns.barplot(x='Category', y='Sales', data=category_group, color='skyblue', label='Sales', ax=ax1)",
    "ax1.set_ylabel('Total Sales ($)', fontsize=12)",
    "ax1.set_title('Total Sales & Profit by Product Category', fontsize=16)",
    "",
    "ax2 = ax1.twinx()",
    "sns.lineplot(x='Category', y='Profit', data=category_group, color='red', marker='o', label='Profit', linewidth=2, ax=ax2)",
    "ax2.set_ylabel('Total Profit ($)', fontsize=12)",
    "",
    "ax1.legend(loc='upper left')",
    "ax2.legend(loc='upper right')",
    "plt.show()"
]))

cells.append(create_markdown_cell([
    "> **Business Insight:** ",
    "> - **Technology** drives the highest revenue and also yields the most profit, indicating a strong margin and high demand for electronics/software.",
    "> - **Furniture**, while generating substantial sales, suffers from significantly lower profit margins. The business should investigate cost-cutting or pricing strategies in Furniture to improve overall profitability."
]))

# 4.2 Sales by Sub-Category
cells.append(create_markdown_cell([
    "### 4.2 Sales and Profit by Sub-Category",
    "To get a granular view, we dive into the specific sub-categories."
]))

cells.append(create_code_cell([
    "subcat_group = df.groupby('Sub-Category')[['Sales', 'Profit']].sum().sort_values(by='Sales', ascending=False)",
    "",
    "subcat_group.plot(kind='bar', figsize=(14, 7), color=['#1f77b4', '#ff7f0e'], edgecolor='black')",
    "plt.title('Total Sales & Profit by Sub-Category', fontsize=16)",
    "plt.xlabel('Sub-Category', fontsize=12)",
    "plt.ylabel('Amount ($)', fontsize=12)",
    "plt.axhline(0, color='black', linewidth=1)",
    "plt.xticks(rotation=45, ha='right')",
    "plt.tight_layout()",
    "plt.show()"
]))

cells.append(create_markdown_cell([
    "> **Business Insight:**",
    "> - **Phones and Chairs** are the top-selling sub-categories.",
    "> - **Copiers** show an exceptional profit margin despite not being the highest in total sales volume.",
    "> - Notably, **Tables** and **Bookcases** are operating at a net loss (negative profit) despite capturing significant sales. Discounting or high supply chain costs might be the root cause here."
]))

# 4.3 Sales by Region
cells.append(create_markdown_cell([
    "### 4.3 Regional Performance",
    "How does geographic location impact sales and profitability?"
]))

cells.append(create_code_cell([
    "region_group = df.groupby('Region')[['Sales', 'Profit']].sum().sort_values(by='Sales', ascending=False)",
    "",
    "fig, axes = plt.subplots(1, 2, figsize=(14, 6))",
    "",
    "# Sales Donut Chart",
    "axes[0].pie(region_group['Sales'], labels=region_group.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette('pastel'))",
    "axes[0].set_title('Sales Distribution by Region', fontsize=14)",
    "# Draw circle for donut",
    "centre_circle = plt.Circle((0,0),0.70,fc='white')",
    "fig = plt.gcf()",
    "fig.gca().add_artist(centre_circle)",
    "",
    "# Profit Bar Chart",
    "sns.barplot(x=region_group.index, y=region_group['Profit'], ax=axes[1], palette='viridis')",
    "axes[1].set_title('Total Profit by Region', fontsize=14)",
    "axes[1].set_ylabel('Profit ($)')",
    "",
    "plt.tight_layout()",
    "plt.show()"
]))

cells.append(create_markdown_cell([
    "> **Business Insight:**",
    "> - The **West region** is the top performer, leading in both total sales and profit. This could be due to a larger customer base or highly effective marketing.",
    "> - The **South region**, while having the lowest total sales proportion, still maintains a respectable profit margin.",
    "> - Resources could be heavily invested in the Central and South regions to unlock more market share."
]))

# 4.4 Monthly Sales Trend
cells.append(create_markdown_cell([
    "### 4.4 Time Series: Monthly Sales Trend",
    "Let's look at how sales fluctuate over time. Is there any seasonality?"
]))

cells.append(create_code_cell([
    "# Aggregate sales by Order Date (Monthly)",
    "monthly_sales = df.set_index('Order Date').resample('M')['Sales'].sum()",
    "",
    "plt.figure(figsize=(15, 6))",
    "monthly_sales.plot(color='darkblue', linewidth=2)",
    "plt.title('Monthly Sales Trend (2014 - 2017)', fontsize=16)",
    "plt.xlabel('Date', fontsize=12)",
    "plt.ylabel('Total Sales ($)', fontsize=12)",
    "plt.grid(True, linestyle='--', alpha=0.6)",
    "plt.show()"
]))

cells.append(create_markdown_cell([
    "> **Business Insight:**",
    "> - Sales exhibit clear **seasonality**, with consistent spikes occurring in Q4 (November and December). This is largely driven by holiday shopping and end-of-year corporate spending.",
    "> - There's a notable dip in the first quarter of every year, which is standard post-holiday behavior.",
    "> - **Strategy:** To maximize revenue during Q4 peaks, ensure inventory levels are well-stocked and logistics are robust by Q3."
]))

# 4.5 Top 10 Products by Sales
cells.append(create_markdown_cell([
    "### 4.5 Top 10 Products by Sales",
    "Which specific products are generating the most revenue for the Superstore?"
]))

cells.append(create_code_cell([
    "top_products = df.groupby('Product Name')['Sales'].sum().sort_values(ascending=False).head(10)",
    "",
    "plt.figure(figsize=(12, 6))",
    "sns.barplot(x=top_products.values, y=top_products.index, palette='crest')",
    "plt.title('Top 10 Products by Total Sales', fontsize=16)",
    "plt.xlabel('Total Sales ($)', fontsize=12)",
    "plt.ylabel('Product Name', fontsize=12)",
    "plt.show()"
]))

cells.append(create_markdown_cell([
    "> **Business Insight:**",
    "> - The top performing products are predominantly high-ticket Technology and Office Supplies items (like advanced Copiers and Machines).",
    "> - **Strategy:** Ensure these flagship products are always in stock, as their consistent availability is crucial for top-line revenue."
]))

# 4.6 Loss-making Products and Discount Impact
cells.append(create_markdown_cell([
    "### 4.6 Exploring Loss-Making Areas: The Impact of Discounts",
    "Why are some products losing money? Let's check the correlation between discounts offered and profit."
]))

cells.append(create_code_cell([
    "plt.figure(figsize=(10, 6))",
    "sns.scatterplot(x='Discount', y='Profit', data=df, alpha=0.5, color='purple')",
    "plt.axhline(0, color='red', linestyle='dashed')",
    "plt.title('Impact of Discounts on Profitability', fontsize=16)",
    "plt.xlabel('Discount Rate', fontsize=12)",
    "plt.ylabel('Profit ($)', fontsize=12)",
    "plt.show()"
]))

cells.append(create_code_cell([
    "# Let's identify the Top 10 products with the highest losses",
    "loss_products = df[df['Profit'] < 0].groupby('Product Name')['Profit'].sum().sort_values().head(10)",
    "print(\"Top 10 Loss-Making Products:\\n\")",
    "print(loss_products)"
]))

cells.append(create_markdown_cell([
    "> **Business Insight:**",
    "> - As observed from the scatter plot, higher **Discounts aggressively destroy Profit**. Almost all transactions with a discount above 0.2 (20%) generate negative profit.",
    "> - Frequent high discounts are likely the reason specific sub-categories like Tables and Bookcases are unprofitable.",
    "> - **Strategy:** Establish a strict ceiling on discount rates (e.g., maximum 15%). The business should avoid indiscriminate discounting and focus on value-based selling."
]))

# 5. Conclusion & Dashboard
cells.append(create_markdown_cell([
    "## 5. Executive Summary & KPI Dashboard",
    "Overall KPIs summarizing the dataset's footprint:"
]))

cells.append(create_code_cell([
    "total_sales = df['Sales'].sum()",
    "total_profit = df['Profit'].sum()",
    "profit_margin = (total_profit / total_sales) * 100",
    "best_category = category_group.iloc[0]['Category']",
    "best_region = region_group.index[0]",
    "",
    "markdown_dashboard = f\"\"\"",
    "### 📊 Final Dashboard Overview 📊",
    "",
    "- **Total Generated Sales:** ${total_sales:,.2f}",
    "- **Total Net Profit:** ${total_profit:,.2f}",
    "- **Overall Profit Margin:** {profit_margin:.2f}%",
    "- **Best Performing Category:** {best_category}",
    "- **Most Lucrative Region:** {best_region}",
    "\"\"\"",
    "",
    "from IPython.display import display, Markdown",
    "display(Markdown(markdown_dashboard))"
]))

cells.append(create_markdown_cell([
    "### Final Recommendations:",
    "1. **Optimize Furniture Pricing Strategy:** The furniture segment is bleeding profit despite decent sales volume. Stop applying steep discounts to Tables and Bookcases. Re-evaluate shipping or handling fees.",
    "2. **Double-Down on Technology & Copiers:** Leverage the high margins found in Copiers and Phones. Introduce bundles to push these high-profit items along with lower-performing segments.",
    "3. **Targeted Seasonal Marketing:** The holiday quarter is crucial. Prepare marketing campaigns early in Q3 to fully capture the inevitable spikes in November and December.",
    "4. **Rethink Discount Ceilings:** Implement a company-wide rule limiting standard discounts to 10-15%, as the data clearly shows that discounts beyond 20% severely cannibalize margins."
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
