# Music Recommender Simulation

## Project Summary

In this project, I built a small music recommender that simulates how a simple content-based recommendation system works. The program reads song data from a CSV file, compares each song to a user's taste profile, and ranks songs based on how well they match the user's preferences. My version focuses on genre, mood, energy, and acousticness to generate recommendations and explain why each result was chosen.

---

## Data Flow

```mermaid
flowchart TD
    A([User Preferences\ngenre · mood · energy · acoustic]) --> B[Load songs.csv\n18 songs]
    B --> C{For each song in catalog}
    C --> D1[Genre match?\n+40 pts]
    C --> D2[Mood match?\n+25 pts]
    C --> D3[Energy closeness\nup to +20 pts]
    C --> D4[Acoustic preference match?\n+10 pts]
    D1 & D2 & D3 & D4 --> E[Total Score per Song]
    E --> C
    C --> F[Sort all songs\nhighest score first]
    F --> G([Top K Recommendations\nwith explanations])
```

---

## How The System Works

Real-world recommendation systems often combine collaborative filtering and content-based filtering. Collaborative filtering uses the behavior of many users, such as likes, skips, playlists, and replay history, to find patterns. Content-based filtering focuses on the features of the item itself, such as genre, mood, energy, or tempo. This project uses a content-based approach because it is easier to understand and fits the small classroom dataset.

In my simulation, each `Song` stores the song's title, artist, genre, mood, energy, tempo, valence, danceability, and acousticness. The `UserProfile` stores a favorite genre, favorite mood, target energy, and whether the user prefers acoustic songs. The recommender computes a weighted score for every song. A matching genre is worth the most points, a matching mood is worth the next most, and songs get additional points when their energy is close to the user's target energy. The system also gives a smaller bonus when the song matches the user's acoustic preference. After scoring all songs, it sorts them from highest to lowest score and returns the top recommendations.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

```bash
python -m venv .venv
source .venv/bin/activate      # Mac or Linux
.venv\Scripts\activate         # Windows
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Sample Terminal Output

Running `python -m src.main` with the default pop/happy profile produces:

```
Loaded songs: 18

User profile: genre=pop | mood=happy | energy=0.8 | acoustic=False
------------------------------------------------------------

Top 5 Recommendations:

#1  Sunrise City by Neon Echo
     Score : 94.60
     Reasons: [genre match], [mood match], [very close energy], [acoustic preference match]
     Why   : Recommended because the genre matches your taste, the mood matches what you want, the energy level is very close to your preference, it is less acoustic and more polished/produced.

#2  Gym Hero by Max Pulse
     Score : 67.40
     Reasons: [genre match], [very close energy], [acoustic preference match]
     Why   : Recommended because the genre matches your taste, the energy level is reasonably close to your preference, it is less acoustic and more polished/produced.

#3  Rooftop Lights by Indigo Parade
     Score : 54.20
     Reasons: [mood match], [very close energy], [acoustic preference match]
     Why   : Recommended because the mood matches what you want, the energy level is very close to your preference, it is less acoustic and more polished/produced.

#4  Streetlight Hustle by DAZE
     Score : 29.80
     Reasons: [very close energy], [acoustic preference match]
     Why   : Recommended because the energy level is very close to your preference, it is less acoustic and more polished/produced.

#5  Night Drive Loop by Neon Echo
     Score : 29.00
     Reasons: [very close energy], [acoustic preference match]
     Why   : Recommended because the energy level is very close to your preference, it is less acoustic and more polished/produced.
```

---

### Running Tests

Run the tests with:

```bash
pytest
```

---

## Experiments You Tried

I tested the system with five profiles: **High-Energy Pop**, **Chill Lofi**, **Deep Intense Rock**, and two edge cases — a conflicting "Sad but Hype" electronic profile and a niche "Acoustic Classical" profile. Here are the results for each:

### Profile 1 — High-Energy Pop
```
genre=pop | mood=happy | energy=0.8 | acoustic=False

#1  Sunrise City by Neon Echo        Score: 94.60  [genre match], [mood match], [very close energy], [acoustic preference match]
#2  Gym Hero by Max Pulse             Score: 67.40  [genre match], [very close energy], [acoustic preference match]
#3  Rooftop Lights by Indigo Parade   Score: 54.20  [mood match], [very close energy], [acoustic preference match]
#4  Streetlight Hustle by DAZE        Score: 29.80  [very close energy], [acoustic preference match]
#5  Night Drive Loop by Neon Echo     Score: 29.00  [very close energy], [acoustic preference match]
```

### Profile 2 — Chill Lofi
```
genre=lofi | mood=chill | energy=0.4 | acoustic=True

