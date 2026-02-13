import trimesh
from trimesh import Trimesh
import numpy as np

""" Mesh faces : A - B = C """


def mesh_faces_difference(mesh_A: Trimesh, mesh_B: Trimesh, tol=1e-5):

    # Compute proximity query for mesh_B
    prox = trimesh.proximity.ProximityQuery(mesh_B)

    # List to store indices of faces in A that are close to B (i.e. common surface)
    common_faces = []

    # extract faces of A that are close to B (i.e. common surface)
    for i, tri in enumerate(mesh_A.triangles):
        center = tri.mean(axis=0)
        dist = abs(prox.signed_distance([center])[0])

        if dist < tol:
            common_faces.append(i)

    # remove common faces from A to get difference mesh C
    range_of_faces = range(len(mesh_A.faces))
    keep_faces = np.setdiff1d(range_of_faces, common_faces)

    # Make submesh of A with only the faces that are not in common with B
    mesh_C = mesh_A.submesh([keep_faces], append=True)

    return mesh_C
