import os
import time
from datetime import timedelta
from script.base.dataframe_base import load_dataframes
from script.build_cache import build_cache


def analyze(submission):
    start_time = time.clock()
    start_time_exec = time.time()

    dataframe = load_dataframes(submission.path())

    build_cache(dataframe)

    cpu_time = timedelta(seconds=round(time.clock() - start_time))
    run_time = timedelta(seconds=round(time.time() - start_time_exec))
    print("--- Tempo de CPU: {} ---".format(cpu_time))
    print("--- Tempo total: {} ---".format(run_time))


def main():
    start_time = time.clock()
    start_time_exec = time.time()

    dataframe = load_dataframes(os.getcwd() + '/script/' + 'base')
    # ~ for i, line in enumerate(dataframe):
    # ~ print(type(dataframe["MEDIA_FINAL"][i]))
    # ~ print(dataframe["MEDIA_FINAL"][i])
    # ~ print(dataframe)
    build_cache(dataframe)

    cpu_time = timedelta(seconds=round(time.clock() - start_time))
    run_time = timedelta(seconds=round(time.time() - start_time_exec))
    print("--- Tempo de CPU: {} ---".format(cpu_time))
    print("--- Tempo total: {} ---".format(run_time))


if __name__ == "__main__":
    main()
