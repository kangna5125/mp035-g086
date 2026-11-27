# Person 4 Daily Updates (Avinash Kumar - S24CSEU0709)

## Day 1, Wed 25 Nov 2026
**Planned:** Setup branch and `.venv`, verify Stage 1 & 2 source files (`data_checks.py`, `cleaning.py`, `params.yaml`), add `tests/test_longest_run.py` and `tests/test_split.py`, run pytest on them, create daily log, commit and push.
**Done:**
- Checked branch (`avinash/pipeline-setup`), `.venv` (`python3.12`), and installed `requirements.txt`.
- Verified `longest_run()` in `src/mp035/data_checks.py`, `split_xy()` in `src/mp035/cleaning.py`, and `params.yaml` exist.
- Added `tests/test_longest_run.py` from `stage1-person4-tests.zip` and `tests/test_split.py` from `stage2-person4-tests.zip`.
- Ran `PYTHONPATH=src python -m pytest -q tests/test_longest_run.py tests/test_split.py`: `3 passed in 0.94s`.
**Not done:** API tests (`tests/test_api.py`), predictions tests (`tests/test_predictions.py`), `pytest.ini` (scheduled for later days).
**Blocked by:** nothing
**Commits today:**
- `295762d` Stage 1: tests for longest_run helper
- `908c6e0` Stage 2: test that split_xy separates target from features
- (plus `Add Person 4 daily update log`)
**Next:** Proceed to Day 2 (Thu 26 Nov): Stage 3 API tests.

## Day 2, Thu 26 Nov 2026
**Planned:** Sync with `main`, verify `app/main.py` (Person 3) and `models/model.joblib` exist, add `pytest.ini` and `tests/test_api.py`, run full pytest suite, commit and push.
**Done:**
- Fetched and merged `origin/main` (`2a12a42 Add config tests for params.yaml`) into `avinash/pipeline-setup`.
- Verified `models/model.joblib` exists.
- Checked for `app/main.py`: missing.
- Ran existing suite (`PYTHONPATH=src python -m pytest -q tests`): `11 passed in 1.90s`.
**Not done:** `pytest.ini`, `tests/test_api.py` (blocked), `tests/test_predictions.py` (scheduled for Day 4).
**Blocked by:** Person 3 (Service lead) — `app/main.py` does not exist yet on `main`.
**Commits today:**
- (merge commit from `origin/main` + `Update Day 2 log: blocked on app/main.py`)
**Next:** Wait for Person 3 to push `app/main.py` to `main`, then pull and add `pytest.ini` + `tests/test_api.py`.

