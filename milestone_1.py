
# =============== Step 1 - Input the number of packages =============== 
print("\n")
num_packages = int(input("Enter the number of packages to load: "))

# =============== Step 2 - Package details collection (Append in "packages") ===============
packages = []

distances = {
        "hanoi": {"hai phong": 120, "da nang": 800, "hcmc": 1400, "nha trang": 1300, "dalat": 1200},
        "hai phong": {"hanoi": 120, "da nang": 900, "hcmc": 1500, "nha trang": 1400, "dalat": 1300},
        "da nang": {"hanoi": 800, "hai phong": 900, "hcmc": 1000, "nha trang": 300, "dalat": 400},
        "nha trang": {"hanoi": 1300, "hai phong": 1400, "hcmc": 400, "da nang": 300, "dalat": 200},
        "dalat": {"hanoi": 1200, "hai phong": 1300, "hcmc": 300, "da nang": 400, "nha trang": 200},
        "hcmc": {"hanoi": 1400, "hai phong": 1500, "da nang": 1000, "nha trang": 400, "dalat": 300}
    }
    
valid_cities = set(distances.keys()) 

for i in range(num_packages):
    print(f"\nEnter details for package {i + 1}:")
    
    while True: # Ask for the city input
        city = input("City: ").strip().lower()
        if city not in valid_cities:
            print(f"Error: '{city}' is invalid. Try again.")
        else:
            break

    while True: # Ask for the weight input
        try:
            weight = float(input("Weight (kg): "))
            if weight <= 0:
                print("Weight must be positive.")
                continue
            break
        except ValueError:
            print("Invalid input. Try again.")

    
    packages.append({ # Append the package's information into the "packages" list 
        "id": i + 1,
        "city": city,
        "weight": weight,
        "distance": distances["hanoi"].get(city, 0),
    })

# =============== Step 3 - Define delivery routes ===============
fixed_route = ["hanoi", "hai phong", "da nang", "nha trang", "dalat", "hcmc"] # Defined delivery route

user_route=[] # Generate a filtered user-defined route (Only cities specified by the user) (It's already in the correct order because it's followin the "fixed_route" list)
for city in fixed_route:
    package_found = False
    for package in packages:
        if package["city"] == city:
            package_found = True
            break
    
    if package_found:
        user_route.append(city)

# =============== Step 4 - Organize packages to load the truck ===============

rate_per_km=3000
truck_stack = [] # The "stack" doesn't fundamentally change anything (It could be any name)

def load_packages(packages, route_order):
        for city in reversed(route_order):
            for package in packages:
                if package["city"] == city:
                    truck_stack.append(package)

# =============== Step 5 - Output the loading order ===============
print(
        "\n==========================="
        "\nLoading Order (Follow This Order for Proper Truck Loading):"  
    )

load_packages(packages, user_route)

for i, package in enumerate(truck_stack): 
    print(f"Load Order: {i+1} | Package ID: {package['id']} | City: {package['city']} | Weight: {package['weight']}kg")

print("\n")