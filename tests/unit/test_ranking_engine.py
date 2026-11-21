
from core.ranking_engine import rank_candidates


candidates = [
    {
        "candidate_name": "Rahul Sharma",
        "final_score": 86.62
    },
    {
        "candidate_name": "Priya Patel",
        "final_score": 92.45
    },
    {
        "candidate_name": "Aman Verma",
        "final_score": 74.80
    },
    {
        "candidate_name": "Sneha Shah",
        "final_score": 89.20
    },
    {
        "candidate_name": "Arjun Mehta",
        "final_score": 68.50
    }
]


ranked_candidates = rank_candidates(candidates)


print("\n========== CANDIDATE RANKING ==========")

for candidate in ranked_candidates:

    print(
        f"Rank {candidate['rank']} | "
        f"{candidate['candidate_name']} | "
        f"{candidate['final_score']}%"
    )
