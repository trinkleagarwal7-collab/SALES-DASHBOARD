import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

random.seed(42)
np.random.seed(42)

regions = ["North", "South", "East", "West", "Central"]
categories = ["Electronics", "Clothing", "Home & Kitchen", "Sports", "Books"]
products_by_cat = {
    "Electronics": ["Wireless Earbuds", "Smartphone", "Laptop", "Smartwatch", "Bluetooth Speaker"],
    "Clothing": ["T-Shirt", "Jeans", "Jacket", "Sneakers", "Cap"],
    "Home & Kitchen": ["Blender", "Coffee Maker", "Vacuum Cleaner", "Air Fryer", "Cookware Set"],
    "Sports": ["Yoga Mat", "Dumbbells", "Running Shoes", "Cricket Bat", "Football"],
    "Books": ["Fiction Novel", "Self-Help Book", "Cookbook", "Biography", "Comic Book"]
}

positive_reviews = [
    "Absolutely love this product, works perfectly!",
    "Great quality and fast delivery, highly recommend.",
    "Exceeded my expectations, will buy again.",
    "Excellent value for money, very satisfied.",
    "This is amazing, exactly what I needed.",
    "Superb build quality, very happy with the purchase.",
    "Fantastic experience, product is top notch.",
    "Really impressed with the performance and design."
]
neutral_reviews = [
    "It's okay, does the job as expected.",
    "Average product, nothing special about it.",
    "Decent quality for the price, acceptable.",
    "Works fine, but packaging could be better.",
    "It is what it is, meets basic requirements.",
]
negative_reviews = [
    "Very disappointed, product broke within a week.",
    "Poor quality, would not recommend this to anyone.",
    "Terrible experience, delivery was delayed a lot.",
    "Not worth the money, quality is really bad.",
    "Product stopped working after two days, frustrating.",
    "Bad customer service and defective item received."
]

def random_date(start, end):
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days))

start_date = datetime(2024, 1, 1)
end_date = datetime(2025, 12, 31)

rows = []
for i in range(1500):
    category = random.choice(categories)
    product = random.choice(products_by_cat[category])
    region = random.choice(regions)
    date = random_date(start_date, end_date)
    quantity = random.randint(1, 20)
    unit_price = round(random.uniform(10, 500), 2)
    sales = round(quantity * unit_price, 2)

    sentiment_type = random.choices(
        ["positive", "neutral", "negative"], weights=[0.55, 0.25, 0.20]
    )[0]
    if sentiment_type == "positive":
        review = random.choice(positive_reviews)
    elif sentiment_type == "neutral":
        review = random.choice(neutral_reviews)
    else:
        review = random.choice(negative_reviews)

    rows.append({
        "Order_ID": f"ORD{1000+i}",
        "Date": date.strftime("%Y-%m-%d"),
        "Region": region,
        "Category": category,
        "Product": product,
        "Quantity": quantity,
        "Unit_Price": unit_price,
        "Sales": sales,
        "Customer_Review": review
    })

df = pd.DataFrame(rows)
df.sort_values("Date", inplace=True)
df.to_csv("data/sales_data.csv", index=False)
print("Generated", len(df), "rows")
print(df.head())
