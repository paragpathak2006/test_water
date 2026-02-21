from trimesh import Trimesh

from src.Performance.perfLog import PerfLog, Variant
from src.Geometry.Processing.pre import (
    preprocess_solid_volume_for_convexhull_difference,
)
from src.Geometry.Processing.post import (
    postprocess_fluid_volume_for_convexhull_difference,
)
from src.Geometry.Processing.export import export_fluid_volumes_and_boundaries

from src.Fluid_region_extraction_algo.selector import (
    convexhull_difference_selector,
    mesh_intersection_difference_selector,
    proximity_selector,
    split_selector,
    tree_or_table_selector,
)


def fluid_extraction_algo(solid_volume: Trimesh, variant=Variant.BASELINE):

    convex_hull_difference_failed_msg = "❌ Convex hull difference algorithm failed or Solid is already convex.No fluid volumes extracted."
    fluid_volume_path_validation_success_msg = "\n✅ Multiple fluid inlets-outlets detected. Fluid volume represents a valid embedded path."
    no_embedded_fluid_volume_msg = "\n❌ No valid embedded fluid volumes with atleast 2 open boundaries (i.e. inlet and outlet) detected.❌"

    if preprocess_solid_volume_for_convexhull_difference(solid_volume) is None:
        return None

    fluid_volumes = convexhull_difference_selector(variant, solid_volume)
    if fluid_volumes is None:
        print(convex_hull_difference_failed_msg)
        return None
    print("\n✅ Number of fluid volumes : ", len(fluid_volumes))

    embedded_volumes = []
    fluid_walls = []  # result list to store fluid wall meshes
    fluid_inlets_outlets_all = (
        []
    )  # result list to store lists of inlet-outlet boundary meshes for each fluid volume

    # compute proximity query for solid volume to be used in intersection-difference method for extracting fluid walls and inlet-outlet boundaries
    prox_solid_volume = proximity_selector(variant, solid_volume)
    tree_or_table = tree_or_table_selector(variant, solid_volume)

    for i, fluid_volume in enumerate(fluid_volumes):
        print("\nExtracting fluid walls and inlet-outlet boundaries...")
        print("\nProcessing fluid volume#", i, " ...")
        print("\nVolume = ", fluid_volumes[i].volume)
        print("surface area = ", fluid_volumes[i].area)

        # extract fluid wall and inlet-outlet boundaries using intersection-difference method
        fluid_wall, fluid_inlets_outlets_combined = (
            mesh_intersection_difference_selector(
                variant, i, fluid_volume, solid_volume, prox_solid_volume, tree_or_table
            )
        )
        fluid_inlets_outlets = split_selector(variant, i, fluid_inlets_outlets_combined)
        print(
            "For volume#",
            i,
            " : Number of fluid inlet and outlet boundaries : ",
            len(fluid_inlets_outlets),
        )

        if len(fluid_inlets_outlets) >= 2:
            # Validation check for output fluid volume mesh
            if postprocess_fluid_volume_for_convexhull_difference(fluid_volume) is None:
                return None
            print(fluid_volume_path_validation_success_msg)

            export_fluid_volumes_and_boundaries(
                variant,
                i,
                fluid_volume,
                fluid_wall,
                fluid_inlets_outlets_combined,
                fluid_inlets_outlets,
            )

            embedded_volumes.append(
                fluid_volumes[i]
            )  # capturing the fluid volume mesh that form a valid path with atleast 2 open boundaries (i.e. inlet and outlet)
            fluid_walls.append(fluid_wall)  # capturing the fluid wall mesh
            fluid_inlets_outlets_all.append(
                fluid_inlets_outlets
            )  # capturing the list of inlet-outlet boundary meshes

    PerfLog.line()
    if len(embedded_volumes) == 0:
        print(no_embedded_fluid_volume_msg)
        return None

    return embedded_volumes, fluid_walls, fluid_inlets_outlets_all
