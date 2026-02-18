import trimesh
from trimesh import Trimesh
import numpy as np

""" Mesh faces : A ∩ B = C """
""" Mesh faces : A - B = D """


# def mesh_faces_intersection_difference(mesh_A: Trimesh, mesh_B: Trimesh, tol=1e-5):

#     # Compute proximity query for mesh_B
#     proxB = trimesh.proximity.ProximityQuery(mesh_B)
#     return mesh_faces_intersection_difference(mesh_A, proxB, tol)


def mesh_faces_intersection_difference(
    mesh_A: Trimesh, prox_B: trimesh.proximity.ProximityQuery, tol=1e-5
):

    # List to store indices of faces in A that are close to B (i.e. common surface)
    common_faces = []

    # extract faces of A that are close to B (i.e. common surface)
    for i, tri in enumerate(mesh_A.triangles):
        center = tri.mean(axis=0)
        dist = prox_B.on_surface([center])[1][0]
        # dist = abs(proxB.signed_distance([center])[0])

        if dist < tol:
            common_faces.append(i)

    print("Intersection mesh extracted with", len(common_faces), " faces")

    # remove common faces from A to get difference mesh C
    uncommon_faces = np.setdiff1d(range(len(mesh_A.faces)), common_faces)

    # Make two submeshes C and D from  A with
    # C: the faces that are in common with B and
    # D: also not in common with B

    mesh_C = mesh_A.submesh([common_faces], append=True)
    mesh_D = mesh_A.submesh([uncommon_faces], append=True)

    return mesh_C, mesh_D
