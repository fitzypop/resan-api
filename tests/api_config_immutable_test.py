import pytest
from api.settings import _APIConfig


def test_api_config_init_works():
    try:
        _APIConfig()
    except Exception:
        pytest.fail("initializing immutable APIConfig class failed")
