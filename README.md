# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

### What features does each Song use?

Every song in the catalog is described by ten attributes. Three of them are just identity information — the id, title, and artist — and are not used for matching. The remaining seven are the ones that actually drive recommendations:

- **Genre** — a label like "pop", "lofi", or "rock" that broadly categorizes the song's style.
- **Mood** — a label like "happy", "chill", or "intense" that describes the emotional tone.
- **Energy** — a number between 0.0 and 1.0. A low value means calm and quiet; a high value means loud and driving.
- **Tempo (BPM)** — the speed of the song in beats per minute. Faster songs have higher values.
- **Valence** — a number between 0.0 and 1.0 that measures how musically positive or upbeat a song feels.
- **Danceability** — a number between 0.0 and 1.0 that reflects how well the song works for dancing.
- **Acousticness** — a number between 0.0 and 1.0. High means the song relies on acoustic instruments; low means it is largely electronic.

### What does a UserProfile store?

A user profile captures four things about a listener's taste:

- **Favorite genre** — the genre they want their recommendations to come from, such as "pop".
- **Favorite mood** — the emotional tone they are looking for right now, such as "happy" or "chill".
- **Target energy** — a number from 0.0 to 1.0 representing how energetic they want the music to feel.
- **Likes acoustic** — a simple yes or no for whether they prefer acoustic sounds over electronic ones.

### How does the Recommender compute a score for each song?

For every song in the catalog, the recommender calculates a score by comparing the song's features against the user's profile. Songs that match closely get a higher score; songs that are a poor fit get a lower one.

The scoring works in four steps:

1. **Genre match** — if the song's genre matches the user's favorite genre, it gets a large bonus. This is weighted the highest because genre is the strongest signal of personal taste.
2. **Mood match** — if the song's mood matches the user's favorite mood, it gets another sizable bonus. Mood captures the listener's context, such as whether they want something to focus to or something to celebrate with.
3. **Energy proximity** — instead of rewarding songs with more or less energy, the score rewards songs that are *closest* to the user's target. A song at exactly the target energy scores a full point; the further away it is, the lower the score.
4. **Acoustic preference** — if the user likes acoustic music, songs with high acousticness score higher. If the user prefers electronic sounds, songs with low acousticness score higher.

### Algorithm Recipe

The four signals are combined into a single numeric score for every song. Higher is better.

| Signal | Points | How it is calculated |
|---|---|---|
| Genre match | +2.0 | Exact string match between `song.genre` and `user.genre`. All-or-nothing. |
| Mood match | +1.0 | Exact string match between `song.mood` and `user.mood`. All-or-nothing. |
| Energy similarity | up to +1.0 | `max(0, 1.0 − |song.energy − user.energy|)`. A perfect match scores 1.0; a song that is 0.5 off scores 0.5; fully opposite scores 0.0. |
| Acoustic bonus | +0.5 | Added only when `user.likes_acoustic = True` and `song.acousticness >= 0.6`. |
| **Maximum possible** | **4.5** | Genre + mood + perfect energy + acoustic bonus. |

**Why these weights?** Genre is weighted the highest because it is the most deliberate signal — a user who says "lofi" has already made a strong statement. Mood gets half the genre weight because it is more contextual and shifts by activity or time of day. Energy uses a gradient so that songs close-but-not-perfect still surface. The acoustic bonus is kept small so it can break ties without overriding stronger matches.

### Potential Biases

- **Genre dominance.** The +2.0 genre bonus is the single largest weight. A song with the right genre but the wrong mood and poor energy (theoretical score: ~3.0) can still outrank a perfect mood-and-energy match in a different genre (theoretical score: ~2.0). Great songs outside the user's stated genre are systematically disadvantaged.
- **Sparse catalog amplifies exact-match luck.** With only 18 songs and 15 genres, most genres appear only once. If that one song happens to also miss on mood, the user gets a lower-ranked result — not because the genre is a bad fit, but because the catalog is too small to find a good genre-and-mood pair.
- **Mood and genre are all-or-nothing.** The scoring gives full points or zero — there is no partial credit for related genres (e.g., "indie pop" vs "pop") or related moods (e.g., "chill" vs "relaxed"). Songs that are semantically close but lexically different are penalized as hard misses.
- **Energy is the only continuous signal.** Tempo, valence, and danceability are loaded from the CSV but ignored by the scorer. A high-tempo, high-valence song and a low-tempo, low-valence song can receive identical energy scores if their energy values happen to be equal.
- **Acoustic preference is binary.** `likes_acoustic` is a yes/no flag. A user who moderately enjoys acoustic elements gets the same treatment as one who exclusively seeks out unplugged recordings.

### How do we choose which songs to recommend?

Once every song has a score, the recommender sorts the full catalog from highest score to lowest and returns the top five results. Songs that matched on genre and mood and were close to the user's energy target will naturally rise to the top. Songs that missed on multiple features will fall to the bottom and not appear in the results.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"




