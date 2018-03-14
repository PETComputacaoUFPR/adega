import os
import time
from script.base.dataframe_base import load_dataframes
from script.build_cache import build_cache
from datetime import timedelta
from script.analysis.degree_analysis import *
from script.utils.situations import *
from script.analysis.course_analysis import *

from datetime import timedelta
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
    build_cache(dataframe)
    cpu_time = timedelta(seconds=round(time.clock() - start_time))
    analises_disciplinas(dataframe)
    run_time = timedelta(seconds=round(time.time() - start_time_exec))
    print("--- Tempo de CPU: {} ---".format(cpu_time))
    print("--- Tempo total: {} ---".format(run_time))

if __name__ == "__main__":
    main()
