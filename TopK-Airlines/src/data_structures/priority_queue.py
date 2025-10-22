class PriorityQueue:
    def __init__(self):
        self.elements = []

    def is_empty(self):
        return not self.elements

    def put(self, item, priority):
        self.elements.append((priority, item))
        self.elements.sort()  # Sort the list based on priority

    def get(self):
        return self.elements.pop(0)[1]  # Return the item with the highest priority

    def peek(self):
        return self.elements[0][1] if not self.is_empty() else None

    def size(self):
        return len(self.elements)