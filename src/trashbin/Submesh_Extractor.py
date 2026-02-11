
import trimesh
import numpy as np

def subtract_submesh(mesh, submesh, tol=1e-6):
    
    prox = trimesh.proximity.ProximityQuery(submesh)

    common_faces_to_remove = []
    for i, tri in enumerate(mesh.triangles):
        dist = abs(prox.signed_distance([tri.mean(axis=0)])[0])
        if dist < tol:
            common_faces_to_remove.append(i)

    result = mesh.submesh([np.setdiff1d(range(len(mesh.faces)), common_faces_to_remove)], append=True)
    return result

# def face_key(verts, tol=1e-6):
#     v = np.round(verts / tol) * tol
#     return tuple(sorted(map(tuple, v)))

#    # build hash set of faces to remove
#     remove_keys = set()
#     for f in submesh.faces:
#         remove_keys.add(face_key(submesh.vertices[f], tol))

#     keep_faces = []
#     for i, f in enumerate(mesh.faces):
#         if face_key(mesh.vertices[f], tol) not in remove_keys:
#             keep_faces.append(i)

#     # build remaining mesh
#     flow_inlet_outlet = mesh.submesh([keep_faces], append=True)

#     # split into connected surface patches
#     pieces = flow_inlet_outlet.split(only_watertight=False)

#     return pieces
