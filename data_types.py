from typing import TypedDict
import pygame

class ButtonStruct(TypedDict):
    label: str
    rect: pygame.Rect
    color: tuple[int, int, int]
    border_width: int
    border_color: tuple[int, int, int]
    text: str
    surf: pygame.Surface
    text_rect: pygame.Rect
    text_color: tuple[int, int, int]
    padding: int
    background: bool

class KnightData(TypedDict):
    image: pygame.Surface
    rect: pygame.Rect | None
    position: tuple[int, int]
    size: tuple[int, int]

class SceneData(TypedDict):
    image: pygame.Surface
    rect: pygame.Rect | None
    knights: dict[str, KnightData]

SceneStruct = dict[str, SceneData]