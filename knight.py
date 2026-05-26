import random, time, threading
from typing import Any

class Knight:
    MAP_TREE = { # A tree for valid cams based on position/scene.
        'office': [],
        'cam1': ['office', 'cam2'],
        'cam2': ['cam1', 'cam3', 'cam5'],
        'cam3': ['cam2', 'cam4', 'cam5'],
        'cam4': ['cam3', 'cam5'],
        'cam5': ['cam2', 'cam3', 'cam4'],
    }

    MAP_TREE_OPTIMAL_PATH = {
        'office': [],
        'cam1': ['office'],
        'cam2': ['cam1'],
        'cam3': ['cam2'],
        'cam4': ['cam3'],
        'cam5': ['cam2', 'cam3', 'cam4'],
    }

    def __init__(self, name: str, starting_scene: str, scenes: dict[str, dict[str, Any]], lock: threading.Lock):
        self.name = name
        self.scene = starting_scene

        self.lock = lock

        self.target_dict = scenes
        self.target_dict[self.scene]['knights_in_scene'].append(self.name)

        self.thread = None

    def moving_logic(self) -> None:
        '''
        Moves the knight between random scenes in sets of time
        '''
        while True:
            time.sleep(random.randint(15, 30))

            if random.randint(0, 1) == 0:
                new_scene = random.choice(Knight.MAP_TREE_OPTIMAL_PATH[self.scene])
            else:
                new_scene = random.choice(Knight.MAP_TREE[self.scene])

            with self.lock:
                self.target_dict[self.scene]['knights_in_scene'].remove(self.name)
                self.target_dict[new_scene]['knights_in_scene'].append(self.name)

                self.scene = new_scene

    def initiate_moving(self) -> None:
        '''
        Initalizes the moving of the knight
        '''
        self.thread = threading.Thread(
            target=self.moving_logic,
            daemon=True
        )

        self.thread.start()

    def force_move(self, target: str) -> None:
        if target in self.target_dict:
            self.target_dict[self.scene]['knights_in_scene'].remove(self.name)
            self.target_dict[target]['knights_in_scene'].append(self.name)
        else:
            return
