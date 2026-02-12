from trimesh import Trimesh


def baseline_heal(mesh: Trimesh):

    if mesh.is_volume:
        print(
            "✅ The mesh already represents a valid watertight volume with consistent normals. No healing needed."
        )
        print("✅ Volume of mesh:", mesh.volume)
        return True  # No healing needed, return True

    mesh.process(
        validate=True
    )  # process the mesh to attempt to fix common issues like non-manifold edges, duplicate vertices, etc.
    mesh.remove_unreferenced_vertices()  # remove any vertices that are not referenced by any faces, as they can cause issues with healing
    mesh.fill_holes()  # fill holes in the mesh, which can help make it watertight

    if mesh.volume > 0:
        mesh.fix_normals()  # fix normals to ensure they are consistent and pointing outward, which is important for a valid volume

    if mesh.is_volume:
        print(
            "✅ Healing successful: The mesh now represents a valid watertight volume with consistent normals."
        )
        print("✅ Volume of mesh:", mesh.volume)
    else:
        print(
            "❌ Healing failed: The mesh still does NOT represent a valid watertight volume. Check the mesh for remaining issues such as holes, non-manifold edges, or inconsistent normals."
        )

    return mesh.is_volume
