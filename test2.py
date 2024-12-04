import heapq


class Truck:
    def __init__(self, rate_per_km=1.0):
        self.rate_per_km = rate_per_km  # Cost rate per kg-km
        self.stack = []  # Stack to hold packages

    def load_packages(self, packages, route_order):
        """
        Load packages in reverse order of the delivery route.
        Route order should be a list of cities in the optimized delivery order.
        """
        for city in reversed(route_order): # Find and load packages for the current city in reverse order
            for package in packages:
                if package['city'] == city:
                    self.stack.append(package)

    def generate_invoice(self):
        """
        Generate an invoice based on the packages in the truck.
        """
        print("\n--- Invoice ---")
        total_cost = 0
        while self.stack:
            package = self.stack.pop()  # Process packages in reverse loading order
            cost = package["weight"] * package["distance"] * self.rate_per_km
            total_cost += cost
            print(
                f"Package ID: {package['id']} | City: {package['city'].capitalize()} "
                f"| Weight: {package['weight']}kg | Distance: {package['distance']}km | Cost: ${cost:.2f}"
            )
        print(f"Total Shipping Cost: ${total_cost:.2f}")
        print("--- End of Invoice ---")


# Step 2: Define the Function for Finding Optimal Route
def find_optimal_route(cities, distances, start_city):
    """
    Use Dijkstra's algorithm to find the shortest path from start_city to other cities.
    """
    # Normalize start_city to lowercase
    start_city = start_city.lower()

    # Priority queue for Dijkstra's algorithm
    queue = [(0, start_city)]  # (distance, city)
    shortest_paths = {city: float('inf') for city in distances.keys()}
    shortest_paths[start_city] = 0
    previous_cities = {city: None for city in distances.keys()}

    while queue:
        current_distance, current_city = heapq.heappop(queue)

        # Explore neighbors
        if current_city in distances:  # Ensure the city exists in distances
            for neighbor, distance in distances[current_city].items():
                distance_via_current = current_distance + distance
                if distance_via_current < shortest_paths[neighbor]:
                    shortest_paths[neighbor] = distance_via_current
                    previous_cities[neighbor] = current_city
                    heapq.heappush(queue, (distance_via_current, neighbor))

    # Build the optimal route by following the previous cities
    route = []
    for city in cities:
        if shortest_paths[city] != float('inf'):  # Only include cities that are reachable
            route.append(city)

    return route


# Step 3: Main Function for Input and Output
def main():
    print("Welcome to the 1-Door Truck Loading Program!")

    # User Inputs: Package Details and Cost Rate
    rate_per_km = float(input("Enter the rate per km per kg: "))
    num_packages = int(input("Enter the number of packages to load: "))

    packages = []
    cities = set()  # To track cities with packages
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
        
        while True:
            try:
                distance = float(input("Distance (km): "))
                if distance <= 0:
                    print("Please enter a positive distance.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter a valid numeric distance.")
        
        # Add the package to the list and track cities
        packages.append({"id": i + 1, "city": city, "weight": weight, "distance": distance})
        cities.add(city)

    # Distance Data
    distances = {
        "hanoi": {"hai phong": 100, "da nang": 800, "nha trang": 1100, "dalat": 1200, "hcmc": 1400},
        "hai phong": {"hanoi": 100, "da nang": 700, "nha trang": 1000, "dalat": 1200, "hcmc": 1300},
        "da nang": {"hanoi": 800, "hai phong": 700, "nha trang": 400, "dalat": 900, "hcmc": 1000},
        "nha trang": {"hanoi": 1100, "hai phong": 1000, "da nang": 400, "dalat": 400, "hcmc": 600},
        "dalat": {"hanoi": 1200, "hai phong": 1200, "da nang": 900, "nha trang": 400, "hcmc": 500},
        "hcmc": {"hanoi": 1400, "hai phong": 1300, "da nang": 1000, "nha trang": 600, "dalat": 500},
    }
    distances = {city.lower(): {k.lower(): v for k, v in adj.items()} for city, adj in distances.items()}
    cities = [city.lower() for city in cities]

    # Ensure city names are valid
    for city in cities:
        if city not in distances:
            print(f"Error: City '{city}' is not valid. Please check your input.")
            return

    # Generate the optimal route
    route_order = find_optimal_route(cities, distances, "hanoi")
    print(f"\nOptimal delivery route: {', '.join(route_order)}")

    # Load packages into the truck and generate the invoice
    truck = Truck(rate_per_km)
    truck.load_packages(packages, route_order)
    truck.generate_invoice()


if __name__ == "__main__":
    main()
