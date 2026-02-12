from trimesh import Trimesh
import numpy as np
import scipy.spatial as spatial

""" Mesh faces : A ∩ B = C """
""" Mesh faces : A - B = D """


def mesh_faces_intersection_difference(mesh_A: Trimesh, mesh_B: Trimesh, tol=1e-5):

    centA = mesh_A.triangles_center
    centB = mesh_B.triangles_center

    normA = mesh_A.face_normals
    normB = mesh_B.face_normals

    tree = spatial.KDTree(centB)

    tol_dot = 1e-4

    common_faces = []

    for i, centroid in enumerate(centA):
        dist, idx = tree.query(centroid)
        if dist < tol and abs(np.dot(normA[i], normB[idx])) > 1 - tol_dot:
            common_faces.append(i)

    print("Intersection mesh extracted with", len(common_faces), " faces")

    # remove common faces from A to get difference mesh C
    range_of_faces = range(len(mesh_A.faces))
    uncommon_faces = np.setdiff1d(range_of_faces, common_faces)

    # Make two submeshes C and D from  A with the common faces and uncommon faces respectively
    mesh_C = mesh_A.submesh([common_faces], append=True)
    mesh_D = mesh_A.submesh([uncommon_faces], append=True)

    return {"intersection": mesh_C, "difference": mesh_D}
