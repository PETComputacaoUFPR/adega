from submission.analysis.utils.situations import Situation
import numpy as np


class CourseGrid:
    def __init__(self, obj):
        self.situation = obj["situacao"]
        self.code = obj["codigo"]
        self.name = obj["nome"]
        self.year = obj["ano"]
        self.semester = obj["semestre"]
        self.grade = obj["nota"]

    def is_approved(self):
        sit = Situation.str_to_code(self.situation)
        return sit in Situation.SITUATION_PASS

    def is_failed(self):
        sit = Situation.str_to_code(self.situation)
        return sit in Situation.SITUATION_FAIL

    def is_registered(self):
        sit = Situation.str_to_code(self.situation)
        return sit == Situation.SIT_MATRICULA

    def is_cancelled(self):
        sit = Situation.str_to_code(self.situation)
        return sit in Situation.SITUATION_CANCELLED

    def is_equivalence(self):
        sit = Situation.str_to_code(self.situation)
        return sit == Situation.SIT_EQUIVALENCIA

    # This is different of Situation.COURSED
    # Check situations.py to confer the difference
    def is_coursed(self):
        return self.is_approved() or self.is_failed()


class CourseGridCollection:
    def __init__(self, code, grid):
        self.grid = grid
        self.code = code
        self.name = grid.code_to_name[code]
        self.historic = []
        self.is_real_code = grid.is_real_code(code)
        self.is_repeated_code = grid.is_repeated_code(code)
    
    def add(self, course_obj):
        code = course_obj["codigo"]

        # If the course_obj was related to this course or an equivalent
        if self.grid.is_equivalence(code, self.code):
            cg = CourseGrid(course_obj)
            self.historic.append(cg)
    
    def reset(self):
        self.historic = []
    
    def get_failed_historic(self):
        return [x for x in self.historic if x.is_failed()]

    def get_approved_historic(self):
        return [x for x in self.historic if x.is_approved()]

    def get_registered_historic(self):
        return [x for x in self.historic if x.is_registered()]

    def get_coursed_historic(self):
        return [x for x in self.historic if x.is_coursed()]

    def get_cancelled_historic(self):
        return [x for x in self.historic if x.is_cancelled()]

    def get_equivalence_historic(self):
        return [x for x in self.historic if x.is_equivalence()]

    def count_approved(self):
        hist = self.get_approved_historic()
        return len(hist)

    def count_failed(self):
        hist = self.get_failed_historic()
        return len(hist)

    def count_registered(self):
        hist = self.get_registered_historic()
        return len(hist)

    def count_equivalence(self):
        hist = self.get_equivalence_historic()
        return len(hist)

    def count_coursed(self):
        hist = self.get_coursed_historic()
        return len(hist)

    def count_cancelled(self):
        hist = self.get_cancelled_historic()
        return len(hist)
    
    def mean_grade(self):
        grades = [x.grade for x in self.get_coursed_historic()]
        return np.mean(grades)
    

    def get_prevalent_situation(self):
        # If this is an course that repeat on grid, then this doesnt have any
        # situation
        if(self.is_repeated_code):
            return ""

        # If there is an approved, registered or equivalence situation,
        # then it is the prevalent
        if self.count_approved() > 0:
            return "approved"
        if self.count_equivalence() > 0:
            return "equivalence"
        if self.count_registered() > 0:
            return "registered"

        # If there is at least one failure, and there is no
        # approve or registered, then the prevalent situation is "failed"
        if self.count_failed() > 0:
            return "failed"

        # Cancelled has an lesser importance
        if self.count_cancelled() > 0:
            return "cancelled"

        return ""

    def has_detail(self):
        p_sit = self.get_prevalent_situation()
        return p_sit == "approved" or p_sit == "failed" or p_sit == "approved"

    def get_info(self):
        p_sit = self.get_prevalent_situation()
        info = {
            "name": self.name,
            "code": self.code,
            "situation": p_sit,
            "is_real_code": self.is_real_code
        }
        if self.has_detail():
            info["detail"] = {
                "count": self.count_coursed(),
                "mean_grade": self.mean_grade(),
            }

        return info


class DegreeGridDescription:
    def __init__(self, obj):
        self.year = obj["year"]
        self.grid = obj["grid"]
        self.code_to_name = obj["code_to_name"]
        self.equiv_codes = obj["equiv_codes"]
        self.fake_codes = obj["fake_codes"]

        # Codes that show more then one time on grid, like OPT
        self.repeated_codes = obj["repeated_codes"]

    def count_code_on_grid(self, code):
        count = 0
        
        for line in self.grid:
            for code2 in line:
                if(code2 == code):
                    count+=1
        
        return count

    def is_repeated_code(self, code):
        return code in self.repeated_codes
    
    def is_real_code(self, code):
        return not code in self.fake_codes

    def is_equivalence(self, code1, code2):
        if(code1 in self.equiv_codes and code2 in self.equiv_codes[code1]):
            return True
        if(code2 in self.equiv_codes and code1 in self.equiv_codes[code2]):
            return True
        if(code1 == code2):
            return True
        return False

