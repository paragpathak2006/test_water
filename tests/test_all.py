import os
from pathlib import Path
import numpy as np
import unittest

import trimesh
from src.Hash_intersection_algo.test_kdtree_algo import test_hash_intersection
from src.KDtree_convexhull_difference_algo.test_kdtree_algo import (
    test_kdtree_convexhull_difference,
)
from src.Baseline_convexhull_difference_algo.test_baseline_algo import (
    test_baseline_convexhull_difference,
)
from src.Performance.perfLog import PerfLog, TargetAlgo

from tests.io_path import OUT_DIR as benchmark_OUT_DIR
from tests.io_path import OUT_DIR_2 as benchmark_2_OUT_DIR

from src.Baseline_convexhull_difference_algo.io_path import OUT_DIR as baseline_OUT_DIR
from src.KDtree_convexhull_difference_algo.io_path import OUT_DIR as kdtree_OUT_DIR
from src.Hash_intersection_algo.io_path import OUT_DIR as hash_OUT_DIR


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
        cls.files = [p.name for p in Path(benchmark_OUT_DIR).iterdir() if p.is_file()]
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

    def test_baseline_convexhull_difference(self):
        print("\n\n 1️⃣ testing baseline convex hull difference algorithm...")

        if test_baseline_convexhull_difference() is None:
            self.fail(
                "❌ Baseline convex hull difference algorithm failed. Aborting test."
            )

        self.files_compare(benchmark_OUT_DIR, baseline_OUT_DIR)

        print("✅ Correctness test is OK\n\n")
        print("────────────────────────────────────────\n\n")

    def test_performance_baseline_convex_hull_algo(self):
        print(
            "\n\n 2️⃣  testing performance of baseline convex hull difference algorithm...\n"
        )

        total_time = (
            PerfLog._events[TargetAlgo.BASELINE.CONVEX_HULL_DIFFERENCE]
            + PerfLog._events[TargetAlgo.BASELINE.MESH_INTERSECTION_DIFFERENCE(0)]
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

    def test_kdtree_convexhull_difference(self):
        print("\n\n  3️⃣  Testing kdtree convex hull difference algorithm...")

        if test_kdtree_convexhull_difference() is None:
            self.fail(
                "❌ KDtree convex hull difference algorithm failed. Aborting test."
            )

        self.files_compare(benchmark_OUT_DIR, kdtree_OUT_DIR)

        print("✅ Correctness test is OK\n\n")
        print("────────────────────────────────────────\n\n")

    def test_performance_kdtree_convex_hull_algo(self):
        print(
            "\n\n  4️⃣  testing performance of kdtree convex hull difference algorithm...\n"
        )

        total_time = (
            PerfLog._events[TargetAlgo.KDTREE.CONVEX_HULL_DIFFERENCE]
            + PerfLog._events[TargetAlgo.KDTREE.MESH_INTERSECTION_DIFFERENCE(0)]
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

    def test_hash_intersection_algo(self):
        print("\n\n 5️⃣  Testing hash intersection algorithm...")

        if test_hash_intersection() is None:
            self.fail("❌ Hash intersection algorithm failed. Aborting test.")

        self.files_compare(benchmark_2_OUT_DIR, hash_OUT_DIR)

        print("✅ Correctness test is OK\n\n")
        print("────────────────────────────────────────\n\n")

    def test_performance_hash_intersection_algo(self):
        print("\n\n  6️⃣   testing performance of hash intersection algorithm...\n")

        total_time = (
            PerfLog._events[TargetAlgo.HASH_INTERSECTION.CONVEX_HULL_DIFFERENCE]
            + PerfLog._events[
                TargetAlgo.HASH_INTERSECTION.MESH_INTERSECTION_DIFFERENCE(0)
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
    def test_report(self):
        print(
            "\n 7️⃣ All tests completed... \n 📝 ✅✅ Final performance report ✅✅\n"
        )
        PerfLog.report()

    # Helper function to compare files in two directories
    def files_compare(self, DIR1, DIR2):

        files = [p.name for p in Path(DIR1).iterdir() if p.is_file()]

        for file in files:
            print("📁 Comparing file : ", file)

            baseline_mesh = trimesh.load(DIR1 / file)
            benchmark_mesh = trimesh.load(DIR2 / file)

            self.assertTrue(
                np.array_equal(baseline_mesh.faces, benchmark_mesh.faces),
                f"❌ Face arrays are not equal for file {file}",
            )
            self.assertTrue(
                np.allclose(baseline_mesh.vertices, benchmark_mesh.vertices),
                f"❌ Vertex arrays are not close for file {file}",
            )


if __name__ == "__main__":
    unittest.main()
