# Load the original mesh
import trimesh
from tests.io_path import OUT_DIR
from baseline_healing import baseline_heal

mesh = trimesh.load(OUT_DIR / "solid-volume.stl")

print()

print("Running baseline geometry healing test:")
baseline_heal(mesh)

print()
