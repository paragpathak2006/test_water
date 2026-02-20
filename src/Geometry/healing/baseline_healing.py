from trimesh import Trimesh


def baseline_heal(mesh: Trimesh):

    mesh_is_volume_msg = "✅ The mesh already represents a valid watertight volume with consistent normals. No healing needed."
    healing_success_msg = "✅ Healing successful: The mesh now represents a valid watertight volume with consistent normals."
    healing_failed_msg = "❌ Healing failed: The mesh still does NOT represent a valid watertight volume. Check the mesh for remaining issues such as holes, non-manifold edges, or inconsistent normals."

    if mesh.is_volume:
        print(mesh_is_volume_msg)
        print("✅ Volume of mesh:", mesh.volume)
        return mesh  # No healing needed, return True

    mesh.process(
        validate=True
    )  # process the mesh to attempt to fix common issues like non-manifold edges, duplicate vertices, etc.
    mesh.remove_unreferenced_vertices()  # remove any vertices that are not referenced by any faces, as they can cause issues with healing
    mesh.fill_holes()  # fill holes in the mesh, which can help make it watertight

    if mesh.volume > 0:
        mesh.fix_normals()  # fix normals to ensure they are consistent and pointing outward, which is important for a valid volume

    if mesh.is_volume:
        print(healing_success_msg)
        print("✅ Volume of mesh:", mesh.volume)
        return mesh
    else:
        print(healing_failed_msg)
        return False  # Healing failed, return False
