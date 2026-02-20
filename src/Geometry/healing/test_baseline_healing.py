# Load the original mesh
import trimesh
from data.io_path import BASELINE_OUT_DIR
from baseline_healing import baseline_heal

mesh = trimesh.load(BASELINE_OUT_DIR / "solid-volume.stl")

print()

print("Running baseline geometry healing test:")
baseline_heal(mesh)

print()
