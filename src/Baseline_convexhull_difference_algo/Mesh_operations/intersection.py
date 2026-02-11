import trimesh
from trimesh import Trimesh
import numpy as np

""" Mesh faces : A ∩ B = C """
def mesh_faces_intersection(mesh_A : Trimesh, mesh_B : Trimesh, tol=1e-5):
    proxB = trimesh.proximity.ProximityQuery(mesh_B)

    common_faces = []

    for i, tri in enumerate(mesh_A.triangles):
        center = tri.mean(axis=0)
        dist = abs(proxB.signed_distance([center])[0])

        if dist < tol:
            common_faces.append(i)

    print("Intersection mesh extracted with", len(common_faces), " faces")

    mesh_C = mesh_A.submesh([common_faces], append=True)
    return mesh_C

# input = trimesh.load(OUT_DIR / "input.stl")
# concave_region = trimesh.load(OUT_DIR / "concave_region_0.stl")
# get_concave_wall(input, concave_region)