import sys
from pathlib import Path
ROOT = Path(__file__).parent.parent
sys.path.append(str(ROOT / "code"))
NET_DIR = ROOT / "examples"

from network import Network


def test_lecture_reseau_petit():
    """Vérifie que from_file lit correctement small.txt."""
    reseau = Network.from_file(NET_DIR / "small.txt")

    assert reseau.start == "lozere"
    assert reseau.end == "saclay"
    assert reseau._roads == {
        "lozere":  [("ensae", 10, 2), ("guichet", 20, 0)],
        "ensae":   [("saclay", 45, 0)],
        "guichet": [("ensae", 15, 1)],
        "saclay":  [],
    }
