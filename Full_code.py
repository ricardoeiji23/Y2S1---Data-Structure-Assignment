class Truck:
    def __init__(self, rate_per_km=3000):  
        self.rate_per_km = rate_per_km 
        self.stack = [] 

    def load_packages(self, packages, route_order):
        for city in reversed(route_order):
            for package in packages:
                if package["city"] == city:
                    self.stack.append(package)

    def generate_invoice(self):
        print("\n===========================")
        print("--- Invoice ---")
        total_cost = 0

        while self.stack:
            package = self.stack.pop()

            if package["city"] == "hanoi":
                cost = package["weight"] * 3000
            else:
                cost = package["weight"] * package["distance"] * self.rate_per_km

            total_cost += cost
            
            print(
                f"Package ID: {package['id']} | City: {package['city'].capitalize()} | Weight: {package['weight']}kg | Distance: {package['distance']}km | Cost: {cost:,.0f} VND".replace(',', '.')
            )

        
        print(f"\nTotal shipping cost: {total_cost:,.0f} VND".replace(',', '.'))
        print("--- End of Invoice ---")
        print("\n")


def main():
    print("\n")
    print("Welcome to the Hanoi Roadways Truck Loading and Route Planning Program!")

    
    rate_per_km = 3000  
    print(f"Shipping rate: {rate_per_km} VND per km per kg.\n")
    num_packages = int(input("Enter the number of packages to load: "))

    
    distances = {
        "hanoi": {"hai phong": 120, "da nang": 800, "hcmc": 1400, "nha trang": 1300, "dalat": 1200},
        "hai phong": {"hanoi": 120, "da nang": 900, "hcmc": 1500, "nha trang": 1400, "dalat": 1300},
        "da nang": {"hanoi": 800, "hai phong": 900, "hcmc": 1000, "nha trang": 300, "dalat": 400},
        "nha trang": {"hanoi": 1300, "hai phong": 1400, "hcmc": 400, "da nang": 300, "dalat": 200},
        "dalat": {"hanoi": 1200, "hai phong": 1300, "hcmc": 300, "da nang": 400, "nha trang": 200},
        "hcmc": {"hanoi": 1400, "hai phong": 1500, "da nang": 1000, "nha trang": 400, "dalat": 300}
    }

    
    packages = []
    
    valid_cities = set(distances.keys()) 

    for i in range(num_packages):
        print(f"\nEnter details for package {i + 1}:")
        
        while True:
            city = input("City: ").strip().lower()
            if city not in valid_cities:
                print(f"Error: '{city}' is invalid. Try again.")
            else:
                break

        while True:
            try:
                weight = float(input("Weight (kg): "))
                if weight <= 0:
                    print("Weight must be positive.")
                    continue
                break
            except ValueError:
                print("Invalid input. Try again.")

        
        packages.append({
            "id": i + 1,
            "city": city,
            "weight": weight,
            "distance": distances["hanoi"].get(city, 0),
        })

    
    fixed_route = ["hanoi", "hai phong", "da nang", "nha trang", "dalat", "hcmc"]
    
    user_route=[]
    for city in fixed_route:
        package_found = False
        for package in packages:
            if package["city"] == city:
                package_found = True
                break
        
        if package_found:
            user_route.append(city)

    print(
        "\n==========================="
        f"\nOptimal delivery route: {' -> '.join(user_route)}" 
    )

    
    truck = Truck(rate_per_km)
    truck.load_packages(packages, user_route)

    print(
        "\n==========================="
        "\nLoading Order (Follow This Order for Proper Truck Loading):"  
    )
    for i, package in enumerate(truck.stack): 
        print(f"Load Order: {i+1} | Package ID: {package['id']} | City: {package['city']} | Weight: {package['weight']}kg")

    truck.generate_invoice()



if __name__ == "__main__":
    main()