class DegreeGrid:
    def __init__(self, grid_detail):
        self.grid_detail = grid_detail
        self.cgc = {}
    
    def compute_cgc(self, hist):
        # Create an instance for each cell in grid
        cgc = {}
        for semester in self.grid_detail.grid:
            for code in semester:
                cgc[code] = CourseGridCollection(code, self.grid_detail)

        for h in hist:
            code = h["codigo"]

            # For each code and equivalent codes from an course in historic
            # and it self
            all_codes = [code]
            if code in self.grid_detail.equiv_codes:
                all_codes += self.grid_detail.equiv_codes[code]
            for code in all_codes:
                # Count it on each grid course only if it is on grid
                # Eletive courses will not be considered
                if(code in cgc):
                    cgc[code].add(h)

        return cgc

    def get_grid(self, cgc):
        new_grid = np.array(self.grid_detail.grid, dtype=np.dtype(object))
        for i, line in enumerate(self.grid_detail.grid):
            for j, course_code in enumerate(line):
                # TODO: Add possibility to insert others grids
                new_grid[i, j] = cgc[course_code].get_info()
        return new_grid
    
    def get_repeated_course_info(self, cgc):
        info = []
        for code in self.grid_detail.repeated_codes:
            info.append({
                "code": cgc[code].code,
                "name": cgc[code].name,
                "approves": cgc[code].count_approved(),
                "registered": cgc[code].count_registered(),
                "fails": cgc[code].count_failed(),
                "equivalences" : cgc[code].count_equivalence(),
                "cancelled" : cgc[code].count_cancelled(),
                "necessary": self.grid_detail.count_code_on_grid(code),
                "grade": cgc[code].mean_grade(),
            })
        return info
    
    def get_situation(self, hist):
        cgc = self.compute_cgc(hist)
        return self.get_grid(cgc), self.get_repeated_course_info(cgc)

    bcc_grid_2011 = DegreeGridDescription({
        "year": 2011,
        "grid": [
            ["CI241", "CI055", "CM201", "CM045", "BA040", ],
            ["CI243", "CI056", "CI067", "CM005", "BQ005", ],
            ["CI244", "CI057", "CI166", "BQ054", "BC056", ],
            ["CI215", "CI062", "CE003", "BG054", "BF075", "CI164", ],
            ["CI162", "CI065", "CI394", "CI316", "MN127", ],
            ["CI167", "CI209", "CI171", "CI218", "CI220","MN128", ],
            ["CI221", "CI169", "CI172", "OPT", "MN129", ],
            ["CI262", "OPT", "OPT", "OPT", ],
        ],
        "repeated_codes": ["OPT"],
        "fake_codes": ["OPT", "TG I"],
        "code_to_name": {
        "BA040":"Anatomia Humana Sistêmica",
        "BC056":"Fundamentos de Biologia Celular e Tecidual",
        "BF075":"Fisiologia para Informática Biomédica",
        "BG054":"Genética e Evolução para o Curso de Informática Biomédica",
        "BQ005":"Introdução à Bioquímica",
        "BQ054":"Biologia Molecular e Bioinformática",
        "CE003":"Estatística II",
        "CI055":"Algoritmos e Estruturas de Dados I",
        "CI056":"Algoritmos e Estruturas de Dados II",
        "CI057":"Algoritmos e Estruturas de Dados III",
        "CI062":"Técnicas Alternativas de Programação",
        "CI065":"Algoritmo e Teoria dos Grafos",
        "CI067":"Oficina de Computação",
        "CI162":"Engenharia de Requisitos",
        "CI164":"Introdução à Computação Científica",
        "CI166":"Metodologia Científica",
        "CI167":"Sistemas de Informação em Saúde",
        "CI169":"Bioinformática",
        "CI171":"Aprendizado de Máquina",
        "CI172":"Processamento de Imagens Biomédicas",
        "CI209":"Inteligência Artificial",
        "CI215":"Sistemas Operacionais",
        "CI218":"Sistemas de Banco de Dados",
        "CI220":"Teoria de Sistemas",
        "CI221":"Engenharia de Software",
        "CI241":"Introdução a Sistemas Computacionais",
        "CI243":"Fundamentos de Projeto e Arquitetura de Computadores",
        "CI244":"Fundamentos de Redes de Sistemas Distribuídos",
        "CI262":"Trabalho de Conclusão de Curso em Informática Biomédica",
        "CI316":"Programação Paralela",
        "CI394":"Processamento de Imagens",
        "CM005":"Álgebra Linear",
        "CM045":"Geometria Analítica",
        "CM201":"Cálculo Diferencial e Integral I",
        "MN127":"Saúde, Meio Ambiente e Sociedade",
        "MN128":"Organização do Sistema de Saúde Brasileiro",
        "MN129":"Metodologia da Pesquisa e Bioética em Saúde",
        "MN130":"Gestão Hospitalar",
        "CE073":"Análise de Dados Categóricos",
        "CE075":"Análise de Dados Longitudinais",
        "CE077":"Análise de Sobrevivência",
        "CI059":"Introdução à Teoria da Computação",
        "CI069":"Administração de Empresas de Informática",
        "CI084":"Tópicos em Teoria dos Grafos",
        "CI085":"Tópicos em Computação Gráfica",
        "CI086":"Tópicos em Arquitetura de Computadores",
        "CI087":"Tópicos em Banco de Dados",
        "CI088":"Tópicos Em Sistemas Distribuídos",
        "CI089":"Tópicos em Teoria da Computação",
        "CI090":"Tópicos em Engenharia de Software",
        "CI091":"Tópicos em Avaliação de Desempenho",
        "CI092":"Tópicos em Tecnologias e Aplicações",
        "CI093":"Tópicos em Análise Numérica",
        "CI094":"Tópicos em Processamento de Imagens",
        "CI095":"Tópicos em Compiladores",
        "CI097":"Tópicos em Sistemas Digitais",
        "CI163":"Projeto de Software",
        "CI168":"Tópicos em Sistemas de Informação em Saúde",
        "CI170":"Tópicos em Bioinformática",
        "CI173":"Computação Gráfica",
        "CI174":"Tópicos em Engenharia da Computação",
        "CI204":"Administração de Informática",
        "CI205":"Administração de Produção para Informática",
        "CI211":"Construção de Compiladores",
        "CI214":"Estrutura de Linguagens de Programação",
        "CI301":"Tópicos em Ciência da Computação I",
        "CI302":"Tópicos em Ciência da Computação II",
        "CI303":"Tópicos em Ciência da Computação III",
        "CI304":"Tópicos em Ciência da Computação IV",
        "CI305":"Tópicos em Ciência da Computação V",
        "CI306":"Tópicos em Ciência da Computação VI",
        "CI309":"Tópicos em Inteligência Artificial",
        "CI310":"Tópicos em Aprendizado de Máquina",
        "CI311":"Fundamentos Lógicos da Inteligência Artificial",
        "CI312":"Arquiteturas Avançadas de Computadores",
        "CI313":"Arquitetura de Computadores Paralelos",
        "CI314":"Introdução à Computação Paralela",
        "CI315":"Projeto de Sistemas Operacionais",
        "CI317":"Tópicos em Sistemas Operacionais",
        "CI318":"Tópicos em Computação Paralela",
        "CI320":"Tópicos em Programação de Computadores",
        "CI321":"Tópicos em Sistemas Embutidos",
        "CI338":"Tópicos em Geometria Computacional",
        "CI339":"Complexidade Computacional",
        "CI340":"Tópicos em Métodos Formais",
        "CI350":"Interação Humano-Computador",
        "CI351":"Tópicos em Interação Humano-Computador",
        "CI355":"Tópicos em Algoritmos",
        "CI358":"Administração e Gerência de Redes de Computadores",
        "CI359":"Laboratório de Redes de Computadores",
        "CI360":"Redes Móveis",
        "CI361":"Sistemas Distribuídos",
        "CI362":"Sistemas Operacionais Distribuídos",
        "CI363":"Tópicos de Multimídia em Redes de Computadores",
        "CI364":"Tópicos em Computação em Rede",
        "CI365":"Tópicos em Redes de Computadores",
        "CI366":"Tópicos em Redes Móveis",
        "CI367":"Tópicos em Simulação de Sistemas Computacionais",
        "CI395":"Oficina de Visão Computacional e Processamento de Imagens",
        "CI396":"Tópicos em Visão Computacional",
        "OPT": "Optativa"
        },

        "equiv_codes": {
        "MN130": ["OPT"],
        "CE073": ["OPT"],
        "CE075": ["OPT"],
        "CE077": ["OPT"],
        "CI059": ["OPT"],
        "CI069": ["OPT"],
        "CI084": ["OPT"],
        "CI085": ["OPT"],
        "CI086": ["OPT"],
        "CI087": ["OPT"],
        "CI088": ["OPT"],
        "CI089": ["OPT"],
        "CI090": ["OPT"],
        "CI091": ["OPT"],
        "CI092": ["OPT"],
        "CI093": ["OPT"],
        "CI094": ["OPT"],
        "CI095": ["OPT"],
        "CI097": ["OPT"],
        "CI163": ["OPT"],
        "CI168": ["OPT"],
        "CI170": ["OPT"],
        "CI173": ["OPT"],
        "CI174": ["OPT"],
        "CI204": ["OPT"],
        "CI205": ["OPT"],
        "CI211": ["OPT"],
        "CI214": ["OPT"],
        "CI301": ["OPT"],
        "CI302": ["OPT"],
        "CI303": ["OPT"],
        "CI304": ["OPT"],
        "CI305": ["OPT"],
        "CI306": ["OPT"],
        "CI309": ["OPT"],
        "CI310": ["OPT"],
        "CI311": ["OPT"],
        "CI312": ["OPT"],
        "CI313": ["OPT"],
        "CI314": ["OPT"],
        "CI315": ["OPT"],
        "CI317": ["OPT"],
        "CI318": ["OPT"],
        "CI320": ["OPT"],
        "CI321": ["OPT"],
        "CI338": ["OPT"],
        "CI339": ["OPT"],
        "CI340": ["OPT"],
        "CI350": ["OPT"],
        "CI351": ["OPT"],
        "CI355": ["OPT"],
        "CI358": ["OPT"],
        "CI359": ["OPT"],
        "CI360": ["OPT"],
        "CI361": ["OPT"],
        "CI362": ["OPT"],
        "CI363": ["OPT"],
        "CI364": ["OPT"],
        "CI365": ["OPT"],
        "CI366": ["OPT"],
        "CI367": ["OPT"],
        "CI395": ["OPT"],
        "CI396": ["OPT"]
        }
    })

	Gestão Hospitalar
	Análise de Dados Categóricos
	Análise de Dados Longitudinais
	Análise de Sobrevivência
	Introdução à Teoria da Computação
	Administração de Empresas de Informática
	Tópicos em Teoria dos Grafos
	Tópicos em Computação Gráfica
	Tópicos em Arquitetura de Computadores
	Tópicos em Banco de Dados
	Tópicos Em Sistemas Distribuídos
	Tópicos em Teoria da Computação
	Tópicos em Engenharia de Software
	Tópicos em Avaliação de Desempenho
	Tópicos em Tecnologias e Aplicações
	Tópicos em Análise Numérica
	Tópicos em Processamento de Imagens
	Tópicos em Compiladores
	Tópicos em Sistemas Digitais
	Projeto de Software
	Tópicos em Sistemas de Informação em Saúde
	Tópicos em Bioinformática
	Computação Gráfica
	Tópicos em Engenharia da Computação
	Administração de Informática
	Administração de Produção para Informática
	Construção de Compiladores
	Estrutura de Linguagens de Programação
	Tópicos em Ciência da Computação I
	Tópicos em Ciência da Computação II
	Tópicos em Ciência da Computação III
	Tópicos em Ciência da Computação IV
	Tópicos em Ciência da Computação V
	Tópicos em Ciência da Computação VI
	Tópicos em Inteligência Artificial
	Tópicos em Aprendizado de Máquina
	Fundamentos Lógicos da Inteligência Artificial
	Arquiteturas Avançadas de Computadores
	Arquitetura de Computadores Paralelos
	Introdução à Computação Paralela
	Projeto de Sistemas Operacionais
	Tópicos em Sistemas Operacionais
	Tópicos em Computação Paralela
	Tópicos em Programação de Computadores
	Tópicos em Sistemas Embutidos
	Tópicos em Geometria Computacional
	Complexidade Computacional
	Tópicos em Métodos Formais
	Interação Humano-Computador
	Tópicos em Interação Humano-Computador
	Tópicos em Algoritmos
	Administração e Gerência de Redes de Computadores
	Laboratório de Redes de Computadores
	Redes Móveis
	Sistemas Distribuídos
	Sistemas Operacionais Distribuídos
	Tópicos de Multimídia em Redes de Computadores
	Tópicos em Computação em Rede
	Tópicos em Redes de Computadores
	Tópicos em Redes Móveis
	Tópicos em Simulação de Sistemas Computacionais
	Oficina de Visão Computacional e Processamento de Imagens
	Tópicos em Visão Computacional
