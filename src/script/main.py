
import time
from script.base.dataframe_base import load_dataframes
from script.build_cache import build_cache

from datetime import timedelta


def analyze(submission, debug=True):
    print(submission.path())


    start_time = time.clock()
    start_time_exec = time.time()
    try:
        path = submission.path()
        dataframe = load_dataframes(path)

        build_cache(dataframe, path)

        submission.set_done(round(time.clock() - start_time))

        cpu_time = timedelta(seconds=round(time.clock() - start_time))
        run_time = timedelta(seconds=round(time.time() - start_time_exec))
        if(debug):
            print("--- Tempo de CPU: {} ---".format(cpu_time))
            print("--- Tempo total: {} ---".format(run_time))

    except:
        if(debug):
            print("Error on submission analysis:",ValueError)
        
        submission.set_fail(round(time.clock() - start_time))
    


def main():
    print("Não pra você estar fazendo isso")


if __name__ == "__main__":
    main()
