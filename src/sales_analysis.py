import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings
warnings.filterwarnings('ignore')

def main():
    # Setup paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, 'dataset', 'superstore.csv')
    outputs_dir = os.path.join(base_dir, 'outputs')
    charts_dir = os.path.join(outputs_dir, 'charts')
    
    os.makedirs(charts_dir, exist_ok=True)
    
    # ---------------------------------------------------------
    # 1. Data Loading and Cleaning
    # ---------------------------------------------------------
    print("Loading data...")
    # Using 'latin1' encoding as superstore dataset often has special characters
    try:
        df = pd.read_csv(data_path, encoding='latin1')
    except Exception as e:
        print(f"Error loading data: {e}")
        return

    print("Cleaning data...")
    # Check missing values
    missing_values = df.isnull().sum()
    
    # Remove duplicates
    df.drop_duplicates(inplace=True)
    
    # Fix column names: strip whitespace, replace spaces with underscores, lowercase
    df.columns = df.columns.str.strip().str.replace(' ', '_').str.replace('-', '_').str.lower()
    
    # Convert date columns properly
    df['order_date'] = pd.to_datetime(df['order_date'], dayfirst=False, errors='coerce')
    df['ship_date'] = pd.to_datetime(df['ship_date'], dayfirst=False, errors='coerce')
    
    # Check outliers (Optional: we will just keep data as is for business context, 
    # but let's drop any rows with negative sales if they exist)
    df = df[df['sales'] > 0]
    
    # Save cleaned final dataset
    clean_data_path = os.path.join(outputs_dir, 'cleaned_data.csv')
    df.to_csv(clean_data_path, index=False)
    print(f"Cleaned dataset saved to {clean_data_path}")

    # ---------------------------------------------------------
    # 2. Exploratory Data Analysis (EDA) & Feature Engineering
    # ---------------------------------------------------------
    df['order_month'] = df['order_date'].dt.to_period('M').astype(str)
    df['order_year'] = df['order_date'].dt.year

    # Key Metrics
    total_sales = df['sales'].sum()
    total_profit = df['profit'].sum()
    total_orders = df['order_id'].nunique()
    total_quantity = df['quantity'].sum()
    avg_order_value = total_sales / total_orders

    insights = []
    insights.append("=========================================")
    insights.append("SALES PERFORMANCE ANALYTICS INSIGHTS")
    insights.append("=========================================\n")
    
    insights.append(f"OVERALL PERFORMANCE:")
    insights.append(f"- Total Sales: ${total_sales:,.2f}")
    insights.append(f"- Total Profit: ${total_profit:,.2f}")
    insights.append(f"- Total Orders: {total_orders:,}")
    insights.append(f"- Total Quantity Sold: {total_quantity:,}")
    insights.append(f"- Average Order Value: ${avg_order_value:,.2f}\n")

    # Set visualization style
    sns.set_theme(style="whitegrid", palette="muted")
    
    # ---------------------------------------------------------
    # 3. Create Professional Charts
    # ---------------------------------------------------------
    print("Generating charts...")

    # Chart 1: Monthly Sales Line Chart
    monthly_sales = df.groupby('order_month')['sales'].sum().reset_index()
    monthly_sales['order_month'] = pd.to_datetime(monthly_sales['order_month'])
    monthly_sales = monthly_sales.sort_values('order_month')
    
    plt.figure(figsize=(14, 6))
    sns.lineplot(data=monthly_sales, x='order_month', y='sales', marker='o', color='b', linewidth=2)
    plt.title('Monthly Sales Trend', fontsize=16)
    plt.xlabel('Month', fontsize=12)
    plt.ylabel('Total Sales ($)', fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(charts_dir, 'monthly_sales_trend.png'), dpi=300)
    plt.close()

    # Chart 2: Monthly Profit Line Chart
    monthly_profit = df.groupby('order_month')['profit'].sum().reset_index()
    monthly_profit['order_month'] = pd.to_datetime(monthly_profit['order_month'])
    monthly_profit = monthly_profit.sort_values('order_month')

    plt.figure(figsize=(14, 6))
    sns.lineplot(data=monthly_profit, x='order_month', y='profit', marker='o', color='g', linewidth=2)
    plt.title('Monthly Profit Trend', fontsize=16)
    plt.xlabel('Month', fontsize=12)
    plt.ylabel('Total Profit ($)', fontsize=12)
    plt.axhline(0, color='r', linestyle='--') # Add zero line for profit
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(charts_dir, 'monthly_profit_trend.png'), dpi=300)
    plt.close()

    # Chart 3: Top 10 Best Selling Products
    top_products = df.groupby('product_name')['sales'].sum().nlargest(10).reset_index()
    plt.figure(figsize=(12, 6))
    sns.barplot(data=top_products, x='sales', y='product_name', palette='viridis')
    plt.title('Top 10 Best Selling Products', fontsize=16)
    plt.xlabel('Total Sales ($)', fontsize=12)
    plt.ylabel('')
    plt.tight_layout()
    plt.savefig(os.path.join(charts_dir, 'top_10_products_sales.png'), dpi=300)
    plt.close()

    # Chart 4: Top 10 Profitable Products
    top_profit_products = df.groupby('product_name')['profit'].sum().nlargest(10).reset_index()
    plt.figure(figsize=(12, 6))
    sns.barplot(data=top_profit_products, x='profit', y='product_name', palette='crest')
    plt.title('Top 10 Most Profitable Products', fontsize=16)
    plt.xlabel('Total Profit ($)', fontsize=12)
    plt.ylabel('')
    plt.tight_layout()
    plt.savefig(os.path.join(charts_dir, 'top_10_profitable_products.png'), dpi=300)
    plt.close()
    
    # Loss Making Products (Insight)
    bottom_profit_products = df.groupby('product_name')['profit'].sum().nsmallest(5).reset_index()
    insights.append("PRODUCT INSIGHTS:")
    insights.append(f"- Best Selling Product: {top_products.iloc[0]['product_name']} (${top_products.iloc[0]['sales']:,.2f})")
    insights.append(f"- Most Profitable Product: {top_profit_products.iloc[0]['product_name']} (${top_profit_products.iloc[0]['profit']:,.2f})")
    insights.append(f"- Biggest Loss Making Product: {bottom_profit_products.iloc[0]['product_name']} (${bottom_profit_products.iloc[0]['profit']:,.2f})\n")

    # Chart 5: Category wise sales bar chart
    cat_sales = df.groupby('category')['sales'].sum().reset_index().sort_values('sales', ascending=False)
    plt.figure(figsize=(8, 5))
    sns.barplot(data=cat_sales, x='category', y='sales', palette='Set2')
    plt.title('Sales by Category', fontsize=16)
    plt.xlabel('Category', fontsize=12)
    plt.ylabel('Total Sales ($)', fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(charts_dir, 'category_sales.png'), dpi=300)
    plt.close()

    # Chart 6: Region wise sales bar chart
    region_sales = df.groupby('region')['sales'].sum().reset_index().sort_values('sales', ascending=False)
    plt.figure(figsize=(8, 5))
    sns.barplot(data=region_sales, x='region', y='sales', palette='magma')
    plt.title('Sales by Region', fontsize=16)
    plt.xlabel('Region', fontsize=12)
    plt.ylabel('Total Sales ($)', fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(charts_dir, 'region_sales.png'), dpi=300)
    plt.close()
    
    best_region = region_sales.iloc[0]
    insights.append("GEOGRAPHICAL INSIGHTS:")
    insights.append(f"- Best Performing Region: {best_region['region']} (${best_region['sales']:,.2f})\n")

    # Chart 7: Segment Pie Chart
    segment_sales = df.groupby('segment')['sales'].sum()
    plt.figure(figsize=(8, 8))
    plt.pie(segment_sales, labels=segment_sales.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'))
    plt.title('Sales Distribution by Customer Segment', fontsize=16)
    plt.tight_layout()
    plt.savefig(os.path.join(charts_dir, 'segment_sales_pie.png'), dpi=300)
    plt.close()
    
    best_segment = segment_sales.idxmax()
    insights.append("CUSTOMER INSIGHTS:")
    insights.append(f"- Maximum Revenue Generating Segment: {best_segment}\n")

    # Chart 8: Scatter plot discount vs profit
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='discount', y='profit', hue='category', alpha=0.6)
    plt.title('Discount vs Profit Analysis', fontsize=16)
    plt.xlabel('Discount', fontsize=12)
    plt.ylabel('Profit ($)', fontsize=12)
    plt.axhline(0, color='red', linestyle='--')
    plt.tight_layout()
    plt.savefig(os.path.join(charts_dir, 'discount_vs_profit.png'), dpi=300)
    plt.close()

    # Chart 9: Heatmap Correlation Chart
    # Select numeric columns only
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    # Drop irrelevant ids if any
    cols_to_drop = ['row_id'] if 'row_id' in numeric_cols else []
    if 'postal_code' in numeric_cols:
         cols_to_drop.append('postal_code')
    corr_data = df[numeric_cols].drop(columns=cols_to_drop, errors='ignore')
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(corr_data.corr(), annot=True, cmap='coolwarm', fmt='.2f', vmin=-1, vmax=1)
    plt.title('Correlation Heatmap', fontsize=16)
    plt.tight_layout()
    plt.savefig(os.path.join(charts_dir, 'correlation_heatmap.png'), dpi=300)
    plt.close()

    # Additional Business Insights Formulation
    insights.append("STRATEGIC RECOMMENDATIONS:")
    insights.append("- High discounts are severely hurting profitability, particularly in certain categories. We recommend capping discounts at 20%.")
    insights.append(f"- The {best_segment} segment is the most lucrative. Marketing efforts should prioritize this segment.")
    insights.append("- Consider discontinuing or re-evaluating the pricing strategy for the top loss-making products.")
    
    # Save insights to text file
    insights_path = os.path.join(outputs_dir, 'insights_report.txt')
    with open(insights_path, 'w') as f:
        f.write('\n'.join(insights))
    
    print(f"Insights report saved to {insights_path}")
    print("Execution completed successfully.")

if __name__ == "__main__":
    main()
