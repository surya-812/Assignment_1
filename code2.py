from collections import defaultdict, deque

class FriendGraph:
    def __init__(self):
        self.graph = defaultdict(set)

    def add_friendship(self, person1, person2):
        self.graph[person1].add(person2)
        self.graph[person2].add(person1)

    def get_friends(self, person):
        return self.graph[person]

    def get_common_friends(self, person1, person2):
        return self.graph[person1].intersection(self.graph[person2])

    def find_nth_connection(self, start, target):
        if start == target:
            return 0

        visited = set()
        queue = deque([(start, 0)])  # (current person, current depth)

        while queue:
            current_person, depth = queue.popleft()

            if current_person in visited:
                continue

            visited.add(current_person)

            for friend in self.graph[current_person]:
                if friend == target:
                    return depth + 1
                if friend not in visited:
                    queue.append((friend, depth + 1))

        return -1

# Example usage
graph = FriendGraph()

# Adding friendships
graph.add_friendship('Alice', 'Bob')
graph.add_friendship('Bob', 'Janice')
graph.add_friendship('Alice', 'Charlie')
graph.add_friendship('Charlie', 'Dan')
graph.add_friendship('Dan', 'Janice')

# Find friends
print("Alice's friends:", graph.get_friends('Alice'))
print("Bob's friends:", graph.get_friends('Bob'))

# Find common friends
print("Common friends of Alice and Bob:", graph.get_common_friends('Alice', 'Bob'))

# Find nth connection
print("Connection between Alice and Janice:", graph.find_nth_connection('Alice', 'Janice'))
print("Connection between Alice and Bob:", graph.find_nth_connection('Alice', 'Bob'))
print("Connection between Alice and Dan:", graph.find_nth_connection('Alice', 'Dan'))
print("Connection between Alice and non-existent person:", graph.find_nth_connection('Alice', 'NonExistent'))