## Day 2 (continued), Thu 26 Nov 2026 — Stage 3 Unblocked
**Planned:** Pull `origin/main` after Person 3 merged `app/main.py`, add `pytest.ini` and `tests/test_api.py`, run full pytest suite, commit and push.
**Done:**
- Merged `origin/main` (`ebf9b25`, including Person 3's `app/main.py`) into `avinash/pipeline-setup`.
- Verified `app/main.py` and `models/model.joblib` exist.
- Added `pytest.ini` and `tests/test_api.py` from `stage3-person4-tests.zip`.
- Confirmed all 4 API tests pass (`/health` ok, `/predict` returns float, `temp_c=71` -> 422, `stubble_fires=-1` -> 422): `4 passed, 1 warning in 32.59s`.
- Ran full suite (`PYTHONPATH=src python -m pytest -q tests`): `22 passed, 1 warning in 11.22s`.
**Not done:** `tests/test_predictions.py` (scheduled for Day 4); GitHub Actions tab check (to be verified after push).
**Blocked by:** nothing
**Commits today:**
- `33d2a97` Merge remote-tracking branch 'origin/main' into avinash/pipeline-setup
- `1a95472` Stage 3: pytest config and API tests with TestClient
- (plus Day 2 log update)
**Next:** Check the GitHub Actions tab for CI status, then proceed to Day 3 (Fri 27 Nov) review & viva prep.

## Day 3, Fri 27 Nov 2026
**Planned:** Verify handbook test rules (3+ tests, `TestClient` used, no dependency on DVC-ignored CSVs), run full suite twice from a clean shell, review all 4 test files line by line, and add 3 viva Q&As per test file to the log.
**Done:**
- Checked handbook rules:
  - 3+ tests: Yes (7 tests across my 3 current files; 22 tests total in `tests/`).
  - Uses `TestClient`: Yes (`tests/test_api.py` uses `fastapi.testclient.TestClient`).
  - No dependency on `train.csv` / `later.csv` (DVC-ignored): Yes (all tests use synthetic inputs or `models/model.joblib` in git).
- Ran full suite twice from a clean shell (`python -m pytest -q tests`):
  - Run 1: `22 passed, 1 warning in 4.06s`
  - Run 2: `22 passed, 1 warning in 1.67s` (no flakiness).
- Reviewed all 4 test files (`test_longest_run.py`, `test_split.py`, `test_api.py`, and upcoming Stage 4 `test_predictions.py`) and added viva Q&As below.
**Not done:** `tests/test_predictions.py` (scheduled for Day 4, Sat 28 Nov).
**Blocked by:** nothing
**Commits today:**
- (Day 3 log update commit)
**Next:** Proceed to Day 4 (Sat 28 Nov): check `predictions/holdout_predictions.csv`, add and run `tests/test_predictions.py`.

### Viva Q&A Prep (Person 4 — Tests Lead)

#### 1. `tests/test_longest_run.py` (Stage 1)
1. **Q:** What does `longest_run(days)` test in `data_checks.py`?
   **A:** It checks that `longest_run` finds the longest streak of consecutive calendar days and returns `(start_date, end_date, length)`.
2. **Q:** Why do we have two tests (`test_longest_run_finds_the_consecutive_block` and `test_a_gap_breaks_the_run`)?
   **A:** The first verifies a 3-day streak (`Jan 1–3`) beats a 2-day streak (`Jan 10–11`); the second verifies a missing day (`Jan 2` missing between `Jan 1` and `Jan 3`) resets the streak to `1`.
3. **Q:** Does this test need `train.csv`?
   **A:** No, it creates a small in-memory list of dates with `pd.to_datetime(...)`, so it runs fast and works in CI without DVC data.

#### 2. `tests/test_split.py` (Stage 2)
1. **Q:** Why is `split_xy()` important to test?
   **A:** It prevents target leakage by ensuring the target column (`pm25_tomorrow`) is separated into `y` and removed from the feature matrix `X`.
2. **Q:** How does the test avoid hardcoding column names?
   **A:** It reads `features_numeric`, `features_categorical`, and `target` dynamically from `params.yaml` using `load_params()`.
3. **Q:** What two things does it assert?
   **A:** That `m["target"] not in X.columns` (target is not in features) and `len(y) == 2` (target length matches the 2-row DataFrame).

#### 3. `tests/test_api.py` (Stage 3)
1. **Q:** What is `TestClient(app)` and why use it instead of starting `uvicorn`?
   **A:** `TestClient` simulates HTTP requests (`GET`, `POST`) directly against the FastAPI `app` in memory—no live server or open port is needed, making CI fast and reliable.
2. **Q:** Why do `temp_c=71` and `stubble_fires=-1` return HTTP `422`?
   **A:** FastAPI uses Pydantic schemas to validate request fields (`temp_c <= 70`, `stubble_fires >= 0`); out-of-range inputs are automatically rejected with `422 Unprocessable Entity`.
3. **Q:** What does `pytest.ini` do?
   **A:** It sets `pythonpath = . src` and `testpaths = tests` so `pytest` can import both `app.main` and `mp035.*` cleanly without manually exporting `PYTHONPATH`.

#### 4. `tests/test_predictions.py` (Stage 4 — upcoming)
1. **Q:** What schema does `test_predictions_have_two_columns` check?
   **A:** It verifies `predictions/holdout_predictions.csv` has the exact columns `["record_id", "prediction"]`.
2. **Q:** What does `test_predictions_cover_every_holdout_row` guarantee?
   **A:** It checks that the set of `record_id` values in `holdout_predictions.csv` matches `data/raw/holdout_features.csv` and that no prediction is `NaN` (`notna().all()`).
3. **Q:** Why does this test work in CI without `train.csv`?
   **A:** Both `data/raw/holdout_features.csv` and `predictions/holdout_predictions.csv` are tracked in Git (not DVC-ignored).
