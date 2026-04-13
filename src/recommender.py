import csv
from typing import List, Dict, Tuple
from dataclasses import dataclass


@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        scored = [(song, self._score(user, song)) for song in self.songs]
        scored.sort(key=lambda x: x[1], reverse=True)
        return [song for song, _ in scored[:k]]

    def _score(self, user: UserProfile, song: Song) -> float:
        score = 0.0
        # +2.0 for genre match
        if song.genre.lower() == user.favorite_genre.lower():
            score += 2.0
        # +1.0 for mood match
        if song.mood.lower() == user.favorite_mood.lower():
            score += 1.0
        # up to +1.0 for energy similarity (linear decay)
        energy_diff = abs(song.energy - user.target_energy)
        score += max(0.0, 1.0 - energy_diff)
        # +0.5 acoustic bonus when user prefers acoustic and song qualifies
        if user.likes_acoustic and song.acousticness >= 0.6:
            score += 0.5
        return score

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        reasons = []
        if song.genre.lower() == user.favorite_genre.lower():
            reasons.append(f"genre match ({song.genre})")
        if song.mood.lower() == user.favorite_mood.lower():
            reasons.append(f"mood match ({song.mood})")
        energy_diff = abs(song.energy - user.target_energy)
        energy_score = max(0.0, 1.0 - energy_diff)
        if energy_score >= 0.8:
            reasons.append(f"energy is a great fit ({song.energy:.2f})")
        elif energy_score >= 0.5:
            reasons.append(f"energy is a decent fit ({song.energy:.2f})")
        else:
            reasons.append(f"energy mismatch ({song.energy:.2f})")
        if user.likes_acoustic and song.acousticness >= 0.6:
            reasons.append(f"acoustic warmth ({song.acousticness:.2f})")
        return ", ".join(reasons) if reasons else "general recommendation"


# ---------------------------------------------------------------------------
# Scoring recipe
# ---------------------------------------------------------------------------
# Max possible score: 4.5
#
#   +2.0  genre match      — most deliberate preference; sparse per genre so
#                            a hit is high-signal
#   +1.0  mood match       — contextual; half the weight because mood shifts
#                            with activity or time of day
#   +1.0  energy similarity — linear decay: 1.0 - |song.energy - target|
#                             Perfect match → 1.0, fully opposite → 0.0
#   +0.5  acoustic bonus   — small reward when likes_acoustic=True and
#                            song.acousticness >= 0.6; informative but
#                            not a dealbreaker
# ---------------------------------------------------------------------------

def score_song(song: Dict, user_prefs: Dict) -> Tuple[float, str]:
    """Return (numeric_score, explanation) for one song using the four-signal recipe: genre +2.0, mood +1.0, energy similarity up to +1.0, acoustic bonus +0.5."""
    score = 0.0
    reasons = []

    # +2.0 genre match
    if song.get("genre", "").lower() == user_prefs.get("genre", "").lower():
        score += 2.0
        reasons.append(f"genre match ({song['genre']})")

    # +1.0 mood match
    if song.get("mood", "").lower() == user_prefs.get("mood", "").lower():
        score += 1.0
        reasons.append(f"mood match ({song['mood']})")

    # up to +1.0 energy similarity (linear decay)
    song_energy = float(song.get("energy", 0.5))
    target_energy = float(user_prefs.get("energy", 0.5))
    energy_diff = abs(song_energy - target_energy)
    energy_score = max(0.0, 1.0 - energy_diff)
    score += energy_score
    if energy_score >= 0.8:
        reasons.append(f"energy is a great fit ({song_energy:.2f})")
    elif energy_score >= 0.5:
        reasons.append(f"energy is a decent fit ({song_energy:.2f})")
    else:
        reasons.append(f"energy mismatch ({song_energy:.2f})")

    # +0.5 acoustic bonus
    if user_prefs.get("likes_acoustic") and float(song.get("acousticness", 0)) >= 0.6:
        score += 0.5
        reasons.append(f"acoustic warmth ({float(song['acousticness']):.2f})")

    explanation = ", ".join(reasons) if reasons else "no strong match"
    return score, explanation


def load_songs(csv_path: str) -> List[Dict]:
    """Read songs.csv with csv.DictReader and return a list of dicts with numeric fields cast to float/int."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id": int(row["id"]),
                "title": row["title"],
                "artist": row["artist"],
                "genre": row["genre"],
                "mood": row["mood"],
                "energy": float(row["energy"]),
                "tempo_bpm": float(row["tempo_bpm"]),
                "valence": float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song with score_song, sort highest-first, and return the top k as (song, score, explanation) tuples."""
    scored = []
    for song in songs:
        score, explanation = score_song(song, user_prefs)
        scored.append((song, score, explanation))

    # .sort() mutates `scored` in-place — no new list is created, which is
    # efficient here because we already own the list and don't need the
    # original order again.
    # sorted() would return a *new* sorted list and leave `scored` unchanged —
    # useful when you need to keep the original order (e.g. for a second pass).
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]
