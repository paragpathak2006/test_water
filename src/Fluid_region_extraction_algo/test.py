import trimesh
from .algo import fluid_extraction_algo
from data.io_path import BENCHMARK_INPUT_DIR


def test_fluid_extraction_algo(variant):
    # Load the original mesh
    solid_volume = trimesh.load(BENCHMARK_INPUT_DIR / "0. solid-volume.stl")

    # Run the fluid extraction algorithm
    fluid_region = fluid_extraction_algo(solid_volume, variant)

    print(fluid_region)
    return fluid_region
