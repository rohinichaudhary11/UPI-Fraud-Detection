<div align="center">

# 💳 UPI Fraud Detection
### ML-powered transaction screening for faster, clearer fraud-risk assessment.

[![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/) [![Flask](https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com/) [![scikit--learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikit-learn&logoColor=111111)](https://scikit-learn.org/)
[![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white)](https://pandas.pydata.org/) [![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white)](https://numpy.org/) [![Render](https://img.shields.io/badge/Render-46E3B7?style=flat-square&logo=render&logoColor=111111)](https://render.com/)

UPI Fraud Detection analyzes transaction details with a trained scikit-learn pipeline and balance-validation rules to estimate fraud risk through a simple browser interface and JSON API.

🌐 **Live application:** [Open UPI Fraud Detection](https://upi-fraud-detection-rohini.onrender.com) · [Health endpoint](https://upi-fraud-detection-rohini.onrender.com/health)

🎬 **Project walkthrough:** [Watch the demo on YouTube](https://www.youtube.com/watch?v=Zj5BvuGiDOg&t=1352s)

**[Features](#-features) · [Workflow](#-prediction-workflow) · [Tech Stack](#️-tech-stack) · [API](#-api) · [Installation](#️-installation) · [Documentation](#-documentation)**

* * *

</div>

## 📖 Overview

Digital payment platforms make transactions convenient, but they also increase the need for fast and reliable fraud screening. This project classifies UPI-style transactions as legitimate or fraudulent by combining a serialized machine-learning pipeline with balance-consistency checks.

## ✨ Features

- 💳 Predict whether a transaction is fraudulent or legitimate
- 🤖 Scikit-learn-based fraud classification
- 📈 Estimated fraud probability
- ⚡ Instant predictions through a Flask web interface
- 🔍 Balance-consistency rules with explanations
- ✅ Validation for missing, negative, malformed, and non-finite values
- 📊 Derived transaction features for model inference
- 🩺 Health endpoint for service and model readiness
- ☁️ Ready for cloud deployment on Render
- 📱 Responsive browser experience

---

## 🏗️ Prediction Workflow

```text
Transaction Details
        │
        ▼
Input Validation & Feature Derivation
        │
        ▼
Balance-Consistency Rules
        │
        ▼
Trained scikit-learn Pipeline
        │
        ▼
Fraud Probability & Explanation
```

---

## 🛠️ Tech Stack

| Domain | Technologies Used |
| --- | --- |
| Backend | Python 3.11, Flask 2.2.5, Gunicorn 23.0.0 |
| Machine Learning | scikit-learn 1.2.2, joblib, supervised classification |
| Data Processing | NumPy 1.26.4, Pandas 2.2.3 |
| Frontend | HTML5, CSS3, JavaScript |
| Validation | Flask request validation, balance-consistency rules |
| Deployment | Render, `render.yaml` |

---

## 📂 Project Structure

```text
UPI-Fraud-Detection/
├── README.md
├── render.yaml
└── UPI-Fraud-Detection-main/
    └── UPI-Fraud-Detection-main/
        ├── app.py
        ├── model/
        │   └── fraud_pipeline.pkl
        ├── templates/
        │   └── index.html
        ├── static/
        ├── datatset/
        ├── notebook/
        ├── requirements.txt
        ├── run_local.bat
        └── LOCAL_SETUP.md
```

---

## 🔌 API

### `POST /predict`

Send transaction type and balance values as JSON:

```json
{
  "type": "TRANSFER",
  "amount": 100,
  "oldbalanceOrg": 500,
  "newbalanceOrig": 400,
  "oldbalanceDest": 200,
  "newbalanceDest": 300
}
```

The response includes `is_fraud`, `probability`, `rule_flagged`, `rule_reason`, and the derived features used for prediction.

### `GET /health`

Returns service and model readiness information.

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/rohinichaudhary11/UPI-Fraud-Detection.git
cd UPI-Fraud-Detection/UPI-Fraud-Detection-main/UPI-Fraud-Detection-main
```

### 2. Create a Python 3.11 environment

```bash
py -3.11 -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Start the application

```bash
python app.py
```

Then open [http://127.0.0.1:5000](http://127.0.0.1:5000). You can also use `run_local.bat` on Windows for the local setup flow.

> The saved pipeline is version-sensitive, so use the pinned dependency versions from `requirements.txt`.

---

## 📈 Future Enhancements

- Fraud risk score instead of binary prediction
- Explainable AI and feature importance
- Real-time transaction monitoring
- Expanded REST API support
- Fraud analytics dashboard
- User authentication and transaction history
- Docker support
- Additional cloud deployment targets
- Payment gateway integrations

---

## ⭐ Support

If this project is useful to you, consider giving the repository a star and sharing feedback through GitHub Issues.

---

## 📚 Documentation

- [Live application](https://upi-fraud-detection-rohini.onrender.com)
- [Health endpoint](https://upi-fraud-detection-rohini.onrender.com/health)
- [Local setup guide](UPI-Fraud-Detection-main/UPI-Fraud-Detection-main/LOCAL_SETUP.md)
- [Dependency reference](UPI-Fraud-Detection-main/UPI-Fraud-Detection-main/requirements.txt)
- [Project walkthrough](https://www.youtube.com/watch?v=Zj5BvuGiDOg&t=1352s)

---

## 🤝 Contributing

Contributions, feature requests, and improvements are welcome. Fork the repository, create a focused feature branch, test your changes, and open a pull request with a clear description.

Please do not commit private transaction data, credentials, environment secrets, or generated model artifacts without reviewing their privacy and licensing requirements.

---

## 📜 License

This project is intended for educational, research, and learning purposes. It is not intended to replace production-grade fraud detection systems used by financial institutions.
