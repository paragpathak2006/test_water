# Load the original mesh
import trimesh
from tests.io_path import OUT_DIR
from baseline_validation import baseline_validation_check

solid_volume = trimesh.load(OUT_DIR / "solid-volume.stl")
fluid_volume = trimesh.load(OUT_DIR / "fluid-volume.stl")

print()
print(solid_volume)
print("baseline validation check : ", baseline_validation_check(solid_volume))
print()
print(fluid_volume)
print("baseline validation check : ", baseline_validation_check(fluid_volume))
print()
