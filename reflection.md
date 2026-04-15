# Reflection: Music Recommender Simulation

## Personal Reflection Questions

**What was your biggest learning moment during this project?**

The biggest learning moment was running the weight-shift experiment in Phase 4. When I halved the genre weight (40→20) and doubled the energy weight (20→40), Rooftop Lights jumped above Gym Hero in the rankings for the pop/happy profile. That one small number change exposed a flaw I had not noticed before: Gym Hero's energy (0.93) was actually further from the user's target (0.8) than Rooftop Lights' energy (0.76), but the original genre bonus was so large it masked the mismatch completely. This taught me that scoring weights are not neutral — they encode assumptions about what matters, and those assumptions can quietly produce unfair or inaccurate results without ever throwing an error.

**How did using AI tools help you, and when did you need to double-check them?**

AI tools were genuinely helpful for generating the expanded song catalog (adding 8 songs with diverse genres and moods), drafting the Mermaid flowchart, and thinking through edge cases like conflicting user preferences. They also helped me write clearer explanations of the scoring logic in plain language. However, I had to verify several things carefully. The AI sometimes suggested scoring formulas that were too simplified and would have broken down for edge values like energy=0.0 or energy=1.0. It also generated songs that looked diverse on the surface but repeated the same moods as the starter dataset. I learned to treat AI suggestions as a starting point that needs review, not a finished answer.

**What surprised you about how simple algorithms can still "feel" like recommendations?**

I was genuinely surprised by how natural the output felt when the weights were reasonable. Running the Chill Lofi profile and seeing Midnight Coding and Library Rain at #1 and #2 felt like a real recommendation, even though the system has no understanding of music whatsoever — it just counted feature matches. The same logic that seems trivial on paper (if genre matches, add 40 points) produces output that a human would look at and say "yeah, that makes sense." It made me realize that a large part of what feels like intelligence in AI systems is really pattern matching on well-designed features. The magic is in choosing the right features and weights, not in any deep understanding of the domain.

**What would you try next if you extended this project?**

I would try two things. First, I would replace the binary genre match with a genre similarity matrix, so that "indie pop" and "pop" get partial credit instead of scoring zero relationship. This would make the scoring feel more natural and reduce the sharp drop in result quality when the user's exact genre has few songs. Second, I would add a diversity enforcement rule so the top 5 cannot all come from the same genre. Even if genre-matching songs score highest, forcing at least one out-of-genre result would help users discover music they would not have found otherwise, which is one of the most valuable things a recommender can do.

---

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
