from trimesh import Trimesh
import numpy as np

""" Mesh faces : A ∩ B = C """
""" Mesh faces : A - B = D """


def mesh_faces_intersection_difference(
    mesh_A: Trimesh, mesh_B: Trimesh, hashtableB, proxB, tol=1e-5
):

    common_faces = intersect_faces(mesh_A, mesh_B, hashtableB)
    # remove common faces from A to get difference mesh C
    uncommon_faces = np.setdiff1d(range(len(mesh_A.faces)), common_faces)

    # transfer faces from uncommon to common if they are actually close to B (i.e. within tol) but were missed by the KDTree query due to its approximation, by rechecking the distance of uncommon faces to B using the proximity query
    transferred_faces = recheck_intersection_proxQ(mesh_A, proxB, uncommon_faces, tol)

    # Update common and uncommon faces after rechecking
    common_faces = np.array(common_faces + transferred_faces)
    uncommon_faces = np.setdiff1d(uncommon_faces, transferred_faces)

    common_faces.sort()
    uncommon_faces.sort()

    # Make two submeshes C and D from  A with the common faces and uncommon faces respectively
    mesh_C = mesh_A.submesh([common_faces], append=True)
    mesh_D = mesh_A.submesh([uncommon_faces], append=True)

    return {"intersection": mesh_C, "difference": mesh_D}


def recheck_intersection_proxQ(mesh_A: Trimesh, proxB, uncommon_faces_A, tol=1e-5):

    transferred_faces = []

    for iA in uncommon_faces_A:
        centroid = mesh_A.triangles_center[iA]
        dist = abs(proxB.signed_distance([centroid])[0])

        if dist <= tol:
            transferred_faces.append(iA)
            print(
                f"Face {iA} transferred from uncommon to common. Distance to B = {dist}"
            )

    return transferred_faces


def intersect_faces(meshA: Trimesh, meshB: Trimesh, hashtableB):
    common = []

    for i, f in enumerate(meshA.faces):
        verts = meshA.vertices[f]
        key = face_key(verts)

        if key in hashtableB:
            common.append(i)

    return common


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
