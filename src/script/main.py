
import time
from script.base.dataframe_base import load_dataframes
from script.build_cache import build_cache
from script.analysis.course_analysis import *

from datetime import timedelta


def analyze(submission):
    start_time = time.clock()
    start_time_exec = time.time()

    dataframe = load_dataframes(submission.path())

    build_cache(dataframe)

    submission.set_done(round(time.clock() - start_time))

    cpu_time = timedelta(seconds=round(time.clock() - start_time))
    run_time = timedelta(seconds=round(time.time() - start_time_exec))
    print("--- Tempo de CPU: {} ---".format(cpu_time))
    print("--- Tempo total: {} ---".format(run_time))


def main():
    print("Não pra você estar fazendo isso")


if __name__ == "__main__":
    main()
