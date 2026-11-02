"""Clean control: bandit -ll must stay silent."""
import yaml


def load(text: str) -> object:
    return yaml.safe_load(text)
