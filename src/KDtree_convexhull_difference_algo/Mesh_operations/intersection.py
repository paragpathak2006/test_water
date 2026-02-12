import trimesh
from trimesh import Trimesh
import numpy as np

""" Mesh faces : A ∩ B = C """
def mesh_faces_intersection_kdtree(mesh_A : Trimesh, mesh_B : Trimesh, tol=1e-5):

    centA = mesh_A.triangles_center
    centB = mesh_B.triangles_center

    normA = mesh_A.face_normals
    normB = mesh_B.face_normals

    tree = trimesh.kdtree.KDTree(centB)

    tol_dot  = 1e-4

    common_faces = []

    for i, centroid in enumerate(centA):
        candidate_points = tree.query_ball_point(centroid, tol)
        for j in candidate_points:
            if abs(np.dot(normA[i], normB[j])) > 1 - tol_dot:
                common_faces.append(i)
    
    # Make submesh of A with only the faces that are in common with B
    mesh_C = mesh_A.submesh([common_faces], append=True)
    
    return mesh_C



""" Mesh faces : A - B = C """
def mesh_faces_intersection_boolean(mesh_A : Trimesh, mesh_B : Trimesh, tol=1e-5):

    # Boolean intersection mesh = A ∩ B
    mesh_C = trimesh.boolean.intersection([mesh_A, mesh_B])
    
    return mesh_C


# input = trimesh.load(OUT_DIR / "input.stl")
# concave_region = trimesh.load(OUT_DIR / "concave_region_0.stl")
# get_concave_wall(input, concave_region)