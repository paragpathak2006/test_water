import time


class PerfLog:
    _events = {}
    _start = time.perf_counter()

    @staticmethod
    def start(name: str):
        PerfLog._events[name] = time.perf_counter()

    @staticmethod
    def stop(name: str):
        PerfLog._events[name] = time.perf_counter() - PerfLog._events[name]

    @staticmethod
    def report():
        print("-- Event Times --")
        for name, time_ in PerfLog._events.items():
            print(f"{name:20}  Δt = {time_:8.4f}s")
