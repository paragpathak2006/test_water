import trimesh
from .algo import convexhull_difference_algo
from .io_path import OUT_DIR


def test_convexhull_difference_algo():
    # Load the original mesh
    solid_volume = trimesh.load(OUT_DIR / "0. solid-volume.stl")

    # Run the kdtree convex hull difference algorithm
    fluid_volumes_walls_inlets_outlets = convexhull_difference_algo(solid_volume)

    print(fluid_volumes_walls_inlets_outlets)

    return fluid_volumes_walls_inlets_outlets
