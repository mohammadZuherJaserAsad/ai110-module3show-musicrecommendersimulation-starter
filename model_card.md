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

The dataset contains **10 songs** in `data/songs.csv`. The catalog includes genres such as pop, lofi, rock, ambient, jazz, synthwave, and indie pop. The moods include happy, chill, intense, relaxed, focused, and moody.

I did not add or remove songs from the starter dataset. Because the dataset is tiny, it only reflects a narrow slice of musical taste. It does not include many cultural styles, languages, or niche genres, so the recommendations are limited by what is present in the file.

---

## 5. Strengths

The recommender works well when the user's preferences closely match the available song features. For example, a user who likes pop, happy songs with high energy should receive strong matches near the top. The system is also easy to understand because every recommendation can be traced back to clear scoring rules.

Another strength is transparency. Since the logic is rule-based, it is easy to explain why a song ranked highly. That makes this simulation good for learning how recommendation systems work.

---

## 6. Limitations and Bias

This recommender only uses a few features, so it ignores many things people care about, such as lyrics, language, artist loyalty, release date, listening context, or whether the user wants variety. It also assumes a person has one stable taste profile, which is not realistic.

The dataset itself is small and uneven, so some genres or moods may be underrepresented. That means the system can accidentally favor the kinds of songs that appear more often in the dataset. If a real product used a narrow dataset like this, some users would receive weaker recommendations simply because their tastes were not well represented.

---

## 7. Evaluation

I evaluated the system by thinking through several user profiles and checking whether the top results matched common sense. For a pop, happy, high-energy user, I expected songs like **Sunrise City** and **Rooftop Lights** to score well. For a chill, more acoustic listener, I expected lofi and ambient tracks to feel more appropriate.

I also used the included tests to make sure the recommender returns results in sorted order and produces a non-empty explanation. I did not use a numeric metric, because the goal of this project was to understand the logic and behavior of the recommender rather than optimize benchmark performance.

---

## 8. Future Work

If I had more time, I would let users express multiple favorite genres or moods instead of just one. I would also add more features, such as tempo ranges, lyric themes, or recent listening behavior. Another useful improvement would be to increase diversity so that the top results are not all too similar.

I would also improve the explanation system so it could be more specific and more natural. In a larger project, I would want the recommender to balance relevance with discovery so users can still find unexpected songs they might enjoy.

---

## 9. Personal Reflection

This project taught me that recommenders are really about turning structured data into a ranking decision. Even a small rule-based system can feel surprisingly realistic when the features match how people think about music, like genre, mood, and energy.

Something that stood out to me was how much the final recommendations depend on the scoring weights. A small change in those weights can change the entire ranking. It also made me more aware of how bias can appear, not just from bad intentions, but from small datasets and design choices that leave out certain users or styles.
