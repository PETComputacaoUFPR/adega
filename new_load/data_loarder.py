import re
import os
import sys
import pandas as pd
import pathlib
from pathlib import Path
from glob import glob
from json import load as json_load

#import django

#sys.path.append(os.getcwd())

#os.environ["DJANGON_SETTINGS_MODULE"] = "adega.settings"
#django.setup()


#from degree.models import *
#from student.models import *
#from course.models import *
#from admission.models import *
#from klass.models import *

def start():
   directory = os.fsencode('relatorios')
#   path = Path(str(directory))
#   print(path)
   for path, subdirs, files in os.walk(directory):
  #     print(subdirs) 
 #      print(pathlib.PurePath(str(p), 'teste'))
#       print(pathlib.PurePath(
       for f in files:
           print(f)
           file_path = pathlib.PurePath(str(path), str(f))
           print(pathlib.PurePath(str(path), str(f)))
           file_open(file_path)
        #   print(pathlib.PurePath(path, str(f)))
       
def file_open(path):
       if str(path).find('csv'):
          print('csv')
          return pd.read_csv(str(path))
       else:
          print('excel')
          return pd.read_excel(str(path))

if __name__ == '__main__':
   start()
