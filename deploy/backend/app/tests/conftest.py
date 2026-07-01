"""Shared test configuration — ensures consistent env across all test files."""
import os
import pytest


@pytest.fixture(autouse=True)
def _reset_api_key(monkeypatch):
    """Ensure all tests run in dev mode (auth bypassed) regardless of env.

    Without this, test isolation fails when the real CAREER_OPS_API_KEY is set
    in the environment: test_health.py imports app.main first (captures real key),
    then test_output.py's module-level os.environ change is too late.
    """
    monkeypatch.setenv("CAREER_OPS_API_KEY", "")
    # Also patch the already-imported module variable if it was captured
    import app.main as main_mod
    monkeypatch.setattr(main_mod, "CAREER_OPS_API_KEY", "")
    yield
