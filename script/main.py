import os
import time
from base.dataframe_base import load_dataframes
from build_cache import build_cache
from datetime import timedelta
from utils.situations import *
from analysis.course_analysis import *
def main():
    start_time = time.clock()
    start_time_exec = time.time()
    dataframe = load_dataframes(os.getcwd() + '/' + 'base')
    build_cache(dataframe)
    Main(dataframe)
    cpu_time = timedelta(seconds=round(time.clock() - start_time))
    run_time = timedelta(seconds=round(time.time() - start_time_exec))
    print("--- Tempo de CPU: {} ---".format(cpu_time))
    print("--- Tempo total: {} ---".format(run_time))

if __name__ == "__main__":
    main()
