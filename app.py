"""
Sales Dashboard with Sentiment Analysis
----------------------------------------
A Streamlit + Plotly dashboard for exploring sales data, with TextBlob-powered
sentiment analysis on customer reviews.

Run with:  streamlit run app.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from textblob import TextBlob

# ----------------------------------------------------------------------------
# Page configuration
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------------------------------------------------------
# Data loading & caching
# ----------------------------------------------------------------------------
@st.cache_data
def load_data(path: str = "data/sales_data.csv") -> pd.DataFrame:
    df = pd.read_csv(path)
    df["Date"] = pd.to_datetime(df["Date"])
    df["Month"] = df["Date"].dt.to_period("M").astype(str)
    return df


@st.cache_data
def add_sentiment(df: pd.DataFrame) -> pd.DataFrame:
    """Add TextBlob sentiment polarity/subjectivity + label to each review."""
    df = df.copy()

    def get_polarity(text):
        return TextBlob(str(text)).sentiment.polarity

    def get_subjectivity(text):
        return TextBlob(str(text)).sentiment.subjectivity

    def label(polarity):
        if polarity > 0.1:
            return "Positive"
        elif polarity < -0.1:
            return "Negative"
        return "Neutral"

    df["Polarity"] = df["Customer_Review"].apply(get_polarity)
    df["Subjectivity"] = df["Customer_Review"].apply(get_subjectivity)
    df["Sentiment"] = df["Polarity"].apply(label)
    return df


df_raw = load_data()
df = add_sentiment(df_raw)

# ----------------------------------------------------------------------------
# Sidebar filters
# ----------------------------------------------------------------------------
st.sidebar.header("🔎 Filters")

min_date, max_date = df["Date"].min(), df["Date"].max()
date_range = st.sidebar.date_input(
    "Date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

regions = st.sidebar.multiselect(
    "Region", options=sorted(df["Region"].unique()), default=sorted(df["Region"].unique())
)
categories = st.sidebar.multiselect(
    "Category", options=sorted(df["Category"].unique()), default=sorted(df["Category"].unique())
)
sentiments = st.sidebar.multiselect(
    "Review Sentiment",
    options=["Positive", "Neutral", "Negative"],
    default=["Positive", "Neutral", "Negative"],
)

# Apply filters
if len(date_range) == 2:
    start, end = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    mask = (df["Date"] >= start) & (df["Date"] <= end)
else:
    mask = pd.Series(True, index=df.index)

mask &= df["Region"].isin(regions)
mask &= df["Category"].isin(categories)
mask &= df["Sentiment"].isin(sentiments)

fdf = df[mask]

st.sidebar.markdown("---")
st.sidebar.caption(f"Showing **{len(fdf):,}** of **{len(df):,}** records")

# ----------------------------------------------------------------------------
# Header + KPIs
# ----------------------------------------------------------------------------
st.title("📊 Sales Performance Dashboard")
st.caption("Interactive sales analytics with TextBlob sentiment analysis on customer reviews")

if fdf.empty:
    st.warning("No data matches the selected filters. Please adjust filters in the sidebar.")
    st.stop()

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Sales", f"${fdf['Sales'].sum():,.0f}")
col2.metric("Total Orders", f"{len(fdf):,}")
col3.metric("Units Sold", f"{fdf['Quantity'].sum():,}")
col4.metric("Avg Order Value", f"${fdf['Sales'].mean():,.2f}")
avg_polarity = fdf["Polarity"].mean()
col5.metric("Avg Sentiment", f"{avg_polarity:+.2f}", help="TextBlob polarity: -1 (negative) to +1 (positive)")

st.markdown("---")

# ----------------------------------------------------------------------------
# Row 1: Sales trend + Sales by region
# ----------------------------------------------------------------------------
r1c1, r1c2 = st.columns((2, 1))

with r1c1:
    st.subheader("Sales Trend Over Time")
    monthly = fdf.groupby("Month", as_index=False)["Sales"].sum().sort_values("Month")
    fig_trend = px.line(
        monthly, x="Month", y="Sales", markers=True,
        template="plotly_white",
    )
    fig_trend.update_traces(line_color="#2E86DE", line_width=3)
    fig_trend.update_layout(margin=dict(t=10, b=10), height=380)
    st.plotly_chart(fig_trend, use_container_width=True)

with r1c2:
    st.subheader("Sales by Region")
    region_sales = fdf.groupby("Region", as_index=False)["Sales"].sum().sort_values("Sales", ascending=False)
    fig_region = px.pie(
        region_sales, names="Region", values="Sales", hole=0.45,
        template="plotly_white",
    )
    fig_region.update_layout(margin=dict(t=10, b=10), height=380)
    st.plotly_chart(fig_region, use_container_width=True)

# ----------------------------------------------------------------------------
# Row 2: Category performance + Top products
# ----------------------------------------------------------------------------
r2c1, r2c2 = st.columns(2)

with r2c1:
    st.subheader("Sales by Category")
    cat_sales = fdf.groupby("Category", as_index=False)["Sales"].sum().sort_values("Sales", ascending=True)
    fig_cat = px.bar(
        cat_sales, x="Sales", y="Category", orientation="h",
        template="plotly_white", color="Sales", color_continuous_scale="Blues",
    )
    fig_cat.update_layout(margin=dict(t=10, b=10), height=380, coloraxis_showscale=False)
    st.plotly_chart(fig_cat, use_container_width=True)

with r2c2:
    st.subheader("Top 10 Products by Sales")
    top_products = (
        fdf.groupby("Product", as_index=False)["Sales"].sum()
        .sort_values("Sales", ascending=False).head(10)
    )
    fig_top = px.bar(
        top_products, x="Sales", y="Product", orientation="h",
        template="plotly_white", color="Sales", color_continuous_scale="Teal",
    )
    fig_top.update_layout(
        margin=dict(t=10, b=10), height=380,
        yaxis=dict(categoryorder="total ascending"), coloraxis_showscale=False,
    )
    st.plotly_chart(fig_top, use_container_width=True)

st.markdown("---")

# ----------------------------------------------------------------------------
# Row 3: Sentiment analysis section
# ----------------------------------------------------------------------------
st.header("💬 Customer Review Sentiment Analysis")
st.caption("Sentiment computed with TextBlob (polarity + subjectivity) on the `Customer_Review` column")

s1, s2, s3 = st.columns((1, 1, 1.4))

with s1:
    st.subheader("Sentiment Distribution")
    sent_counts = fdf["Sentiment"].value_counts().reindex(["Positive", "Neutral", "Negative"]).fillna(0)
    fig_sent = px.bar(
        x=sent_counts.index, y=sent_counts.values,
        color=sent_counts.index,
        color_discrete_map={"Positive": "#2ecc71", "Neutral": "#f1c40f", "Negative": "#e74c3c"},
        template="plotly_white",
        labels={"x": "Sentiment", "y": "Number of Reviews"},
    )
    fig_sent.update_layout(margin=dict(t=10, b=10), height=350, showlegend=False)
    st.plotly_chart(fig_sent, use_container_width=True)

with s2:
    st.subheader("Sentiment by Category")
    sent_by_cat = fdf.groupby(["Category", "Sentiment"]).size().reset_index(name="Count")
    fig_sbc = px.bar(
        sent_by_cat, x="Category", y="Count", color="Sentiment",
        color_discrete_map={"Positive": "#2ecc71", "Neutral": "#f1c40f", "Negative": "#e74c3c"},
        template="plotly_white", barmode="stack",
    )
    fig_sbc.update_layout(margin=dict(t=10, b=10), height=350, xaxis_tickangle=-30)
    st.plotly_chart(fig_sbc, use_container_width=True)

with s3:
    st.subheader("Polarity vs Subjectivity")
    fig_scatter = px.scatter(
        fdf, x="Polarity", y="Subjectivity", color="Sentiment",
        color_discrete_map={"Positive": "#2ecc71", "Neutral": "#f1c40f", "Negative": "#e74c3c"},
        hover_data=["Product", "Region"],
        template="plotly_white",
    )
    fig_scatter.update_layout(margin=dict(t=10, b=10), height=350)
    st.plotly_chart(fig_scatter, use_container_width=True)

# ----------------------------------------------------------------------------
# Row 4: Live sentiment tester
# ----------------------------------------------------------------------------
st.subheader("🧪 Try It Yourself: Analyze Custom Text")
user_text = st.text_area(
    "Enter a review or any text to analyze its sentiment:",
    placeholder="Type something like: 'The product quality was amazing and delivery was fast!'",
)
if user_text.strip():
    blob = TextBlob(user_text)
    pol = blob.sentiment.polarity
    subj = blob.sentiment.subjectivity
    label = "Positive 😊" if pol > 0.1 else ("Negative 😞" if pol < -0.1 else "Neutral 😐")
    c1, c2, c3 = st.columns(3)
    c1.metric("Sentiment", label)
    c2.metric("Polarity", f"{pol:+.3f}")
    c3.metric("Subjectivity", f"{subj:.3f}")

st.markdown("---")

# ----------------------------------------------------------------------------
# Row 5: Data table
# ----------------------------------------------------------------------------
with st.expander("📄 View Filtered Raw Data"):
    st.dataframe(
        fdf[[
            "Order_ID", "Date", "Region", "Category", "Product",
            "Quantity", "Unit_Price", "Sales", "Customer_Review",
            "Sentiment", "Polarity", "Subjectivity",
        ]].sort_values("Date", ascending=False),
        use_container_width=True,
        height=350,
    )
    st.download_button(
        "⬇️ Download filtered data as CSV",
        data=fdf.to_csv(index=False).encode("utf-8"),
        file_name="filtered_sales_data.csv",
        mime="text/csv",
    )

st.caption("Built with Streamlit, Plotly, and TextBlob")
