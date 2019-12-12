import time
from submission.analysis.base.dataframe_base import load_dataframes
from submission.analysis.build_cache import build_cache

from datetime import timedelta
import traceback


def analyze(submission, debug=True):
    start_time = time.clock()
    start_time_exec = time.time()
    submission.set_executing()
    try:
        path = submission.path()
        dataframe = load_dataframes(path)

        build_cache(dataframe, path, submission.degree.code,
                    submission.relative_year, submission.relative_semester)

        submission.set_done(round(time.clock() - start_time))

        cpu_time = timedelta(seconds=round(time.clock() - start_time))
        run_time = timedelta(seconds=round(time.time() - start_time_exec))
        if(debug):
            print("--- Tempo de CPU: {} ---".format(cpu_time))
            print("--- Tempo total: {} ---".format(run_time))


    except Exception as e:
        error = traceback.format_exc()
        # if(debug):
        #     print("Error on submission analysis:", error)
        print("Error on submission analysis:", error)

        submission.set_fail(round(time.clock() - start_time), error_message=str(error))


if __name__ == "__main__":
    pass
