import trimesh
from trimesh import Trimesh

""" Mesh faces : A ∩ B = C """


def mesh_faces_intersection(mesh_A: Trimesh, mesh_B: Trimesh, tol=1e-5):

    # Compute proximity query for mesh_B
    proxB = trimesh.proximity.ProximityQuery(mesh_B)

    # List to store indices of faces in A that are close to B (i.e. common surface)
    common_faces = []

    # extract faces of A that are close to B (i.e. common surface)
    for i, tri in enumerate(mesh_A.triangles):
        center = tri.mean(axis=0)
        dist = abs(proxB.signed_distance([center])[0])

        if dist < tol:
            common_faces.append(i)

    print("Intersection mesh extracted with", len(common_faces), " faces")

    # Make submesh of A with only the faces that are in common with B
    mesh_C = mesh_A.submesh([common_faces], append=True)

    return mesh_C
