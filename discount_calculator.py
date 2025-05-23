import streamlit as st
import pandas as pd

# Page settings
st.set_page_config(page_title="Battle Nexus Discount Calculator", layout="wide")

st.title("🛠️ Battle Nexus Discount Calculator")

st.markdown("""
Upload a CSV file with your product data, then edit values directly before downloading your results.

**CSV Format Expected:**
- Product Name
- Retail Price (£)
- Discount %
- Cost Price (£)
""")

uploaded_file = st.file_uploader("📤 Upload your CSV file here", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)

        # Ensure all required columns are present
        expected_cols = {"Product Name", "Retail Price (£)", "Discount %", "Cost Price (£)"}
        if not expected_cols.issubset(set(df.columns)):
            st.error("CSV is missing one or more required columns.")
        else:
            # Editable table
            st.markdown("### ✏️ Edit Product Data")
            edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)

            # Perform calculations
            edited_df["Discounted Price (£)"] = edited_df["Retail Price (£)"] * (1 - edited_df["Discount %"] / 100)
            edited_df["Profit (£)"] = edited_df["Discounted Price (£)"] - edited_df["Cost Price (£)"]
            edited_df["Margin %"] = (edited_df["Profit (£)"] / edited_df["Discounted Price (£)"]) * 100

            # Round values
            edited_df["Discounted Price (£)"] = edited_df["Discounted Price (£)"].round(2)
            edited_df["Profit (£)"] = edited_df["Profit (£)"].round(2)
            edited_df["Margin %"] = edited_df["Margin %"].round(2)

            st.markdown("### 💰 Final Calculated Results")
            st.dataframe(edited_df, use_container_width=True)

            # Download result
            csv = edited_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Final Results as CSV",
                data=csv,
                file_name='discount_calculations.csv',
                mime='text/csv',
            )
    except Exception as e:
        st.error(f"Error processing file: {e}")
else:
    st.info("Awaiting CSV upload to begin calculations.")

st.markdown("---")
st.caption("Built for Battle Nexus • Editable CSV version")
