# # Collect package data from the user
# # Calculate the optimal delivery route
# # Load the truck based on the delivery order
# # Generate an invoice with shipping costs

# # User input about the package details
# num_packages = int(input("Enter the number of packages: "))
# packages=[]

# for i in range(num_packages):
#     city = input(f"Enter the destination city for package {i+1}: ")
#     weight = float(input(f"Enter the weight of package {i+1} (Kg): "))

#     packages.append({"id": i+1, "city":city, "weight":weight})

# # Store the distances between cities
# distances = {
#     "hanoi": {"hai phong": 120, "da nang": 800, "hcmc": 1400, "nha trang": 1300, "dalat": 1200},
#     "hai phong": {"hanoi": 120, "da nang": 900, "hcmc": 1500, "nha trang": 1400, "dalat": 1300},
#     "da nang": {"hanoi": 800, "hai phong": 900, "hcmc": 1000, "nha trang": 300, "dalat": 400},
#     "nha trang": {"hanoi": 1300, "hai phong": 1400, "hcmc": 400, "da nang": 300, "dalat": 200},
#     "dalat": {"hanoi": 1200, "hai phong": 1300, "hcmc": 300, "da nang": 400, "nha trang": 200},
#     "hcmc": {"hanoi": 1400, "hai phong": 1500, "da nang": 1000, "nha trang": 400, "dalat": 300}
# }

# # Add the "distance" data to each package | In the package we have (ID, City, Weight)
# for i in packages:
#     i["distance"] = distances["hanoi"].get(i["city"], 0) # We need the city to know the distance 

# # Fixed delivery route (Even if some of them are not inserted)
# fixed_route = ["hanoi", "hai phong", "da nang", "nha trang", "dalat", "hcmc"]

# # Include only the user-specified cities
# user_route = [city for city in fixed_route if any(p["city"] == city for p in packages)]


# Create the truck class
class Truck:
    def __init__(self,rate_per_km=3000):
        self.rate_per_km = rate_per_km
        self.stack = [] # Store the packages in the correct order

    def load_packages(self, packages, route_order):
        for city in reversed(route_order):
            for package in packages:
                if package["city"] == city:
                    self.stack.append(package)

    def generate_invoice(self):
        print("\n --- Invoice ---")
        total_cost = 0

        while self.stack:
            package = self.stack.pop()
            cost = package["weight"] * package["distance"] * self.rate_per_km
            total_cost += cost
            print(f"Package ID: {package['id']} | Cost: {cost:,.0f} VND")

        print(f"\nTotal cost: {total_cost:,.0f} VND")


# Create the main function to tie everything together and then just call main()

def main():
    rate_per_km = 3000
    num_packages = int(input("Enter the number of packages: "))

    distances = {
        "hanoi": {"hai phong": 120, "da nang": 800, "hcmc": 1400},
        "hai phong": {"hanoi": 120, "da nang": 900, "hcmc": 1500},
        "da nang": {"hanoi": 800, "hai phong": 900, "hcmc": 1000},
        "nha trang": {"hanoi": 1300, "hai phong": 1400, "hcmc": 400},
        "dalat": {"hanoi": 1200, "hai phong": 1300, "hcmc": 300},
        "hcmc": {"hanoi": 1400, "hai phong": 1500, "da nang": 1000},
    }

    packages = []
    valid_cities = set(distances.keys())

    for i in range(num_packages):
        while True:
            city = input(f"Enter the city for package {i+1}: ").lower()
            if city in valid_cities:
                break
            print("Invalid city. Try again.")

        weight = float(input(f"Enter the weight of package {i+1} (kg): "))
        packages.append({"id": i + 1, "city": city, "weight": weight, "distance": distances["hanoi"].get(city, 0)})

    fixed_route = ["hanoi", "hai phong", "da nang", "nha trang", "dalat", "hcmc"]
    user_route = [city for city in fixed_route if any(p["city"] == city for p in packages)]

    print("\nOptimal delivery route:", " -> ".join(user_route))

    truck = Truck(rate_per_km)
    truck.load_packages(packages, user_route)
    truck.generate_invoice()
    
if __name__ == "__main__":
    main()


