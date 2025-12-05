# ✨ Davison Synastry Mapper

A custom-built astrology tool designed to map **planets into houses across multiple charts**  
(`A`, `B`, `Composite`, and `Davison`) and compare relational dynamics based on house placement.

You can input:

- House cusps (with automatic opposite cusp generation)
- Planetary placements (free-naming allowed)
- Any number of celestial bodies — not restricted to traditional planets.

The tool will automatically:

- Convert zodiac signs into absolute degree positions
- Determine house placement distance from cusp
- Sort results by proximity to the house cusp
- Generate a clean table output
- Export a **multi-sheet Excel file (XLSX)** with one sheet per chart reference mode.


---

## 🚀 Features

| Feature | Supported |
|--------|:--------:|
| Manual house cusp entry | ✔ |
| Auto-generation of opposite cusps (7–12H) | ✔ |
| Free-form planet entry | ✔ |
| Synastry house mapping | ✔ |
| Sorting by cusp distance | ✔ |
| Display by reference mode (A/B/Composite/Davison) | ✔ |
| XLSX export (multi-sheet) | ✔ |
| Deletes, editing refresh | ✔ |
| Unicode zodiac symbols | ✔ |


---

## 🧭 How It Works

### Step 1 — Enter House Cusps  
Every chart gets its own house cusps.  
Only Houses **1–6** are manually entered — Houses **7–12** auto-mirror.

Example:

| Input | Auto |
|-------|------|
| `1H Aries 10°` | `7H Libra 10°` |
| `2H Taurus 22°` | `8H Scorpio 22°` |
| ... | ... |


### Step 2 — Enter Planets
You can input **any object**, e.g.:
Sun
Venus
Black Moon Lilith
Vertex
Part of Fortune
Asteroid 588 Achilles
My Cat's Natal Pluto (lol)


The system doesn't validate astronomical correctness — it's intentionally flexible.


### Step 3 — Results & Export

You can:

- View synastry based on selected reference chart
- See sorted planets in each house
- Export to XLSX file containing four sheets:

A.xlsx
B.xlsx
Composite.xlsx
Davison.xlsx





---

## 📁 File Output Example (Sheet Format)

| House | A | B | Composite | Davison |
|-------|----|----|-----------|---------|
| **1H (♈ 10°22′)** | Sun ♈ 12°03′ | Venus ♈ 13°55′ | — | — |
|  | Mars ♈ 18°11′ | — | Moon ♈ 19°40′ | — |
| **2H (♉ 03°09′)** | Jupiter ♉ 5°44′ | Saturn ♉ 7°33′ | — | — |
| ... | ... | ... | ... | ... |

---

## ⚙ Requirements

Create a new virtual environment (optional but recommended):

```sh
python -m venv venv
source venv/bin/activate  # or: venv\Scripts\activate on Windows


Install dependencies:

pip install -r requirements.txt

requirements.txt
streamlit
pandas
openpyxl
(Yes — only 3 packages.)


▶ Running the App

streamlit run app.py

📝 Notes

This project is not tied to fixed astrology systems (Whole Sign, Placidus, etc.)
— it simply maps defined positions to cusps you provide.

Best for relationship analysis, asteroids, hypothetical objects, and experimental astrology research.

📌 License

MIT License — free to modify and use.

💫 Contributions

Ideas, features, and UX improvements welcome — open an issue or PR.

⭐ If you use this tool and love it...

Consider starring the repo ♥
You can input **any object**, e.g.:

