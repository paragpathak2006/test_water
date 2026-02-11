import trimesh
from trimesh import Trimesh
import numpy as np

""" Mesh faces : A - B = C """
def mesh_faces_difference(mesh_A : Trimesh, mesh_B : Trimesh, tol=1e-5):
  
    prox = trimesh.proximity.ProximityQuery(mesh_B)

    common_faces_to_remove = []
    for i, tri in enumerate(mesh_A.triangles):
        dist = abs(prox.signed_distance([tri.mean(axis=0)])[0])
        if dist < tol:
            common_faces_to_remove.append(i)

    mesh_C = mesh_A.submesh([np.setdiff1d(range(len(mesh_A.faces)), common_faces_to_remove)], append=True)

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
