from typing import List, Dict, Callable
from pymatgen.core import Structure, Element
import numpy as np

def filter_direct(
    structures: List[Structure],
    dft_budget: int,
    seed: int,
) -> List[int]:
    """TODO: implement DIRECT pipeline steps..."""
    raise NotImplementedError

# Registry for structure encoders
ENCODERS: Dict[str, Callable[[Structure], np.ndarray]] = {}
