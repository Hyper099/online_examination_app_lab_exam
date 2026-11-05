# Online Examination Application

A small Flask and HTML app with one 10-question Python basics exam. Register with a username and a password of at least eight characters, then log in, take the exam, and view your score. You can retake the exam. MongoDB saves accounts and the latest score for each user.

## Run locally

```powershell
docker compose up --build -d
```

Open [Online Exam](http://127.0.0.1:5000). The app listens on port 5000 on this computer. MongoDB runs inside Docker and stores data in a named volume. An optional `SECRET_KEY` in a local `.env` file keeps login sessions valid across app restarts.

Stop the app and database with `docker compose down`.

## Scoring and tests

```powershell
python result_calculation.py
python -m pip install pytest
python -m pytest -q tests/tets_calcualtion.py
```

The GitHub Actions workflow runs the script and tests on every push to `main`. The Actions tab shows the run status and step logs.
