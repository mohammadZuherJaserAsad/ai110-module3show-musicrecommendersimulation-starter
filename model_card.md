# Model Card: Music Recommender Simulation

---

## 1. Model Name

**VibeMatch 1.0**

---

## 2. Goal / Task

VibeMatch 1.0 tries to predict which songs a user will enjoy based on a few simple taste preferences. Given a user's favorite genre, favorite mood, target energy level, and whether they prefer acoustic music, the system scores every song in the catalog and returns the top matches in ranked order. It also generates a short plain-language explanation for each recommendation so the user understands why a song was suggested.

This is a content-based recommender. It compares song features directly to user preferences rather than relying on what other users have listened to.

---

## 3. Data Used

**Dataset:** `data/songs.csv` — 18 songs

**Features per song:** id, title, artist, genre, mood, energy (0.0–1.0), tempo_bpm, valence, danceability, acousticness (0.0–1.0)

**Genres in catalog:** pop, lofi, rock, ambient, jazz, synthwave, indie pop, r&b, latin, country, metal, classical, hip-hop, electronic, world

**Moods in catalog:** happy, chill, intense, relaxed, focused, moody, romantic, energetic, melancholic, confident, euphoric, calm, nostalgic

**Limits:** Most genres appear only once or twice. The catalog does not include songs in languages other than English, does not represent every cultural style, and has no data on lyrics, artist popularity, or listening history. Because the dataset is so small, the system cannot generalize beyond this narrow slice of music.

---

## 4. Algorithm Summary

The recommender works by giving each song a score based on how well it matches the user's preferences. Here is the scoring recipe in plain language:

- **Genre match → +40 points.** If the song's genre exactly matches the user's favorite genre, it gets the biggest bonus. Genre is treated as the broadest signal of taste.
- **Mood match → +25 points.** If the song's mood matches the user's target mood, it gets the second-largest bonus.
- **Energy closeness → up to +20 points.** The closer the song's energy is to the user's target energy, the more points it earns. A perfect match gives the full 20 points. Songs that are far from the target get zero energy points.
- **Acoustic preference → +10 points.** If the user likes acoustic music and the song has high acousticness (≥0.60), or the user prefers produced music and the song has low acousticness (<0.60), the song gets a small bonus.

After every song is scored, the system sorts them from highest to lowest and returns the top 5. It also generates a sentence explaining which of these four factors applied to each recommendation.

---

## 5. Observed Behavior / Biases

**Genre dominance creates a filter bubble.** The genre weight (40 points) is so large that a song with a matching genre will almost always outrank songs from other genres, even when the other songs are a much better fit for mood and energy. For example, "Gym Hero" (pop, intense, energy=0.93) ranks #2 for a pop/happy/energy=0.8 user even though its mood is wrong and its energy overshoots the target. The genre bonus covers up those mismatches. This means users who pick a popular genre like pop or lofi will see the same songs repeatedly, while users with niche genres will get thin, low-confidence results after the first match.

**Missing moods are silent failures.** When a user's preferred mood does not exist in the catalog (for example, "sad"), the mood weight contributes zero points to every song. The system does not alert the user — it just drops mood from the scoring entirely without saying so. The recommendations look normal but are actually based on only three features.

**Catalog imbalance punishes niche listeners.** For profiles like Acoustic Classical, only one song perfectly matches. The score drops from 93.60 at #1 to 27.40 at #2 — a gap of over 66 points. Users with rare genre preferences will always see one strong result followed by weak fallback suggestions based purely on energy proximity.

---

## 6. Evaluation Process

I tested the system by running five distinct user profiles through the recommender and checking whether the results made intuitive sense.

**High-Energy Pop** (genre=pop, mood=happy, energy=0.8): Sunrise City ranked #1 and felt correct. Gym Hero appeared at #2 despite a mismatched mood, which revealed the genre weight issue.

**Chill Lofi** (genre=lofi, mood=chill, energy=0.4, acoustic=True): The top 3 were all lofi tracks. Results felt accurate and confident.

