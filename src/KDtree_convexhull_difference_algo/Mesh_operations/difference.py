import trimesh
from trimesh import Trimesh
import numpy as np

""" Mesh faces : A - B = C """
def mesh_faces_difference_kdtree(mesh_A : Trimesh, mesh_B : Trimesh, tol=1e-5):

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

    # remove common faces from A to get difference mesh C
    range_of_faces = range(len(mesh_A.faces))
    keep_faces = np.setdiff1d(range_of_faces, common_faces)

    mesh_C = mesh_A.submesh([keep_faces], append=True)

    return mesh_C

""" Mesh faces : A - B = C """
def mesh_faces_difference_boolean(mesh_A : Trimesh, mesh_B : Trimesh, tol=1e-5):

    # Boolean difference mesh = A - B 
    mesh_C = trimesh.boolean.difference([mesh_A, mesh_B])
    
    return mesh_C

# def face_key(verts, tol=1e-6):
#     v = np.round(verts / tol) * tol
#     return tuple(sorted(map(tuple, v)))

# def subtract_surface(mesh_A, mesh_B, tol=1e-6):

#     # build hash set of faces to remove
#     remove_keys = set()
#     for f in mesh_B.faces:
#         remove_keys.add(face_key(mesh_B.vertices[f], tol))

#     keep_faces = []
#     for i, f in enumerate(mesh_A.faces):
#         if face_key(mesh_A.vertices[f], tol) not in remove_keys:
#             keep_faces.append(i)

#     # build remaining mesh
#     flow_inlet_outlet = mesh_A.submesh([keep_faces], append=True)

#     # split into connected surface patches
#     pieces = flow_inlet_outlet.split(only_watertight=False)

#     return pieces

# concave_region = trimesh.load(OUT_DIR / "concave_region_0.stl")
# concave_wall = trimesh.load(OUT_DIR / "concave_wall.stl")
# get_flow_boundary(concave_region, concave_wall)

  # proxB = trimesh.proximity.ProximityQuery(concave_wall)

    # common_faces = []

    # # tol = 1e-5

    # for i, tri in enumerate(concave_region.triangles):
    #     center = tri.mean(axis=0)
    #     dist = abs(proxB.signed_distance([center])[0])

    #     if dist < tol:
    #         common_faces.append(i)

    # concave_boundary = concave_region.submesh([common_faces], append=True)
    # concave_boundary.export(OUT_DIR / "3. common_surface.stl")

    # pieces = subtract_surface(B, common_surface)

        # prox = trimesh.proximity.ProximityQuery(concave_wall)

    # common_faces_to_remove = []
    # for i, tri in enumerate(concave_region.triangles):
    #     dist = abs(prox.signed_distance([tri.mean(axis=0)])[0])
    #     if dist < tol:
    #         common_faces_to_remove.append(i)

    # flow_inlet_outlet = concave_region.submesh([np.setdiff1d(range(len(concave_region.faces)), common_faces_to_remove)], append=True)

    # flow_inlet_outlet = concave_region.difference(concave_wall, engine='scad')
