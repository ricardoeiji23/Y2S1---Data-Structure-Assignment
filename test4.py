import heapq


class Truck:
    def __init__(self, rate_per_km=3000):  # Rate per km per weight in VND
        self.rate_per_km = rate_per_km  # Standard rate
        self.stack = []  # Packages stack for reverse loading

    def load_packages(self, packages, route_order):
        """
        Load packages in reverse order of their planned optimal route.
        Only consider packages along the computed route.
        """
        for city in reversed(route_order):
            for package in packages:
                if package["city"] == city:
                    self.stack.append(package)

    def generate_invoice(self):
        """
        Generate the invoice by calculating costs of each package in the stack.
        Special case: If the city is 'hanoi', multiply the weight by 3000 directly.
        """
        print("\n===========================")
        print("--- Invoice ---")
        total_cost = 0

        while self.stack:
            package = self.stack.pop()

            # Special condition: If the delivery city is Hanoi, calculate differently
            if package["city"] == "hanoi":
                cost = package["weight"] * 3000  # Special rate for Hanoi
            else:
                cost = package["weight"] * package["distance"] * self.rate_per_km  # Default calculation

            total_cost += cost

            # Replace only the commas in costs with periods
            print(
                f"Package ID: {package['id']} | City: {package['city'].capitalize()} | "
                f"Weight: {package['weight']}kg | Distance: {package['distance']}km | Cost: {cost:,.0f} VND".replace(',', '.')
            )

        # Change only the total cost format
        print(f"\nTotal shipping cost: {total_cost:,.0f} VND".replace(',', '.'))
        print("--- End of Invoice ---")
        print("\n")


def dijkstra_algorithm(start, graph, packages):
    """
    Standard Dijkstra's to find shortest paths only relevant to cities with packages.
    """
    queue = [(0, start)]
    distances = {city: float('inf') for city in graph.keys()}
    distances[start] = 0

    while queue:
        current_distance, current_city = heapq.heappop(queue)

        if current_distance > distances[current_city]:
            continue

        for neighbor, distance in graph[current_city].items():
            new_distance = current_distance + distance
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                heapq.heappush(queue, (new_distance, neighbor))

    # Return only the shortest paths to cities with packages
    valid_cities = [city for city in packages if distances[city] != float('inf')]
    return valid_cities, distances


def main():
    print("Welcome to the Hanoi Roadways Truck Loading and Route Planning Program!")

    # Fixed shipping rate per km/weight
    rate_per_km = 3000  # Rate per km per kg
    print(f"Shipping rate: {rate_per_km} VND per km per kg.\n")
    num_packages = int(input("Enter the number of packages to load: "))

    # Distance map
    distances = {
        "hanoi": {"hai phong": 120, "da nang": 800, "hcmc": 1400, "nha trang": 1300, "dalat": 1200},
        "hai phong": {"hanoi": 120, "da nang": 900, "hcmc": 1500, "nha trang": 1400, "dalat": 1300},
        "da nang": {"hanoi": 800, "hai phong": 900, "hcmc": 1000, "nha trang": 300, "dalat": 400},
        "nha trang": {"hanoi": 1300, "hai phong": 1400, "hcmc": 400, "da nang": 300, "dalat": 200},
        "dalat": {"hanoi": 1200, "hai phong": 1300, "hcmc": 300, "da nang": 400, "nha trang": 200},
        "hcmc": {"hanoi": 1400, "hai phong": 1500, "da nang": 1000, "nha trang": 400, "dalat": 300}
    }

    # Package input
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

        # Append package info
        packages.append({
            "id": i + 1,
            "city": city,
            "weight": weight,
            "distance": distances["hanoi"].get(city, 0),
        })

    # Fixed delivery route
    fixed_route = ["hanoi", "hai phong", "da nang", "nha trang", "dalat", "hcmc"]
    
    # Filter the route to only show cities the user entered
    user_route = [city for city in fixed_route if any(package["city"] == city for package in packages)]

    print(
        "\n==========================="
        f"\nOptimal delivery route: {' -> '.join(user_route)}"
    )  # Dynamically show only user-entered cities in the fixed path

    # Load packages into truck
    truck = Truck(rate_per_km)
    truck.load_packages(packages, user_route)

    print(
        "\n==========================="
        "\nLoading Order:"
    )
    for package in truck.stack:
        print(f"Package ID: {package['id']} | City: {package['city']} | Weight: {package['weight']}kg")

    truck.generate_invoice()


if __name__ == "__main__":
    main()
