import numpy as np
from submission.analysis.json_submission_to_csv.common_conversor import get_all_subjson, PeriodType
import os
import pandas as pd
import json
from pathlib import Path
from collections import defaultdict

class StudentConversor:
    def __init__(self, submission_path, not_allowed_keys=None,
                 min_year=None, max_year=None,
                 submission_raw_data_fname="csv_data_file.csv"):
        student_dir = os.path.join(submission_path, "students")
        self.submission_path = submission_path
        self.student_dir = student_dir
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
        
        if graph_name == "ira_semestral":
            range_size = (self.max_year-self.min_year+1)*len(period_list)
            # Consider average and std
            vector_size = range_size
            vector_data = np.zeros(vector_size)
            for key in graph_data:

                year = int(key.split("/")[0])
                period = key.split("/")[1]
                
                period_id = PeriodType.str_to_code(period)
                idx_in_vector = (year - self.min_year)*len(period_list)+period_id

                ira_by_semester = float(graph_data[key])

                vector_data[idx_in_vector] = ira_by_semester
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
        if graph_name == "posicao_turmaIngresso_semestral":
            range_size = (self.max_year-self.min_year+1)*len(period_list)
            # Consider average and std
            vector_size = range_size
            vector_data = np.zeros(vector_size)
            for key in graph_data:

                year = int(key.split("/")[0])
                period = key.split("/")[1]
                
                period_id = PeriodType.str_to_code(period)
                idx_in_vector = (year - self.min_year)*len(period_list)+period_id

                relative_pos = float(graph_data[key])

                vector_data[idx_in_vector] = relative_pos
            if return_header:
                header = []
                for year in range(self.min_year, self.max_year+1):
                    for period_id, period_name in enumerate(period_list):
                        key_name = "{}_{}_{}".format(
                            graph_name,
                            year,
                            period_name)
                        header.append(key_name)
                return (vector_data, np.array(header))
            else:
                return vector_data
        if graph_name == "indice_aprovacao_semestral":
            range_size = (self.max_year-self.min_year+1)*len(period_list)
            # Consider average and std
            vector_size = 2*range_size
            vector_data = np.zeros(vector_size)
            for key in graph_data:

                year = int(key.split("/")[0])
                period = key.split("/")[1]
                
                period_id = PeriodType.str_to_code(period)
                idx_in_vector = (year - self.min_year)*len(period_list)+period_id

                approved_count, register_count = graph_data[key]
                approved_count = int(approved_count)
                register_count = int(register_count)

                vector_data[           idx_in_vector] = approved_count
                vector_data[range_size+idx_in_vector] = register_count
            if return_header:
                header = []
                metric_list = ["QuantidadeAprovacao",
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
        if graph_name == "ira_por_quantidade_disciplinas":
            range_size = (self.max_year-self.min_year+1)*len(period_list)
            # Consider average and std
            vector_size = 3*range_size
            vector_data = np.zeros(vector_size)
            for key in graph_data:

                year = int(key.split("/")[0])
                period = key.split("/")[1]
                
                period_id = PeriodType.str_to_code(period)
                idx_in_vector = (year - self.min_year)*len(period_list)+period_id

                ira_in_semester, register_count, workload = graph_data[key]
                ira_in_semester = float(ira_in_semester)
                register_count = int(register_count)
                workload = float(workload)

                vector_data[             idx_in_vector] = ira_in_semester
                vector_data[range_size+  idx_in_vector] = register_count
                vector_data[2*range_size+idx_in_vector] = workload
            if return_header:
                header = []
                metric_list = ["Ira",
                               "QuantidadeMatriculas",
                               "CargaHoraria"]
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
        if graph_name == "student":
            vector_data = np.array(list(graph_data.values()))
            if return_header:
                header = np.array(list(graph_data.keys()))
                return (vector_data, np.array(header))
            else:
                return vector_data
                
        if graph_name == "aluno_turmas":
            if return_header:
                return (np.array([]), np.array([]))
            else:
                return np.array([])
        
        raise Exception("A graph data cannot be converted: {}".format(
            graph_name))


    def get_list_col_header(self, list_file_path, return_data=False):
        with open(list_file_path, 'r') as f:
            # Get only the file name from the path
            list_file_name = os.path.basename(list_file_path)

            json_list_content = json.load(f)
            desc_name_list = json_list_content["description_name"]
            col_name = desc_name_list
            
            if  col_name == "Forma de evasão":
                col_val = defaultdict(lambda: "")
            elif col_name == "Disciplinas restantes":
                col_name = list_file_name.replace(".json","")
                col_name += " - Disciplinas restantes"
                col_val = defaultdict(lambda: 0)
            elif col_name == "Período pretendido":
                # If col_name is Periodo pretendido, then the column must
                # inform if a student is a trainee candidate
                col_name = "Formando (último período)"
                col_val = defaultdict(lambda: 0)
            else:
                raise Exception("Student list file cannot be converted: {}".format(
                                col_name))

            for student in json_list_content["student_list"]:
                grr = student["grr"]
                description_value = student["description_value"]
                if col_name == "Formando (último período)":
                    description_value = 1
                col_val[grr] = description_value
        
        if return_data:
            return col_name, col_val
        else:
            return col_name
    
    def get_header(self, keys_from_instances=True, keys_from_list=True):
        # Get only the first level of student path (subdirectories)
        keys_set = set()
        instance_files = get_all_subjson(self.student_dir,
                                         only_subdir=False)
        
        # Collect the keys of each student instance
        if keys_from_instances:
            for json_instance_path in instance_files:
                with open(json_instance_path, 'r') as f:
                    student_instance = json.load(f)
                    new_keys = set(student_instance.keys())
                    for key in new_keys:
                        if key in self.not_allowed_keys:
                            continue
                        
                        # keys_set = keys_set.union({key})
                        if type(student_instance[key]) in [int, float, str,
                                                           type(None)]:
                            keys_set = keys_set.union({key})
                        else: # is an attribute with graph data
                            _, graph_header = self.convert_graph_data_to_vector(
                                student_instance[key],
                                key,
                                return_header=True)
                            if len(graph_header) > 0:
                                keys_set = keys_set.union(set(graph_header))
        
        
        # Collect the keys of each student instance inside list file
        if keys_from_list:
            list_files = get_all_subjson(self.student_dir,
                                         only_subdir=True)
            for list_file_path in list_files:
                col_name = self.get_list_col_header(list_file_path)
                keys_set = keys_set.union({col_name})
            
            '''
            json_instance_path = os.path.join(self.student_dir,
                                              "lista_turma_ingresso.json")
            with open(json_instance_path, 'r') as f:
                json_list_content = json.load(f)
                for student_instance in json_list_content:
                    new_keys = set(student_instance.keys())
                    for key in new_keys:
                        if key in self.not_allowed_keys:
                            continue

                        if type(student_instance[key]) in [int, float, str]:
                            keys_set = keys_set.union({key})
                        else: # is an attribute with graph data
                            _, graph_header = self.convert_graph_data_to_vector(
                                student_instance[key],
                                key,
                                return_header=True)
                            keys_set = keys_set.union(set(graph_header))
            '''
        
        # TODO: Implement not_allowed_keys in analysis or remove if from build_cache 
        
        for key in self.not_allowed_keys:
            # Remove 'banned' key from the set if it exists
            keys_set = keys_set - {key}
        
        keys_list = sorted(list(keys_set))
        return keys_list

    def get_student_as_matrix(self):
        
        # header_instances = get_header(self.student_dir,
        #                                         keys_from_instances=True,
        #                                         keys_from_list=False)
        # header_list = get_header(self.student_dir,
        #                                         keys_from_instances=False,
        #                                         keys_from_list=True)
        header = self.get_header()

        instance_files = get_all_subjson(self.student_dir, only_subdir=False)

        instances_grr = [os.path.basename(p.replace(".json", "")) for p in instance_files]
        instances_names = []

        student_matrix = np.zeros((len(instance_files),len(header)),dtype=object)
        student_matrix[:,:] = None
        
        get_student_id = {}
        for inst_id, instance_path in enumerate(instance_files):
            with open(instance_path, 'r') as f:
                student_instance = json.load(f)
                for key in student_instance:
                    if key in self.not_allowed_keys:
                        continue

                    if type(student_instance[key]) in [int, float, str,
                                                           type(None)]:
                        col_id = header.index(key)
                        cell_val = student_instance[key]
                        if cell_val is None:
                            cell_val = 0

                        student_matrix[inst_id,col_id] = student_instance[key]
                    else: # is an attribute with graph data
                        graph_data, graph_header = self.convert_graph_data_to_vector(
                            student_instance[key],
                            key,
                            return_header=True)
                        
                        if len(graph_header) > 0:
                            for key, val in zip(graph_header, graph_data):
                                col_id = header.index(key)
                                student_matrix[inst_id,col_id] = val

                name_val = str(student_instance["student"]["name"])
                instances_names.append(name_val)

                grr_val = str(student_instance["student"]["grr"])
                get_student_id[grr_val] = inst_id

                ###
        list_files = get_all_subjson(self.student_dir,
                                     only_subdir=True)

        for list_file_path in list_files:
            # col_data is a default dict
            col_name, col_data = self.get_list_col_header(list_file_path,
                                                            return_data=True)
            col_id = header.index(col_name)
            for grr in get_student_id:
                inst_id = get_student_id[grr]
                # If the column is not relative to 'Forma de evasao',
                # then use default dict value to overwrite np.zeros val
                # Trust in the analysis to create at list one instance
                # of each student between 'Forma de evasão' list files
                if not (col_name == "Forma de evasão"):
                    student_matrix[inst_id,col_id] = col_data[grr]
            '''
            for student_instance in json_list_content:
                ano_val = str(student_instance["ano"])
                semestre_val = str(student_instance["semestre"])
                inst_id = get_student_id[(ano_val, semestre_val)]
                
                for key in student_instance:
                    if key in self.not_allowed_keys:
                        continue
                    
                    if type(student_instance[key]) in [int, float, str]:
                        col_id = header.index(key)
                        student_matrix[inst_id,col_id] = student_instance[key]
                    else: # is an attribute with graph data
                        graph_data, graph_header = self.convert_graph_data_to_vector(
                            student_instance[key],
                            key,
                            return_header=True)
                        
                        for key, val in zip(graph_header, graph_data):
                            col_id = header.index(key)
                            student_matrix[inst_id,col_id] = val
            '''

        instances_grr = np.array(instances_grr)
        instances_names = np.array(instances_names)
        
        header = ["GRR", "Nome"] + header
        header = np.array(header)
        student_matrix = np.concatenate((instances_names.reshape(-1,1), student_matrix), axis=1)
        student_matrix = np.concatenate((instances_grr.reshape(-1,1), student_matrix), axis=1)
        return student_matrix, header