#1  Midnight Coding by LoRoom         Score: 94.60  [genre match], [mood match], [very close energy], [acoustic preference match]
#2  Library Rain by Paper Lanterns    Score: 94.00  [genre match], [mood match], [very close energy], [acoustic preference match]
#3  Focus Flow by LoRoom              Score: 70.00  [genre match], [very close energy], [acoustic preference match]
#4  Spacewalk Thoughts by Orbit Bloom Score: 52.60  [mood match], [very close energy], [acoustic preference match]
#5  Monsoon Letters by Arya Sen       Score: 29.80  [very close energy], [acoustic preference match]
```

### Profile 3 — Deep Intense Rock
```
genre=rock | mood=intense | energy=0.9 | acoustic=False

#1  Storm Runner by Voltline          Score: 94.80  [genre match], [mood match], [very close energy], [acoustic preference match]
#2  Gym Hero by Max Pulse             Score: 54.40  [mood match], [very close energy], [acoustic preference match]
#3  Iron Cathedral by Blackvein       Score: 53.60  [mood match], [very close energy], [acoustic preference match]
#4  Wildfire Dance by Cruz Tempo      Score: 29.60  [very close energy], [acoustic preference match]
#5  Electric Feel by Nova Pulse       Score: 29.20  [very close energy], [acoustic preference match]
```

### Profile 4 — Edge Case: Sad but Hype (conflicting preferences)
```
genre=electronic | mood=sad | energy=0.95 | acoustic=False

#1  Electric Feel by Nova Pulse       Score: 68.20  [genre match], [very close energy], [acoustic preference match]
#2  Gym Hero by Max Pulse             Score: 29.60  [very close energy], [acoustic preference match]
#3  Iron Cathedral by Blackvein       Score: 29.60  [very close energy], [acoustic preference match]
#4  Storm Runner by Voltline          Score: 29.20  [very close energy], [acoustic preference match]
#5  Wildfire Dance by Cruz Tempo      Score: 28.60  [very close energy], [acoustic preference match]
```
*No song in the catalog has mood=sad, so the mood weight went entirely unused.*

### Profile 5 — Edge Case: Acoustic Classical (niche)
```
genre=classical | mood=calm | energy=0.15 | acoustic=True

#1  Pastel Afternoon by Yuki Mori     Score: 93.60  [genre match], [mood match], [very close energy], [acoustic preference match]
#2  Spacewalk Thoughts by Orbit Bloom Score: 27.40  [very close energy], [acoustic preference match]
#3  Library Rain by Paper Lanterns    Score: 26.00  [very close energy], [acoustic preference match]
#4  Coffee Shop Stories by Slow Stereo Score: 25.60 [fairly close energy], [acoustic preference match]
#5  Monsoon Letters by Arya Sen       Score: 25.20  [fairly close energy], [acoustic preference match]
```
*Only one classical song exists, so #2–5 scored only on energy + acoustic proximity — no genre or mood match.*

---

### Weight-Shift Experiment

I tested halving the genre weight (40→20) and doubling the energy weight (20→40) for the High-Energy Pop profile:

```
EXPERIMENT: genre=20pts, energy=40pts (vs. original genre=40, energy=20)

#1  Sunrise City        Score: 94.20  (unchanged at top — matches genre+mood+energy)
#2  Rooftop Lights      Score: 73.40  (moved UP from #3 — better energy 0.76 vs target 0.8)
#3  Gym Hero            Score: 64.80  (moved DOWN from #2 — energy 0.93 is further from 0.8)
#4  Streetlight Hustle  Score: 49.60
#5  Night Drive Loop    Score: 48.00
```

**Finding:** When energy is weighted higher, **Rooftop Lights** jumps above **Gym Hero** because its energy (0.76) is closer to the target (0.8) than Gym Hero's (0.93). This shows the genre weight was masking an energy mismatch in Gym Hero's ranking.

---

## Limitations and Risks

This recommender only works on a very small catalog, so it cannot represent the full range of musical taste. It also does not understand lyrics, language, artist popularity, listening history, or changing preferences over time. Because the score is based on a few fixed rules, it may over-favor one genre or mood and miss songs that are good recommendations for more subtle reasons.

Another limitation is that this system assumes user taste can be captured in a few simple fields. Real people often like multiple genres depending on the moment, activity, or context. A real product would also need to avoid creating narrow filter bubbles where users keep seeing the same type of content over and over.

---

## Reflection

This project helped me understand how recommendation systems turn input data into predictions. Even a simple system can feel useful when the features and weights make sense. I also learned that small design choices, like how many points to give a genre match, can strongly affect which songs get recommended.

It also made me think more about bias and unfairness in recommender systems. If the dataset is small or unbalanced, the system may unfairly favor certain genres, moods, or listening styles. In real apps, this could limit what users discover and reinforce narrow patterns instead of giving a healthy mix of recommendations.

See the full model card here: [model_card.md](model_card.md)
