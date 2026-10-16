import streamlit as st

from database import (
    initialize_database,
    save_purchase_order,
    get_purchase_order,
)
initialize_database()

st.set_page_config(
    page_title="SmartBuy AI",
    page_icon="🛒",
    layout="wide"
)

st.title("🛒 SmartBuy AI")
st.subheader("Intelligent Purchasing Agent")

st.write(
    "An AI purchasing agent that reviews recommendations, "
    "checks business constraints, and validates purchasing decisions."
)

st.divider()

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

st.subheader("📊 Purchasing Information")

col1, col2, col3 = st.columns(3)

col1.metric("Recommended Purchase", f"{recommended_qty} units")
col2.metric("Current Inventory", f"{current_inventory} units")
col3.metric("Expected Demand", f"{expected_demand} units")

col4, col5, col6 = st.columns(3)

col4.metric("Incoming Orders", f"{incoming_orders} units")
col5.metric("Available Budget", f"₹{available_budget:,}")
col6.metric("Available Storage", f"{available_storage} units")

st.divider()

st.header("🧠 Purchasing Decision")

if st.button("Analyse Purchase Recommendation"):

    required_qty = max(
        0,
        expected_demand - current_inventory - incoming_orders
    )

    required_qty = max(required_qty, supplier_minimum) if required_qty > 0 else 0

    estimated_cost = required_qty * unit_price

    st.subheader("Investigation Results")

    st.write(f"Calculated purchase quantity: **{required_qty} units**")
    st.write(f"Unit price: **₹{unit_price}**")
    st.write(f"Estimated purchase cost: **₹{estimated_cost:,}**")

    issues = []

    if estimated_cost > available_budget:
        issues.append("The purchase exceeds the available budget.")

    if required_qty > available_storage:
        issues.append("The purchase exceeds available storage capacity.")

    if required_qty > 0 and required_qty < supplier_minimum:
        issues.append("The purchase is below the supplier minimum order quantity.")

    st.subheader("Final Recommendation")

    if issues:
        st.error("INVESTIGATE FURTHER")

        for issue in issues:
            st.write(f"- {issue}")

        st.write(
            "The purchase should not proceed until the constraints are resolved."
        )

    elif required_qty == 0:
        st.success("REJECT THE PURCHASE")

        st.write(
            "Existing inventory and incoming orders are sufficient "
            "to cover expected demand."
        )

    elif required_qty != recommended_qty:
        st.warning("MODIFY THE PURCHASE")

        st.write(
            f"Recommended quantity: {recommended_qty} units"
        )

        st.write(
            f"Calculated quantity: {required_qty} units"
        )

        st.write(
            "The original recommendation should be modified "
            "to better match the calculated requirement."
        )

    else:
        st.success("ACCEPT THE PURCHASE")

        st.write(
            "The recommendation matches the calculated requirement "
            "and satisfies the configured constraints."
        )

st.divider()

st.caption("SmartBuy AI | Rappi Purchasing Agent Assignment")

# Purchase Order Section

st.divider()

st.header("📝 Purchase Order Management")

st.write(
    "After reviewing the recommendation, the buyer can "
    "approve the calculated quantity and create a purchase order."
)

if "purchase_order" not in st.session_state:
    st.session_state.purchase_order = None

if st.button("Create Purchase Order"):

    required_qty = max(
        0,
        expected_demand - current_inventory - incoming_orders
    )

    if required_qty > 0:
        required_qty = max(required_qty, supplier_minimum)

    estimated_cost = required_qty * unit_price

    if required_qty == 0:
        st.warning("No purchase is required.")

    elif estimated_cost > available_budget:
        st.error("Purchase blocked: insufficient budget.")

    elif required_qty > available_storage:
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
                "quantity": required_qty,
                "unit_price": unit_price,
                "total_cost": estimated_cost,
                "status": "Created",
            }

            save_purchase_order(order)

            st.success("Purchase order saved to the database!")

            st.subheader("📄 Created Purchase Order")

            st.write(f"**Order ID:** {order['order_id']}")
            st.write(f"**Quantity:** {order['quantity']} units")
            st.write(f"**Unit Price:** ₹{order['unit_price']}")
            st.write(f"**Total Cost:** ₹{order['total_cost']:,}")
            st.write(f"**Status:** {order['status']}")


    # Purchase Order Validation

st.divider()

st.header("✅ Purchase Order Validation")

st.write(
    "Verify that the created purchase order matches the "
    "approved quantity, cost, budget, and storage constraints."
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
            expected_demand - current_inventory - incoming_orders
        )

        if expected_quantity > 0:
            expected_quantity = max(
                expected_quantity,
                supplier_minimum
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

