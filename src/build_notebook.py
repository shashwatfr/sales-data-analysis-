import nbformat as nbf
import os

def create_notebook():
    nb = nbf.v4.new_notebook()
    
    cells = []
    
    # Title
    cells.append(nbf.v4.new_markdown_cell("# Sales Performance Analytics Dashboard\n\n## Project Overview\nThis notebook contains the complete Data Analysis workflow for the Superstore dataset. We will cover Data Cleaning, Exploratory Data Analysis (EDA), Data Visualization, and Business Insights Generation."))
    
    # Imports
    cells.append(nbf.v4.new_code_cell("import pandas as pd\nimport numpy as np\nimport matplotlib.pyplot as plt\nimport seaborn as sns\nimport warnings\nwarnings.filterwarnings('ignore')\n\n# Set plotting style\nsns.set_theme(style='whitegrid', palette='muted')"))
    
    # Load Data
    cells.append(nbf.v4.new_markdown_cell("### 1. Data Loading"))
    cells.append(nbf.v4.new_code_cell("# Load dataset\ndf = pd.read_csv('../dataset/superstore.csv', encoding='latin1')\ndf.head()"))
    
    # Data Cleaning
    cells.append(nbf.v4.new_markdown_cell("### 2. Data Cleaning\nHandling missing values, duplicates, column names, and data types."))
    cells.append(nbf.v4.new_code_cell("# Check missing values\nprint('Missing values before cleaning:\\n', df.isnull().sum())\n\n# Remove duplicates\ndf.drop_duplicates(inplace=True)\n\n# Fix column names\ndf.columns = df.columns.str.strip().str.replace(' ', '_').str.replace('-', '_').str.lower()\n\n# Date conversion\ndf['order_date'] = pd.to_datetime(df['order_date'], dayfirst=False, errors='coerce')\ndf['ship_date'] = pd.to_datetime(df['ship_date'], dayfirst=False, errors='coerce')\n\nprint('\\nData Types after conversion:\\n', df.dtypes)"))
    
    # EDA
    cells.append(nbf.v4.new_markdown_cell("### 3. Exploratory Data Analysis (EDA)\nExtracting total metrics."))
    cells.append(nbf.v4.new_code_cell("total_sales = df['sales'].sum()\ntotal_profit = df['profit'].sum()\ntotal_orders = df['order_id'].nunique()\n\nprint(f'Total Sales: ${total_sales:,.2f}')\nprint(f'Total Profit: ${total_profit:,.2f}')\nprint(f'Total Orders: {total_orders:,}')"))
    
    # Visualizations
    cells.append(nbf.v4.new_markdown_cell("### 4. Data Visualizations"))
    
    cells.append(nbf.v4.new_code_cell("df['order_month'] = df['order_date'].dt.to_period('M').astype(str)\nmonthly_sales = df.groupby('order_month')['sales'].sum().reset_index()\nmonthly_sales['order_month'] = pd.to_datetime(monthly_sales['order_month'])\nmonthly_sales = monthly_sales.sort_values('order_month')\n\nplt.figure(figsize=(14, 6))\nsns.lineplot(data=monthly_sales, x='order_month', y='sales', marker='o', color='b', linewidth=2)\nplt.title('Monthly Sales Trend', fontsize=16)\nplt.xlabel('Month', fontsize=12)\nplt.ylabel('Total Sales ($)', fontsize=12)\nplt.xticks(rotation=45)\nplt.show()"))
    
    cells.append(nbf.v4.new_code_cell("top_products = df.groupby('product_name')['sales'].sum().nlargest(10).reset_index()\nplt.figure(figsize=(12, 6))\nsns.barplot(data=top_products, x='sales', y='product_name', palette='viridis')\nplt.title('Top 10 Best Selling Products', fontsize=16)\nplt.show()"))

    cells.append(nbf.v4.new_code_cell("plt.figure(figsize=(10, 6))\nsns.scatterplot(data=df, x='discount', y='profit', hue='category', alpha=0.6)\nplt.title('Discount vs Profit Analysis', fontsize=16)\nplt.axhline(0, color='red', linestyle='--')\nplt.show()"))

    # Insights
    cells.append(nbf.v4.new_markdown_cell("### 5. Business Insights\n- **Discounting Strategy**: High discounts are severely hurting profit margins.\n- **Top Products**: A small segment of products generates the majority of sales.\n- **Recommendations**: Cap discounts on loss-making categories and focus marketing on the most profitable segments."))

    nb['cells'] = cells
    
    # Write notebook
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    nb_path = os.path.join(base_dir, 'notebooks', 'analysis.ipynb')
    with open(nb_path, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    
    print(f"Created notebook at {nb_path}")

if __name__ == "__main__":
    create_notebook()
