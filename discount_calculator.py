import streamlit as st

# Page settings
st.set_page_config(page_title="Battle Nexus Discount Calculator", layout="wide")

# Title
st.title("🛠️ Battle Nexus Discount Calculator")

st.markdown("""
Use this tool to calculate your discounted prices and profit margins in real-time.
Enter your retail price, desired discount percentage, and cost price to see the results instantly.
""")

# Editable input table
st.markdown("### 📦 Product Discount Table")
data = st.data_editor(pd.DataFrame({
    "Product Name": ["Example Product"],
    "Retail Price (£)": [100.00],
    "Discount %": [10],
    "Cost Price (£)": [60.00],
}), num_rows="dynamic", use_container_width=True)

# Perform calculations if table is not empty
if not data.empty:
    data["Discounted Price (£)"] = data["Retail Price (£)"] * (1 - data["Discount %"] / 100)
    data["Profit (£)"] = data["Discounted Price (£)"] - data["Cost Price (£)"]
    data["Margin %"] = (data["Profit (£)"] / data["Discounted Price (£)"]) * 100
    data["Discounted Price (£)"] = data["Discounted Price (£)"].round(2)
    data["Profit (£)"] = data["Profit (£)"].round(2)
    data["Margin %"] = data["Margin %"].round(2)

    st.markdown("### 💰 Calculated Results")
    st.dataframe(data, use_container_width=True)

# Export to CSV
csv = data.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Download Results as CSV",
    data=csv,
    file_name='discount_calculations.csv',
    mime='text/csv',
)

st.markdown("---")
st.caption("Built for Battle Nexus • Streamlit-powered discount tool")
