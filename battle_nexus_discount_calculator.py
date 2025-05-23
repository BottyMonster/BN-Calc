st.set_page_config(page_title="Battle Nexus Discount Calculator", layout="centered")

st.title("🔫 Battle Nexus Discount Calculator")

# Input fields
original_price = st.number_input("Original Price (£)", min_value=0.0, step=0.01)
discount_percent = st.number_input("Discount Percentage (%)", min_value=0.0, max_value=100.0, step=0.1)
cost_price = st.number_input("Cost Price (£)", min_value=0.0, step=0.01)

# Calculations
discount_amount = (original_price * discount_percent) / 100
final_price = original_price - discount_amount
profit = final_price - cost_price
profit_margin = (profit / final_price) * 100 if final_price > 0 else 0

# Display results
st.markdown("---")
st.subheader("Results")
st.write(f"**Discount Amount:** £{discount_amount:.2f}")
st.write(f"**Final Price:** £{final_price:.2f}")
st.write(f"**Profit:** £{profit:.2f}")
st.write(f"**Profit Margin:** {profit_margin:.2f}%")

st.markdown("---")
st.info("Edit the values above to see live calculations. Built for Battle Nexus.")
