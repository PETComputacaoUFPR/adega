from pathlib import Path
import json
import csv

import os
import argparse
import numpy as np

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, help="name of the sheet",
                        required=True)
    # parser.add_argument('--output', type=str,help="path to sheet",
    #                     required=True)
    # parser.add_argument('--type_input', type=str,help="input type",
    #                     required=False, default="SIE")
    # parser.add_argument('--output_fname', type=str,help="output file name",
    #                     required=False, default="adega_input.csv")
    args = parser.parse_args()

    return args

def get_all_subjson(path):
    '''
    Return all json files that is in the subdirectories of a path 
    --
    return: list
    '''
    return_list = []

    subpath = next(os.walk(path))[1]
    for admission_year in subpath:
        year_path = os.path.join(path,admission_year) 
        for file in os.listdir(year_path):
            if file.endswith(".json"):
                return_list.append(os.path.join(year_path, file))

    return return_list


class Admission:
    def __init__(self, submission_path, not_allowed_keys=None):
        admission_dir = os.path.join(submission_path, "admissions")
        self.submission_path = submission_path
        self.admission_dir = admission_dir


        if not_allowed_keys is None:
            self.not_allowed_keys = ["evasion_per_semester"]

    def convert_graph_data_to_vector(self):
        # data minima
        # data maxima
        # cria o range entre eles
        # percorre os dados e coloca no range
        pass

    def get_header(self, keys_from_instances=True, keys_from_list=True):
        # Get only the first level of admission path (subdirectories)
        keys_set = set()
        instance_files = get_all_subjson(self.admission_dir)
        
        # Collect the keys of each admission instance
        if keys_from_instances:
            for json_instance_path in instance_files:
                with open(json_instance_path, 'r') as f:
                    admission_instance = json.load(f)
                    new_keys = set(admission_instance.keys())
                    for key in new_keys:
                        keys_set = keys_set.union({key})
                        # if type(admission_instance[key]) in [int, float, str]:
                        #     keys_set = keys_set.union({key})
                        # else: # is an attribute with graph data
                        #     data = convert_graph_data_to_vector(admission_instance[key])
                        #     pass
        # Collect the keys of each admission instance inside list file
        if keys_from_list:
            json_instance_path = os.path.join(self.admission_dir,
                                              "lista_turma_ingresso.json")
            with open(json_instance_path, 'r') as f:
                json_list_content = json.load(f)
                for admission_instance in json_list_content:
                    new_keys = set(admission_instance.keys())
                    keys_set = keys_set.union(new_keys)
        
        # TODO: Implement not_allowed_keys in analysis or remove if from build_cache 
        
        for key in self.not_allowed_keys:
            # Remove 'banned' key from the set if it exists
            keys_set = keys_set - {key}
        
        keys_list = sorted(list(keys_set))
        return keys_list

    def convert_admission_instance(self):
        '''
        ---
        return np.array of shape (len(get_admission_header()) )
        '''
        

    def convert_admission_list(self):
        pass

    def get_admission_as_matrix(self):
        
        # header_instances = get_header(self.admission_dir,
        #                                         keys_from_instances=True,
        #                                         keys_from_list=False)
        # header_list = get_header(self.admission_dir,
        #                                         keys_from_instances=False,
        #                                         keys_from_list=True)
        header = self.get_header()
        print(header)

        instance_files = get_all_subjson(self.admission_dir)

        admission_matrix = np.zeros((len(instance_files),len(header)),dtype=object)
        admission_matrix[:,:] = None
        
        get_admission_id = {}
        for inst_id, instance_path in enumerate(instance_files):
            with open(instance_path, 'r') as f:
                admission_instance = json.load(f)
                for key in admission_instance:
                    if key in self.not_allowed_keys:
                        continue

                    col_id = header.index(key)
                    if type(admission_instance[key]) in [int, float, str]:
                        admission_matrix[inst_id,col_id] = admission_instance[key]
                    else:
                        # print(key, type(admission_instance[key]))
                        pass
                ano_val = str(admission_instance["ano"])
                semestre_val = str(admission_instance["semestre"])
                get_admission_id[(ano_val, semestre_val)] = inst_id

                ###
        json_instance_path = os.path.join(self.admission_dir,
                                          "lista_turma_ingresso.json")
        with open(json_instance_path, 'r') as f:
            json_list_content = json.load(f)
            for admission_instance in json_list_content:
                ano_val = str(admission_instance["ano"])
                semestre_val = str(admission_instance["semestre"])
                inst_id = get_admission_id[(ano_val, semestre_val)]
                
                for key in admission_instance:
                    if key in self.not_allowed_keys:
                        continue
                    
                    col_id = header.index(key)
                    if type(admission_instance[key]) in [int, float, str]:
                        admission_matrix[inst_id,col_id] = admission_instance[key]
                ###
        
        header = np.array(header)
        admission_matrix = np.concatenate((header.reshape(1,-1), admission_matrix))
        import pandas
        df = pandas.DataFrame(admission_matrix)
        print(df)

def main():
    args = get_args()
    submission_path = args.input
    admission = Admission(submission_path)

    admission.get_admission_as_matrix()
    
    exit()

if __name__ == '__main__':
    main()
    #teste da funcao create_csv
    #lista = ['coluna1','coluna70','coluna22','coluna42']
    #create_csv('testeDaFuncao.csv', lista, 7)
