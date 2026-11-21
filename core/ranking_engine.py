
def rank_candidates(candidate_results: list) -> list:
    """
    Sort candidates by final match score
    and assign ranking positions.
    """

    if not isinstance(candidate_results, list):
        raise TypeError("Candidate results must be a list.")

    # Validate candidate results
    for candidate in candidate_results:

        if "final_score" not in candidate:
            raise ValueError(
                "Each candidate must contain a final_score."
            )

    # Sort candidates from highest to lowest score
    ranked_candidates = sorted(
        candidate_results,
        key=lambda candidate: candidate["final_score"],
        reverse=True
    )

    # Assign ranking positions
    for position, candidate in enumerate(
        ranked_candidates,
        start=1
    ):
        candidate["rank"] = position

    return ranked_candidates
