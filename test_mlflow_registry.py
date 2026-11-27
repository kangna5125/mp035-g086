import mlflow
from mlflow import MlflowClient

from mp035.config import load_params


def _client_and_name():
    params = load_params()
    mlflow.set_tracking_uri(params["paths"]["mlflow_uri"])
    return MlflowClient(), params["model"]["name"]


def test_registry_has_at_least_one_version():
    client, name = _client_and_name()
    assert len(client.search_model_versions(f"name='{name}'")) >= 1


def test_champion_alias_points_to_a_version():
    client, name = _client_and_name()
    version = client.get_model_version_by_alias(name, "champion")
    assert int(version.version) >= 1
