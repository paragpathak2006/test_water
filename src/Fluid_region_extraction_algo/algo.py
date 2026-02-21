from trimesh import Trimesh
from src.Performance.perfLog import PerfLog
from src.Geometry.Processing.pre import preprocess
from src.Geometry.Processing.post import postprocess
from src.Geometry.Processing.export import export_all

from src.Fluid_region_extraction_algo.selector import (
    convexhull_difference_selector as ConvHull_diff,
    mesh_intersection_difference_selector as int_diff,
    proximity_selector as prox,
    split_selector as split,
    tree_or_table_selector as tree_or_table,
)


class Fluid_region_extraction_algo:

    @classmethod
    def fluid_extraction_algo_summary(cls, solid: Trimesh, variant):

        prox_solid = prox(variant, solid)
        tree_table = tree_or_table(variant, solid)
        fluids = ConvHull_diff(variant, solid)

        for i, fluid in enumerate(fluids):
            wall, IOs_all = int_diff(variant, i, fluid, solid, prox_solid, tree_table)
            IOs = split(variant, i, IOs_all)
            if len(IOs) >= 2:
                cls.add(fluid, wall, IOs_all, IOs)

        return cls.embedded, cls.walls, cls.IOs

    @classmethod
    def fluid_extraction_algo(cls, solid: Trimesh, variant):

        if preprocess(solid) is None:
            return None

        # compute proximity query for solid volume to be used in intersection-difference method for extracting fluid walls and inlet-outlet boundaries
        prox_solid = prox(variant, solid)
        tree_table = tree_or_table(variant, solid)

        fluids = ConvHull_diff(variant, solid)
        if fluids is None:
            print(cls.convex_hull_difference_failed_msg)
            return None

        print("\n✅ Number of fluid volumes : ", len(fluids))

        for i, fluid in enumerate(fluids):
            print("\nExtracting fluid walls and inlet-outlet boundaries...")
            print("\nProcessing fluid volume#", i, " ...")
            print("\nVolume = ", fluid.volume)
            print("surface area = ", fluid.area)

            # extract fluid wall and inlet-outlet boundaries using intersection-difference method
            wall, IOs_all = int_diff(variant, i, fluid, solid, prox_solid, tree_table)
            IOs = split(variant, i, IOs_all)
            print(cls.num_of_fluids_msg(i, IOs))

            if len(IOs) >= 2:
                # Validation check for output fluid volume mesh
                if postprocess(fluid) is None:
                    return None

                print(cls.fluid_volume_path_validation_success_msg)
                # capturing the list of inlet-outlet boundary meshes
                cls.add(fluid, wall, IOs_all, IOs)

        PerfLog.line()

        if len(cls.embedded) == 0:
            print(cls.no_embedded_fluid_volume_msg)
            return None

        export_all(cls, variant)
        return cls.embedded, cls.walls, cls.IOs

    @classmethod
    def add(cls, fluid, wall, IOs_combined, IOs):
        # capturing the fluid volume mesh that form a valid path with atleast 2 open boundaries (i.e. inlet and outlet)
        cls.embedded.append(fluid)
        cls.walls.append(wall)  # capturing the fluid wall mesh
        cls.IOs_all.append(IOs_combined)
        cls.IOs.append(IOs)
        # capturing the list of inlet-outlet boundary meshes

    @classmethod
    def num_of_fluids_msg(cls, i, ios):
        return (
            f"For volume#{i} : Number of fluid inlet and outlet boundaries : {len(ios)}"
        )

    convex_hull_difference_failed_msg = "❌ Convex hull difference algorithm failed or Solid is already convex.No fluid volumes extracted."
    fluid_volume_path_validation_success_msg = "\n✅ Multiple fluid inlets-outlets detected. Fluid volume represents a valid embedded path."
    no_embedded_fluid_volume_msg = "\n❌ No valid embedded fluid volumes with atleast 2 open boundaries (i.e. inlet and outlet) detected.❌"

    # result list to store combined inlet-outlet boundary meshes for each fluid volume
    embedded = []
    walls = []  # result list to store fluid wall meshes
    IOs_all = []
    IOs = []

    @classmethod
    def cleanup(cls):
        cls.embedded = []
        cls.walls = []  # result list to store fluid wall meshes
        cls.IOs_all = []
        cls.IOs = []
