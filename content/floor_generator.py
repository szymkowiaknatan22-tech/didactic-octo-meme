"""
Procedural floor generation with room graph.
"""
import random
from enum import Enum

class RoomType(Enum):
    START = 1
    COMBAT = 2
    BOSS = 3
    REWARD = 4
    SHOP = 5

class FloorRoom:
    def __init__(self, x, y, room_type):
        self.x = x
        self.y = y
        self.room_type = room_type
        self.doors = {"N": False, "S": False, "E": False, "W": False}
        self.cleared = False

class FloorGenerator:
    def __init__(self, grid_size=9):
        self.grid_size = grid_size
        self.rooms = {}
        self.start_room = None
        self.boss_room = None
    
    def generate(self):
        self.rooms = {}
        
        # Start at center
        center = self.grid_size // 2
        self.start_room = (center, center)
        
        # Random walk to create path
        current = self.start_room
        path = [current]
        visited = {current}
        
        # Generate main path (10-15 rooms)
        target_rooms = random.randint(10, 15)
        
        while len(path) < target_rooms:
            neighbors = self._get_unvisited_neighbors(current, visited)
            if not neighbors:
                # Backtrack
                if len(path) > 1:
                    path.pop()
                    current = path[-1]
                else:
                    break
            else:
                next_room = random.choice(neighbors)
                path.append(next_room)
                visited.add(next_room)
                current = next_room
        
        # Add some branches
        all_rooms = list(visited)
        for _ in range(3):
            if len(all_rooms) > 2:
                branch_start = random.choice(all_rooms[1:-1])
                neighbors = self._get_unvisited_neighbors(branch_start, visited)
                if neighbors:
                    branch_room = random.choice(neighbors)
                    visited.add(branch_room)
                    all_rooms.append(branch_room)
        
        # Assign room types
        all_rooms = list(visited)
        self.rooms[self.start_room] = FloorRoom(self.start_room[0], self.start_room[1], RoomType.START)
        
        # Boss is furthest from start
        max_dist = 0
        boss_pos = all_rooms[-1]
        for pos in all_rooms:
            dist = abs(pos[0] - self.start_room[0]) + abs(pos[1] - self.start_room[1])
            if dist > max_dist:
                max_dist = dist
                boss_pos = pos
        
        self.boss_room = boss_pos
        self.rooms[boss_pos] = FloorRoom(boss_pos[0], boss_pos[1], RoomType.BOSS)
        
        # Fill remaining rooms
        for pos in all_rooms:
            if pos not in self.rooms:
                # Random type: mostly combat, some rewards
                if random.random() < 0.2:
                    room_type = RoomType.REWARD
                else:
                    room_type = RoomType.COMBAT
                self.rooms[pos] = FloorRoom(pos[0], pos[1], room_type)
        
        # Set up doors
        for pos, room in self.rooms.items():
            # Check each direction
            directions = [
                ("N", (pos[0], pos[1] - 1)),
                ("S", (pos[0], pos[1] + 1)),
                ("E", (pos[0] + 1, pos[1])),
                ("W", (pos[0] - 1, pos[1]))
            ]
            for dir_name, neighbor_pos in directions:
                if neighbor_pos in self.rooms:
                    room.doors[dir_name] = True
    
    def _get_unvisited_neighbors(self, pos, visited):
        neighbors = []
        directions = [
            (pos[0], pos[1] - 1),  # N
            (pos[0], pos[1] + 1),  # S
            (pos[0] + 1, pos[1]),  # E
            (pos[0] - 1, pos[1])   # W
        ]
        for neighbor in directions:
            if neighbor not in visited and self._is_valid_pos(neighbor):
                neighbors.append(neighbor)
        return neighbors
    
    def _is_valid_pos(self, pos):
        return 0 <= pos[0] < self.grid_size and 0 <= pos[1] < self.grid_size
