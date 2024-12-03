import heapq

# Step 1: Package and City Details (Milestone 1)
class Truck:
    def __init__(self, rate_per_km=1.0):
        self.rate_per_km = rate_per_km  # Cost rate per kg-km
        self.stack = []  # Stack to hold packages
    
    def load_packages(self, packages, route_order):
        """
        Load packages in reverse order of the delivery route.
        Route order should be a list of cities in the optimized delivery order.
        """
        for city in route_order:
            # Find and load packages for the current city in reverse order
            for package in packages:
                if package['city'] == city:
                    self.stack.append(package)
    
    def generate_invoice(self):
        print("\nInvoice:")
        total_cost = 0
        while self.stack:
            package = self.stack.pop()  # Process packages in reverse loading order
            cost = package["weight"] * package["distance"] * self.rate_per_km
            total_cost += cost
            print(f"Package ID: {package['id']} | City: {package['city']} | Cost: ${cost:.2f}")
        print(f"Total Cost: ${total_cost:.2f}")


# Step 2: Route Planning (Milestone 2)
def find_optimal_route(cities, distances, start_city):
    """
    Use Dijkstra's algorithm to find the shortest path from start_city to other cities.
    Cities: A list of all cities (nodes).
    Distances: A dictionary of distances between cities.
    start_city: The city from where the journey begins.
    """
    # Priority queue for Dijkstra's algorithm
    queue = [(0, start_city)]  # (distance, city)
    shortest_paths = {city: float('inf') for city in cities}
    shortest_paths[start_city] = 0
    previous_cities = {city: None for city in cities}
    
    while queue:
        current_distance, current_city = heapq.heappop(queue)
        
        # Explore neighbors
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


# Step 3: Main Program
def main():
    print("Welcome to the 1-Door Truck Loading Program!")

    # Step 1: User Inputs Package and City Details
    rate_per_km = float(input("Enter the rate per km per kg: "))
    num_packages = int(input("Enter the number of packages to load: "))

    packages = []
    cities = set()  # To track cities with packages
    for i in range(num_packages):
        print(f"\nEnter details for Package {i + 1}:")
        city = input("City: ")
        weight = float(input("Weight (kg): "))
        distance = float(input("Distance (km): "))
        packages.append({"id": i + 1, "city": city, "weight": weight, "distance": distance})
        cities.add(city)
    
    # Step 2: Route Planning (Milestone 2)
    print("\nGenerating optimal route...")
    
    # Fixing the distances dictionary to ensure all cities have all distances
    distances = {
        "Hanoi": {"Hai Phong": 100, "Da Nang": 800, "Nha Trang": 1100, "Dalat": 1200, "HCMC": 1400},
        "Hai Phong": {"Hanoi": 100, "Da Nang": 700, "Nha Trang": 1000, "Dalat": 1200, "HCMC": 1300},
        "Da Nang": {"Hanoi": 800, "Hai Phong": 700, "Nha Trang": 400, "Dalat": 900, "HCMC": 1000},
        "Nha Trang": {"Hanoi": 1100, "Hai Phong": 1000, "Da Nang": 400, "Dalat": 400, "HCMC": 600},
        "Dalat": {"Hanoi": 1200, "Hai Phong": 1200, "Da Nang": 900, "Nha Trang": 400, "HCMC": 500},
        "HCMC": {"Hanoi": 1400, "Hai Phong": 1300, "Da Nang": 1000, "Nha Trang": 600, "Dalat": 500},
    }
    
    # Ensure every city has a distance to all others (including itself with distance 0)
    all_cities = list(cities)
    for city in all_cities:
        if city not in distances:
            distances[city] = {}
        for other_city in all_cities:
            if other_city not in distances[city]:
                # Assuming a default distance of 0 to itself
                distances[city][other_city] = 0

    route_order = find_optimal_route(list(cities), distances, "Hanoi")
    print(f"\nOptimal delivery route: {route_order}")

    # Step 3: Load the Truck Based on the Route
    truck = Truck(rate_per_km)
    truck.load_packages(packages, route_order)
    truck.generate_invoice()


# Run the program
main()
