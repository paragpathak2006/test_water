from pathlib import Path

# Directory where this script lives
BASE_DIR = Path(__file__).resolve().parent

# Output directory for the generated STL files
BENCHMARK_INPUT_DIR = Path(BASE_DIR / "0. benchmark")
BASELINE_OUT_DIR = Path(BASE_DIR / "1. baseline")
HASHING_OUT_DIR = Path(BASE_DIR / "2. hashing")
KDTREE_OUT_DIR = Path(BASE_DIR / "3. kdtree")
PARTS_DIR = Path(BASE_DIR / "parts")

BENCHMARK_INPUT_DIR.mkdir(exist_ok=True)
BASELINE_OUT_DIR.mkdir(exist_ok=True)
HASHING_OUT_DIR.mkdir(exist_ok=True)
KDTREE_OUT_DIR.mkdir(exist_ok=True)
PARTS_DIR.mkdir(exist_ok=True)
