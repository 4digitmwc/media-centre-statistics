from dataclasses import dataclass

@dataclass
class Beatmap:
    beatmap_id: int
    beatmap_category: str
    beatmap_tag: int
    beatmap_round: str
    beatmap_metadata: str

@dataclass
class User:
    user_id: int
    username: str

@dataclass
class PickBanStatistics:
    beatmap_metadata: int
    ban_rate: float
    pick_rate: float
    beatmap_thumbnail: str

@dataclass
class ScoreHighlight:
    user_name: int
    beatmap_metadata: int
    beatmap_thumbnail: str
    score: int
    screenshot_url: str
    score_description: str

@dataclass
class ScoreLeaderboard:
    user_id: int
    beatmap_id: int
