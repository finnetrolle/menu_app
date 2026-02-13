"""Pytest configuration for async tests."""
import pytest

# Configure asyncio mode
pytest_plugins = ('pytest_asyncio',)


def pytest_configure(config):
    """Configure pytest with asyncio settings."""
    config.addinivalue_line(
        "markers", "asyncio: mark test as async"
    )
