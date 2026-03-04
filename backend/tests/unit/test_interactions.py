"""Unit tests for interaction filtering logic."""

from app.models.interaction import InteractionLog
from app.routers.interactions import _filter_by_item_id


def _make_log(id: int, learner_id: int, item_id: int) -> InteractionLog:
    return InteractionLog(id=id, learner_id=learner_id, item_id=item_id, kind="attempt")


def test_filter_returns_all_when_item_id_is_none() -> None:
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 2)]
    result = _filter_by_item_id(interactions, None)
    assert result == interactions


def test_filter_returns_empty_for_empty_input() -> None:
    result = _filter_by_item_id([], 1)
    assert result == []


def test_filter_returns_interaction_with_matching_ids() -> None:
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 2)]
    result = _filter_by_item_id(interactions, 1)
    assert len(result) == 1
    assert result[0].id == 1

def test_filter_returns_empty_when_no_item_id_matches() -> None:
    interactions = [_make_log(1, 1, 2), _make_log(2, 2, 3)]
    result = _filter_by_item_id(interactions, 1)
    assert result == []


def test_filter_returns_multiple_when_multiple_match_same_item_id() -> None:
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 1), _make_log(3, 3, 2)]
    result = _filter_by_item_id(interactions, 1)

    assert [i.id for i in result] == [1, 2]


def test_filter_preserves_input_order_for_matches() -> None:
    interactions = [_make_log(10, 1, 1), _make_log(5, 2, 1), _make_log(7, 3, 1)]
    result = _filter_by_item_id(interactions, 1)

    assert [i.id for i in result] == [10, 5, 7]


def test_filter_handles_large_item_id() -> None:
    big_item_id = 2**31 - 1
    interactions = [_make_log(1, 1, big_item_id), _make_log(2, 2, 1)]
    result = _filter_by_item_id(interactions, big_item_id)

    assert [i.id for i in result] == [1]
