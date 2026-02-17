import trimesh
from trimesh import Trimesh


def convex_hull_difference(mesh: Trimesh):

    if mesh.is_convex:
        print("❌ Mesh is already convex. No concave regions to extract.")
        return None

    # Compute convex hull of the entire mesh
    convex_hull = mesh.convex_hull

    # Subtract original mesh from convex hull
    # This gives the concave "gaps"
    concave_regions = convex_hull.difference(mesh, engine="manifold")

    if concave_regions is None:
        print(
            "❌ Either mesh is already convex or convex hull difference failed. Therefore no concave regions extracted. "
        )
        return None

    elif isinstance(concave_regions, Trimesh):
        print("✅ Single concave region found")
        return [concave_regions]

    elif isinstance(concave_regions, trimesh.Scene):
        print("✅ Multiple concave regions found :", len(concave_regions.geometry))
        return list(concave_regions.geometry.values())

    return concave_regions
    # concave_regions.export("concave_regions.stl")


# Load your original mesh
# mesh = trimesh.load("input.stl")
