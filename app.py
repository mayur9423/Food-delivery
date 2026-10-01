import streamlit as st
from food_delivery import Customer, DeliveryPartner, Restaurant, MenuItem

st.set_page_config(page_title="Food Delivery", page_icon="🍔")
st.title("🍔 Food Delivery (OOP Demo)")

# ---------- session state ----------
if "restaurant" not in st.session_state:
    r = Restaurant("Spice Garden", "Aurangabad")
    r.add_item(MenuItem("Paneer Tikka", 220, True))
    r.add_item(MenuItem("Veg Biryani", 180, True))
    r.add_item(MenuItem("Chicken Biryani", 260, False))
    r.add_item(MenuItem("Butter Naan", 40, True))
    st.session_state.restaurant = r
    st.session_state.customers = {}   # name -> Customer
    st.session_state.partners = {}    # name -> DeliveryPartner
    st.session_state.orders = []      # list of (Customer, Order)

ss = st.session_state
restaurant = ss.restaurant

tabs = st.tabs(["1. Customer", "2. Wallet", "3. Menu", "4. Place Order",
                "5. Delivery Partner", "6. Accept Order", "7. OTP & Deliver"])

# ---------- 1. create customer ----------
with tabs[0]:
    st.subheader("Create Customer")
    name = st.text_input("Name", key="c_name")
    phone = st.text_input("Phone", key="c_phone")
    address = st.text_input("Address", key="c_addr")
    if st.button("Create customer"):
        if name and phone and address:
            ss.customers[name] = Customer(name, phone, address)
            st.success(f"Customer '{name}' created.")
        else:
            st.warning("Fill in all fields.")
    for c in ss.customers.values():
        st.write(f"**{c._name}** | {c._phone} | {c.address} | Wallet: ₹{c._wallet_balance}")

# ---------- 2. wallet ----------
with tabs[1]:
    st.subheader("Add Wallet Balance")
    if ss.customers:
        who = st.selectbox("Customer", list(ss.customers), key="w_who")
        amt = st.number_input("Amount (₹)", min_value=0, step=50, key="w_amt")
        if st.button("Add to wallet"):
            ss.customers[who].add_to_wallet(amt)
            st.success(f"Wallet balance: ₹{ss.customers[who]._wallet_balance}")
    else:
        st.info("Create a customer first.")

# ---------- 3. menu ----------
with tabs[2]:
    st.subheader(f"{restaurant.name} – {restaurant.location}")
    st.caption("Open now" if restaurant.is_open() else "Closed")
    for item in restaurant.get_menu():
        st.write(f"{'🟢' if item.is_veg else '🔴'} **{item.name}** — ₹{item.price}")

# ---------- 4. place order ----------
with tabs[3]:
    st.subheader("Place Order")
    if ss.customers:
        who = st.selectbox("Customer", list(ss.customers), key="o_who")
        menu = restaurant.get_menu()
        picked = st.multiselect("Items", [m.name for m in menu])
        if st.button("Place order"):
            items = [m for m in menu if m.name in picked]
            if not items:
                st.warning("Select at least one item.")
            else:
                cust = ss.customers[who]
                order = cust.place_order(restaurant, items)
                ss.orders.append((cust, order))
                st.success(f"Order #{order._order_id} placed. "
                           f"Bill: ₹{order.calculate_bill():.2f} | "
                           f"ETA: {order.estimated_time()} min")
                st.info(f"Your OTP: {order._otp}  (share with the delivery partner)")
    else:
        st.info("Create a customer first.")

# ---------- 5. delivery partner ----------
with tabs[4]:
    st.subheader("Create Delivery Partner")
    pname = st.text_input("Name", key="p_name")
    pphone = st.text_input("Phone", key="p_phone")
    vehicle = st.text_input("Vehicle", key="p_vehicle")
    if st.button("Create partner"):
        if pname and pphone and vehicle:
            ss.partners[pname] = DeliveryPartner(pname, pphone, vehicle)
            st.success(f"Partner '{pname}' created.")
        else:
            st.warning("Fill in all fields.")
    for p in ss.partners.values():
        st.write(f"**{p._name}** | {p._phone} | {p.vehicle} | "
                 f"{'Available' if p.is_available else 'Busy'} | ⭐ {p.rating}")

# ---------- 6. accept order ----------
with tabs[5]:
    st.subheader("Accept Order")
    new_orders = {f"Order #{o._order_id} ({c._name})": o
                  for c, o in ss.orders if o._status == "Placed"}
    free = [n for n, p in ss.partners.items() if p.is_available]
    if new_orders and free:
        o_label = st.selectbox("Order", list(new_orders))
        p_name = st.selectbox("Delivery partner", free)
        if st.button("Accept order"):
            ss.partners[p_name].accept_order(new_orders[o_label])
            st.success(f"{p_name} accepted {o_label}.")
            st.rerun()
    else:
        st.info("Need at least one placed order and one available partner.")

# ---------- 7. otp & deliver ----------
with tabs[6]:
    st.subheader("Enter OTP & Complete Delivery")
    active = {f"Order #{o._order_id} ({c._name}) – {o._status}": o
              for c, o in ss.orders if o._status == "Order Accepted"}
    busy = [n for n, p in ss.partners.items() if not p.is_available]
    if active and busy:
        o_label = st.selectbox("Order", list(active), key="d_order")
        p_name = st.selectbox("Delivery partner", busy, key="d_partner")
        otp = st.number_input("OTP", min_value=0, max_value=9999, step=1)
        if st.button("Deliver"):
            order = active[o_label]
            ss.partners[p_name].deliver(order, int(otp))
            if order._status == "Delivered":
                st.success("Delivered! ✅")
                st.rerun()
            else:
                st.error("Wrong OTP.")
    else:
        st.info("No accepted orders awaiting delivery.")

    st.divider()
    st.caption("All orders")
    for c, o in ss.orders:
        st.write(f"Order #{o._order_id} – {c._name} – **{o._status}** – ₹{o.calculate_bill():.2f}")
