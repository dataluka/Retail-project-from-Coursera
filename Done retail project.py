#!/usr/bin/env python
# coding: utf-8

# In[22]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

df = pd.read_csv('retail.csv')
print('Dataset Overview:')
print(df.head())
# Display basic information about the dataset
print('Dataset Info:')
print(df.info())

# Display basic statistics
print('Basic Statistics:')
print(df.describe())

# Check for missing values
print('Missing Values:')
print(df.isnull().sum())

# Save the outputs
print('Analysis completed.')



# In[23]:


# Remove rows with missing descriptions
df = df.dropna(subset=['Description'])

# Remove rows with negative quantities or prices
df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)]

# Create a TotalAmount column
df['TotalAmount'] = df['Quantity'] * df['UnitPrice']

# Display the cleaned dataset info
print("Cleaned Dataset Info:")
print(df.info())

# Display basic statistics of the cleaned dataset
print("\nCleaned Dataset Statistics:")
print(df.describe())

# Save the cleaned dataset
df.to_csv('cleaned_online_retail.csv', index=False)
print("\nCleaned dataset saved as 'cleaned_online_retail.csv'")


# In[25]:


# Visualize the distribution of TotalAmount

sns.histplot(df['TotalAmount'], bins=50, kde=True)
plt.figure(figsize=(10,6))
plt.title('Distribution of Total Amount')
plt.xlabel('Total Amount')
plt.ylabel('Frequency')
plt.savefig('total_amount_distribution.png')
plt.close()

print("Total Amount distribution plot saved as 'total_amount_distribution.png'")


# In[27]:


# Analyze sales trends over time
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
df['Month'] = df['InvoiceDate'].dt.to_period('M')
monthly_sales = df.groupby('Month')['TotalAmount'].sum().reset_index()
monthly_sales['Month'] = monthly_sales['Month'].astype(str)

plt.figure(figsize=(12,6))
plt.plot(monthly_sales['Month'], monthly_sales['TotalAmount'])
plt.title('Monthly Sales Trend')
plt.xlabel('Month')
plt.ylabel('Total Sales Amount')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('monthly_sales_trend.png')
plt.show()
plt.close()

print("Monthly sales trend plot saved as 'monthly_sales_trend.png'")

print("Analysis completed.")


# In[33]:


# Group by StockCode and Description, calculate total quantity and revenue
product_analysis = df.groupby(['StockCode', 'Description']).agg({
    'Quantity': 'sum',
    'TotalAmount': 'sum'
}).reset_index()

# Sort by total revenue (TotalAmount) in descending order
product_analysis = product_analysis.sort_values('TotalAmount', ascending=False)

# Display top 10 products
print("Top 10 Products by Revenue:")
print(product_analysis.head(10))

# Calculate percentage of total revenue
total_revenue = product_analysis['TotalAmount'].sum()
product_analysis['Revenue_Percentage'] = (product_analysis['TotalAmount'] / total_revenue) * 100

# Display top 10 products with revenue percentage
print("\nTop 10 Products by Revenue (with percentage):")
print(product_analysis[['StockCode', 'Description', 'TotalAmount', 'Revenue_Percentage']].head(10))

# Visualize top 10 products by revenue
plt.figure(figsize=(12, 6))
sns.barplot(x='TotalAmount', y='Description', data=product_analysis.head(10))
plt.title('Top 10 Products by Revenue')
plt.xlabel('Total Revenue')
plt.tight_layout()
plt.savefig('top_10_products_revenue.png')
plt.show()
plt.close()

print("Top 10 products by revenue plot saved as 'top_10_products_revenue.png'")


# In[38]:


# Group by Country and calculate total sales
sales_by_country = df.groupby('Country')['TotalAmount'].sum().sort_values(ascending=False)

# Create a bar plot for sales by country
plt.figure(figsize=(12, 6))
sales_by_country.plot(kind='bar')
plt.title('Total Sales by Country')
plt.xlabel('Country')
plt.ylabel('Total Sales')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('sales_by_country.png')
plt.show()
plt.close()

print("Sales by country plot saved as 'sales_by_country.png'")


# In[36]:


# Analyze product distribution across top 5 countries
top_5_countries = sales_by_country.head(5).index.tolist()
# Group by Country and StockCode, calculate total sales
product_sales_by_country = df[df['Country'].isin(top_5_countries)].groupby(['Country', 'StockCode', 'Description'])['TotalAmount'].sum().reset_index()

# Get top 5 products for each country
top_products_by_country = product_sales_by_country.groupby('Country').apply(lambda x: x.nlargest(5, 'TotalAmount')).reset_index(drop=True)

# Create a grouped bar plot for top products in each country
plt.figure(figsize=(15, 10))
sns.barplot(x='Country', y='TotalAmount', hue='Description', data=top_products_by_country)
plt.title('Top 5 Products by Sales in Top 5 Countries')
plt.xlabel('Country')
plt.ylabel('Total Sales')
plt.xticks(rotation=45, ha='right')
plt.legend(title='Product', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('top_products_by_country.png')
plt.show()
plt.close()

print("Top products by country plot saved as 'top_products_by_country.png'")


# In[ ]:




