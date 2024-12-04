# Step 2: Define the Fixed Route (including HQ as the starting point)
def fixed_route():
    """
    Return a fixed delivery route including HQ.
    """
    return ["hq", "hanoi", "hai phong", "da nang", "nha trang", "dalat", "hcmc"]

class Truck:
    def __init__(self, rate_per_km=1.0):
        self.rate_per_km = rate_per_km  # Cost rate per kg-km
        self.packages = []  # List to hold packages in the correct order

    def load_packages(self, packages, route_order, distances):
        """
        Load packages based on the fixed delivery route.
        Assign distances to the packages based on the route.
        """
        for city in route_order:
            for package in packages:
                if package['city'] == city:
                    # Assign distance to the package
                    if city == 'hq':
                        package['distance'] = distances['hq']['hanoi']
                    else:
                        prev_city = route_order[route_order.index(city) - 1]
                        package['distance'] = distances[prev_city].get(city, 0)
                    self.packages.append(package)

    def generate_invoice(self, route_order):
        """
        Generate an invoice based on the packages in the truck.
        """
        print("\n--- Invoice ---")
        total_cost = 0
        for city in route_order:
            for package in self.packages:
                if package['city'] == city:
                    cost = package["weight"] * package["distance"] * self.rate_per_km
                    total_cost += cost
                    print(
                        f"Package ID: {package['id']} | City: {package['city'].capitalize()} "
                        f"| Weight: {package['weight']}kg | Distance: {package['distance']}km | Cost: ${cost:.2f}"
                    )
        print(f"Total Shipping Cost: ${total_cost:.2f}")
        print("--- End of Invoice ---")

def main():
    print("Welcome to the 1-Door Truck Loading Program!")

    # User Inputs: Package Details and Cost Rate
    rate_per_km = float(input("Enter the rate per km per kg: "))
    num_packages = int(input("Enter the number of packages to load: "))

    packages = []
    cities_with_packages = set()  # To track cities with packages
    for i in range(num_packages):
        print(f"\nEnter details for Package {i + 1}:")
        
        city = input("City: ").strip().lower()
        while True:
            try:
                weight = float(input("Weight (kg): "))
                if weight <= 0:
                    print("Please enter a positive weight.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter a valid numeric weight.")
        
        # Add the package to the list and track cities with packages
        package = {"id": i + 1, "city": city, "weight": weight, "distance": 0}  # Initialize package with weight and distance
        packages.append(package)
        cities_with_packages.add(city)

    # Distance Data (Complete distances between cities)
    distances = {
        "hq": {"hanoi": 5},  # Distance from HQ to Hanoi (user input)
        "hanoi": {"hai phong": 120, "da nang": 800, "hcmc": 1400, "nha trang": 1300, "dalat": 1200},
        "hai phong": {"hanoi": 120, "da nang": 900, "hcmc": 1500, "nha trang": 1400, "dalat": 1300},
        "da nang": {"hanoi": 800, "hai phong": 900, "hcmc": 1000, "nha trang": 300, "dalat": 400},
        "nha trang": {"hanoi": 1300, "hai phong": 1400, "hcmc": 400, "da nang": 300, "dalat": 200},
        "dalat": {"hanoi": 1200, "hai phong": 1300, "hcmc": 300, "da nang": 400, "nha trang": 200},
        "hcmc": {"hanoi": 1400, "hai phong": 1500, "da nang": 1000, "nha trang": 400, "dalat": 300}
    }

    # Get user input for distances, specifically from HQ to Hanoi
    hanoi_to_hq_distance = float(input("Enter the distance from the HQ to the street in Hanoi: "))
    distances["hq"]["hanoi"] = hanoi_to_hq_distance  # Set this as the distance from HQ to Hanoi

    # Filter route to include only cities that have packages
    route_order = ["hq"] + [city for city in fixed_route()[1:] if city in cities_with_packages]
    
    print(f"\nOptimal delivery route: {', '.join(route_order)}")

    # Load packages into the truck and generate the invoice
    truck = Truck(rate_per_km)
    truck.load_packages(packages, route_order, distances)
    truck.generate_invoice(route_order)


if __name__ == "__main__":
    main()
