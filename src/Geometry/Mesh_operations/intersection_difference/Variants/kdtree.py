from trimesh import Trimesh
import numpy as np
import scipy.spatial as spatial
import trimesh

""" Mesh faces : A ∩ B = C """
""" Mesh faces : A - B = D """


def mesh_faces_intersection_difference(mesh_A: Trimesh, mesh_B: Trimesh, tol=1e-5):

    centA = mesh_A.triangles_center
    centB = mesh_B.triangles_center

    normA = mesh_A.face_normals
    normB = mesh_B.face_normals

    treeB = spatial.KDTree(centB)

    tol_dot = 1e-7  # tolerance for dot product to consider normals as parallel (i.e. faces are coplanar)

    common_faces = []

    for iA, centroid in enumerate(centA):

        dist, iB = treeB.query(centroid)
        if dist < tol and abs(np.dot(normA[iA], normB[iB])) > 1 - tol_dot:
            common_faces.append(iA)
        # else:
        #     if dist < 1:
        #         proxB_dist = abs(proxB.signed_distance([centroid])[0])
        #         if proxB_dist < tol:
        #             common_faces.append(iA)

    # common(mesh_A, mesh_B, common_faces, tol)
    print("Intersection mesh extracted with", len(common_faces), " faces")

    # remove common faces from A to get difference mesh C
    uncommon_faces = np.setdiff1d(range(len(mesh_A.faces)), common_faces)

    # transfer faces from uncommon to common if they are actually close to B (i.e. within tol) but were missed by the KDTree query due to its approximation, by rechecking the distance of uncommon faces to B using the proximity query
    transferred_faces = recheck_intersection_proxQ(mesh_A, mesh_B, uncommon_faces, tol)

    # Update common and uncommon faces after rechecking
    common_faces = np.array(common_faces + transferred_faces)
    uncommon_faces = np.setdiff1d(uncommon_faces, transferred_faces)
    common_faces.sort()
    uncommon_faces.sort()

    # Make two submeshes C and D from  A with the common faces and uncommon faces respectively
    mesh_C = mesh_A.submesh([common_faces], append=True)
    mesh_D = mesh_A.submesh([uncommon_faces], append=True)

    return {"intersection": mesh_C, "difference": mesh_D}


def recheck_intersection_proxQ(
    mesh_A: Trimesh, mesh_B: Trimesh, uncommon_faces_A, tol=1e-5
):

    proxB = trimesh.proximity.ProximityQuery(mesh_B)

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


# def common(mesh_A: Trimesh, mesh_B: Trimesh, KDTREE_common_faces, tol=1e-5):

#     centA = mesh_A.triangles_center
#     centB = mesh_B.triangles_center

#     normA = mesh_A.face_normals
#     normB = mesh_B.face_normals

#     # Compute proximity query for mesh_B
#     proxB = trimesh.proximity.ProximityQuery(mesh_B)

#     # List to store indices of faces in A that are close to B (i.e. common surface)
#     prox_common_faces = []

#     # extract faces of A that are close to B (i.e. common surface)
#     for iA, tri in enumerate(mesh_A.triangles):
#         center = tri.mean(axis=0)
#         dist = abs(proxB.signed_distance([center])[0])

#         if dist < tol:
#             prox_common_faces.append(iA)

#         if iA in [10, 99, 150, 151]:
#             print(f"ProxB = {proxB.signed_distance([center])[0]}")

#             print(f"iA = {iA}")
#             print(f"center = {center}")
#             print(f"centroid = {centA[iA]}")
#             print(f"normal = {normA[iA]}")

#             print("dist : ", dist)
#             print("dist < tol : ", dist < tol)

#             print(f"Verdict : Face {iA} is {'common' if dist < tol else 'not common'}")

#             print("--------------------------------------------------")

#     # Debugging: print the common faces found by both methods and check if they match
#     diff_prox = set(prox_common_faces) - set(KDTREE_common_faces)

#     if diff_prox:
#         print("Faces found by proximity method but not by KDTree method:", diff_prox)
#         for i in diff_prox:
#             print(mesh_A.faces[i])

#     diff_kdtree = set(KDTREE_common_faces) - set(prox_common_faces)
#     if diff_kdtree:
#         print("Faces found by KDTree but not by proximity method:", diff_kdtree)
#         for i in diff_kdtree:
#             print(mesh_A.faces[i])

#     if iA in [10, 99, 150, 151]:

#         dist2 = float('inf')
#         closest_iB = None
#         for iB2, centroidB in enumerate(centB):
#             if dist2 > np.linalg.norm(centroid - centroidB):
#                 dist2 = np.linalg.norm(centroid - centroidB)
#                 closest_iB = iB2

#         dist, iB = treeB.query(centroid)
#         res = treeB.query_ball_point(centroid, tol)
#         if dist < tol and abs(np.dot(normA[iA], normB[iB])) > 1 - tol_dot:
#             common_faces.append(iA)

#         print(f"iA = {iA}")
#         print(f"centroid = {centroid}")
#         print(f"normal = {normA[iA]}")

#         print(f"iB = {iB}")
#         print(f"centroid = {centB[iB]}")
#         print(f"normal = {normB[iB]}")

#         print(f"closest_iB = {closest_iB}")
#         print(f"centroid = {centB[closest_iB]}")
#         print(f"normal = {normB[closest_iB]}")
#         print(f"dist2 = {dist2}")

#         print(f"dot product = {np.dot(normA[iA], normB[iB])}")

#         print("dist : ", dist)
#         print("dist < tol : ", dist < tol)

#         print("abs(dot) > 1 - tol_dot : ", abs(np.dot(normA[iA], normB[iB])) > 1 - tol_dot)
#         print("abs(dot) : ", abs(np.dot(normA[iA], normB[iB])))

#         print(f"Verdict : Face {iA} is {'common' if dist < tol and abs(np.dot(normA[iA], normB[iB])) > 1 - tol_dot else 'not common'}")

#         print("--------------------------------------------------")
