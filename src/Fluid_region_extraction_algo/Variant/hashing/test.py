import trimesh
from .algo import fluid_extraction_algo
from .io_path import OUT_DIR


def test_fluid_extraction_algo():
    # Load the original mesh
    solid_volume = trimesh.load(OUT_DIR / "0. solid-volume.stl")

    # Run the hash intersection algorithm
    fluid_volumes_walls_inlets_outlets = fluid_extraction_algo(solid_volume)

    print(fluid_volumes_walls_inlets_outlets)

    return fluid_volumes_walls_inlets_outlets
