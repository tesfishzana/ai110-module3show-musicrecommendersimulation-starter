# Music Recommender — Data Flow

```mermaid
flowchart TD
    UP["User Preferences
    genre · mood · energy · likes_acoustic"]
    CSV["songs.csv"]

    CSV --> LOAD["load_songs()
    csv.DictReader → List[Dict]"]
    LOAD --> CAT["Song Catalog
    18 song dicts"]

    UP  --> RS["recommend_songs(user_prefs, songs, k)"]
    CAT --> RS

    RS --> LOOP["for song in songs"]

    subgraph SCORING["score_song(song, user_prefs)"]
        direction TB
        INIT["score = 0.0  ·  reasons = []"]
        INIT --> GEN{"song.genre == user.genre?"}
        GEN -- "Yes  +2.0" --> MOO{"song.mood == user.mood?"}
        GEN -- "No   +0.0" --> MOO
        MOO -- "Yes  +1.0" --> ENE["energy_score =
        max(0,  1.0 − |song.energy − target|)
        score += energy_score  (up to +1.0)"]
        MOO -- "No   +0.0" --> ENE
        ENE --> ACO{"likes_acoustic AND
        acousticness ≥ 0.6?"}
        ACO -- "Yes  +0.5" --> EXP["', '.join(reasons)
        return score, explanation"]
        ACO -- "No   +0.0" --> EXP
    end

    LOOP    --> SCORING
    SCORING --> APP["scored.append((song, score, explanation))"]
    APP     --> MORE{"More songs?"}
    MORE -- "Yes" --> LOOP
    MORE -- "No"  --> SORT["scored.sort(key=score, reverse=True)"]
    SORT  --> SLICE["scored[:k]"]
    SLICE --> OUT["Top K Output
    Title — Score: X.XX
    Because: reason1, reason2, ..."]
```

## Score breakdown

| Signal | Points | Formula |
|---|---|---|
| Genre match | +2.0 | exact string match |
| Mood match | +1.0 | exact string match |
| Energy similarity | up to +1.0 | `max(0, 1.0 − \|Δenergy\|)` |
| Acoustic bonus | +0.5 | `likes_acoustic=True` and `acousticness ≥ 0.6` |
| **Max possible** | **4.5** | |
