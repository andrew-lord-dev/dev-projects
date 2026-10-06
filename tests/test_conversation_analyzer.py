"""
Tests for conversation_analyzer.py

Run from the repository root with:
    pytest
"""

import json
import sys
from pathlib import Path

import pytest

# Make the analyzer importable when tests run from the repo root
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "conversation_analyzer"))

from conversation_analyzer import (
    load_conversation_file,
    detect_participants,
    extract_topics,
    categorize_time_period,
    calculate_duration,
    get_basic_stats,
)


@pytest.fixture
def sample_data():
    """A small, two-person conversation dataset in the new format."""
    return {
        "date": "2026-09-25",
        "conversations": [
            {
                "start_time": "09:00 AM",
                "end_time": "09:10 AM",
                "messages": [
                    {"role": "sam", "content": "Planning the hiking trip for Saturday morning."},
                    {"role": "riley", "content": "The hiking route with the waterfall sounds great."},
                ],
            },
            {
                "start_time": "06:30 PM",
                "end_time": "06:45 PM",
                "messages": [
                    {"role": "riley", "content": "Found a recipe for trail snacks."},
                    {"role": "sam", "content": "That recipe sounds perfect for hiking."},
                    {"role": "sam", "content": "Making a batch tonight."},
                ],
            },
        ],
    }


@pytest.fixture
def new_format_file(tmp_path, sample_data):
    path = tmp_path / "daily_conversations_2026-09-25.json"
    path.write_text(json.dumps(sample_data), encoding="utf-8")
    return path


@pytest.fixture
def old_format_file(tmp_path, sample_data):
    """Old format: a bare list of conversations, date only in the filename."""
    path = tmp_path / "daily_conversations_2026-09-25.json"
    path.write_text(json.dumps(sample_data["conversations"]), encoding="utf-8")
    return path


def test_load_new_format(new_format_file):
    data = load_conversation_file(str(new_format_file))
    assert data["date"] == "2026-09-25"
    assert len(data["conversations"]) == 2


def test_load_old_format_wraps_and_recovers_date(old_format_file):
    data = load_conversation_file(str(old_format_file))
    assert "conversations" in data
    assert len(data["conversations"]) == 2
    assert data["date"] == "2026-09-25"


def test_load_rejects_unknown_format(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps("just a string"), encoding="utf-8")
    with pytest.raises(ValueError):
        load_conversation_file(str(bad))


def test_detect_participants_sorted_and_unique(sample_data):
    assert detect_participants(sample_data) == ["riley", "sam"]


@pytest.mark.parametrize(
    "time_string,expected",
    [
        ("06:00 AM", "Morning"),
        ("11:59 AM", "Morning"),
        ("12:00 PM", "Afternoon"),
        ("04:59 PM", "Afternoon"),
        ("05:00 PM", "Evening"),
        ("09:59 PM", "Evening"),
        ("10:00 PM", "Night"),
        ("02:30 AM", "Night"),
        ("05:59 AM", "Night"),
    ],
)
def test_categorize_time_period_boundaries(time_string, expected):
    assert categorize_time_period(time_string) == expected


def test_duration_same_period():
    assert calculate_duration("03:03 PM", "03:08 PM") == 5


def test_duration_across_noon():
    assert calculate_duration("11:50 AM", "12:10 PM") == 20


def test_duration_across_midnight():
    # A conversation from 11:50 PM to 12:10 AM lasts 20 minutes,
    # not -1420. Regression test for the midnight-crossing bug.
    assert calculate_duration("11:50 PM", "12:10 AM") == 20


def test_basic_stats_counts(sample_data):
    stats = get_basic_stats(sample_data)
    assert stats["num_conversations"] == 2
    assert stats["total_messages"] == 5
    assert stats["messages_by_participant"] == {"riley": 2, "sam": 3}
    assert stats["conversations_started_by"] == {"riley": 1, "sam": 1}


def test_basic_stats_time_periods(sample_data):
    stats = get_basic_stats(sample_data)
    assert stats["time_periods"]["Morning"] == 2
    assert stats["time_periods"]["Evening"] == 3
    assert stats["time_periods"]["Afternoon"] == 0
    assert stats["time_periods"]["Night"] == 0


def test_basic_stats_shortest_and_longest(sample_data):
    stats = get_basic_stats(sample_data)
    assert stats["shortest_conversation"]["message_count"] == 2
    assert stats["longest_conversation"]["message_count"] == 3


def test_extract_topics_filters_stop_words_and_short_words(sample_data):
    topics = dict(extract_topics(sample_data))
    assert "the" not in topics
    assert "for" not in topics
    assert all(len(word) >= 3 for word in topics)


def test_extract_topics_counts_and_ranks(sample_data):
    topics = extract_topics(sample_data, top_n=5)
    topic_dict = dict(topics)
    assert topic_dict.get("hiking") == 3
    assert topic_dict.get("recipe") == 2
    counts = [count for _, count in topics]
    assert counts == sorted(counts, reverse=True)


def test_extract_topics_respects_top_n(sample_data):
    assert len(extract_topics(sample_data, top_n=3)) == 3
