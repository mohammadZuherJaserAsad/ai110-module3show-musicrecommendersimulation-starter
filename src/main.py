"""Command line runner for the Music Recommender Simulation."""

from .recommender import load_songs, recommend_songs, score_song


# ── Profiles ──────────────────────────────────────────────────────────────────
PROFILES = {
    "High-Energy Pop": {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
        "likes_acoustic": False,
    },
    "Chill Lofi": {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.4,
        "likes_acoustic": True,
    },
    "Deep Intense Rock": {
        "genre": "rock",
        "mood": "intense",
        "energy": 0.9,
        "likes_acoustic": False,
    },
    # Edge case: conflicting preferences (high energy but sad mood)
    "Edge Case – Sad but Hype": {
        "genre": "electronic",
        "mood": "sad",
        "energy": 0.95,
        "likes_acoustic": False,
    },
    # Edge case: fully acoustic, calm, niche genre
    "Edge Case – Acoustic Classical": {
        "genre": "classical",
        "mood": "calm",
        "energy": 0.15,
        "likes_acoustic": True,
    },
}


def print_profile_results(label: str, user_prefs: dict, songs: list, k: int = 5) -> None:
    """Print the top-k recommendations for a single user profile."""
    print(f"\n{'=' * 60}")
    print(f"  PROFILE: {label}")
    print(f"  genre={user_prefs['genre']} | mood={user_prefs['mood']} "
          f"| energy={user_prefs['energy']} | acoustic={user_prefs['likes_acoustic']}")
    print(f"{'=' * 60}\n")

    recommendations = recommend_songs(user_prefs, songs, k=k)
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        _, reasons = score_song(user_prefs, song)
        reasons_str = ", ".join(f"[{r}]" for r in reasons) if reasons else "[no strong match]"
        print(f"  #{rank}  {song['title']} by {song['artist']}")
        print(f"       Score  : {score:.2f}")
        print(f"       Reasons: {reasons_str}")
        print(f"       Why    : {explanation}")
        print()


def main() -> None:
    """Load songs and run recommendations for all defined user profiles."""
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    for label, prefs in PROFILES.items():
        print_profile_results(label, prefs, songs, k=5)


if __name__ == "__main__":
    main()
