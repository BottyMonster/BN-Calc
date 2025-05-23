import streamlit as st
import pandas as pd

# Page settings
st.set_page_config(page_title="Battle Nexus Discount Calculator", layout="wide")

st.title("🛠️ Battle Nexus Discount Calculator")

st.markdown("""
Manually enter product details below to calculate the discount price and margin.
Use the 'Add Product' button to input multiple products.
""")

# Initialize session state for multiple entries
if 'products' not in st.session_state:
    st.session_state.products = []

# Add new product entry
with st.form("product_form", clear_on_submit=True):
    st.subheader("➕ Add New Product")
    name = st.text_input("Product Name")
    retail = st.number_input("Retail Price (£)", min_value=0.0, step=0.01)
    discount = st.number_input("Discount %", min_value=0.0, max_value=100.0, step=0.1)
    cost = st.number_input("Cost Price (£)", min_value=0.0, step=0.01)
    submitted = st.form_submit_button("Add Product")

    if submitted:
        discounted = retail * (1 - discount / 100)
        profit = discounted - cost
        margin = (profit / discounted) * 100 if discounted else 0
        st.session_state.products.append({
            "Product Name": name,
            "Retail Price (£)": retail,
            "Discount %": discount,
            "Cost Price (£)": cost,
            "Discounted Price (£)": round(discounted, 2),
            "Profit (£)": round(profit, 2),
            "Margin %": round(margin, 2)
        })

# Display results
if st.session_state.products:
    st.markdown("### 💰 Calculated Products")
    df = pd.DataFrame(st.session_state.products)
    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Results as CSV",
        data=csv,
        file_name='discount_calculations.csv',
        mime='text/csv',
    )

st.markdown("---")
st.caption("Built for Battle Nexus • Compatible with older Streamlit versions")

