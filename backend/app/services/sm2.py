def sm2_update(
    interval: int,
    ease_factor: float,
    repetitions: int,
    quality: int,  # 0, 3, 4, nebo 5
) -> dict:
    """
    Standardní SM-2 algoritmus.
    quality: 0=Nevím, 3=Těžké, 4=Umím, 5=Lehké
    """
    if quality < 3:
        new_interval = 1
        new_repetitions = 0
        new_ef = ease_factor
    else:
        new_repetitions = repetitions + 1
        if repetitions == 0:
            new_interval = 1
        elif repetitions == 1:
            new_interval = 6
        else:
            new_interval = max(1, round(interval * ease_factor))

        new_ef = ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
        new_ef = max(1.3, new_ef)

    return {
        "interval": new_interval,
        "ease_factor": round(new_ef, 4),
        "repetitions": new_repetitions,
    }


def is_learned(interval: int, threshold: int) -> bool:
    return interval >= threshold
