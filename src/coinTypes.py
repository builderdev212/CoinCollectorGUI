from dataclasses import dataclass

@dataclass
class Coin:
    """
    Class for keeping track of information about a coin.
    """
    kind: str = ""
    year: int = -1
    mint: str = ""
    description: str = ""
    condition: str = ""
    value: int = -1
