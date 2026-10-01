from food_delivery import Customer, DeliveryPartner, Restaurant, MenuItem

# 1. Register customer Priya
priya = Customer("Priya", "9876543210", "Bangalore")
print("--- Customer registered ---")
priya.display_profile()

# 2. Register delivery partner Rajesh
rajesh = DeliveryPartner("Rajesh", "9123456780", "Bike")
print("\n--- Delivery partner registered ---")
rajesh.display_profile()

# 3. Create restaurant Bawarchi and add menu items
bawarchi = Restaurant("Bawarchi", "MG Road")
biryani = MenuItem("Biryani", 250, False)
kebab = MenuItem("Kebab", 150, False)
bawarchi.add_item(biryani)
bawarchi.add_item(kebab)
print("\n--- Menu at", bawarchi.name, "---")
for item in bawarchi.get_menu():
    print(f"{item.name}: Rs.{item.price} ({'Veg' if item.is_veg else 'Non-veg'})")

# 4. Top up wallet by 500, then try -100 (should be ignored)
print("\n--- Wallet ---")
priya.add_to_wallet(500)
print("After top-up of 500:", priya._wallet_balance)
priya.add_to_wallet(-100)
print("After attempted top-up of -100:", priya._wallet_balance)

# 5. Priya places an order for Biryani and Kebab
print("\n--- Placing order ---")
order = priya.place_order(bawarchi, [biryani, kebab])

# 6. Bill breakdown and estimated time
subtotal = sum(item.price for item in order._items)
gst = subtotal * 0.05
packaging_fee = 20
print("\n--- Bill ---")
print("Subtotal:", subtotal)
print("GST (5%):", gst)
print("Packaging fee:", packaging_fee)
print("Total:", order.calculate_bill())
print("Estimated delivery time:", order.estimated_time(), "minutes")

# 7. Rajesh accepts, wrong OTP, then correct OTP.
# The OTP is random, so fix it to 1234 to make the demo repeatable.
order._otp = 1234
print("\n--- Delivery ---")
rajesh.accept_order(order)
print("Status after accept:", order._status)

rajesh.deliver(order, 9999)
print("Wrong OTP (9999) -> status:", order._status)

rajesh.deliver(order, 1234)
print("Correct OTP (1234) -> status:", order._status)

# 8. Notifications
print("\n--- Notifications ---")
priya.notify("Order delivered")
rajesh.notify("Order delivered")
