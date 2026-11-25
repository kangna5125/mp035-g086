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
