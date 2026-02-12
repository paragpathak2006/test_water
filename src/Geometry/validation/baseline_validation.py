from trimesh import Trimesh


def baseline_validation_check(mesh: Trimesh):

    if mesh.is_volume:
        print("✅ Validation check cleared")
        print(
            "✅ The mesh dose represents a valid watertight volume with consistent normals ..."
        )
        print("Volume of mesh : ", mesh.volume)

    else:
        print(
            "❌ The mesh does NOT represent a valid watertight volume. Check the mesh for issues such as holes, non-manifold edges, or inconsistent normals."
        )

    return mesh.is_volume
