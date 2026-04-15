"""Command line runner for the Music Recommender Simulation."""

from .recommender import load_songs, recommend_songs, score_song


def main() -> None:
    """Load songs, apply a default user profile, and print ranked recommendations."""
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}\n")

    user_prefs = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
        "likes_acoustic": False,
    }

    print(f"User profile: genre={user_prefs['genre']} | mood={user_prefs['mood']} "
          f"| energy={user_prefs['energy']} | acoustic={user_prefs['likes_acoustic']}")
    print("-" * 60)

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop 5 Recommendations:\n")
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        _, reasons = score_song(user_prefs, song)
        reasons_str = ", ".join(f"[{r}]" for r in reasons) if reasons else "[no strong match]"
        print(f"#{rank}  {song['title']} by {song['artist']}")
        print(f"     Score : {score:.2f}")
        print(f"     Reasons: {reasons_str}")
        print(f"     Why   : {explanation}")
        print()


if __name__ == "__main__":
    main()
