# Model Card: Music Recommender Simulation

## 1. Model Name

**VibeMatch 1.0**

---

## 2. Intended Use

This recommender is designed to suggest a few songs from a small catalog based on a user's preferred genre, mood, target energy level, and acoustic preference. It is intended for classroom exploration only. The goal is not to build a production-quality music recommender, but to show how a simple recommendation system can transform song data and user preferences into ranked results.

It assumes that a user's taste can be represented by a small set of fixed preferences. That assumption is useful for a simulation, but it is much simpler than real-world music behavior.

---

## 3. How the Model Works

The model looks at a song's genre, mood, energy, and acousticness. It compares those features to the user's taste profile and assigns a weighted score. A genre match is worth the most points, because genre is usually the broadest signal of a person's taste. A mood match is also important, and then the model adds points when the song's energy is close to the user's target energy. Finally, it adds a small bonus if the acousticness of the song matches the user's preference for acoustic or less-acoustic music.

After every song receives a score, the recommender sorts the songs from highest to lowest score and returns the top results. It also generates a short explanation that tells the user why a song was recommended.

---

## 4. Data

The dataset contains **18 songs** in `data/songs.csv`. The catalog includes genres such as pop, lofi, rock, ambient, jazz, synthwave, indie pop, r&b, latin, country, metal, classical, hip-hop, electronic, and world. The moods include happy, chill, intense, relaxed, focused, moody, romantic, energetic, melancholic, confident, euphoric, and nostalgic.

The starter dataset was expanded from 10 to 18 songs to improve genre and mood diversity. However, most genres are still represented by only one or two songs, which means the system can still produce thin results for users whose tastes fall outside the two or three best-covered genres.

---

## 5. Strengths

The recommender works well when the user's preferences closely match the available song features. For example, a user who likes pop, happy songs with high energy should receive strong matches near the top. The system is also easy to understand because every recommendation can be traced back to clear scoring rules.

Another strength is transparency. Since the logic is rule-based, it is easy to explain why a song ranked highly. That makes this simulation good for learning how recommendation systems work.

---

## 6. Limitations and Bias

This recommender only uses a few features, so it ignores many things people care about, such as lyrics, language, artist loyalty, release date, listening context, or whether the user wants variety. It also assumes a person has one stable taste profile, which is not realistic.

The dataset itself is small and uneven, so some genres or moods may be underrepresented. That means the system can accidentally favor the kinds of songs that appear more often in the dataset. If a real product used a narrow dataset like this, some users would receive weaker recommendations simply because their tastes were not well represented.

A key weakness discovered during evaluation is that the genre weight (40 points) dominates the scoring so strongly that a perfect genre match alone pushes a song above all non-matching songs, even if its mood, energy, and acoustic qualities are a poor fit. For example, "Gym Hero" (pop, intense, energy=0.93) consistently ranks #2 for a pop/happy/energy=0.8 user, even though its mood is wrong and its energy overshoots the target by 0.13. The 40-point genre bonus makes up for both shortfalls. This creates a filter bubble where users who prefer a single genre will rarely see music from outside it, even when an out-of-genre song might actually feel closer to what they want. Additionally, the edge case test revealed that when a user requests a mood that has no matching songs in the catalog (such as "sad"), the mood weight contributes zero points to every song, effectively reducing the recommender to a three-feature system without any warning to the user.

---

## 7. Evaluation

I evaluated the system by running five distinct user profiles and checking whether the top results matched common sense.

**High-Energy Pop (genre=pop, mood=happy, energy=0.8):** Sunrise City ranked #1 with a near-perfect score of 94.60, hitting all four scoring criteria. This matched expectations. Gym Hero ranked #2 because of the genre bonus despite a mismatched mood, which felt slightly off.

**Chill Lofi (genre=lofi, mood=chill, energy=0.4, acoustic=True):** Both Midnight Coding and Library Rain scored in the mid-90s range. The top 3 were all lofi tracks, which felt very accurate to what this listener would want.

**Deep Intense Rock (genre=rock, mood=intense, energy=0.9):** Storm Runner was the clear #1 and felt correct. The surprise was that only one rock song exists in the catalog, so #2 and #3 were pop and metal songs that shared only the "intense" mood.

**Edge Case — Sad but Hype (genre=electronic, mood=sad, energy=0.95):** No song in the catalog has mood="sad", so the mood weight contributed zero points for every song. The system silently fell back to genre + energy scoring, and the results felt slightly random beyond the genre match. This exposed a real gap in the system.

**Edge Case — Acoustic Classical (genre=classical, mood=calm, energy=0.15):** Only one classical song exists, so Pastel Afternoon was a runaway #1. The rest of the top 5 were unrelated acoustic songs that matched only on energy proximity. The sharp drop from #1 (93.60) to #2 (27.40) shows how thin single-genre coverage is.

I also ran a weight-shift experiment (genre 40→20, energy 20→40) and found that Rooftop Lights jumped above Gym Hero because its energy is actually closer to 0.8. This confirmed that the high genre weight was masking an energy mismatch in the original ranking.

---

## 8. Future Work

If I had more time, I would let users express multiple favorite genres or moods instead of just one. I would also add more features, such as tempo ranges, lyric themes, or recent listening behavior. Another useful improvement would be to increase diversity so that the top results are not all too similar.

I would also improve the explanation system so it could be more specific and more natural. In a larger project, I would want the recommender to balance relevance with discovery so users can still find unexpected songs they might enjoy.

---

## 9. Personal Reflection

This project taught me that recommenders are really about turning structured data into a ranking decision. Even a small rule-based system can feel surprisingly realistic when the features match how people think about music, like genre, mood, and energy.

Something that stood out to me was how much the final recommendations depend on the scoring weights. A small change in those weights can change the entire ranking. It also made me more aware of how bias can appear, not just from bad intentions, but from small datasets and design choices that leave out certain users or styles.
