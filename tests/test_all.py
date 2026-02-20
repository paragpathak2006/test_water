import unittest
from tests.helpers import files_compare, pre_cleanup_outputs

from src.Fluid_region_extraction_algo.test import test_fluid_extraction_algo

from src.Performance.perfLog import PerfLog, Algo, Variant

from data.io_path import (
    BASELINE_OUT_DIR,
    HASHING_OUT_DIR,
    KDTREE_OUT_DIR,
    BENCHMARK_INPUT_DIR,
)


class Run_Unit_Tests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        print("\nSetting up fluid volume extraction algorithm test...\n")

        cls.maxTimeAllowed = 1  # time limit of 1 seconds
        cls.pre_cleanup_output_dir()

        print("─────୨ৎ────୨ৎ────୨ৎ────୨ৎ────\n\n")

    @classmethod
    def pre_cleanup_output_dir(cls):
        print("Pre-cleaning output directories...")
        pre_cleanup_outputs([BASELINE_OUT_DIR, HASHING_OUT_DIR, KDTREE_OUT_DIR])
        print("Pre-cleanup done.\n\n")

    def test_baseline_correctness(self):
        print("\n\n C1️⃣ testing baseline convex hull difference algorithm...")

        if test_fluid_extraction_algo(Variant.BASELINE) is None:
            self.fail(
                "❌ Baseline convex hull difference algorithm failed. Aborting test."
            )

        files_compare(self, BENCHMARK_INPUT_DIR, BASELINE_OUT_DIR)
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

        files_compare(self, BENCHMARK_INPUT_DIR, KDTREE_OUT_DIR)

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

        files_compare(self, BENCHMARK_INPUT_DIR, HASHING_OUT_DIR)

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


if __name__ == "__main__":
    unittest.main()
