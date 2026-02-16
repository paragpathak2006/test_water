import trimesh
from .hash_intersection_algo import hash_intersection_algo
from .io_path import OUT_DIR


def test_hash_intersection():
    # Load the original mesh
    solid_volume = trimesh.load(OUT_DIR / "0. solid-volume.stl")

    # Run the hash intersection algorithm
    fluid_volumes_walls_inlets_outlets = hash_intersection_algo(solid_volume)

    print(fluid_volumes_walls_inlets_outlets)

    return fluid_volumes_walls_inlets_outlets
