from unittest import TestCase

from footballdb2wikidata.parse_football_format import get_class_from_text, FootballGame
from dataclasses import dataclass, asdict


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
