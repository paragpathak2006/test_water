from trimesh import Trimesh
import numpy as np
from src.Geometry.Tolerence.mesh import Tolerence as Tol

""" Mesh faces : A ∩ B = C """
""" Mesh faces : A - B = D """


def mesh_faces_intersection_difference(
    mesh_A: Trimesh, hashtableB, proxB, tol=Tol.DIST
):
    # Find common faces (C) and uncommon faces (D) of mesh A with respect to mesh B using the hash table for an initial intersection query
    common_faces = intersect_faces(mesh_A, hashtableB)
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

    return mesh_C, mesh_D


# This function rechecks the faces that were classified as uncommon (i.e. not intersecting) to see if any of them are actually close enough to the other mesh (within a specified tolerance) to be considered as intersecting. This is necessary because the initial intersection query using the hash table may miss some faces due to its approximation, and the proximity query provides a more accurate distance measurement to ensure that we correctly classify faces as common or uncommon.
def recheck_intersection_proxQ(mesh_A: Trimesh, proxB, uncommon_faces_A, tol=Tol.DIST):

    transferred_faces = []

    for iA in uncommon_faces_A:
        centroid = mesh_A.triangles_center[iA]
        dist = abs(proxB.signed_distance([centroid])[0])

        if dist <= tol:
            transferred_faces.append(iA)
            print(
                f"⚠️ Face {iA} transferred from uncommon to common. Distance to B = {dist}"
            )

    return transferred_faces


# Intersect faces of mesh A with the hash table of mesh B to find common faces. This function checks the centroids of the faces in mesh A against the quantized keys in the hash table of mesh B to identify which faces are likely to be intersecting or close to faces in mesh B, which is a crucial step in the intersection-difference algorithm for mesh processing.
def intersect_faces(meshA: Trimesh, hashtableB):
    common = []

    centroids = meshA.triangles_center
    for i, centroid in enumerate(centroids):
        key = quantize(centroid)

        if key in hashtableB:
            common.append(i)

    return common


# Build a hash table for the faces of a mesh based on the quantized centroids of the faces. This allows for efficient lookup of faces in another mesh that are close to these centroids, which is useful for intersection queries in the mesh processing algorithms.
def build_face_hash(mesh: Trimesh):
    table = set()

    centroids = mesh.triangles_center
    for centroid in centroids:
        table.add(quantize(centroid))

    return table


def face_key(vertices):
    keys = [quantize(v) for v in vertices]
    return tuple(sorted(keys))


# Quantization function to convert 3D coordinates to discrete keys for hashing, with a specified scale factor to control the precision of the quantization. This helps in efficiently identifying nearby faces in the mesh for intersection queries while being robust to small numerical differences.
def quantize(v, scale=1e6):
    return tuple(np.round(v * scale).astype(int))
