from src.Performance.perfLog import Variant
from data.io_path import BASELINE_OUT_DIR, HASHING_OUT_DIR, KDTREE_OUT_DIR


def export_fluid_volumes_and_boundaries(
    variant,
    i,
    fluid_volume,
    fluid_wall,
    fluid_inlets_outlets_combined,
    fluid_inlets_outlets,
):

    match variant:
        case Variant.BASELINE:
            OUT_DIR = BASELINE_OUT_DIR
        case Variant.KDTREE:
            OUT_DIR = KDTREE_OUT_DIR
        case Variant.HASH_INTERSECTION:
            OUT_DIR = HASHING_OUT_DIR

    print(f"\n📁 Exporting file : fluid-volume-{i} ...")

    fluid_volume.export(OUT_DIR / f"1. fluid-volume-{i}.stl")

    # export each inlet-outlet boundary separately
    print(f"📁 Exporting file : fluid-wall-{i} ...")
    fluid_wall.export(OUT_DIR / f"2. fluid_wall-{i}.stl")

    print(f"📁 Exporting file : fluid-inlets-outlets-combined-{i} ...")
    fluid_inlets_outlets_combined.export(
        OUT_DIR / f"3. fluid_inlets-outlets-combined-{i}.stl"
    )

    for ii, fluid_inlet_outlet in enumerate(fluid_inlets_outlets):
        print(f"📁 Exporting file : fluid-inlet-outlet-{i}-{ii} ...")
        fluid_inlet_outlet.export(OUT_DIR / f"4. fluid-inlet-outlet-{i}-{ii}.stl")
