import streamlit as st
import pandas as pd

# Page settings
st.set_page_config(page_title="Battle Nexus Discount Calculator", layout="wide")
st.title("🛠️ Battle Nexus Discount Calculator with VAT")

st.markdown("""
Upload a CSV or manually enter product data. Calculate discounts, margins, and optionally include VAT.

**CSV Format Required:**
- Product Name
- Retail Price (£)
- Discount %
- Cost Price (£)
""")

# Session state initialization
if 'products' not in st.session_state:
    st.session_state.products = []

# VAT Toggle
include_vat = st.toggle("Include VAT in Calculations (20%)", value=True)
vat_rate = 0.20

# CSV Upload
uploaded_file = st.file_uploader("📤 Upload your CSV file here (optional)", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        expected_cols = {"Product Name", "Retail Price (£)", "Discount %", "Cost Price (£)"}
        if not expected_cols.issubset(set(df.columns)):
            st.error("CSV is missing one or more required columns.")
        else:
            st.markdown("### ✏️ Edit Uploaded Product Data")
            df = st.data_editor(df, num_rows="dynamic", use_container_width=True)
            st.session_state.products = df.to_dict(orient="records")
    except Exception as e:
        st.error(f"Error processing file: {e}")

# Manual Entry Form
st.markdown("### ➕ Add Product Manually")
with st.form("manual_entry", clear_on_submit=True):
    name = st.text_input("Product Name")
    retail = st.number_input("Retail Price (£)", min_value=0.0, step=0.01)
    discount = st.number_input("Discount %", min_value=0.0, max_value=100.0, step=0.1)
    cost = st.number_input("Cost Price (£)", min_value=0.0, step=0.01)
    submitted = st.form_submit_button("Add Product")
    if submitted:
        final_retail = retail * (1 + vat_rate) if include_vat else retail
        discounted = final_retail * (1 - discount / 100)
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
    st.markdown("### 💰 Final Calculated Results")
    df = pd.DataFrame(st.session_state.products)
    df["Final Retail (£)"] = df["Retail Price (£)"] * (1 + vat_rate) if include_vat else df["Retail Price (£)"]
    df["Discounted Price (£)"] = df["Final Retail (£)"] * (1 - df["Discount %"] / 100)
    df["Profit (£)"] = df["Discounted Price (£)"] - df["Cost Price (£)"]
    df["Margin %"] = (df["Profit (£)"] / df["Discounted Price (£)"]) * 100
    df = df.round(2)
    st.dataframe(df, use_container_width=True)

    # Export to CSV
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Results as CSV",
        data=csv,
        file_name='discount_calculations_with_vat.csv',
        mime='text/csv',
    )

st.markdown("---")
st.caption("Built for Battle Nexus • VAT Support Included")
