"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from .recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # Taste profile: "Weekend Vibes"
    # An upbeat listener who wants feel-good pop energy to kick off their day.
    user_prefs = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.80,
        "likes_acoustic": False,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print(f"\nProfile: genre={user_prefs['genre']} | mood={user_prefs['mood']} | energy={user_prefs['energy']}")
    print("=" * 52)
    print(f"  Top {len(recommendations)} Recommendations")
    print("=" * 52)

    for rank, rec in enumerate(recommendations, start=1):
        song, score, explanation = rec
        print(f"  #{rank}  {song['title']} by {song['artist']}")
        print(f"       Score : {score:.2f} / 4.50")
        print(f"       Why   : {explanation}")
        print("-" * 52)


if __name__ == "__main__":
    main()
