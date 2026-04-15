# Reflection: Music Recommender Simulation

## Profile Comparisons

### High-Energy Pop vs. Chill Lofi

The High-Energy Pop profile (genre=pop, mood=happy, energy=0.8) and the Chill Lofi profile (genre=lofi, mood=chill, energy=0.4) produced completely different top results with almost no overlap. The pop profile surfaced Sunrise City and Gym Hero, while the lofi profile surfaced Midnight Coding and Library Rain. This makes sense because the two profiles differ on every single feature: genre, mood, energy, and acoustic preference. The genre weight being the highest factor (40 points) means these two users will almost never share a recommendation unless the catalog has a song that blurs the line between genres. The output difference is valid and is exactly what the system should do.

### Deep Intense Rock vs. Edge Case: Sad but Hype

Both of these profiles target high-energy, non-acoustic songs. The rock profile (genre=rock, mood=intense, energy=0.9) placed Storm Runner at #1 with a full 4-factor match. The Sad but Hype profile (genre=electronic, mood=sad, energy=0.95) placed Electric Feel at #1 on genre+energy alone, since no song in the catalog has mood=sad. The key difference is that the rock profile got a valid mood match, while the electronic/sad profile did not. As a result, the rock rankings feel more meaningful and confident, while the sad/electronic rankings feel thin. This comparison revealed that the system does not warn the user when their mood preference matches nothing in the catalog — it just silently scores as if mood does not exist.

### Chill Lofi vs. Edge Case: Acoustic Classical

Both profiles prefer acoustic sounds and low energy, so you might expect them to overlap. And they do — Library Rain, Spacewalk Thoughts, and Monsoon Letters appear in both top-5 lists. The big difference is that the lofi profile had three genre-matching lofi songs to pull from, giving it high-confidence results in positions #1–3. The classical profile had only one matching song (Pastel Afternoon at #1), and then dropped sharply to general acoustic/low-energy songs for positions #2–5. This shows that the quality of recommendations depends heavily on how many songs in the catalog match the user's genre. A user with a rare or niche genre preference will always see a steep quality drop after the first position. In a real app, this would be a serious problem for listeners who prefer less popular genres.

---

## Key Takeaways

**The genre weight is too dominant.** At 40 points, a single genre match outweighs a perfect mood (25 pts) and a perfect energy score (20 pts) combined. This means a song with a matching genre but mismatched mood and wrong energy can still rank above a song that nails the mood and energy but belongs to a slightly different genre. For a real recommender, I would lower the genre weight or add a penalty when other features miss badly.

**Missing moods are invisible.** When a user requests a mood that does not exist in the catalog, the system does not say anything. It just recommends songs as if mood was never a preference. A better system would detect this and either tell the user, expand the catalog, or increase the weight of the remaining features to compensate.

**Small catalogs create false confidence.** Songs like Gym Hero or Storm Runner appear in the top 3 for multiple unrelated profiles simply because the dataset does not have enough variety. A song can rank highly not because it is a great match, but because it is one of the few options that scores at all. Real recommendation systems need large, balanced catalogs to avoid this.

**Weight shifts change the story.** Doubling the energy weight moved Rooftop Lights above Gym Hero for the pop/happy profile. This small change revealed that Gym Hero's energy (0.93) is actually further from the user's target (0.8) than it appears. Scoring weights are not just numbers — they decide whose music gets heard and whose does not.
