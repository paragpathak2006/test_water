import trimesh
from baseline_convexhull_difference_algo import baseline_convexhull_difference
from io_path import OUT_DIR

# Load the original mesh
solid_volume = trimesh.load(OUT_DIR / "0. solid-volume.stl")

# Run the baseline convex hull difference algorithm
fluid_volumes_walls_inlets_outlets = baseline_convexhull_difference(solid_volume)    

print(fluid_volumes_walls_inlets_outlets)

