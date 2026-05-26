from dataclasses import dataclass, field


@dataclass
class PlayerState:
    player_id: str
    name: str
    x: int = 100
    y: int = 100
    room: int = 1
    caught: bool = False
    sprite: str = ''


@dataclass
class LevelState:
    level_id: str = "niveau_1"
    code_digits: list = field(default_factory=lambda: [None, None, None, None])
    solved_puzzles: set = field(default_factory=set)
    alert_triggered: bool = False
    level_failed: bool = False


@dataclass
class GameState:
    players: dict = field(default_factory=dict)
    level: LevelState = field(default_factory=LevelState)
