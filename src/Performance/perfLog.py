import time


class TargetAlgo:

    class BASELINE:
        CONVEX_HULL_DIFFERENCE = "Baseline CHD"

        def MESH_INTERSECTION_DIFFERENCE(i):
            return f"Baseline mesh (∩,Δ) - vol#{i}"

        def SPLIT(i):
            return f"Baseline split - vol#{i}"

    class KDTREE:
        CONVEX_HULL_DIFFERENCE = "KDtree CHD"

        def MESH_INTERSECTION_DIFFERENCE(i):
            return f"KDtree mesh (∩,Δ) - vol#{i}"

        def SPLIT(i):
            return f"KDtree split - vol#{i}"

    class HASH_INTERSECTION:
        CONVEX_HULL_DIFFERENCE = "Hash Intersection CHD"

        def MESH_INTERSECTION_DIFFERENCE(i):
            return f"Hash Intersection mesh (∩,Δ) - vol#{i}"

        def SPLIT(i):
            return f"Hash Intersection split - vol#{i}"


class PerfLog:
    _events = {}
    _start = time.perf_counter()

    @staticmethod
    def start(name: str):
        PerfLog._events[name] = time.perf_counter()

    @staticmethod
    def log(name: str, func: callable, *args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        PerfLog._events[name] = time.perf_counter() - start_time
        return result

    @staticmethod
    def stop(name: str):
        PerfLog._events[name] = time.perf_counter() - PerfLog._events[name]

    @staticmethod
    def report():
        print(" Event Times ")
        for name, time_ in PerfLog._events.items():
            print(f" 📍 {name:20}  Δt = ⏰{time_ * 1e3:8.4f}ms")
