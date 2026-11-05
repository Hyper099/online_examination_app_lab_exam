def calculate_score(answers, answer_key):
    """Count correct answers. Each answer is a zero-based option index."""
    if not isinstance(answers, (list, tuple)) or not isinstance(answer_key, (list, tuple)):
        raise ValueError("Answers and answer key must be lists or tuples.")
    if not answer_key or len(answers) != len(answer_key):
        raise ValueError("Provide one answer per question.")
    if any(type(option) is not int or not 0 <= option < 4 for option in (*answers, *answer_key)):
        raise ValueError("Each option must be an integer from 0 to 3.")
    return sum(answer == correct for answer, correct in zip(answers, answer_key))


if __name__ == "__main__":
    key = [1, 3, 0, 2, 1, 0, 3, 2, 1, 0]
    sample_answers = key[:7] + [0, 0, 1]
    score = calculate_score(sample_answers, key)
    if score != 7:
        raise SystemExit(f"Result calculation failed. Expected 7/10, got {score}/10.")
    print(f"Result calculation succeeded. Sample score: {score}/10.")
