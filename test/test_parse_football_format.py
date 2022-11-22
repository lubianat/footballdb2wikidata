import re
from unittest import TestCase

from footballdb2wikidata.parse_football_format import *
from dataclasses import dataclass, asdict
from footballdb2wikidata.dicts import dicts


def test_get_class_from_text(sample_football_text):

    target_class = FootballGame(
        date="Nov/20",
        time="19:00",
        team_1="Qatar",
        team_2="Ecuador",
        score="0-2",
        stadium="Al Bayt Stadium",
        goals="[-; Enner Valencia 16' (pen.), 31']",
    )
    result_class = get_class_from_text(sample_football_text)

    TestCase().assertDictEqual(asdict(target_class), asdict(result_class))


def test_convert_class_to_wikidata(sample_football_text):

    goal_1 = WikidataGoal("Q62521848", 16, "Q62521848", "Q279532")
    goal_2 = WikidataGoal("Q2843080", 31, "Q62521848")
    target_class = WikidataFootballGame(
        date="+2022-11-20T00:00:00Z/11",
        time="Q55812019",  # 19:00,
        timezone="Q6760",  # UTC+3
        team_1="Q232731",  # Qatar national association football team
        team_1_goals=0,
        team_2="Q987584",  # Ecuador national association football team
        team_2_goals=2,
        winner="Q987584",
        stadium="Q1050220",  # Al Bayt Stadium
        goals=[
            goal_1,
            goal_2,
        ],
        event="Q284163",
        match_type="Q17315159",
        sport="Q2736",
    )
    result_class = get_class_from_text(sample_football_text)
    result_class.parse_to_wikidata()
    result_class_wikidata = result_class.wikidata_version

    TestCase().assertDictEqual(asdict(target_class), asdict(result_class_wikidata))
