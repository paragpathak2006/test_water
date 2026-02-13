from trimesh import Trimesh
from .Convexhull_operations.self_difference import convex_hull_difference
from .Mesh_operations.intersection_difference import mesh_faces_intersection_difference
from .io_path import OUT_DIR
from ..Performance.perfLog import PerfLog
from ..Geometry.validation.baseline_validation import baseline_validation_check
from ..Geometry.healing.baseline_healing import baseline_heal


def kdtree_convexhull_difference(solid_volume: Trimesh):

    if not baseline_validation_check(solid_volume):
        print("❌Input solid volume mesh is not valid. Attempting to heal geometry.❌")
        baseline_heal(solid_volume)
        if not baseline_validation_check(solid_volume):
            print(
                "❌Input solid volume mesh could not be healed to a valid mesh. Aborting convex hull difference algorithm.❌"
            )
            return None
        else:
            print(
                "✅Input solid volume mesh has been successfully healed to a valid mesh. Proceeding with convex hull difference algorithm.✅"
            )

    print("\nRunning kdtree convex hull difference algorithm...\n")
    PerfLog.start("KDtree Convex hull difference")
    fluid_volumes = convex_hull_difference(solid_volume)
    PerfLog.stop("KDtree Convex hull difference")

    if fluid_volumes is None:
        print(
            "❌Convex hull difference algorithm failed or Solid is already convex. No fluid volumes extracted.❌"
        )
        return None

    print("\n✅ Number of fluid volumes : ", len(fluid_volumes))

    fluid_embedded_path = (
        []
    )  # result list to store fluid volume meshes that are embedded in the solid volume (i.e. not separate disconnected components) and can be used for CFD simulation without further processing
    fluid_walls = []  # result list to store fluid wall meshes
    fluid_inlets_outlets_all = (
        []
    )  # result list to store lists of inlet-outlet boundary meshes for each fluid volume

    for i, fluid_volume in enumerate(fluid_volumes):
        print("\nExtracting fluid walls and inlet-outlet boundaries...")

        print("\nProcessing fluid volume#", i, " ...")
        print("\nvolume = ", fluid_volumes[i].volume)
        print("surface area = ", fluid_volumes[i].area)

        print("\nExtracting fluid wall and inlet-outlet boundaries...\n")

        # extract fluid wall and inlet-outlet boundaries using intersection-difference method
        PerfLog.start("KDtree mesh faces (∩,Δ) - vol#" + str(i))
        fluid_boundary = mesh_faces_intersection_difference(
            fluid_volumes[i], solid_volume
        )
        PerfLog.stop("KDtree mesh faces (∩,Δ) - vol#" + str(i))

        fluid_wall = fluid_boundary["intersection"]
        fluid_inlets_outlets_combined = fluid_boundary["difference"]
        fluid_inlets_outlets = fluid_inlets_outlets_combined.split(
            only_watertight=False
        )

        print(
            "For volume#",
            i,
            " : Number of fluid inlet and outlet boundaries : ",
            len(fluid_inlets_outlets),
        )

        if len(fluid_inlets_outlets) >= 2:
            print(
                "\n✅ Multiple fluid inlets-outlets detected. Fluid volume represents a valid embedded path."
            )

            # Validation check for output fluid volume mesh
            if not baseline_validation_check(fluid_volumes[i]):
                print(
                    "❌ Output fluid volume mesh is not valid. Attempting to heal geometry.❌"
                )
                baseline_heal(fluid_volumes[i])
                if not baseline_validation_check(fluid_volumes[i]):
                    print(
                        "❌ Output fluid volume mesh could not be healed to a valid mesh. Aborting convex hull difference algorithm.❌"
                    )
                    return None
                else:
                    print(
                        "✅ Output fluid volume mesh has been successfully healed to a valid mesh. Proceeding with convex hull difference algorithm.✅"
                    )
            else:
                print(
                    "✅ Output fluid volume mesh is valid and represents a fluid volume. No healing needed."
                )

            export_fluid_volumes_and_boundaries(
                i,
                fluid_volume,
                fluid_wall,
                fluid_inlets_outlets_combined,
                fluid_inlets_outlets,
            )

            fluid_embedded_path.append(
                fluid_volumes[i]
            )  # capturing the fluid volume mesh that form a valid path with atleast 2 open boundaries (i.e. inlet and outlet)
            fluid_walls.append(fluid_wall)  # capturing the fluid wall mesh
            fluid_inlets_outlets_all.append(
                fluid_inlets_outlets
            )  # capturing the list of inlet-outlet boundary meshes

    return {
        "fluid_volumes": fluid_embedded_path,
        "fluid_walls": fluid_walls,
        "all_fluid_inlets_outlets": fluid_inlets_outlets_all,
    }


def export_fluid_volumes_and_boundaries(
    i, fluid_volume, fluid_wall, fluid_inlets_outlets_combined, fluid_inlets_outlets
):

    print(f"\n✅ Exporting file : fluid-volume-{i} ...")

    fluid_volume.export(OUT_DIR / f"1. fluid-volume-{i}.stl")

    # export each inlet-outlet boundary separately
    print(f"✅ Exporting file : fluid-wall-{i} ...")
    fluid_wall.export(OUT_DIR / f"2. fluid_wall-{i}.stl")

    print(f"✅ Exporting file : fluid-inlets-outlets-combined-{i} ...")
    fluid_inlets_outlets_combined.export(
        OUT_DIR / f"3. fluid_inlets-outlets-combined-{i}.stl"
    )

    for ii, fluid_inlet_outlet in enumerate(fluid_inlets_outlets):
        print(f"✅ Exporting file : fluid-inlet-outlet-{i}-{ii} ...")
        fluid_inlet_outlet.export(OUT_DIR / f"4. fluid-inlet-outlet-{i}-{ii}.stl")
