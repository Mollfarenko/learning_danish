from datetime import date, timedelta

def calculate_next_review(
    correct: bool,
    repetitions: int,
    interval: int,
    easiness_factor: float
) -> dict:

    if correct:
        # Move forward in the schedule
        if repetitions == 0:
            new_interval = 1
        elif repetitions == 1:
            new_interval = 6
        else:
            new_interval = round(interval * easiness_factor)

        new_repetitions = repetitions + 1

        # Easiness factor grows slightly on correct answer
        # Formula from original SM-2 paper
        new_ef = easiness_factor + 0.1

    else:
        # Reset — word comes back tomorrow
        new_interval = 1
        new_repetitions = 0

        # Easiness factor shrinks on wrong answer, minimum 1.3
        new_ef = max(1.3, easiness_factor - 0.2)

    new_next_review = date.today() + timedelta(days=new_interval)

    return {
        "interval": new_interval,
        "repetitions": new_repetitions,
        "easiness_factor": round(new_ef, 2),
        "next_review_date": new_next_review
    }
