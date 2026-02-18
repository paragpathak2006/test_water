import os
from pathlib import Path
import numpy as np
import unittest

import trimesh
from src.Fluid_region_extraction_algo.test import test_fluid_extraction_algo

from src.Performance.perfLog import PerfLog, Algo, Variant

from tests.io_path import OUT_DIR as benchmark_OUT_DIR

from src.Fluid_region_extraction_algo.baseline.io_path import (
    OUT_DIR as baseline_OUT_DIR,
)
from src.Fluid_region_extraction_algo.Variant.kdtree.io_path import (
    OUT_DIR as kdtree_OUT_DIR,
)
from src.Fluid_region_extraction_algo.Variant.hashing.io_path import (
    OUT_DIR as hash_OUT_DIR,
)


class Run_Unit_Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):

        print("\nSetting up fluid volume extraction algorithm test...\n")

        cls.times = ["0.1", "0.1"]
        cls.maxTimeAllowed = 1  # time limit of 1 seconds

        cls.benchmark_files_list()
        cls.pre_cleanup_output_dir()

        print("─────୨ৎ────୨ৎ────୨ৎ────୨ৎ────\n\n")

    @classmethod
    def benchmark_files_list(cls):
        cls.files = get_files_list(benchmark_OUT_DIR)
        print("Files to be tested : ", cls.files)

    @classmethod
    def pre_cleanup_output_dir(cls):
        print("\nPre-cleaning up the output directory...\n")
        for file in cls.files:
            if file.startswith("0."):
                continue

            baseline_file = baseline_OUT_DIR / file
            if os.path.exists(baseline_file):
                os.remove(baseline_file)

            hash_file = hash_OUT_DIR / file
            if os.path.exists(hash_file):
                os.remove(hash_file)

            kdtree_file = kdtree_OUT_DIR / file
            if os.path.exists(kdtree_file):
                os.remove(kdtree_file)

        print("Pre-cleanup done.\n\n")

    def test_baseline_correctness(self):
        print("\n\n C1️⃣ testing baseline convex hull difference algorithm...")

        if test_fluid_extraction_algo(Variant.BASELINE) is None:
            self.fail(
                "❌ Baseline convex hull difference algorithm failed. Aborting test."
            )

        self.files_compare(benchmark_OUT_DIR, baseline_OUT_DIR)

        print("✅ Correctness test is OK\n\n")
        print("────────────────────────────────────────\n\n")

    def test_baseline_performance(self):
        print(
            "\n\n P1️⃣  testing performance of baseline convex hull difference algorithm...\n"
        )

        total_time = (
            PerfLog._events[Variant.BASELINE(Algo.CONVEX_HULL_DIFFERENCE)]
            + PerfLog._events[Variant.BASELINE(Algo.MESH_INTERSECTION_DIFFERENCE(0))]
        )

        self.assertLessEqual(
            total_time,
            self.maxTimeAllowed,
            f"❌ Performance test failed: Time taken {total_time * 1e3:.1f}ms exceeds allowed limit of {self.maxTimeAllowed * 1e3:.0f}ms",
        )

        print(
            f"\n✅ Performance test passed: Total time taken: {total_time * 1e3:.1f}ms is within the allowed limit of {self.maxTimeAllowed * 1e3:.0f}ms\n"
        )

        print("✅ Performance Test is OK\n\n")
        print("────────────────────────────────────────\n\n")

    def test_kdtree_correctness(self):
        print("\n\n C2️⃣   Testing kdtree convex hull difference algorithm...")

        if test_fluid_extraction_algo(Variant.KDTREE) is None:
            self.fail(
                "❌ KDtree convex hull difference algorithm failed. Aborting test."
            )

        self.files_compare(benchmark_OUT_DIR, kdtree_OUT_DIR)

        print("✅ Correctness test is OK\n\n")
        print("────────────────────────────────────────\n\n")

    def test_kdtree_performance(self):
        print(
            "\n\n P2️⃣   testing performance of kdtree convex hull difference algorithm...\n"
        )

        total_time = (
            PerfLog._events[Variant.KDTREE(Algo.CONVEX_HULL_DIFFERENCE)]
            + PerfLog._events[Variant.KDTREE(Algo.MESH_INTERSECTION_DIFFERENCE(0))]
        )

        self.assertLessEqual(
            total_time,
            self.maxTimeAllowed,
            f"❌ Performance test failed: Time taken {total_time * 1e3:.1f}ms exceeds allowed limit of {self.maxTimeAllowed * 1e3:.0f}ms",
        )

        print(
            f"\n✅ Performance test passed: Total time taken: {total_time * 1e3:.1f}ms is within the allowed limit of {self.maxTimeAllowed * 1e3:.0f}ms\n"
        )

        print("✅ Performance Test is OK\n\n")
        print("────────────────────────────────────────\n\n")

    def test_hash_intersection_correctness(self):
        print("\n\n C3️⃣  Testing hash intersection algorithm...")

        if test_fluid_extraction_algo(Variant.HASH_INTERSECTION) is None:
            self.fail("❌ Hash intersection algorithm failed. Aborting test.")

        self.files_compare(benchmark_OUT_DIR, hash_OUT_DIR)

        print("✅ Correctness test is OK\n\n")
        print("────────────────────────────────────────\n\n")

    def test_hash_intersection_performance(self):
        print("\n\n  P3️⃣   testing performance of hash intersection algorithm...\n")

        total_time = (
            PerfLog._events[Variant.HASH_INTERSECTION(Algo.CONVEX_HULL_DIFFERENCE)]
            + PerfLog._events[
                Variant.HASH_INTERSECTION(Algo.MESH_INTERSECTION_DIFFERENCE(0))
            ]
        )

        self.assertLessEqual(
            total_time,
            self.maxTimeAllowed,
            f"❌ Performance test failed: Time taken {total_time * 1e3:.1f}ms exceeds allowed limit of {self.maxTimeAllowed * 1e3:.0f}ms",
        )

        print(
            f"\n✅ Performance test passed: Total time taken: {total_time * 1e3:.1f}ms is within the allowed limit of {self.maxTimeAllowed * 1e3:.0f}ms\n"
        )

        print("✅ Performance Test is OK\n\n")
        print("────────────────────────────────────────\n\n")

    # Final report after all tests are done
    def test_report_all(self):
        print(
            "\n 4️⃣ All tests completed... \n 📝 ✅✅ Final performance report ✅✅\n"
        )
        PerfLog.report()

    # Helper function to compare files in two directories
    def files_compare(self, DIR1, DIR2):

        files = get_files_list(DIR1)

        for file in files:
            print("📁 Comparing file : ", file)

            mesh1 = trimesh.load(DIR1 / file)
            mesh2 = trimesh.load(DIR2 / file)

            self.assertTrue(
                np.array_equal(mesh1.faces, mesh2.faces),
                f"❌ Face arrays are not equal for file {file}",
            )
            self.assertTrue(
                np.allclose(mesh1.vertices, mesh2.vertices),
                f"❌ Vertex arrays are not close for file {file}",
            )


# Helper function to get list of files in a directory
def get_files_list(DIR):
    print(f"\nGetting list of files in directory : {DIR}")
    files = [p.name for p in Path(DIR).iterdir() if p.is_file()]

    print("files found : ")
    for i, file in enumerate(files):
        print(f"📁 {i}: {file}")

    return files


if __name__ == "__main__":
    unittest.main()
