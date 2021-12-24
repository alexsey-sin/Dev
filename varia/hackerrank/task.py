class MyDeckMax:
    def __init__(self, max_size):
        self.items = []
        self.max_size = max_size

    def push_back(self, item):
        self.items.append(item)

    def push_front(self, item):
        self.items.insert(0, item)

    def pop_front(self):
        return self.items.pop(0)

    def pop_back(self):
        return self.items.pop()

    def is_max(self):
        return self.max_size == len(self.items)

    def is_empty(self):
        return len(self.items) == 0


if __name__ == '__main__':
    n = int(input())
    max = int(input())
    deckmax = MyDeckMax(max)
    for _ in range(n):
        comm = list(input().split())
        if comm[0] == 'push_back':
            if deckmax.is_max():
                print('error')
            else:
                deckmax.push_back(int(comm[1]))
        if comm[0] == 'push_front':
            if deckmax.is_max():
                print('error')
            else:
                deckmax.push_front(int(comm[1]))
        if comm[0] == 'pop_front':
            if deckmax.is_empty():
                print('error')
            else:
                print(deckmax.pop_front())
        if comm[0] == 'pop_back':
            if deckmax.is_empty():
                print('error')
            else:
                print(deckmax.pop_back())
