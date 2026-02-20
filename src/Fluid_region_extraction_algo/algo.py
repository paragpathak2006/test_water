from scipy import spatial
from trimesh import Trimesh
import trimesh

# from .Convexhull_operations.self_difference import convex_hull_difference
# from .Mesh_operations.intersection_difference import mesh_faces_intersection_difference

from src.Performance.perfLog import PerfLog, Algo, Variant
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
    mesh_faces_intersection_difference as mesh_faces_intersection_difference_baseline,
)
from src.Geometry.Mesh_operations.intersection_difference.Variants.kdtree import (
    mesh_faces_intersection_difference as mesh_faces_intersection_difference_kdtree,
)
from src.Geometry.Mesh_operations.intersection_difference.Variants.hashing import (
    build_face_hash,
    mesh_faces_intersection_difference as mesh_faces_intersection_difference_hashing,
)


def fluid_extraction_algo(solid_volume: Trimesh, variant=Variant.BASELINE):

    if preprocess_solid_volume_for_convexhull_difference(solid_volume) is None:
        return None

    print("\nRunning baseline convex hull difference algorithm...\n")
    fluid_volumes = PerfLog.log(
        variant(Algo.CONVEX_HULL_DIFFERENCE),
        convex_hull_difference,
        solid_volume,
    )

    if fluid_volumes is None:
        print(
            "❌Convex hull difference algorithm failed or Solid is already convex. No fluid volumes extracted.❌"
        )
        return None

    print("\n✅ Number of fluid volumes : ", len(fluid_volumes))

    embedded_volumes = []
    fluid_walls = []  # result list to store fluid wall meshes
    fluid_inlets_outlets_all = (
        []
    )  # result list to store lists of inlet-outlet boundary meshes for each fluid volume

    # compute proximity query for solid volume to be used in intersection-difference method for extracting fluid walls and inlet-outlet boundaries
    prox_solid_volume = PerfLog.log(
        variant(Algo.PROXIMITY_CONSTRUCT),
        trimesh.proximity.ProximityQuery,
        solid_volume,
    )
    if variant == Variant.KDTREE:
        # compute KDTree for solid volume to be used in intersection-difference method for extracting fluid walls and inlet-outlet boundaries
        tree_solid_volume = PerfLog.log(
            variant(Algo.TREE_CONSTRUCT),
            spatial.KDTree,
            solid_volume.triangles_center,
        )
    if variant == Variant.HASH_INTERSECTION:
        # compute hash table for solid volume to be used in intersection-difference method for extracting fluid walls and inlet-outlet boundaries
        table_solid_volume = PerfLog.log(
            variant(Algo.HASH_CONSTRUCT), build_face_hash, solid_volume
        )

    for i, fluid_volume in enumerate(fluid_volumes):
        print("\nExtracting fluid walls and inlet-outlet boundaries...")

        print("\nProcessing fluid volume#", i, " ...")
        print("\nvolume = ", fluid_volumes[i].volume)
        print("surface area = ", fluid_volumes[i].area)

        print("\nExtracting fluid wall and inlet-outlet boundaries...\n")

        # extract fluid wall and inlet-outlet boundaries using intersection-difference method

        match variant:
            case Variant.BASELINE:
                fluid_wall, fluid_inlets_outlets_combined = PerfLog.log(
                    variant(Algo.MESH_INTERSECTION_DIFFERENCE(i)),
                    mesh_faces_intersection_difference_baseline,
                    fluid_volumes[i],
                    prox_solid_volume,
                )
            case Variant.KDTREE:
                fluid_wall, fluid_inlets_outlets_combined = PerfLog.log(
                    variant(Algo.MESH_INTERSECTION_DIFFERENCE(i)),
                    mesh_faces_intersection_difference_kdtree,
                    fluid_volumes[i],
                    solid_volume,
                    tree_solid_volume,
                    prox_solid_volume,
                )
            case Variant.HASH_INTERSECTION:
                fluid_wall, fluid_inlets_outlets_combined = PerfLog.log(
                    variant(Algo.MESH_INTERSECTION_DIFFERENCE(i)),
                    mesh_faces_intersection_difference_hashing,
                    fluid_volumes[i],
                    table_solid_volume,
                    prox_solid_volume,
                )

        fluid_inlets_outlets = PerfLog.log(
            variant(Algo.SPLIT(i)),
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
        print(
            "\n❌ No valid embedded fluid volumes with atleast 2 open boundaries (i.e. inlet and outlet) detected.❌"
        )
        return None

    return embedded_volumes, fluid_walls, fluid_inlets_outlets_all
