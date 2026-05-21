import os, threading, sys
from tkinter import messagebox
from knight import Knight
import data_types

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame
pygame.init()

class Game:
    def __init__(self, title: str):
        pygame.display.set_caption(title)

        # Enter fullscreen.
        self.screen = pygame.display.set_mode(
            (0, 0),
            pygame.NOFRAME
        )
        pygame.event.set_grab(True)
        
        # Variables
        self.clock = pygame.time.Clock()

        self.FPS = 60
        self.dt = None

        self.running = True
        self.game_over = False
        self.playing = False

        self.WIDTH, self.HEIGHT = self.screen.get_size()
        self.center = (self.WIDTH // 2, self.HEIGHT // 2)

        # Text
        self.font = pygame.font.SysFont('Comic Sans', 35)

        # Loading screen + asset loading
        image_dir = "assets/images/"

        files = [f for f in os.scandir(image_dir) if f.name.endswith((".jpeg", ".png"))]
        file_len = len(files)

        self.images: dict[str, pygame.Surface] = {} # Carried into [# Images] section and prevents loading images more than once

        for count, file in enumerate(files, start=1):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop()

            self.images[file.name] = pygame.image.load(file.path).convert_alpha()

            loading_text_surface = self.font.render(f"Initializing... {count}/{file_len}", True, (255, 255, 255))
            loading_text_rect = loading_text_surface.get_rect(center=self.center)

            self.screen.fill((0,0,0))
            self.screen.blit(loading_text_surface, loading_text_rect)
            pygame.display.flip()

        # Images
        self.scene = "menu"
        self.camera_ui_active = False
        
        try:
            self.scenes: data_types.SceneStruct = {
                'menu': { # Start should not change throughout the game
                    'image': self.images['menu.jpeg'],
                    'rect': None, # All nones are fixed (repaced) in the future of the program
                    'knights': { # Knights = Hardcoded data for each scene and position
                        'mason': {
                            'image': self.images['mason.png'],
                            'rect': None,
                            'position': (1020, 435),
                            'size': (150, 80)
                        },
                        'ethan': {
                            'image': self.images['ethan.png'],
                            'rect': None,
                            'position': (1200, 280),
                            'size': (150, 150)
                        }
                    },
                    'knights_in_scene': [ # Which of the data will be used/displayed
                        'mason', 'ethan'
                    ]
                },
                'office': {
                    'image': self.images['office.jpeg'],
                    'rect': None,
                    'knights': {
                        'mason': {
                            'image': self.images['mason.png'],
                            'rect': None,
                            'position': (-600, -300),
                            'size': (3000, 1500)
                        },
                        'ethan': {
                            'image': self.images['ethan.png'],
                            'rect': None,
                            'position': (-600, -300),
                            'size': (3000, 1500)
                        },
                    },
                    'knights_in_scene': [] # Will check for death/jumpscare
                },
                'cam1': {
                    'image': self.images['cam1.jpeg'],
                    'rect': None,
                    'knights': {
                        'mason': {
                            'image': self.images['mason.png'],
                            'rect': None,
                            'position': (1200, 75),
                            'size': (200, 125)
                        },
                        'ethan': {
                            'image': self.images['ethan.png'],
                            'rect': None,
                            'position': (1050, 600),
                            'size': (200, 200)
                        },
                    },
                    'knights_in_scene': []
                },
                'cam2': {
                    'image': self.images['cam2.jpeg'],
                    'rect': None,
                    'knights': {
                        'mason': {
                            'image': self.images['mason.png'],
                            'rect': None,
                            'position': (700, 670),
                            'size': (100, 50)
                        },
                        'ethan': {
                            'image': self.images['ethan.png'],
                            'rect': None,
                            'position': (1000, 700),
                            'size': (300, 200)
                        },
                    },
                    'knights_in_scene': []
                },
                'cam3': {
                    'image': self.images['cam3.jpeg'],
                    'rect': None,
                    'knights': {
                        'mason': {
                            'image': self.images['mason.png'],
                            'rect': None,
                            'position': (50, 700),
                            'size': (200, 100)
                        },
                        'ethan': {
                            'image': self.images['ethan.png'],
                            'rect': None,
                            'position': (1590, 710),
                            'size': (200, 200)
                        },
                    },
                    'knights_in_scene': []
                },
                'cam4': {
                    'image': self.images['cam4.jpeg'],
                    'rect': None,
                    'knights': {
                        'mason': {
                            'image': self.images['mason.png'],
                            'rect': None,
                            'position': (1045, 684),
                            'size': (100, 50)
                        },
                        'ethan': {
                            'image': self.images['ethan.png'],
                            'rect': None,
                            'position': (100, 675),
                            'size': (100, 50)
                        },
                    },
                    'knights_in_scene': []
                },
                'cam5': {
                    'image': self.images['cam5.jpeg'],
                    'rect': None,
                    'knights': {
                        'mason': {
                            'image': self.images['mason.png'],
                            'rect': None,
                            'position': (1050, 735),
                            'size': (400, 200)
                        },
                        'ethan': {
                            'image': self.images['ethan.png'],
                            'rect': None,
                            'position': (220, 750),
                            'size': (500, 350)
                        },
                    },
                    'knights_in_scene': []
                }
            }

            self.mini_map: tuple[pygame.Surface, pygame.Rect] = (self.images['mini_map.png'], self.images['mini_map.png'].get_rect())
        except KeyError:
            messagebox.showerror("Missing Images", "There are missing images or the game can't\nlocate them. Try to reinstall.")
            self.stop()

        self.mini_map[1].y = 500

        self.lock = threading.Lock()
        self.knights = [
            Knight(name, 'cam4', self.scenes, self.lock)
            for name in ['mason', 'ethan']
        ]

        self.fix_img_dict(self.scenes, 1.25)

        # Sounds
        self.camera_sound = pygame.mixer.Sound('assets/camera.mp3')
        self.cam_sound_toggle = True
        self.camera_channel = None
        
        self.static_sound = pygame.mixer.Sound("assets/static.ogg")
        self.static_sound.set_volume(0.01)
        self.static_channel = self.static_sound.play(-1)

        # Mouse & Panning
        pygame.mouse.set_pos(self.center)
        self.mouse_x = self.mouse_y = None # Defined later
        self.MOUSE_MOVE_PADDING = 75
        self.MOUSE_MOVE_SPEED = 300

        # UI
        self.not_playing_buttons = [
            self.create_text("Start", 160, 350, 200, 100),
            self.create_text("Credits", 174, 470, 175, 75),
        ]

        self.camera_button = self.create_text("Cameras", 10, self.HEIGHT - 85, 150, 75)
        self.alt_camera_button = self.create_text("X", 10, self.HEIGHT - 85, 150, 75, (255, 0, 0))

        self.credits = self.create_text("""Credits:
    Mason Rustad - Coder & Mason Enemy
    Trenton - Photos & Trenstein & Trenstein Enemy
    Ethan Rustad - Ethan Enemy""", 50, 50, 900, 250)
        self.show_credits = False

        # Button System
        excluded = {"menu", "office"} # Temporary
        
        cams_pos = [
            (345, 660), # Cam1
            (345, 600), # Cam2
            (100, 610), # ...
            (75, 780),
            (230, 650)
        ]
        self.camera_buttons = [
            self.create_text(scene.title(), cams_pos[i][0], cams_pos[i][1], 100, 50)
            for i, scene in enumerate(s for s in self.scenes if s not in excluded)
        ]

    def stop(self) -> None:
        '''
        Ends the game.
        '''
        pygame.quit()
        sys.exit()

    def draw_buttons(self, buttons: list[data_types.ButtonStruct], mouse: tuple[int, int]) -> None:
        '''
        Draws all buttons from a list (Called every frame)

        :param buttons: All button objects.
        :type buttons: list[dict[str, Any]]
        :param mouse: Mouse position
        :type mouse: tuple[int, int]
        '''
        for b in buttons:
            color = b['color']
            if b['rect'].collidepoint(mouse):
                color = tuple(max(0, c-30) for c in color)

                if pygame.mouse.get_pressed()[0]:
                    color = tuple(min(255, c+40) for c in color)

            pygame.draw.rect(self.screen, color, b['rect'])
            pygame.draw.rect(
                self.screen,
                b['border_color'],
                b['rect'],
                b['border_width']
            )

            self.screen.blit(b['surf'], b['text_rect'])
    
    def draw_text(self, text: data_types.ButtonStruct) -> None:
        '''
        Draws text for one frame. Must be called every frame in a loop.
        '''
        if text['background']:
            pygame.draw.rect(self.screen, text['color'], text['rect'])
            pygame.draw.rect(
                self.screen,
                text['border_color'],
                text['rect'],
                text['border_width']
            )

        x = text['rect'].x + text['padding']
        y = text['rect'].y + text['padding']

        for line in text['text'].splitlines():
            surf = self.font.render(line, True, text['text_color'])

            self.screen.blit(surf, (x, y))

            y += surf.get_height() + 5

    def create_text(self, text: str, x: int, y: int, w: int, h: int, color: tuple[int, int, int] = (100, 100, 100), text_color: tuple[int, int, int] = (255, 255, 255), background: bool = True) -> data_types.ButtonStruct:
        '''
        Fabricates and returns text data. Could be utilized for buttons.

        :param text: Text for the button.
        :type text: str
        :param x: X coordinate.
        :type x: int
        :param y: Y coordinate.
        :type y: int
        :param w: Width.
        :type w: int
        :param h: Height
        :type h: int
        '''
        rect = pygame.Rect(x, y, w, h)
        surf = self.font.render(text, True, text_color)

        return {
            "label": text.strip(),
            "rect": rect,
            "color": color,
            "border_width": 3,
            "border_color": (0, 0, 0),

            # raw text
            "text": text.strip(),

            # button compatibility
            "surf": surf,
            "text_rect": surf.get_rect(center=rect.center),

            # multiline settings
            "text_color": text_color,
            "padding": 10,

            "background": background
        }

    def fix_img_dict(self, dictionary: data_types.SceneStruct, scale: float) -> None:
        '''
        Modifies the image dictionary to store rects.

        :param dictionary: Image dictionary
        :type dictionary: dict
        :param scale: Image scale to apply
        :type scale: float
        '''
        for data in dictionary.values():
            data['image'] = pygame.transform.scale(
                data['image'],
                (int(self.WIDTH * scale), int(self.HEIGHT * scale))
            )
            data['rect'] = data['image'].get_rect(center=self.center)

            for data2 in data['knights'].values():
                data2['image'] = pygame.transform.scale(
                    data2['image'],
                    (data2['size'][0], data2['size'][1])
                )
                data2['rect'] = data2['image'].get_rect()

    def img_pan(self, dt: float, img_rect: pygame.Rect) -> None:
        '''
        Pans an image's pygame.rect so it moves with the mouse.

        :param dt: DeltaTime
        :type dt: float
        :param img_rect: Image Rectangle
        :type img_rect: pygame.Rect
        '''
        # Get position and make center = (0, 0)
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        self.mouse_x -= self.center[0]
        self.mouse_y -= self.center[1]

        oldImgPos = img_rect.topleft
        
        # Direction
        dx = dy = 0

        if self.mouse_x > self.MOUSE_MOVE_PADDING: # Right
            dx = -1
        elif self.mouse_x < -self.MOUSE_MOVE_PADDING: # Left
            dx = 1

        if self.mouse_y > self.MOUSE_MOVE_PADDING: # Down
            dy = -1
        elif self.mouse_y < -self.MOUSE_MOVE_PADDING: # Up
            dy = 1

        # Apply direction, speed, and delta time
        img_rect.x += dx * self.MOUSE_MOVE_SPEED * dt
        img_rect.y += dy * self.MOUSE_MOVE_SPEED * dt

        # Cap the image's position
        img_rect.right = max(self.WIDTH, img_rect.right)
        img_rect.left = min(0, img_rect.left)

        img_rect.top = min(0, img_rect.top)
        img_rect.bottom = max(self.HEIGHT, img_rect.bottom)

        # Sound
        newImgPos = img_rect.topleft
        moving = oldImgPos != newImgPos

        if moving and self.scene != "office":
            if not self.camera_channel or not self.camera_channel.get_busy():
                self.camera_channel = self.camera_sound.play(-1)
        else:
            if self.camera_channel:
                self.camera_channel.stop()
                self.camera_channel = None
        
    def check_buttons(self, event: pygame.event.Event):
        '''
        Checks and runs the corresponding action for buttons that are pressed.

        :param event: The event that occured
        :type event: Event
        '''
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                mouse_pos = event.pos

                for button in self.not_playing_buttons:
                    if button["rect"].collidepoint(mouse_pos):
                        label = button['label']

                        if label == "Start": # Start
                            self.playing = True
                            self.scene = "office"

                            for knight in self.knights:
                                knight.initiate_moving()

                        elif label == "Credits": # Credits
                            self.show_credits = not self.show_credits
                
                if not self.camera_ui_active:
                    if self.camera_button['rect'].collidepoint(mouse_pos):
                        self.camera_ui_active = True
                else:
                    if self.alt_camera_button['rect'].collidepoint(mouse_pos):
                        self.camera_ui_active = False
                        self.scene = "office"

                    for button in self.camera_buttons:
                        if button["rect"].collidepoint(mouse_pos):
                            self.scene = button['label'].lower()
    
    def check_jumpscare(self):
        for knight in self.knights:
            if knight.scene == "office":
                self.camera_ui_active = False
                self.scene = "office" # Jumpscare
                # Then play sound

    def update_game(self, dt: float) -> None:
        '''
        Processes the logic (player movement, etc.)

        :param dt: DeltaTime
        :type dt: float
        '''
        scene_dict = self.scenes.get(self.scene)
        if not scene_dict:
            return

        self.img_pan(dt, scene_dict['rect'])
        bg_rect = scene_dict['rect']

        # Place and scale scene knights
        for name in scene_dict['knights_in_scene']:
            knight = scene_dict['knights'][name]

            x, y = knight['position']
            knight['rect'].topleft = (
                bg_rect.left + x,
                bg_rect.top + y
            )

        # Sound
        if self.scene == "office":
            if self.static_channel and self.static_channel.get_busy():
                self.static_channel.stop()
                self.static_channel = None
        else:
            if not self.static_channel or not self.static_channel.get_busy():
                self.static_channel = self.static_sound.play(-1)

    def update_frame(self) -> None:
        '''
        Processes the rendering.
        '''
        scene_dict = self.scenes.get(self.scene)
        if not scene_dict:
            return
        
        # Background
        self.screen.blit(scene_dict['image'], scene_dict['rect'])

        # Knights
        for name, knight in scene_dict['knights'].items():
            if name in scene_dict['knights_in_scene']:
                self.screen.blit(knight['image'], knight['rect'])

        # Buttons
        mouse = pygame.mouse.get_pos()

        if self.playing:
            self.check_jumpscare()

            if self.camera_ui_active:
                self.screen.blit(self.mini_map[0], self.mini_map[1])

                self.draw_buttons([self.alt_camera_button], mouse)
                self.draw_buttons(self.camera_buttons, mouse)

                self.draw_text(self.create_text(self.scene.title(), self.WIDTH-150, 0, 150, 100, text_color=(0, 255, 0), background=False))
            else:
                self.draw_buttons([self.camera_button], mouse)
        else:
            self.draw_buttons(self.not_playing_buttons, mouse)

            # Credits
            if self.show_credits and not self.playing:
                self.draw_text(self.credits)

        pygame.display.flip()

    def loop(self) -> None:
        '''
        Stitches the exit, logic, and rendering together in one function.
        '''
        while self.running:
            dt = self.clock.tick(self.FPS) / 1000 # DeltaTime

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

                self.check_buttons(event)

            if not self.game_over:
                self.update_game(dt)

            self.update_frame()
        
        # Cleanup and exit
        self.stop()