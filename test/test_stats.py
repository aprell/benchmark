from pytest import approx
from random import shuffle
from src.stats import summarize


def test_summarize_0():
    numbers = []
    stats = summarize(numbers)
    assert stats == []


def test_summarize_1():
    numbers = [1]
    stats = summarize(numbers)
    assert stats == [
        1,
        None,
        None,
        None,
        None,
        None,
        1,
        None,
        None,
        0,
        (1.0, None)
    ]


def test_summarize_2():
    numbers = [1, 2]
    shuffle(numbers)
    stats = summarize(numbers)
    assert stats == [
        1,
        approx(1.1),
        1.25,
        1.5,
        1.75,
        approx(1.9),
        2,
        0.5,
        approx(0.8),
        1,
        (1.5, approx(47.14, 0.1))
    ]


def test_summarize_10():
    numbers = list(range(1, 11))
    shuffle(numbers)
    stats = summarize(numbers)
    assert stats == [
        1,
        approx(1.9),
        3.25,
        5.5,
        7.75,
        approx(9.1),
        10,
        4.5,
        approx(7.2),
        9,
        (5.5, approx(55, 0.1))
    ]


def test_summarize_11():
    numbers = list(range(0, 11))
    shuffle(numbers)
    stats = summarize(numbers)
    assert stats == [
        0,
        1,
        2.5,
        5,
        7.5,
        9,
        10,
        5,
        8,
        10,
        (5, approx(66.33, 0.1))
    ]
