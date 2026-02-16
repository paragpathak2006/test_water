from trimesh import Trimesh
import numpy as np

""" Mesh faces : A ∩ B = C """
""" Mesh faces : A - B = D """


def mesh_faces_intersection_difference(mesh_A: Trimesh, mesh_B: Trimesh, tol=1e-5):

    common_faces_A = intersect_faces(mesh_A, mesh_B)
    uncommon_faces_A = np.setdiff1d(range(len(mesh_A.faces)), common_faces_A)

    mesh_C = mesh_A.submesh([common_faces_A], append=True)
    mesh_D = mesh_A.submesh([uncommon_faces_A], append=True)

    print("Intersection mesh extracted with", len(common_faces_A), " faces")
    return {"intersection": mesh_C, "difference": mesh_D}


def intersect_faces(meshA: Trimesh, meshB: Trimesh):
    tableB = build_face_hash(meshB)
    common = []

    for i, f in enumerate(meshA.faces):
        verts = meshA.vertices[f]
        key = face_key(verts)

        if key in tableB:
            common.append(i)

    return np.array(common)


def build_face_hash(mesh: Trimesh):
    table = set()

    for f in mesh.faces:
        verts = mesh.vertices[f]
        table.add(face_key(verts))

    return table


def face_key(vertices):
    q = [quantize(v) for v in vertices]
    return tuple(sorted(q))


def quantize(v, scale=1e6):
    return tuple(np.round(v * scale).astype(int))
