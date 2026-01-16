"""Configuration management with TOML support."""

import os
from pathlib import Path
from typing import Any, Optional
from platformdirs import user_config_dir

import tomllib


class Config:
    """Application configuration."""

    DEFAULT_CONFIG = {
        "default_language": None,
        "default_limit": 10,
        "default_duration": "week",
        "api_token": None,
        "theme": "dark",
    }

    def __init__(self) -> None:
        self.config_dir = Path(user_config_dir("trending-repos"))
        self.config_file = self.config_dir / "config.toml"
        self._config: dict[str, Any] = {}
        self._load_config()

    def _load_config(self) -> None:
        """Load config from file"""
        if self.config_file.exists():
            with open(self.config_file, "rb") as f:
                self._config = tomllib.load(f)
        else:
            self._config = self.DEFAULT_CONFIG.copy()

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value with environment variable override."""
        # Check env variable first
        env_key = f"TRENDING_REPOS_{key.upper()}"
        env_value = os.environ.get(env_key)
        if env_value is not None:
            return env_value
            # Then check config file
        return self._config.get(key, default or self.DEFAULT_CONFIG.get(key))

    @property
    def api_token(self) -> Optional[str]:
        """Get GitHub API token from config or environment."""
        return self.get("api_token") or os.environ.get("GITHUB_TOKEN")

    def ensure_dirs(self) -> None:
        """Create config and cache directories if they don't exist."""
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.cache_dir.mkdir(parents=True, exist_ok=True)


# Global config instance
config = Config()
