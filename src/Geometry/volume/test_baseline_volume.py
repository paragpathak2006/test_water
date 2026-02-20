# Load the original mesh
import trimesh
from data.io_path import PARTS_DIR
from baseline_volume import baseline_volume_calculate

solid_volume = trimesh.load(PARTS_DIR / "solid-volume.stl")
fluid_volume = trimesh.load(PARTS_DIR / "fluid-volume.stl")

print()
print(solid_volume)
print("Volume of solid : ", baseline_volume_calculate(solid_volume))

print()
print(fluid_volume)
print("Volume of fluid : ", baseline_volume_calculate(fluid_volume))

print()
