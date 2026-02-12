import trimesh
from trimesh import Trimesh


def convex_hull_difference(mesh: Trimesh):

    # Compute convex hull of the entire mesh
    convex_hull = mesh.convex_hull

    # Subtract original mesh from convex hull
    # This gives the concave "gaps"
    concave_regions = convex_hull.difference(mesh)

    if concave_regions is None:
        print("No concavity — mesh already convex")
        return None

    elif isinstance(concave_regions, Trimesh):
        print("Single concave region")
        return [concave_regions]

    elif isinstance(concave_regions, trimesh.Scene):
        print("Multiple concave regions:", len(concave_regions.geometry))
        return list(concave_regions.geometry.values())

    return concave_regions
    # concave_regions.export("concave_regions.stl")


# Load your original mesh
# mesh = trimesh.load("input.stl")
