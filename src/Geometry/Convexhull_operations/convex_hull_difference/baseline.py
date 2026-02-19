import trimesh
from trimesh import Trimesh


def convex_hull_difference(mesh: Trimesh):

    # messages
    mesh_convex_msg = "❌ Mesh is already convex. No concave regions to extract."
    convex_hull_extraction_failed_msg = (
        "❌ Convex hull extraction failed. Cannot compute convex hull difference."
    )
    concave_regions_extraction_failed_msg = (
        "❌ Concave regions extraction failed. Cannot compute convex hull difference."
    )
    single_concave_region_msg = "✅ Single concave region found"
    multiple_concave_regions_msg = "✅ Multiple concave regions found :"

    if mesh.is_convex:
        print(mesh_convex_msg)
        return None

    # Compute convex hull of the entire mesh
    convex_hull = mesh.convex_hull
    if convex_hull is None:
        print(convex_hull_extraction_failed_msg)
        return None

    # Subtract original mesh from convex hull. This gives the concave "gaps"
    concave_regions = convex_hull.difference(mesh, engine="manifold")

    if concave_regions is None:
        print(concave_regions_extraction_failed_msg)
        return None

    elif isinstance(concave_regions, Trimesh):
        print(single_concave_region_msg)
        return [concave_regions]

    elif isinstance(concave_regions, trimesh.Scene):
        print(multiple_concave_regions_msg, len(concave_regions.geometry))
        return list(concave_regions.geometry.values())

    return concave_regions
