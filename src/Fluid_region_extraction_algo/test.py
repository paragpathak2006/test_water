import trimesh
from .algo import fluid_extraction_algo
from tests.io_path import OUT_DIR as INPUT_DIR


def test_fluid_extraction_algo(variant):
    # Load the original mesh
    solid_volume = trimesh.load(INPUT_DIR / "0. solid-volume.stl")

    # Run the fluid extraction algorithm
    fluid_region = fluid_extraction_algo(solid_volume, variant)

    print(fluid_region)
    return fluid_region
