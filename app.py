import streamlit as st

from database import (
    initialize_database,
    save_purchase_order,
    get_purchase_order,
)

# Initialize database
initialize_database()

# Page configuration
st.set_page_config(
    page_title="SmartBuy AI",
    page_icon="🛒",
    layout="wide",
)

# Application heading
st.title("🛒 SmartBuy AI")
st.subheader("Intelligent Purchasing Agent")

st.write(
    "An AI purchasing agent that reviews recommendations, "
    "checks business constraints, and validates purchasing decisions."
)

st.divider()

# --------------------------------------------------
# SCENARIO 1: PURCHASE RECOMMENDATION REVIEW
# --------------------------------------------------

st.header("📦 Scenario 1: Purchase Recommendation Review")

st.info("The purchasing system recommends buying 800 units.")

# Sample purchasing information
recommended_qty = 800
current_inventory = 200
expected_demand = 400
incoming_orders = 100
supplier_minimum = 50
available_budget = 30000
available_storage = 500
unit_price = 40

# Display purchasing information
st.subheader("📊 Purchasing Information")

col1, col2, col3 = st.columns(3)

col1.metric("Recommended Purchase", f"{recommended_qty} units")
col2.metric("Current Inventory", f"{current_inventory} units")
col3.metric("Expected Demand", f"{expected_demand} units")

col4, col5, col6 = st.columns(3)

col4.metric("Incoming Orders", f"{incoming_orders} units")
col5.metric("Available Budget", f"₹{available_budget:,}")
col6.metric("Available Storage", f"{available_storage} units")

# --------------------------------------------------
# PURCHASING ANALYSIS
# --------------------------------------------------

st.divider()
st.header("🧠 Purchasing Decision")

required_qty = max(
    0,
    expected_demand - current_inventory - incoming_orders,
)

if required_qty > 0:
    required_qty = max(required_qty, supplier_minimum)

estimated_cost = required_qty * unit_price

# Store calculated analysis for use by other sections
issues = []

if estimated_cost > available_budget:
    issues.append("The purchase exceeds the available budget.")

if required_qty > available_storage:
    issues.append("The purchase exceeds available storage capacity.")

st.write(f"Recommended quantity: **{recommended_qty} units**")
st.write(f"Calculated purchase quantity: **{required_qty} units**")
st.write(f"Unit price: **₹{unit_price}**")
st.write(f"Estimated purchase cost: **₹{estimated_cost:,}**")

st.subheader("Final Recommendation")

if issues:
    decision = "INVESTIGATE FURTHER"
    st.error(decision)

    for issue in issues:
        st.write(f"- {issue}")

    st.write(
        "The purchase must not proceed until the issues are resolved."
    )

elif required_qty == 0:
    decision = "REJECT THE PURCHASE"
    st.success(decision)

    st.write(
        "Existing inventory and incoming orders are sufficient "
        "to cover expected demand."
    )

elif required_qty != recommended_qty:
    decision = "MODIFY THE PURCHASE"
    st.warning(decision)

    st.write(
        f"The recommended quantity of {recommended_qty} units "
        f"should be modified to {required_qty} units."
    )

else:
    decision = "ACCEPT THE PURCHASE"
    st.success(decision)

    st.write(
        "The recommendation matches the calculated requirement "
        "and satisfies the configured constraints."
    )

# Save the analysis result in the current session
st.session_state["purchase_analysis"] = {
    "decision": decision,
    "required_qty": required_qty,
    "estimated_cost": estimated_cost,
    "issues": issues,
}

st.divider()

# --------------------------------------------------
# PURCHASE ORDER MANAGEMENT
# --------------------------------------------------

st.header("📝 Purchase Order Management")

st.write(
    "Review the recommendation and approve the purchase "
    "before creating a purchase order."
)

analysis = st.session_state["purchase_analysis"]

# Buyer approval is available only when the purchase is eligible
if analysis["decision"] in ("ACCEPT THE PURCHASE", "MODIFY THE PURCHASE"):
    buyer_approved = st.checkbox(
        "I have reviewed and approve this purchase order."
    )
else:
    buyer_approved = False

if st.button("Create Purchase Order"):

    # Block orders if investigation is required
    if analysis["issues"]:
        st.error(
            "Purchase blocked: resolve the investigation issues "
            "before creating an order."
        )

    elif analysis["decision"] == "REJECT THE PURCHASE":
        st.warning("No purchase is required.")

    elif not buyer_approved:
        st.warning(
            "Please approve the purchase recommendation before "
            "creating an order."
        )

    elif analysis["required_qty"] <= 0:
        st.warning("Purchase quantity must be greater than zero.")

    elif analysis["estimated_cost"] > available_budget:
        st.error("Purchase blocked: insufficient budget.")

    elif analysis["required_qty"] > available_storage:
        st.error("Purchase blocked: insufficient storage.")

    else:
        order_id = "PO-1001"

        existing_order = get_purchase_order(order_id)

        if existing_order:
            st.warning(
                f"Purchase order {order_id} already exists. "
                "No duplicate order was created."
            )

        else:
            order = {
                "order_id": order_id,
                "quantity": analysis["required_qty"],
                "unit_price": unit_price,
                "total_cost": analysis["estimated_cost"],
                "status": "Created",
            }

            try:
                save_purchase_order(order)

                st.session_state["purchase_order"] = order

                st.success("Purchase order saved to the database!")

                st.subheader("📄 Created Purchase Order")

                st.write(f"**Order ID:** {order['order_id']}")
                st.write(f"**Quantity:** {order['quantity']} units")
                st.write(f"**Unit Price:** ₹{order['unit_price']}")
                st.write(f"**Total Cost:** ₹{order['total_cost']:,}")
                st.write(f"**Status:** {order['status']}")

            except Exception as error:
                st.error(f"Unable to create purchase order: {error}")

# --------------------------------------------------
# PURCHASE ORDER VALIDATION
# --------------------------------------------------

st.divider()
st.header("✅ Purchase Order Validation")

st.write(
    "Verify that the saved purchase order matches the calculated "
    "quantity, cost, budget, and storage constraints."
)

if st.button("Validate Purchase Order"):

    order = get_purchase_order("PO-1001")

    if order is None:
        st.error(
            "VALIDATION FAILED: Purchase order not found in the database."
        )

    else:
        validation_errors = []

        expected_quantity = max(
            0,
            expected_demand - current_inventory - incoming_orders,
        )

        if expected_quantity > 0:
            expected_quantity = max(
                expected_quantity,
                supplier_minimum,
            )

        expected_cost = order["quantity"] * order["unit_price"]

        if order["quantity"] != expected_quantity:
            validation_errors.append(
                "Purchase quantity does not match the calculated requirement."
            )

        if abs(order["total_cost"] - expected_cost) > 0.01:
            validation_errors.append(
                "Purchase order total does not match the calculated cost."
            )

        if order["total_cost"] > available_budget:
            validation_errors.append(
                "Purchase order exceeds the available budget."
            )

        if order["quantity"] > available_storage:
            validation_errors.append(
                "Purchase quantity exceeds available storage capacity."
            )

        if order["status"] != "Created":
            validation_errors.append(
                "Purchase order status is not Created."
            )

        if validation_errors:
            st.error("VALIDATION FAILED")

            for error in validation_errors:
                st.write(f"- {error}")

        else:
            st.success("VALIDATION PASSED")

            st.write(
                "The saved purchase order passed all configured checks."
            )

            st.write(f"Verified order: {order['order_id']}")

st.divider()

st.caption("SmartBuy AI | Rappi Purchasing Agent Assignment")
