# Run UPI Guard locally

The bundled model was serialized with scikit-learn 1.2.2. Use Python 3.11 for this project so that version can load the model correctly.

## First-time setup

Open PowerShell in this folder and run:

```powershell
py -3.11 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

If `py -3.11` is unavailable, install Python 3.11 and reopen PowerShell.

## Start the app

Double-click `run_local.bat`, or run:

```powershell
.venv\Scripts\python.exe app.py
```

Open http://127.0.0.1:5000 in your browser. Keep the terminal open while using the app; press Ctrl+C to stop the server.
