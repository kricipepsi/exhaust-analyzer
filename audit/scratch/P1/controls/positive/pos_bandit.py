"""Positive control: bandit -ll must flag shell=True (B602) and yaml.load (B506)."""
import subprocess

import yaml


def run(cmd: str) -> None:
    subprocess.call(cmd, shell=True)


def load(text: str) -> object:
    return yaml.load(text)
