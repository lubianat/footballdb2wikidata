from pathlib import Path
from dataclasses import dataclass
from .dicts import dicts
from datetime import datetime
from wdcuration import add_key
from pathlib import Path
import json

HERE = Path(__file__).parent.resolve()
DICTS = HERE.parent.joinpath("footballdb2wikidata").joinpath("dicts").resolve()


def main():
    sample_football_text = """(1) Sun Nov/20 19:00      Qatar   0-2 (0-2)   Ecuador    @ Al Bayt Stadium, Al Khor
              [-; Enner Valencia 16' (pen.), 31']  """
    result_class = get_class_from_text(sample_football_text)
    result_class.parse_to_wikidata()
    result_class_wikidata = result_class.wikidata_version


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
    stadium: str  # Q1050220 (Al Bayt Stadium)
    goals: list  # [WikidataGoal(Q62521848, 16, Q62521848, Q279532), WikidataGoal(Q2843080, 31,Q62521848 )]
    event: str = "Q284163"  # FIFA World Cup
    match_type: str = "Q17315159"  # international association football match
    sport: str = "Q2736"  # Association football
    timezone: str = "Q6760"  #  (UTC+3)
    winner: str = ""  # Q987584

    def __post_init__(self):
        if self.team_1_goals > self.team_2_goals:
            self.winner = self.team_1
        elif self.team_1_goals < self.team_2_goals:
            self.winner = self.team_2


def check_and_save_dict(dict_name, string, path=DICTS):
    if string not in dicts[dict_name]:
        dicts[dict_name] = add_key(dicts["time"], string)
        path.joinpath(f"{dict_name}.json").write_text(
            json.dumps(dicts[dict_name], indent=4, sort_keys=True)
        )
    return dicts[dict_name]


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
        dicts["time"] = check_and_save_dict("time", self.time, path=DICTS)
        dicts["team"] = check_and_save_dict("team", self.team_1, path=DICTS)
        dicts["team"] = check_and_save_dict("team", self.team_2, path=DICTS)
        dicts["stadium"] = check_and_save_dict("stadium", self.stadium, path=DICTS)

        self.wikidata_version = WikidataFootballGame(
            date=date_python.strftime("+%Y-%m-%dT00:00:00Z/11"),
            time=dicts["time"][self.time],
            team_1=dicts["team"][self.team_1],
            team_2=dicts["team"][self.team_2],
            team_1_goals=int(self.score.split("-")[0]),
            team_2_goals=int(self.score.split("-")[1]),
            stadium=dicts["stadium"][self.stadium],
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


if __name__ == "__main__":
    main()
