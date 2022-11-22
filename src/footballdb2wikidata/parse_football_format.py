from pathlib import Path
from dataclasses import dataclass


@dataclass
class FootballGame:
    """Class with metadata for a football match from footballdb"""

    date: str  # Nov/20
    time: str  # 19:00
    team_1: str  # Qatar
    team_2: str  # Ecuador
    score: str  #  0-2
    stadium: str  #  Al Bayt Stadium
    goals: str  # [-; Enner Valencia 16' (pen.), 31']


def get_class_from_text(text):
    lines = text.split("\n")
    for i, line in enumerate(lines):
        if "@" in line:
            first_half = list(filter(None, line.split("@")[0].split(" ")))
            print(first_half)
            second_half = list(filter(None, line.split("@")[1].split(",")))
            game = FootballGame(
                date=first_half[2],
                time=first_half[3],
                team_1=first_half[4],
                team_2=first_half[7],
                score=first_half[5],
                stadium=second_half[0].strip(),
                goals=lines[i + 1].strip(),
            )
            print(game)
    return game
