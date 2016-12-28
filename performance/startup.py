import statistics
from timeit import Timer
from subprocess import check_call, DEVNULL

class Stat:
    name = None
    call = None
    avg = None
    call = None
    data = None


benchmarks = [
    ["/bin/true"],
    ["/usr/bin/python3", "-c", ""],
    ["/usr/bin/python3", "-S", "-c", ""],
    ["/usr/bin/python3", "-m", "infoline"],
    ["/usr/bin/python3", "import_1.py"],
    ["/usr/bin/python3", "import_infoline.py"]
]

if __name__ == "__main__":
    stats = []
    for bench in benchmarks:
        def call():
            check_call(bench, stdout=DEVNULL)
        stat = Stat()
        stat.call = call
        stat.name = " ".join(bench)
        stat.data = Timer(call).repeat(100, 1)
        stat.avg = statistics.mean(stat.data)
        stat.dev = statistics.pstdev(stat.data)
        stats.append(stat)
    for stat in sorted(stats, key=lambda x: x.avg):
        print("{s.name:>35}: {s.avg:.6f}s ~{s.dev:.6f}s".format(s=stat))
