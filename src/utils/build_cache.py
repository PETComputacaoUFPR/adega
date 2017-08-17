import sys
import os
import django
import time
import math

from datetime import timedelta
from pathlib import Path

os.environ["DJANGO_SETTINGS_MODULE"] = "adega.settings"
django.setup()
