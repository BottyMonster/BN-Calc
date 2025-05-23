import streamlit as st
import pandas as pd

# Page setup
st.set_page_config(page_title="Battle Nexus Discount Calculator", layout="wide")
st.title("🛠️ Battle Nexus Discount Calculator")

st.markdown("""Upload a CSV file or manually enter product data. Then edit or delete items, calculate discounts, track stock, and include VAT if required.

**CSV Format Required:**
- Product Name
- Retail Price (£)
- Discount %
- Cost Price (£)
- Stock Qty
""")

# Initialize session state
if 'products' not in st.session_state:
    st.session_state.products = []

# VAT toggle
include_vat = st.toggle("Include VAT in Calculations (20%)", value=True)
vat_rate = 0.20

# CSV Upload
uploaded_file = st.file_uploader("📤 Upload your CSV file here (optional)", type=["csv"])
if uploaded_file:
    try:
        df_upload = pd.read_csv(uploaded_file)
        expected_cols = {"Product Name", "Retail Price (£)", "Discount %", "Cost Price (£)", "Stock Qty"}
        if not expected_cols.issubset(df_upload.columns):
            st.error("CSV is missing one or more required columns.")
        else:
            st.session_state.products.extend(df_upload.to_dict(orient="records"))
    except Exception as e:
        st.error(f"Error processing file: {e}")

# Manual Entry
st.markdown("### ➕ Manually Add Product")
with st.form("manual_entry", clear_on_submit=True):
    name = st.text_input("Product Name")
    retail = st.number_input("Retail Price (£)", min_value=0.0, step=0.01)
    discount = st.number_input("Discount %", min_value=0.0, max_value=100.0, step=0.1)
    cost = st.number_input("Cost Price (£)", min_value=0.0, step=0.01)
    stock = st.number_input("Stock Qty", min_value=0, step=1)
    submitted = st.form_submit_button("Add Product")
    if submitted:
        st.session_state.products.append({
            "Product Name": name,
            "Retail Price (£)": retail,
            "Discount %": discount,
            "Cost Price (£)": cost,
            "Stock Qty": stock
        })

# Editable table with delete buttons
if st.session_state.products:
    st.markdown("### ✏️ Edit or Delete Products")
    edited_products = []
    for i, item in enumerate(st.session_state.products):
        cols = st.columns([3, 2, 2, 2, 2, 1])
        with cols[0]:
            item["Product Name"] = st.text_input(f"Product Name {i}", value=item["Product Name"], key=f"name_{i}")
        with cols[1]:
            item["Retail Price (£)"] = st.number_input(f"Retail Price {i}", value=float(item["Retail Price (£)"]), key=f"retail_{i}")
        with cols[2]:
            item["Discount %"] = st.number_input(f"Discount % {i}", value=float(item["Discount %"]), key=f"discount_{i}")
        with cols[3]:
            item["Cost Price (£)"] = st.number_input(f"Cost Price {i}", value=float(item["Cost Price (£)"]), key=f"cost_{i}")
        with cols[4]:
            item["Stock Qty"] = st.number_input(f"Stock Qty {i}", value=int(item.get("Stock Qty", 0)), step=1, key=f"stock_{i}")
        with cols[5]:
            if st.button("❌", key=f"delete_{i}"):
                continue
        edited_products.append(item)

    st.session_state.products = edited_products

    # Calculations
    df = pd.DataFrame(st.session_state.products)
    df["Final Retail (£)"] = df["Retail Price (£)"] * (1 + vat_rate) if include_vat else df["Retail Price (£)"]
    df["Discounted Price (£)"] = df["Final Retail (£)"] * (1 - df["Discount %"] / 100)
    df["Profit (£)"] = df["Discounted Price (£)"] - df["Cost Price (£)"]
    df["Margin %"] = (df["Profit (£)"] / df["Discounted Price (£)"]) * 100
    df = df.round(2)

    st.markdown("### 📦 Final Calculated Results with Stock")
    st.dataframe(df, use_container_width=True)

    # Download CSV
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Results as CSV",
        data=csv,
        file_name='discount_calculations_with_stock.csv',
        mime='text/csv',
    )

st.markdown("---")
st.caption("Built for Battle Nexus • Stock Tracking, VAT, Edit & Delete Enabled")
