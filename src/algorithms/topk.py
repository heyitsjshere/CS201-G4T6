class TopKAirlines:
    def __init__(self):
        self.airlines = []

    def add_airline(self, airline_name, rating):
        self.airlines.append((airline_name, rating))
        self.airlines.sort(key=lambda x: x[1], reverse=True)

    def get_top_k(self, k):
        return self.airlines[:k]

    def remove_airline(self, airline_name):
        self.airlines = [airline for airline in self.airlines if airline[0] != airline_name]