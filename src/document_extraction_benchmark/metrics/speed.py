from __future__ import annotations


def evaluate_speed(
    timings_seconds: list[float],
    page_count: int | None,
) -> dict:
    """
    Summarize repeated ``extract()`` timings (after optional warmup, applied by caller).

    ``seconds_per_page`` is only defined when ``page_count`` is a positive integer.
    """
    if not timings_seconds:
        return {
            "runs": 0,
            "total_seconds_mean": None,
            "total_seconds_stdev": None,
            "seconds_per_page_mean": None,
        }
    n = len(timings_seconds)
    mean = sum(timings_seconds) / n
    if n > 1:
        var = sum((t - mean) ** 2 for t in timings_seconds) / (n - 1)
        stdev = var**0.5
    else:
        stdev = 0.0
    per_page = None
    if page_count and page_count > 0:
        per_page = mean / page_count
    return {
        "runs": n,
        "total_seconds_mean": mean,
        "total_seconds_stdev": stdev,
        "seconds_per_page_mean": per_page,
        "page_count": page_count,
    }
