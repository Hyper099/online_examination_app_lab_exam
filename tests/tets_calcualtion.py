import pytest

from result_calculation import calculate_score

KEY = [1, 3, 0, 2, 1, 0, 3, 2, 1, 0]


@pytest.mark.parametrize(
    ("answers", "expected"),
    [
        pytest.param(KEY, 10, id="full-marks"),
        pytest.param(KEY[:5] + [1, 0, 0, 0, 1], 5, id="partial-marks"),
        pytest.param([(option + 1) % 4 for option in KEY], 0, id="zero-marks"),
    ],
)
def test_calculate_score(answers, expected):
    assert calculate_score(answers, KEY) == expected


@pytest.mark.parametrize(
    ("answers", "key", "message"),
    [
        (None, KEY, "lists or tuples"),
        (KEY[:-1], KEY, "one answer per question"),
        ([], [], "one answer per question"),
        ([4, *KEY[1:]], KEY, "integer from 0 to 3"),
        (["1", *KEY[1:]], KEY, "integer from 0 to 3"),
        (KEY, [True, *KEY[1:]], "integer from 0 to 3"),
    ],
)
def test_invalid_inputs(answers, key, message):
    with pytest.raises(ValueError, match=message):
        calculate_score(answers, key)
