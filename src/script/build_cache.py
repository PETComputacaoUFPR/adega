from script.utils.utils import *
from script.utils.situations import *
from script.analysis.degree_analysis import *
from script.analysis.student_analysis import *
from script.analysis.course_analysis import *
from script.analysis.admission_analysis import *


try:
        to_unicode = unicode
except NameError:
        to_unicode = str


def build_cache(dataframe,path):
#       os.chdir("../src")
        ensure_path_exists(path)

        for cod, df in dataframe.groupby('COD_CURSO'):
                path = path + '/'
                generate_degree_data(path, df)
                generate_student_data(path+'students/',df)
                #~ generate_admission_data(path+'/'+cod+'/admission/',df)
        #generate_degree_data(path, dataframe)
        #generate_student_data(path, dataframe)
        #generate_student_list(path)
        #generate_admission_data(path)
        #generate_admission_list(path)
                generate_course_data(path+'disciplina/' ,dataframe)

def generate_degree_data(path, dataframe):
        ensure_path_exists(path)
        ensure_path_exists(path+'students')

        students = dataframe[['MATR_ALUNO', 'FORMA_EVASAO']].drop_duplicates()
        build_degree_json(path,dataframe) 

#       data = {
#               'average_graduation': average_graduation(dataframe),
#               'general_failure': general_failure(dataframe),
#               'general_ira': general_ira(dataframe),
#               'active_students': students[students.FORMA_EVASAO == EvasionForm.EF_ATIVO].shape[0],
#               'graduated_students': students[students.FORMA_EVASAO == EvasionForm.EF_FORMATURA].shape[0],
#       }

        #save_json(path+'/degree.json', data)
        
        #~ for ind, hist in dataframe.groupby('MATR_ALUNO'):
                #~ generate_student_data_old(path+'students/{}.json'.format(ind), dataframe)



def historico(dataframe):
        res = []

        for _, row in dataframe.iterrows():
                res.append(dict(row[['ANO', 'MEDIA_FINAL', 'PERIODO', 'SITUACAO', 'COD_ATIV_CURRIC', 'NOME_ATIV_CURRIC',
                                                         'CREDITOS', 'CH_TOTAL', 'DESCR_ESTRUTURA', 'FREQUENCIA']]))

        return res


def process_semestre(per, df):
        ira = df[df.SITUACAO.isin(Situation.SITUATION_AFFECT_IRA)].MEDIA_FINAL.mean()
        completas = df[df.SITUACAO.isin(Situation.SITUATION_PASS)].shape[0]
        tentativas = df[df.SITUACAO.isin(Situation.SITUATION_COURSED)].shape[0]

        return {
                'semestre': per,
                'ira': ira,
                'completas': completas,
                'tentativas': tentativas,
                'aprovacao': completas/tentativas if tentativas else 0,
                'ira_por_quantidade_disciplinas': ira/tentativas if tentativas else 0
        }



def generate_student_data(path, dataframe):
        student_data = dict()
        all_grrs = list(dataframe["MATR_ALUNO"].drop_duplicates())
        for x in all_grrs:
                student_data[x] = dict()
        
        
        analises = [
                # tupla que contem no primeiro elemento a funcao que retorna um dicionario com {"GRR": valor}
                # e na segunda posicao o nome que esta analise tera no json
                
                (posicao_turmaIngresso_semestral(dataframe),
                "posicao_turmaIngresso_semestral"),
                
                (periodo_real(dataframe),
                "periodo_real"),
                
                (periodo_pretendido(dataframe),
                "periodo_pretendido"),
                
                (ira_semestral(dataframe),
                "ira_semestral"),
                
                (ira_por_quantidade_disciplinas(dataframe),
                "ira_por_quantidade_disciplinas"),
                
                (indice_aprovacao_semestral(dataframe),
                "indice_aprovacao_semestral"),
                
                (aluno_turmas(dataframe),
                "aluno_turmas"),
                
                (taxa_aprovacao(dataframe),
                "taxa_aprovacao"),
        ]
        
        for x in student_data:
                for a in analises:                                                                                      # Usar para fazer a verificacao de 
                        student_data[x][a[1]] = a[0][x]                                                 # analises nulas para um GRR
                        
                save_json(path+x+".json", student_data[x])
        
        listagens_arquivos = [
                EvasionForm.EF_ABANDONO,
                EvasionForm.EF_DESISTENCIA,
                EvasionForm.EF_FORMATURA,
                EvasionForm.EF_ATIVO
        ]
        
        listagens = listagem_alunos(dataframe)
        for l in listagens:
                if(l in listagens_arquivos):
                        save_json(path+"listagem/"+str(l)+".json", listagens[l])
        
        
        
        
        #Falta verificar se alguem nao recebeu algumas analises
        
def generate_student_list(path):
        pass

def generate_admission_data(path,df):
        listagem_turma_ingresso(df)
        pass

def generate_admission_list(path):
        pass

def generate_course_data(path,df):
        lista_disciplinas = {} 
        informacoes_gerais(df,lista_disciplinas) 
        analises_gerais(df,lista_disciplinas) 
        analises_semestrais(df,lista_disciplinas) 
        for disciplina in lista_disciplinas.keys():
                save_json(path+disciplina+'.json' ,lista_disciplinas[disciplina]) 
        disciplinas = listagem_disciplina(df,lista_disciplinas) 
        save_json(path+'disciplinas.json',disciplinas) 
        
