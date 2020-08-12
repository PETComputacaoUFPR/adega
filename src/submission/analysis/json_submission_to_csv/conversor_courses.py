import numpy as np
from submission.analysis.json_submission_to_csv.common_conversor import get_all_subjson, PeriodType
import os
import pandas as pd
import json
from pathlib import Path


class CourseConversor:
    def __init__(self, submission_path, not_allowed_keys=None,
                 min_year=None, max_year=None):
        course_dir = os.path.join(submission_path, "courses")
        self.submission_path = submission_path
        self.course_dir = course_dir


        if not_allowed_keys is None:
            self.not_allowed_keys = ["evasion_per_semester"]

        if (min_year is None) or (max_year is None):
            self.init_min_max_year()
        else:
            self.min_year = min_year
            self.max_year = max_year
    
    def init_min_max_year(self):
        df = pd.read_csv(os.path.join(self.submission_path,"csv_data_file.csv"))
        self.min_year = int(df["ANO_ATIV_CURRIC"].min())
        self.max_year = int(df["ANO_ATIV_CURRIC"].max())

    def convert_graph_data_to_vector(self, graph_data, graph_name,
                                     return_header=False):
        
        # Collect the second element of the list of tuples
        # This is the name of each type period (see situations.py)
        period_list = [x[1] for x in PeriodType.PERIODS]
        if graph_name == "grafico_qtd_cursada_aprov":
            #TODO: Import range size from analysis
            range_size = 5
            # Consider average and std
            vector_size = range_size
            vector_data = np.zeros(vector_size)
            for key in graph_data:
                
                coursed_count = graph_data[key]
                key_idx = int(key)-1
                vector_data[key_idx] = coursed_count

            if return_header:
                header = []
                for i in range(range_size):
                    count = i+1
                    if count == 5:
                        count = "MaisQue4"
                    key_name = "{}_{}_{}".format(
                        "grafico_qtd_cursada_aprov",
                        "QuantidadeDeVezesCursadaAteAprovacao",
                        count
                    )
                    header.append(key_name)
                return (vector_data, np.array(header))
            else:
                return vector_data
        
        if graph_name == "nota":
            vector_data = np.array(graph_data)
            header = ["NotaMedia", "NotaDesvioPadrao"]
            if return_header:
                return (vector_data, np.array(header))
            else:
                return vector_data
        if graph_name == "nota_ultimo_ano":
            vector_data = np.array(graph_data)
            header = ["NotaUltimoAnoMedia", "NotaUltimoAnoDesvioPadrao"]
            if return_header:
                return (vector_data, np.array(header))
            else:
                return vector_data
        
        if graph_name == "nota_ultimo_ano":
            vector_data = np.array(graph_data)
            header = ["NotaUltimoAnoMedia", "NotaUltimoAnoDesvioPadrao"]
            if return_header:
                return (vector_data, np.array(header))
            else:
                return vector_data

        if graph_name == "aprovacao_semestral":
            range_size = (self.max_year-self.min_year+1)*len(period_list)
            # Consider average and std
            vector_size = 3*range_size
            vector_data = np.zeros(vector_size)
            for key in graph_data:

                year = int(key.split("/")[0])
                period = key.split("/")[1]
                
                period_id = PeriodType.str_to_code(period)
                idx_in_vector = (year - self.min_year)*len(period_list)+period_id

                approve_rate, approve_count, register_count = graph_data[key]
                approve_rate = float(approve_rate)
                approve_count = int(approve_count)
                register_count = int(register_count)

                vector_data[           idx_in_vector] = approve_rate
                vector_data[range_size+idx_in_vector] = approve_count
                vector_data[2*range_size+idx_in_vector] = register_count

            if return_header:
                header = []
                metric_list = ["TaxaAprovacao",
                               "QuantidadeAprovacao",
                               "QuantidadeMatriculas"]

                for i, metric_name in enumerate(metric_list):
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
            
        raise Exception(
            "A graph data cannot be converted: {}".format(graph_name))
        
    def get_header(self, keys_from_instances=True, keys_from_list=True):
        # Get only the first level of course path (subdirectories)
        keys_set = set()
        instance_files = get_all_subjson(self.course_dir, only_subdir=False,
                                         ignore_files=["disciplinas.json"])
        
        # Collect the keys of each course instance
        if keys_from_instances:
            for json_instance_path in instance_files:
                with open(json_instance_path, 'r') as f:
                    course_instance = json.load(f)
                    new_keys = set(course_instance.keys())
                    for key in new_keys:
                        if key in self.not_allowed_keys:
                            continue
                        
                        # keys_set = keys_set.union({key})
                        if type(course_instance[key]) in [int, float, str]:
                            keys_set = keys_set.union({key})
                        else: # is an attribute with graph data
                            _, graph_header = self.convert_graph_data_to_vector(
                                course_instance[key],
                                key,
                                return_header=True)
                            keys_set = keys_set.union(set(graph_header))
        
        
        # Collect the keys of each course instance inside list file
        if keys_from_list:
            json_instance_path = os.path.join(self.course_dir,
                                              "disciplinas.json")
            with open(json_instance_path, 'r') as f:
                # TODO: Remove 'cache' key on analysis
                #       And also add compara_aprov graph data

                # Get only the values of each course as list
                # and ignore dict keys (course codes)
                json_list_content = list(json.load(f)["cache"].values())

                for course_instance in json_list_content:
                    new_keys = set(course_instance.keys())
                    for key in new_keys:
                        if key in self.not_allowed_keys:
                            continue

                        if type(course_instance[key]) in [int, float, str]:
                            keys_set = keys_set.union({key})
                        else: # is an attribute with graph data
                            _, graph_header = self.convert_graph_data_to_vector(
                                course_instance[key],
                                key,
                                return_header=True)
                            keys_set = keys_set.union(set(graph_header))

        
        # TODO: Implement not_allowed_keys in analysis or remove if from build_cache 
        
        for key in self.not_allowed_keys:
            # Remove 'banned' key from the set if it exists
            keys_set = keys_set - {key}
        
        keys_list = sorted(list(keys_set))
        return keys_list

    def get_course_as_matrix(self):
        
        # header_instances = get_header(self.course_dir,
        #                                         keys_from_instances=True,
        #                                         keys_from_list=False)
        # header_list = get_header(self.course_dir,
        #                                         keys_from_instances=False,
        #                                         keys_from_list=True)
        header = self.get_header()

        instance_files = get_all_subjson(self.course_dir, only_subdir=False,
                                         ignore_files=["disciplinas.json"])

        # Get the period of each course instance (json name)
        instances_code = [os.path.basename(p.replace(".json", "")) for p in instance_files]
        instances_names = []

        course_matrix = np.zeros((len(instance_files),len(header)),dtype=object)
        course_matrix[:,:] = None
        
        get_course_id = {}
        for inst_id, instance_path in enumerate(instance_files):
            with open(instance_path, 'r') as f:
                course_instance = json.load(f)
                for key in course_instance:
                    if key in self.not_allowed_keys:
                        continue

                    if type(course_instance[key]) in [int, float, str]:
                        col_id = header.index(key)
                        course_matrix[inst_id,col_id] = course_instance[key]
                    else: # is an attribute with graph data
                        graph_data, graph_header = self.convert_graph_data_to_vector(
                            course_instance[key],
                            key,
                            return_header=True)
                        
                        for key, val in zip(graph_header, graph_data):
                            col_id = header.index(key)
                            course_matrix[inst_id,col_id] = val

                course_code = str(course_instance["disciplina_codigo"])
                course_name = str(course_instance["disciplina_nome"])
                instances_names.append(course_name)

                get_course_id[course_code] = inst_id

                ###
        json_instance_path = os.path.join(self.course_dir,
                                          "disciplinas.json")
        with open(json_instance_path, 'r') as f:
            # TODO: Remove 'cache' key on analysis
            #       And also add compara_aprov graph data
            
            # Get only the values of each course as list
            # and ignore dict keys (course codes)
            json_data = json.load(f)["cache"]
            
            for course_code in json_data:
                course_instance = json_data[course_code]

                inst_id = get_course_id[course_code]
                
                for key in course_instance:
                    if key in self.not_allowed_keys:
                        continue
                    
                    if type(course_instance[key]) in [int, float, str]:
                        col_id = header.index(key)
                        course_matrix[inst_id,col_id] = course_instance[key]
                    else: # is an attribute with graph data
                        graph_data, graph_header = self.convert_graph_data_to_vector(
                            course_instance[key],
                            key,
                            return_header=True)
                        
                        for key, val in zip(graph_header, graph_data):
                            col_id = header.index(key)
                            course_matrix[inst_id,col_id] = val
        
        instances_code = np.array(instances_code)
        instances_names = np.array(instances_names)
        
        header = ["Código", "Nome"] + header
        header = np.array(header)
        course_matrix = np.concatenate((instances_names.reshape(-1,1), course_matrix), axis=1)
        course_matrix = np.concatenate((instances_code.reshape(-1,1), course_matrix), axis=1)
        return course_matrix, header
