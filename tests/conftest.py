from __future__ import annotations

from pathlib import Path

import pytest

from purrimer_build.cli import main

ROOT = Path(__file__).resolve().parents[1]
TOKENS = ROOT / "tokens" / "tokens.json"
FONTS = ROOT / "tokens" / "fonts"


@pytest.fixture(scope="session")
def built(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """One full build of every target, shared by the output tests."""
    out = tmp_path_factory.mktemp("dist")
    code = main(["build", "--tokens", str(TOKENS), "--fonts", str(FONTS), "--out", str(out), "--clean"])
    assert code == 0
    return out
