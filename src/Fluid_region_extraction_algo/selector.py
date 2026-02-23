from scipy import spatial
import trimesh
from trimesh import Trimesh
from typing import Union

from src.Logging.log import log_tree
from src.Geometry.Convexhull_operations.convex_hull_difference.baseline import (
    convex_hull_difference,
)
from src.Performance.perfLog import Algo, PerfLog, Variant
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


@log_tree
def mesh_intersection_difference_selector(
    variant,
    i,
    fluid_volume: Trimesh,
    solid_volume: Trimesh,
    prox_solid_volume: trimesh.proximity.ProximityQuery,
    treeorTableB: Union[dict, spatial.KDTree],
):

    print("─" * 50)
    match variant:
        case Variant.BASELINE:
            return PerfLog.log(
                variant(Algo.MESH_INTERSECTION_DIFFERENCE(i)),
                mesh_faces_intersection_difference_baseline,
                fluid_volume,
                prox_solid_volume,
            )
        case Variant.KDTREE:
            return PerfLog.log(
                variant(Algo.MESH_INTERSECTION_DIFFERENCE(i)),
                mesh_faces_intersection_difference_kdtree,
                fluid_volume,
                solid_volume,
                treeorTableB,
                prox_solid_volume,
            )
        case Variant.HASH_INTERSECTION:
            return PerfLog.log(
                variant(Algo.MESH_INTERSECTION_DIFFERENCE(i)),
                mesh_faces_intersection_difference_hashing,
                fluid_volume,
                treeorTableB,
                prox_solid_volume,
            )


@log_tree
def tree_or_table_selector(variant, solid_volume: Trimesh):
    print("─" * 50)
    match variant:
        case Variant.KDTREE:
            return PerfLog.log(
                variant(Algo.TREE_CONSTRUCT),
                spatial.KDTree,
                solid_volume.triangles_center,
            )
        case Variant.HASH_INTERSECTION:
            return PerfLog.log(
                variant(Algo.HASH_CONSTRUCT), build_face_hash, solid_volume
            )

    return None


@log_tree
def proximity_selector(variant, solid_volume: Trimesh):

    print("─" * 50)
    return PerfLog.log(
        variant(Algo.PROXIMITY_CONSTRUCT),
        trimesh.proximity.ProximityQuery,
        solid_volume,
    )


@log_tree
def convexhull_difference_selector(variant, solid_volume: Trimesh):

    return PerfLog.log(
        variant(Algo.CONVEX_HULL_DIFFERENCE),
        convex_hull_difference,
        solid_volume,
    )


@log_tree
def split_selector(variant, i, mesh: Trimesh):

    print("─" * 50)
    return PerfLog.log(
        variant(Algo.SPLIT(i)),
        mesh.split,
        only_watertight=False,
    )
