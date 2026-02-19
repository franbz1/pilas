class Stack:
    def __init__(self):
        self._items = []

    def push(self, item):
        """Add an item to the top of the stack."""
        self._items.append(item)

    def pop(self):
        """Remove and return the top item of the stack."""
        if self.isempty():
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def top(self):
        """Return the top item without removing it."""
        if self.isempty():
            raise IndexError("top from empty stack")
        return self._items[-1]

    def isempty(self):
        """Return True if the stack is empty, otherwise False."""
        return len(self._items) == 0

    def __str__(self):
        """String representation for print(stack)."""
        return f"Stack({self._items})"