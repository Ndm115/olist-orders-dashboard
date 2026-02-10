import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


#Task 1:

#olist_orders_dataset contains information about the orders placed by customers, such as order_id, purchase timestamp, and delivery date.
order = pd.read_csv("C:\\Users\\User\\Downloads\\archive\\olist_orders_dataset.csv")
#olist_order_items_dataset contains details about the items purchased in each order, such as order_id, product_id, price, and freight value.
order_items = pd.read_csv("C:\\Users\\User\\Downloads\\archive\\olist_order_items_dataset.csv")

#This is where we merge the datasets
#order_id is present in both datasets, serving as common key to combining them
#how=inner ensures that only rows with matching order_id in both datasets are kept in the merged dataset.
combined_orders_dataset = pd.merge(order_items, order, on="order_id", how="inner")
print(combined_orders_dataset)


#Task 2:

combined_orders_dataset["order_purchase_timestamp"] = pd.to_datetime(combined_orders_dataset["order_purchase_timestamp"])
combined_orders_dataset["order_delivered_customer_date"] = pd.to_datetime(combined_orders_dataset["order_delivered_customer_date"])
#Delivery time calculated in days:
combined_orders_dataset['delivery_time_days'] = (combined_orders_dataset['order_delivered_customer_date'] - combined_orders_dataset['order_purchase_timestamp']).dt.days

plt.hist(combined_orders_dataset['delivery_time_days'].dropna(), bins=30, color='red', edgecolor = "yellow")
plt.title('Distribution of Delivery Times')
plt.xlabel('Delivery Time in days')
plt.ylabel('Number of Orders')
plt.grid(True)
plt.show()

#average:
average = combined_orders_dataset['delivery_time_days'].mean()
#min and max:
minimum = combined_orders_dataset['delivery_time_days'].min()
maximum = combined_orders_dataset['delivery_time_days'].max()
range = maximum - minimum
#outliers
outliers = combined_orders_dataset[combined_orders_dataset['delivery_time_days'] > 30]

print("The minimum is: ", minimum)
print("The maximum is: ", maximum)
print("The average delivery time is: ", average)
print("The range of data is: ", range)
print("The outliers are: ", outliers)

#Task 3:

top_products = combined_orders_dataset['product_id'].value_counts().head(10)
print("The top 10 most sold products:  \n", top_products)
plt.title("Top 10 most sold products")
plt.xlabel("Product ID")
plt.ylabel("Number of items sold")
colors = ["red", "blue", "red", "purple", "brown", "green", "black", "gold", "pink", "orange"]
top_products.plot(kind="bar", color=colors , edgecolor="red")
plt.show()

print("The top products are: ", top_products)

#Task 4:

combined_orders_dataset["total_revenue"] = (
    combined_orders_dataset["price"] + combined_orders_dataset["freight_value"]
)

seller_revenue = combined_orders_dataset.groupby("seller_id")["total_revenue"].sum().sort_values(ascending=False).head(10)

plt.title("Top 10 sellers")
plt.xlabel("Seller ID")
plt.ylabel("Total revenue")
seller_revenue.plot(kind="bar", color="gold", edgecolor="black")
plt.legend()
plt.show()

print("The seller revenue is: ", seller_revenue)

#Task 5:

combined_orders_dataset["order_purchase_month"] = combined_orders_dataset["order_purchase_timestamp"].dt.to_period("M")
monthly_revenue = combined_orders_dataset.groupby("order_purchase_month")["total_revenue"].sum()

plt.title("Monthly revenue trends")
plt.xlabel("Months")
plt.ylabel("Total revenue")
monthly_revenue.plot(marker="o", kind="line", color="red")
plt.grid(True)
plt.legend()
plt.show()

print("The monthly revenue is: ", monthly_revenue)