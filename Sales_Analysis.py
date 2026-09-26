import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Read the file
df = pd.read_csv('Sales_Data_project.csv')
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

# Display the first 5 rows
print(df.head())

# Display information about the dataset
print(df.info())
print(df.shape)
print(df.describe().T)

# Check if the DataFrame is empty
print(df.empty)

# Remove extra spaces and replace spaces with underscores in column names
df.columns = df.columns.str.strip().str.replace(' ', '_').str.capitalize()

# Clean text columns and handle missing values
Text_columns = ['Sales_rep', 'Region', 'Product_category',
                'Customer_type', 'Payment_method', 'Sales_channel']
for i in Text_columns:
    df[i] = df[i].astype(str).str.strip()
    df[i] = df[i].replace(('NAN', 'Nan', 'nan'), np.nan)
    df[i] = df[i].str.title()

# Handle the date column
df['Sales_date'] = pd.to_datetime(
    df['Sales_date'],
    format='%d/%m/%Y',
    errors='coerce'
)

df['Order_Month'] = df['Sales_date'].dt.to_period('M')

# create new column fro profit per unit
df['Profit_Per_unit'] = (df['Unit_price'] - df['Unit_cost'])
print(df['Profit_Per_unit'])

# create new column for total profit

df['Total_Profit'] = (df['Unit_price'] - df['Unit_cost'])*df['Quantity_sold']
print(df['Total_Profit'])

# Calculate Total sales
Total_sales = df['Total_sales_after_amount'].sum()
print(Total_sales)

Profit_Margin = ((df['Total_Profit'].sum() /
                 df['Total_sales_after_amount'].sum()) * 100).round(2)
print(Profit_Margin)
# Calculate monthly sales
Month_sales = df.groupby('Order_Month').agg(
    Sales=('Total_sales_after_amount', 'sum')
).reset_index()
print(Month_sales)

# Calculate the average order value
Avg_order_values = df['Total_sales_after_amount'].mean().round(2)
print(Avg_order_values)

# Calculate total sales and quantity by product category
Sales_by_Category = df.groupby('Product_category').agg(
    Total_sales=('Total_sales_after_amount', 'sum'),
    Total_Quantity=('Quantity_sold', 'sum')
).sort_values('Total_sales', ascending=False).reset_index()
print(Sales_by_Category)

# Calculate total sales and quantity by region
Sales_by_Region = df.groupby('Region').agg(
    Total_sales=('Total_sales_after_amount', 'sum'),
    Total_Quantity=('Quantity_sold', 'sum')
).sort_values('Total_sales', ascending=False).reset_index()
print(Sales_by_Region)

# Calculate total sales and quantity by region and product category
Sales_by_Region_and_Category = df.groupby(['Region', 'Product_category']).agg(
    Total_sales=('Total_sales_after_amount', 'sum'),
    Total_Quantity=('Quantity_sold', 'sum')
).sort_values('Total_sales', ascending=False).reset_index()
print(Sales_by_Region_and_Category)

# Calculate total sales and quantity by Sales rep
Sales_rep_performance = df.groupby('Sales_rep').agg(
    Total_Sold=('Total_sales_after_amount', 'sum'),
    Total_Quantity=('Quantity_sold', 'sum')
).sort_values('Total_Sold', ascending=False).reset_index()
print(Sales_rep_performance)

# Calculate total sales and quantity by region and Sales rep
Region_by_rep = df.groupby(['Region', 'Sales_rep']).agg(
    Total_Sold=('Total_sales_after_amount', 'sum'),
    Total_Quantity=('Quantity_sold', 'sum')
).sort_values('Total_Sold', ascending=False).reset_index()
print(Region_by_rep)

# Calculate total sales and quantity by Payment method
Sales_by_Payment_Method = df.groupby('Payment_method').agg(
    Total_Sold=('Total_sales_after_amount', 'sum'),
    Total_Quantity=('Quantity_sold', 'sum')
).sort_values('Total_Sold', ascending=False).reset_index()
print(Sales_by_Payment_Method)

# Calculate total sales  by Product category
Sales_by_category = df.groupby('Product_category')[
    'Total_sales_after_amount'].sum()

# Bar cart for Sales by category
plt.bar(Sales_by_category.index, Sales_by_category.values)
plt.xlabel('Category')
plt.ylabel('Total_Sales')
plt.title('Sales by category')
plt.show()

# Pie chart showing the percentage of orders by payment method
Order_count = df['Payment_method'].value_counts()
plt.pie(Order_count, labels=Order_count.index, autopct='%1.1f%%')
plt.title('Orders by Payment Method')
plt.show()

# save file after cleaning
# df.to_csv('Cleaning_Sales_Data.csv', index = False)
