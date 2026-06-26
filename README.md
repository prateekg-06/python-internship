# Python Mini-Projects: Regression, Matrix Tool & Voice Assistant

Three standalone Python projects, each in its own folder with its own
README, dependencies, and instructions.

| # | Project | Folder | Tech |
|---|---|---|---|
| 1 | House Price Prediction (Linear Regression) | [`task1-house-price-regression/`](./task1-house-price-regression) | pandas, scikit-learn, matplotlib, seaborn |
| 2 | Matrix Operations Tool | [`task2-matrix-operations-tool/`](./task2-matrix-operations-tool) | NumPy |
| 3 | Voice-Activated Personal Assistant | [`task3-voice-assistant/`](./task3-voice-assistant) | SpeechRecognition, pyttsx3, requests |

Each folder is fully independent — its own `requirements.txt`, its own
`README.md`, and no shared code between them. You can `cd` into any one
folder and run it on its own.

## Quick start

```bash
git clone <this-repo-url>
cd <repo-name>

# Task 1
cd task1-house-price-regression
pip install -r requirements.txt
# update the CSV path inside house_price_regression.py first — see its README
python house_price_regression.py

# Task 2
cd ../task2-matrix-operations-tool
pip install -r requirements.txt
python matrix_operations_tool.py

# Task 3
cd ../task3-voice-assistant
pip install -r requirements.txt
cp .env.example .env   # then add your OpenWeatherMap / NewsAPI keys
python main.py --text  # or `python main.py` for voice mode
```

## Project summaries

### 1. House Price Prediction
Trains and compares Linear Regression and Ridge Regression models on a
545-row housing dataset (`area`, `bedrooms`, `bathrooms`, `stories`,
amenities, `furnishingstatus`, etc.) to predict `price`. Includes
preprocessing (categorical encoding, IQR-based outlier removal),
5-fold cross-validation, feature-importance ranking, an 8-panel
diagnostic visualization, and a sample prediction for a new house.
Best model achieves R² ≈ 0.66 on this dataset. See the
[task README](./task1-house-price-regression/README.md) for full
details and the **dataset path you need to update before running**.

### 2. Matrix Operations Tool
An interactive CLI built on NumPy supporting addition, subtraction,
matrix multiplication, element-wise multiplication, transpose,
determinant, inverse, eigenvalues/eigenvectors, rank, and trace —
with input validation and boxed, readable output. See the
[task README](./task2-matrix-operations-tool/README.md).

### 3. Voice-Activated Personal Assistant
A wake-word-driven assistant (default wake word: "jarvis") that sets
and tracks reminders (persisted to disk, fires in the background),
checks the weather (OpenWeatherMap), and reads news headlines
(NewsAPI), using `SpeechRecognition` for speech-to-text and `pyttsx3`
for offline text-to-speech. Includes a `--text` mode for testing
without a microphone. See the
[task README](./task3-voice-assistant/README.md).

## Repo structure

```
.
├── README.md                          <- you are here
├── task1-house-price-regression/
│   ├── house_price_regression.py
│   ├── data/
│   │   └── house.csv
│   ├── requirements.txt
│   └── README.md
├── task2-matrix-operations-tool/
│   ├── matrix_operations_tool.py
│   ├── requirements.txt
│   └── README.md
└── task3-voice-assistant/
    ├── main.py
    ├── assistant/
    │   ├── __init__.py
    │   ├── config.py
    │   ├── speech_io.py
    │   ├── commands.py
    │   ├── reminders.py
    │   ├── weather.py
    │   └── news.py
    ├── requirements.txt
    ├── .env.example
    └── README.md
```