**Deep Intense Rock** (genre=rock, mood=intense, energy=0.9): Storm Runner ranked #1, which was correct. But only one rock song exists, so #2 and #3 were pop and metal songs connected only by mood.

**Edge Case — Sad but Hype** (genre=electronic, mood=sad, energy=0.95): No song in the catalog has mood=sad, so the mood feature contributed nothing. The system still returned results without warning the user.

**Edge Case — Acoustic Classical** (genre=classical, mood=calm, energy=0.15): Only one classical song exists. The #1 result was a strong match, but #2–5 were generic acoustic songs with no genre or mood connection.

I also ran a weight-shift experiment where I halved the genre weight (40→20) and doubled the energy weight (20→40). The result was that Rooftop Lights moved above Gym Hero for the pop/happy profile, because Rooftop Lights has energy 0.76, which is actually closer to the target of 0.8 than Gym Hero's 0.93. This confirmed that the original genre weight was masking a real energy mismatch.

---

## 7. Intended Use and Non-Intended Use

**Intended use:** This system is designed for classroom exploration of how content-based recommendation systems work. It is meant to help students understand the connection between input features, scoring logic, and ranked output. It is appropriate for learning, experimentation, and discussion about algorithmic bias in small-scale simulations.

**Not intended for:** This system should not be used as a real music discovery product. It should not be used to make decisions about which artists or genres receive exposure on a platform. It is not designed to work with catalogs larger than a few dozen songs, to handle users with complex or shifting tastes, or to represent the diversity of global music. Using it outside of a classroom context could reinforce genre bias and create narrow filter bubbles that harm users with less common musical preferences.

---

## 8. Ideas for Improvement

**Allow multiple favorite genres and moods.** Right now a user can only specify one favorite genre and one mood. Real listeners often enjoy several genres depending on context. Supporting a list of preferences with individual weights would make recommendations much more flexible and personal.

**Add a "missing preference" warning.** When the user's mood or genre does not appear in the catalog, the system should detect this and tell the user instead of silently ignoring it. It could also suggest the closest available mood or genre as an alternative.

**Balance the genre weight.** The 40-point genre bonus is too dominant. Lowering it to around 20–25 points and increasing the energy or mood weight would create more diverse results and reduce the filter bubble effect. Adding a soft penalty when a song misses two or more features would also help prevent poor-fit songs from benefiting too much from a single match.

---

## 9. Personal Reflection

**Biggest learning moment:** The weight-shift experiment was the most eye-opening part of the project. When I halved the genre weight and doubled the energy weight, the ranking changed in a way that actually felt more accurate. Rooftop Lights moved above Gym Hero because its energy was genuinely closer to the target. That moment made it clear that scoring weights are not just numbers — they are design decisions that determine which songs users actually hear. A small change in a single number can shift the entire output of the system.

**How AI tools helped and when I needed to double-check:** AI tools were helpful for generating the expanded song catalog, suggesting the Mermaid flowchart structure, and thinking through edge cases like conflicting user preferences. But I had to verify every suggestion carefully. For the scoring logic, the AI sometimes suggested simpler formulas that would have broken the math for edge cases like energy values at the extremes (0.0 or 1.0). I also had to review the generated songs to make sure they were actually diverse in genre and mood rather than just superficially different names.

**What surprised me about simple algorithms:** I was surprised by how "real" the recommendations felt even though the logic is entirely rule-based. When I ran the Chill Lofi profile and Midnight Coding came out #1, it genuinely felt like a good suggestion. It made me realize that a lot of what feels like intelligence in a recommendation system is really just well-chosen weights applied consistently. The system does not "understand" music at all — it just counts matching features — but when the weights are reasonable, the output mimics good taste surprisingly well.

**What I would try next:** I would add a diversity penalty so that the top 5 results cannot all come from the same genre, forcing the system to surface at least one or two songs from outside the user's comfort zone. I would also try replacing the binary genre match (match = +40, no match = +0) with a genre similarity matrix, so that genres like "indie pop" and "pop" would get partial credit instead of zero, which would make the scoring feel more natural and reduce the sharp cliff between genre-matching and non-matching songs.
