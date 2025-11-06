class PriorityQueue:
    def __init__(self):
        self.elements = []

    def is_empty(self):
        return not self.elements

    def put(self, item, priority):
        self.elements.append((priority, item))
        self.elements.sort(reverse=True)

    def get(self):
        return self.elements.pop()[1] if not self.is_empty() else None

    def peek(self):
        return self.elements[-1][1] if not self.is_empty() else None

    def size(self):
        return len(self.elements)