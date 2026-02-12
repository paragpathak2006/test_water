from pathlib import Path

# Directory where this script lives
BASE_DIR = Path(__file__).resolve().parent
print("BASE_DIR : ", BASE_DIR)

# Output directory for the generated STL files
OUT_DIR = Path(BASE_DIR / "test_parts")
OUT_DIR.mkdir(exist_ok=True)
