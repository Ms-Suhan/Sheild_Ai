# Shelid AI — SMS Spam Detector

A machine-learning web application that classifies SMS messages as **spam** or **not spam**. Built with Python, Streamlit, and scikit-learn, Shelid AI provides a simple interface for checking suspicious messages.

## Features

- **SMS classification** — predicts whether a message is spam or not spam.
- **Text preprocessing** — lowercases text, tokenizes words, removes English stopwords and punctuation/non-alphanumeric tokens, and applies Porter stemming.
- **TF-IDF vectorization** — transforms processed text into features for the trained classifier.
- **Interactive web UI** — includes sample messages, prediction feedback, and a responsive dark-themed interface.
- **Local inference** — prediction runs using the saved model and vectorizer files; no external prediction API is required.

## Tech Stack

- Python
- Streamlit
- scikit-learn
- NLTK
- TF-IDF
- Multinomial Naive Bayes (if this is the model saved in `model.pkl`)

## Project Structure

```text
sms-spam-classifier/
├── app.py                 # Streamlit application
├── model.pkl              # Trained scikit-learn model
├── vectorizer.pkl         # Fitted TF-IDF vectorizer
├── requirements.txt       # Python dependencies (recommended)
└── README.md
```

> Keep `model.pkl` and `vectorizer.pkl` in the same directory as `app.py`. These files must be generated from compatible training code: the model must be fitted, and the vectorizer must match the model's expected feature representation.

## Getting Started

### 1. Clone the repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd sms-spam-classifier
```

Replace `<YOUR_REPOSITORY_URL>` with your Git repository URL and update the directory name if needed.

### 2. Create and activate a virtual environment

**Linux / macOS**
```bash
python -m venv venv
source venv/bin/activate
```

**Windows (PowerShell)**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

If the project has a `requirements.txt` file:

```bash
pip install -r requirements.txt
```

Otherwise, install the main dependencies:

```bash
pip install streamlit scikit-learn nltk
```

### 4. Check required files

Confirm the following files are present:

```text
app.py
model.pkl
vectorizer.pkl
```

The saved model must be trained before it can make predictions. If you see a `NotFittedError`, regenerate `model.pkl` from a fitted model and ensure both `.pkl` files belong to the same training pipeline.

### 5. Run the application

```bash
streamlit run app.py
```

Streamlit will print a local URL, usually `http://localhost:8501`. Open it in your browser.

## How It Works

1. The user enters an SMS message or selects a sample.
2. The app converts the message to lowercase and tokenizes it with NLTK.
3. English stopwords and non-alphanumeric tokens are removed.
4. Remaining tokens are stemmed using `PorterStemmer`.
5. The fitted TF-IDF vectorizer converts the processed message into numerical features.
6. The trained classifier predicts the label.
7. The interface displays whether the message was classified as spam or not spam.

### Prediction labels

The app expects the model to use these labels:

- `1` — spam
- `0` — not spam

If your training dataset uses a different label mapping, update the result-handling code in `app.py`.

## Model and Data

The repository uses two serialized artifacts:

- `model.pkl` — the fitted classification model.
- `vectorizer.pkl` — the fitted TF-IDF vectorizer used during training.

The app does not train the model at startup. Train the model in your notebook or training script, then save both artifacts. Use the same text-cleaning steps for training and inference; mismatched preprocessing can reduce prediction quality.

If you are using a notebook for model training, include it in the repository if appropriate, along with the dataset source and training instructions. Do not commit private data or datasets whose licenses do not allow redistribution.

## Requirements

Recommended Python packages:

```text
streamlit
scikit-learn
nltk
```

You can create a `requirements.txt` file with those package names, or pin the exact versions from your working environment for more reproducible installs.

NLTK may need to download its English stopwords and tokenizer data on first use. Ensure the runtime environment can access those resources, or download the resources ahead of time.

## Limitations

- Predictions are estimates, not guarantees that a message is safe or malicious.
- Model performance depends on the quality, coverage, and balance of the training dataset.
- New spam patterns, shortened URLs, misspellings, and other languages may not be handled well unless represented in the training data.
- Avoid entering sensitive personal information into demo or shared deployments.
- Only use model and dataset files from trusted sources. Loading pickle files from untrusted sources can execute malicious code.

## Future Improvements

- Display prediction confidence or class probabilities when supported by the model.
- Add evaluation metrics such as precision, recall, F1-score, and a confusion matrix.
- Add a history page for previous predictions, with clear privacy controls.
- Improve accessibility and mobile layout.
- Add automated tests for preprocessing and prediction behavior.
- Deploy the app using Streamlit Community Cloud or another hosting platform.

## Contributing

Contributions and suggestions are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Make your changes and test the app.
4. Open a pull request describing the changes.

## License

Add a license file (for example, MIT) if you want others to reuse and modify this project. Do not claim a license until you have selected and included one.

---

**Built with Python, Streamlit, NLTK, and scikit-learn.**
