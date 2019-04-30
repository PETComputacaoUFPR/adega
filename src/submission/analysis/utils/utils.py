import os
import copy
import numpy as np
import ujson as json
import pprint


try:
    from django.conf import settings

    DEBUG = settings.DEBUG
except:
    DEBUG = True

'''
Use this class to generate a dictionary like this:
  {"00-4.9":0, "05-9.9":0, "10-14.9":0, "15-19.9":0, "20-24.9":0,
         "25-29.9":0, "30-34.9":0, "35-39.9":0, "40-44.9":0, "45-49.9":0,
         "50-54.9":0, "55-59.9":0, "60-64.9":0, "65-69.9":0, "70-74.9":0,
         "75-79.9":0, "80-84.9":0, "85-89.9":0, "90-94.9": 0,"95-100":0}

Where
sup is the maximum value of range
inf is the minumum
and gap is the shift between elements keys

do_count(value) increment the value in specific range

to_dict return the specified dictionary above
'''
class IntervalCount:
    def __init__(self, sup, inf=0, gap=1, digit=3):
        self.sup = sup
        self.inf = inf
        self.gap = gap
        self.dict = {key:0 for key in range(self.get_total_slices())}
        print(self.dict)
        self.digit = "{:."+str(digit)+"f}"  # number of digits after .
        # for interval in zip( np.arange(inf,sup,gap, dtype=np.float), np.arange(inf+gap,sup+gap,gap, dtype=np.float)):
        #     self.dict[interval] = 0

    def get_total_slices(self):
        return round((self.sup-self.inf)/self.gap)

    def projection_inf(self,key):
        return key*self.gap + self.inf

    def projection_sup(self,key):
        return key*self.gap + self.inf + self.gap

    def count_on_interval(self, value):
        if(value >= self.inf):
            for key in self.dict:
                # pinf = self.projection_inf(key)
                # psup = self.projection_sup(key)
                pinf = float(self.digit.format(key))
                psup = float(self.digit.format(key))

                print(pinf,psup,value)
                if(value >= pinf and value < psup):
                    break

        self.dict[key]+=1


    def to_dict(self):
        dic = {}
        for key in self.dict:
            pinf = self.projection_inf(key)
            psup = self.projection_sup(key)
            convert_key = "{:.2f}".format(pinf) + "-" + "{:.2f}".format(psup)
            dic[convert_key] = self.dict[key]

        return dic


# Use this class as decorator to save functions returns
def memoize(f):
    memo = {}
    def helper(x, df=None):
        if str(df) not in memo:
            memo[str(df)] = f(x, df)
        return copy.deepcopy(memo[str(df)])
    return helper



def invert_dict(d):
    return {v: k for k, v in d}


def build_path(path):
    if not os.path.exists(path):
        os.mkdir(path)


def ensure_path_exists(complete_path):
    parts = complete_path.split('/')

    for i in range(1,len(parts)):
        if not os.path.exists('/'.join(parts[:i+1])):
            os.mkdir('/'.join(parts[:i+1]))


def save_json(path, data):

    ensure_path_exists(os.path.dirname(path))

    # params = {} if not DEBUG else {'indent': 4}
    params = {'indent': 4}
    with open(path, 'w') as f:
        json.dump(data, f, **params, ensure_ascii=False)

if __name__ == "__main__":
    icount = IntervalCount(1,0,0.05)
    icount.count_on_interval(0.3)
    icount.count_on_interval(0.3)
    icount.count_on_interval(0.9)
    icount.count_on_interval(0.98)
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(icount.to_dict())
