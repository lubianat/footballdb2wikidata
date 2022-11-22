from pathlib import Path
from dataclasses import dataclass
from .dicts import dicts
from datetime import datetime


@dataclass
class WikidataGoal:
    """Class with Wikidata-formatted metadata for a goal"""

    scorer: str  # Q62521848 (Enner Valencia)
    time: int  # 16
    interval: str  # Q62521848 (first half)
    score_method: str = ""  # Q279532


@dataclass
class WikidataFootballGame:
    """Class with Wikidata-formatted metadata for a football match"""

    date: str  # +2022-11-20T00:00:00Z/11
    time: str  # Q55812019 (19:00)
    team_1: str  # Q232731 (Qatar national association football team)
    team_1_goals: int  # 0
    team_2: str  # Q987584 (Ecuador national association football team)
    team_2_goals: int  # 2
    winner: str  # Q987584
    stadium: str  # Q1050220 (Al Bayt Stadium)
    goals: list  # [WikidataGoal(Q62521848, 16, Q62521848, Q279532), WikidataGoal(Q2843080, 31,Q62521848 )]
    event = "Q284163"  # FIFA World Cup
    match_type: str = "Q17315159"  # international association football match
    sport: str = "Q2736"  # Association football
    timezone = "Q6760"  #  (UTC+3)


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
    wikidata_version = None
    event = "FIFA World Cup 2022 - Group Phase"

    def parse_to_wikidata(self, year="2022"):
        date_python = datetime.strptime(self.date + f"-{year}", "%b/%d-%Y")

        self.wikidata_version = WikidataFootballGame(
            date=date_python.strftime(
                "+%Y-%m-%dT00:00:00Z/11",
            )
        )


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
