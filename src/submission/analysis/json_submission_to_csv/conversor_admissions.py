import numpy as np
from submission.analysis.json_submission_to_csv.common_conversor import get_all_subjson, PeriodType
import os
import pandas as pd
import json
from pathlib import Path


class AdmissionConversor:
    def __init__(self, submission_path, not_allowed_keys=None,
                 min_year=None, max_year=None,
                 submission_raw_data_fname="csv_data_file.csv"):
        admission_dir = os.path.join(submission_path, "admissions")
        self.submission_path = submission_path
        self.admission_dir = admission_dir
        self.submission_raw_data_fname = submission_raw_data_fname

        if not_allowed_keys is None:
            self.not_allowed_keys = ["evasion_per_semester"]

        if (min_year is None) or (max_year is None):
            self.init_min_max_year()
        else:
            self.min_year = min_year
            self.max_year = max_year
    
    def init_min_max_year(self):
        df = pd.read_csv(os.path.join(self.submission_path,
                         self.submission_raw_data_fname))
        self.min_year = int(df["ANO_ATIV_CURRIC"].min())
        self.max_year = int(df["ANO_ATIV_CURRIC"].max())

    def convert_graph_data_to_vector(self, graph_data, graph_name,
                                     return_header=False):
        # Collect the second element of the list of tuples
        # This is the name of each type period (see situations.py)
        period_list = [x[1] for x in PeriodType.PERIODS]
        if graph_name == "ira_per_semester":
            range_size = (self.max_year-self.min_year+1)*len(period_list)
            # Consider average and std
            vector_size = 2*range_size
            vector_data = np.zeros(vector_size)
            for key in graph_data:
                # Recover the first parameter of the tuple
                year = int(key.split(",")[0].replace("(",""))
                # Recover the second parameter of the tuple
                period = key.split(",")[1].replace(")","").replace("'", "")
                period = str(period.replace("'", ""))
                # Remove the white space after ','
                period = period[1:]

                period_id = PeriodType.str_to_code(period)
                idx_in_vector = (year - self.min_year)*len(period_list)+period_id

                mean_val, std_val = graph_data[key]
                vector_data[           idx_in_vector] = mean_val
                vector_data[range_size+idx_in_vector] = std_val

            if return_header:
                header = []
                for i, metric_name in enumerate(["Media", "DesvioPadrao"]):
                    for year in range(self.min_year, self.max_year+1):
                        for period_id, period_name in enumerate(period_list):
                            key_name = "{}_{}_{}_{}".format(
                                graph_name,
                                metric_name,
                                year,
                                period_name
                            )
                            header.append(key_name)
                return (vector_data, np.array(header))
            else:
                return vector_data
        if graph_name == "students_per_semester":
            range_size = (self.max_year-self.min_year+1)*len(period_list)
            # Consider average and std
            vector_size = range_size
            vector_data = np.zeros(vector_size)
            for key in graph_data:
                # Recover the first parameter of the tuple
                year = int(key.split(",")[0].replace("(",""))
                # Recover the second parameter of the tuple
                period = key.split(",")[1].replace(")","").replace("'", "")
                period = str(period.replace("'", ""))
                # Remove the white space after ','
                period = period[1:]
                
                period_id = PeriodType.str_to_code(period)
                idx_in_vector = (year - self.min_year)*len(period_list)+period_id
                students_count = int(graph_data[key])
                vector_data[idx_in_vector] = students_count

            if return_header:
                header = []
                for year in range(self.min_year, self.max_year+1):
                    for period_id, period_name in enumerate(period_list):
                        key_name = "{}_{}_{}".format(
                            graph_name,
                            year,
                            period_name
                        )
                        header.append(key_name)
                
                return (vector_data, np.array(header))
            else:
                return vector_data

        raise Exception("A graph data cannot be converted: {}".format(
            graph_name))

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
                        if key in self.not_allowed_keys:
                            continue
                        
                        # keys_set = keys_set.union({key})
                        if type(admission_instance[key]) in [int, float, str]:
                            keys_set = keys_set.union({key})
                        else: # is an attribute with graph data
                            _, graph_header = self.convert_graph_data_to_vector(
                                admission_instance[key],
                                key,
                                return_header=True)
                            keys_set = keys_set.union(set(graph_header))
        
        
        # Collect the keys of each admission instance inside list file
        if keys_from_list:
            json_instance_path = os.path.join(self.admission_dir,
                                              "lista_turma_ingresso.json")
            with open(json_instance_path, 'r') as f:
                json_list_content = json.load(f)
                for admission_instance in json_list_content:
                    new_keys = set(admission_instance.keys())
                    for key in new_keys:
                        if key in self.not_allowed_keys:
                            continue

                        if type(admission_instance[key]) in [int, float, str]:
                            keys_set = keys_set.union({key})
                        else: # is an attribute with graph data
                            _, graph_header = self.convert_graph_data_to_vector(
                                admission_instance[key],
                                key,
                                return_header=True)
                            keys_set = keys_set.union(set(graph_header))

        
        # TODO: Implement not_allowed_keys in analysis or remove if from build_cache 
        
        for key in self.not_allowed_keys:
            # Remove 'banned' key from the set if it exists
            keys_set = keys_set - {key}
        
        keys_list = sorted(list(keys_set))
        return keys_list

    def get_admission_as_matrix(self):
        
        # header_instances = get_header(self.admission_dir,
        #                                         keys_from_instances=True,
        #                                         keys_from_list=False)
        # header_list = get_header(self.admission_dir,
        #                                         keys_from_instances=False,
        #                                         keys_from_list=True)
        header = self.get_header()

        instance_files = get_all_subjson(self.admission_dir)

        # Get the period of each admission instance (json name)
        instances_year = [os.path.basename(p.replace(".json", "")) for p in instance_files]
        # Get the year of each admission instance (parent dir name)
        instances_period = [os.path.basename(str(Path(p).parent)) for p in instance_files]

        admission_matrix = np.zeros((len(instance_files),len(header)),dtype=object)
        admission_matrix[:,:] = None
        
        get_admission_id = {}
        for inst_id, instance_path in enumerate(instance_files):
            with open(instance_path, 'r') as f:
                admission_instance = json.load(f)
                for key in admission_instance:
                    if key in self.not_allowed_keys:
                        continue

                    if type(admission_instance[key]) in [int, float, str]:
                        col_id = header.index(key)
                        admission_matrix[inst_id,col_id] = admission_instance[key]
                    else: # is an attribute with graph data
                        graph_data, graph_header = self.convert_graph_data_to_vector(
                            admission_instance[key],
                            key,
                            return_header=True)
                        
                        for key, val in zip(graph_header, graph_data):
                            col_id = header.index(key)
                            admission_matrix[inst_id,col_id] = val

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
                    
                    if type(admission_instance[key]) in [int, float, str]:
                        col_id = header.index(key)
                        admission_matrix[inst_id,col_id] = admission_instance[key]
                    else: # is an attribute with graph data
                        graph_data, graph_header = self.convert_graph_data_to_vector(
                            admission_instance[key],
                            key,
                            return_header=True)
                        
                        for key, val in zip(graph_header, graph_data):
                            col_id = header.index(key)
                            admission_matrix[inst_id,col_id] = val
        
        instances_year = np.array(instances_year)
        instances_period = np.array(instances_period)
        
        header = ["Ano", "Período"] + header
        header = np.array(header)
        admission_matrix = np.concatenate((instances_year.reshape(-1,1), admission_matrix), axis=1)
        admission_matrix = np.concatenate((instances_period.reshape(-1,1), admission_matrix), axis=1)
        return admission_matrix, header
