from trimesh import Trimesh
from src.Geometry.Tolerence.mesh import Tolerence as Tol


def baseline_validation_check(mesh: Trimesh):

    if mesh.is_volume:
        print("✅ Validation check cleared")
        print(
            "✅ The mesh dose represents a valid watertight volume with consistent normals ..."
        )
        print("Volume of mesh : ", mesh.volume)

        if abs(mesh.volume) < Tol.VOLUME:
            print(
                "⚠️ However, the volume of the mesh is very small (close to zero). This may indicate a degenerate or nearly flat mesh. Please check the mesh for issues such as coplanar faces or very thin geometry."
            )
            return False

    else:
        print(
            "❌ The mesh does NOT represent a valid watertight volume. Check the mesh for issues such as holes, non-manifold edges, or inconsistent normals."
        )

    return mesh.is_volume
