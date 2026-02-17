from trimesh import Trimesh

# from .Convexhull_operations.self_difference import convex_hull_difference
# from .Mesh_operations.intersection_difference import mesh_faces_intersection_difference
from .io_path import OUT_DIR

from src.Performance.perfLog import PerfLog, TargetAlgo
from src.Geometry.Processing.pre import (
    preprocess_solid_volume_for_convexhull_difference,
)
from src.Geometry.Processing.post import (
    postprocess_fluid_volume_for_convexhull_difference,
)
from src.Geometry.Processing.export import export_fluid_volumes_and_boundaries


from src.Geometry.Convexhull_operations.convex_hull_difference.baseline import (
    convex_hull_difference,
)
from src.Geometry.Mesh_operations.intersection_difference.baseline import (
    mesh_faces_intersection_difference,
)


def convexhull_difference_algo(solid_volume: Trimesh):

    if preprocess_solid_volume_for_convexhull_difference(solid_volume) is None:
        return None

    print("\nRunning baseline convex hull difference algorithm...\n")
    fluid_volumes = PerfLog.log(
        TargetAlgo.BASELINE.CONVEX_HULL_DIFFERENCE, convex_hull_difference, solid_volume
    )

    if fluid_volumes is None:
        print(
            "❌Convex hull difference algorithm failed or Solid is already convex. No fluid volumes extracted.❌"
        )
        return None

    print("\n✅ Number of fluid volumes : ", len(fluid_volumes))

    fluid_embedded_path = (
        []
    )  # result list to store fluid volume meshes that are embedded in the solid volume (i.e. not separate disconnected components) and can be used for CFD simulation without further processing
    fluid_walls = []  # result list to store fluid wall meshes
    fluid_inlets_outlets_all = (
        []
    )  # result list to store lists of inlet-outlet boundary meshes for each fluid volume

    for i, fluid_volume in enumerate(fluid_volumes):
        print("\nExtracting fluid walls and inlet-outlet boundaries...")

        print("\nProcessing fluid volume#", i, " ...")
        print("\nvolume = ", fluid_volumes[i].volume)
        print("surface area = ", fluid_volumes[i].area)

        print("\nExtracting fluid wall and inlet-outlet boundaries...\n")

        # extract fluid wall and inlet-outlet boundaries using intersection-difference method

        fluid_boundary = PerfLog.log(
            TargetAlgo.BASELINE.MESH_INTERSECTION_DIFFERENCE(i),
            mesh_faces_intersection_difference,
            fluid_volumes[i],
            solid_volume,
        )

        fluid_wall = fluid_boundary["intersection"]
        fluid_inlets_outlets_combined = fluid_boundary["difference"]

        fluid_inlets_outlets = PerfLog.log(
            TargetAlgo.BASELINE.SPLIT(i),
            fluid_inlets_outlets_combined.split,
            only_watertight=False,
        )

        print(
            "For volume#",
            i,
            " : Number of fluid inlet and outlet boundaries : ",
            len(fluid_inlets_outlets),
        )

        if len(fluid_inlets_outlets) >= 2:
            print(
                "\n✅ Multiple fluid inlets-outlets detected.",
                "Fluid volume represents a valid embedded path.",
            )

            # Validation check for output fluid volume mesh
            if postprocess_fluid_volume_for_convexhull_difference(fluid_volume) is None:
                return None

            export_fluid_volumes_and_boundaries(
                OUT_DIR,
                i,
                fluid_volume,
                fluid_wall,
                fluid_inlets_outlets_combined,
                fluid_inlets_outlets,
            )

            fluid_embedded_path.append(
                fluid_volumes[i]
            )  # capturing the fluid volume mesh that form a valid path with atleast 2 open boundaries (i.e. inlet and outlet)
            fluid_walls.append(fluid_wall)  # capturing the fluid wall mesh
            fluid_inlets_outlets_all.append(
                fluid_inlets_outlets
            )  # capturing the list of inlet-outlet boundary meshes

    return {
        "fluid_volumes": fluid_embedded_path,
        "fluid_walls": fluid_walls,
        "all_fluid_inlets_outlets": fluid_inlets_outlets_all,
    }
