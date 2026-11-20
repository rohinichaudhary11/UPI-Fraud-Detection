# UPI Fraud Detection

A full-stack demonstration app that analyzes a UPI-style transaction and estimates its fraud risk using a trained scikit-learn model and balance-based validation rules. The Flask backend serves a responsive browser UI and a JSON prediction endpoint.

> **Educational demo:** predictions are for learning and demonstration only. They are not financial advice, a bank decision, or a guarantee that a transaction is safe.

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/rohinichaudhary11/UPI-Fraud-Detection)

## Features

- Enter a payment or transfer and the sender/receiver balances before and after it.
- Receive an ML fraud classification and estimated fraud probability.
- Apply balance consistency rules and show the rule that flagged a transaction.
- Validate missing, negative, malformed, or non-finite transaction data.
- Use a responsive UI, sample transaction, and health endpoint.
- Deploy as a Render web service from the included Blueprint.

## How prediction works

1. The form sends transaction details to Flask at `POST /predict`.
2. The backend validates the inputs and derives the features used when the model was trained, including balance changes, amount ratio, local transaction hour, and transaction type.
3. Balance-based rules flag inconsistent transaction movements. Otherwise, the saved scikit-learn pipeline returns a classification and fraud probability.
4. The UI displays the result, probability, and any rule-based explanation.

The saved pipeline is `UPI-Fraud-Detection-main/UPI-Fraud-Detection-main/model/fraud_pipeline.pkl`. Its dependency versions are pinned because serialized scikit-learn models are version-sensitive.

## Run locally

Use **Python 3.11** with the pinned requirements. From the project directory:

```powershell
cd UPI-Fraud-Detection-main\UPI-Fraud-Detection-main
py -3.11 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe app.py
```

Then open [http://127.0.0.1:5000](http://127.0.0.1:5000). On Windows, `run_local.bat` in the project directory creates the environment and opens the app for you. Keep the terminal open while the app is running; press **Ctrl+C** to stop it.

## API

`POST /predict` accepts JSON with transaction type and all four balance values:

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

The response includes `is_fraud`, `probability`, `rule_flagged`, `rule_reason`, and the derived features. `GET /health` returns service/model readiness.

## Deploy to Render

The repository includes [`render.yaml`](render.yaml), which defines a free Python web service, its project subdirectory, dependency installation, Gunicorn start command, Python 3.11 runtime, and `/health` check.

1. Sign in to Render and choose **New → Blueprint**.
2. Connect `rohinichaudhary11/UPI-Fraud-Detection` and select the `main` branch.
3. Review the `upi-fraud-detection-rohini` service and deploy the Blueprint.
4. Render builds the app and provides its public `onrender.com` URL. Subsequent pushes to `main` trigger deploys.

Render’s free web services spin down after 15 minutes without traffic and may take about a minute to wake on the next request. This plan is suitable for a demo, not production use. [Render free service limitations](https://render.com/docs/free).

## Project layout

```text
UPI_fraudDetection/
├── README.md
├── render.yaml
└── UPI-Fraud-Detection-main/
    └── UPI-Fraud-Detection-main/
        ├── app.py
        ├── model/fraud_pipeline.pkl
        ├── templates/index.html
        ├── static/
        ├── requirements.txt
        └── notebook/ and datatset/
```
