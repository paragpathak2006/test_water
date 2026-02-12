import trimesh
from .kdtree_convexhull_difference_algo import kdtree_convexhull_difference
from .io_path import OUT_DIR

def test_kdtree_convexhull_difference():
    # Load the original mesh
    solid_volume = trimesh.load(OUT_DIR / "0. solid-volume.stl")

    # Run the kdtree convex hull difference algorithm
    fluid_volumes_walls_inlets_outlets = kdtree_convexhull_difference(solid_volume)    

    print(fluid_volumes_walls_inlets_outlets)

    return fluid_volumes_walls_inlets_outlets
