import csv
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


@dataclass
class Song:
    """Represents a song and its attributes."""

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
    """Represents a user's taste preferences."""

    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


def _closeness_score(value: float, target: float, max_points: float) -> float:
    """Return a score that rewards values closer to the target."""
    difference = abs(value - target)
    score = max_points * (1 - difference)
    return max(0.0, round(score, 4))


def _song_to_dict(song: Song) -> Dict:
    return {
        "id": song.id,
        "title": song.title,
        "artist": song.artist,
        "genre": song.genre,
        "mood": song.mood,
        "energy": song.energy,
        "tempo_bpm": song.tempo_bpm,
        "valence": song.valence,
        "danceability": song.danceability,
        "acousticness": song.acousticness,
    }


def _build_explanation(
    user_genre: Optional[str],
    user_mood: Optional[str],
    target_energy: Optional[float],
    likes_acoustic: Optional[bool],
    song: Dict,
) -> str:
    reasons: List[str] = []

    if user_genre and song["genre"].strip().lower() == user_genre.strip().lower():
        reasons.append("the genre matches your taste")

    if user_mood and song["mood"].strip().lower() == user_mood.strip().lower():
        reasons.append("the mood matches what you want")

    if target_energy is not None:
        energy_gap = abs(float(song["energy"]) - float(target_energy))
        if energy_gap <= 0.10:
            reasons.append("the energy level is very close to your preference")
        elif energy_gap <= 0.25:
            reasons.append("the energy level is reasonably close to your preference")

    if likes_acoustic is True and float(song["acousticness"]) >= 0.60:
        reasons.append("it has a more acoustic sound")
    elif likes_acoustic is False and float(song["acousticness"]) < 0.60:
        reasons.append("it is less acoustic and more polished/produced")

    if not reasons:
        reasons.append("it still has some overlap with your preferences")

    return "Recommended because " + ", ".join(reasons) + "."


class Recommender:
    """OOP implementation of the recommendation logic."""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def _score_song(self, user: UserProfile, song: Song) -> float:
        score = 0.0

        if song.genre.strip().lower() == user.favorite_genre.strip().lower():
            score += 40.0

        if song.mood.strip().lower() == user.favorite_mood.strip().lower():
            score += 25.0

        score += _closeness_score(song.energy, user.target_energy, 20.0)

        acoustic_match = (
            user.likes_acoustic and song.acousticness >= 0.60
        ) or (
            not user.likes_acoustic and song.acousticness < 0.60
        )
        if acoustic_match:
            score += 10.0

        return round(score, 4)

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        ranked = sorted(
            self.songs,
            key=lambda song: self._score_song(user, song),
            reverse=True,
        )
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        return _build_explanation(
            user_genre=user.favorite_genre,
            user_mood=user.favorite_mood,
            target_energy=user.target_energy,
            likes_acoustic=user.likes_acoustic,
            song=_song_to_dict(song),
        )


def load_songs(csv_path: str) -> List[Dict]:
    """Loads songs from a CSV file and returns a list of dictionaries."""
    songs: List[Dict] = []

    with open(csv_path, "r", encoding="utf-8", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            songs.append(
                {
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
                }
            )

    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Scores a single song against user preferences."""
    score = 0.0
    reasons: List[str] = []

    user_genre = user_prefs.get("genre")
    user_mood = user_prefs.get("mood")
    target_energy = user_prefs.get("energy")
    likes_acoustic = user_prefs.get("likes_acoustic")

    if user_genre and song["genre"].strip().lower() == user_genre.strip().lower():
        score += 40.0
        reasons.append("genre match")

    if user_mood and song["mood"].strip().lower() == user_mood.strip().lower():
        score += 25.0
        reasons.append("mood match")

    if target_energy is not None:
        energy_points = _closeness_score(float(song["energy"]), float(target_energy), 20.0)
        score += energy_points
        if energy_points >= 16:
            reasons.append("very close energy")
        elif energy_points >= 8:
            reasons.append("fairly close energy")

    if likes_acoustic is not None:
        acoustic_match = (
            likes_acoustic and float(song["acousticness"]) >= 0.60
        ) or (
            not likes_acoustic and float(song["acousticness"]) < 0.60
        )
        if acoustic_match:
            score += 10.0
            reasons.append("acoustic preference match")

    return round(score, 4), reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Functional implementation of the recommendation logic."""
    ranked: List[Tuple[Dict, float, str]] = []

    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = _build_explanation(
            user_genre=user_prefs.get("genre"),
            user_mood=user_prefs.get("mood"),
            target_energy=user_prefs.get("energy"),
            likes_acoustic=user_prefs.get("likes_acoustic"),
            song=song,
        )
        ranked.append((song, score, explanation))

    ranked.sort(key=lambda item: item[1], reverse=True)
    return ranked[:k]
