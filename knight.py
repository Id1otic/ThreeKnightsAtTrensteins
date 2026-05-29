import random, time, threading, data_types, pygame

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

    def __init__(self, name: str, starting_scene: str, scenes: data_types.SceneStruct, lock: threading.Lock, jumpscare: pygame.mixer.Sound, jumpscare_volume: float = 1.0):
        self.name = name
        self.scene = starting_scene

        self.lock = lock

        self.target_dict = scenes
        self.target_dict[self.scene]['knights_in_scene'].append(self.name)

        self.jumpscare_sound = jumpscare
        self.jumpscare_sound.set_volume(jumpscare_volume)

        self.thread: threading.Thread | None = None
        self.thread_on = True

    def moving_logic(self) -> None:
        '''
        Moves the knight between random scenes in sets of time
        '''
        while self.thread_on:
            time.sleep(random.randint(15, 30))

            if random.randint(0, 1) == 0:
                new_scene = random.choice(Knight.MAP_TREE_OPTIMAL_PATH[self.scene])
            else:
                new_scene = random.choice(Knight.MAP_TREE[self.scene])

            with self.lock:
                self.target_dict[self.scene]['knights_in_scene'].remove(self.name)
                self.target_dict[new_scene]['knights_in_scene'].append(self.name)

                self.scene = new_scene
        
        self.thread_on = True

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
            self.thread_on = False

            self.target_dict[self.scene]['knights_in_scene'].remove(self.name)
            self.target_dict[target]['knights_in_scene'].append(self.name)

            self.scene = target

            self.initiate_moving()
        else:
            return