# app.py
from pathlib import Path
from math import isfinite
import os
from threading import Timer
import webbrowser

from flask import Flask, request, jsonify, render_template
import joblib
import pandas as pd
from datetime import datetime

app = Flask(__name__)
PROJECT_DIR = Path(__file__).resolve().parent

# Load ML pipeline
pipe = joblib.load(PROJECT_DIR / "model" / "fraud_pipeline.pkl")


# ---------------------------------------------------------
# Feature computation
# ---------------------------------------------------------
def compute_features_and_values(payload: dict):
    if not isinstance(payload, dict):
        raise ValueError("Send transaction details as a JSON object.")

    tx_type = str(payload.get("type", "")).upper()
    if tx_type not in {"PAYMENT", "TRANSFER"}:
        raise ValueError("Transaction type must be PAYMENT or TRANSFER.")

    required_fields = (
        "amount",
        "oldbalanceOrg",
        "newbalanceOrig",
        "oldbalanceDest",
        "newbalanceDest",
    )
    missing_fields = [field for field in required_fields if field not in payload]
    if missing_fields:
        raise ValueError("Missing required transaction fields: " + ", ".join(missing_fields))

    try:
        amount, oldbalanceOrg, newbalanceOrig, oldbalanceDest, newbalanceDest = (
            float(payload[field]) for field in required_fields
        )
    except (TypeError, ValueError):
        raise ValueError("Transaction amounts and balances must be valid numbers.") from None

    if not all(isfinite(value) for value in (amount, oldbalanceOrg, newbalanceOrig, oldbalanceDest, newbalanceDest)):
        raise ValueError("Transaction amounts and balances must be finite numbers.")
    if amount <= 0:
        raise ValueError("Transaction amount must be greater than zero.")
    if min(oldbalanceOrg, newbalanceOrig, oldbalanceDest, newbalanceDest) < 0:
        raise ValueError("Balances cannot be negative.")

    # Using server time
    hour = datetime.now().hour
    is_night = 1 if hour < 6 else 0
    amount_ratio = amount / (oldbalanceOrg + 1.0)

    sender_balance_change = oldbalanceOrg - newbalanceOrig
    receiver_balance_change = newbalanceDest - oldbalanceDest

    orig_balance_zero = 1 if oldbalanceOrg == 0 else 0
    dest_balance_zero = 1 if oldbalanceDest == 0 else 0
    type_TRANSFER = 1 if tx_type == "TRANSFER" else 0

    features = [
        amount,
        oldbalanceOrg,
        newbalanceOrig,
        oldbalanceDest,
        newbalanceDest,
        hour,
        is_night,
        amount_ratio,
        sender_balance_change,
        receiver_balance_change,
        orig_balance_zero,
        dest_balance_zero,
        type_TRANSFER
    ]

    vals = {
        "tx_type": tx_type,
        "amount": amount,
        "oldbalanceOrg": oldbalanceOrg,
        "newbalanceOrig": newbalanceOrig,
        "oldbalanceDest": oldbalanceDest,
        "newbalanceDest": newbalanceDest,
        "hour": hour,
        "is_night": is_night,
        "amount_ratio": amount_ratio,
        "sender_balance_change": sender_balance_change,
        "receiver_balance_change": receiver_balance_change,
        "orig_balance_zero": orig_balance_zero,
        "dest_balance_zero": dest_balance_zero,
        "type_TRANSFER": type_TRANSFER
    }

    X = pd.DataFrame([features], columns=pipe.feature_names_in_)
    return X, vals


# ---------------------------------------------------------
# Rule-Based Fraud Checks
# ---------------------------------------------------------
def rule_based_checks(v):

    amount = v["amount"]
    sender_change = v["sender_balance_change"]
    receiver_change = v["receiver_balance_change"]
    oldbalanceOrg = v["oldbalanceOrg"]
    tx_type = v["tx_type"]

    if amount <= 0:
        return False, ""

    # ----------------------------------------------
    # NEW RULE A: Amount cannot exceed sender balance
    # ----------------------------------------------
    if amount > oldbalanceOrg:
        return True, "amount exceeds sender available balance"

    # ----------------------------------------------
    # NEW RULE B: Receiver cannot get MORE than amount
    # ----------------------------------------------
    if receiver_change > amount:
        return True, "receiver credited more than transferred amount"

    # -------------------------
    # Rule 1: Sender loses ≈ amount (±20%)
    # -------------------------
    if abs(sender_change - amount) > 0.20 * amount:
        return True, "sender balance change inconsistent with amount"

    # -------------------------
    # Rule 2: Receiver gets enough credit (>=70%)
    # -------------------------
    if receiver_change < 0.70 * amount:
        return True, "receiver credited significantly less than expected"

    # -------------------------
    # Rule 3: Receiver got zero in TRANSFER
    # -------------------------
    if tx_type == "TRANSFER" and receiver_change == 0:
        return True, "receiver balance not updated"

    # -------------------------
    # Rule 4: total movement should be ≈ 2 × amount (±30%)
    # -------------------------
    total_movement = sender_change + receiver_change
    expected_total = 2 * amount

    if abs(total_movement - expected_total) > 0.30 * expected_total:
        return True, "inconsistent total money movement"

    return False, ""


# ---------------------------------------------------------
# Routes
# ---------------------------------------------------------
@app.route('/')
def home():
    return render_template('index.html')


@app.route("/health")
def health():
    return jsonify({"status": "ok", "model_loaded": pipe is not None})


@app.route("/predict", methods=["POST"])
def predict():
    try:
        payload = request.get_json(silent=True)
        if payload is None:
            raise ValueError("Send transaction details as a JSON object.")

        X, vals = compute_features_and_values(payload)

        # Rule-based fraud check
        flagged, reason = rule_based_checks(vals)

        if flagged:
            return jsonify({
                "is_fraud": 1,
                "probability": 1.0,
                "rule_flagged": True,
                "rule_reason": reason,
                "features": vals
            })

        # ML prediction
        pred = int(pipe.predict(X)[0])
        proba = float(pipe.predict_proba(X)[0][1])

        return jsonify({
            "is_fraud": pred,
            "probability": round(proba, 6),
            "rule_flagged": False,
            "rule_reason": "",
            "features": vals
        })

    except Exception as exc:
        return jsonify({"error": str(exc)}), 400


# ---------------------------------------------------------
# Start Server
# ---------------------------------------------------------
if __name__ == "__main__":
    if os.environ.get("OPEN_BROWSER") == "1":
        Timer(1.0, lambda: webbrowser.open("http://127.0.0.1:5000")).start()
    app.run(host="127.0.0.1", port=5000, debug=False)
