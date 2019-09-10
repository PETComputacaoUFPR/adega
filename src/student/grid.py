from submission.analysis.utils.situations import Situation
from grid.models import Grid
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
        print(self.grid_detail)
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
                __import__('pprint').pprint(cgc[course_code].get_info())
                __import__('pprint').pprint(new_grid)


                new_grid[i][j] = cgc[course_code].get_info()
                #new_grid[i, j] = cgc[course_code].get_info()
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
                "equivalences": cgc[code].count_equivalence(),
                "cancelled": cgc[code].count_cancelled(),
                "necessary": self.grid_detail.count_code_on_grid(code),
                "grade": cgc[code].mean_grade(),
            })
        return info
    
    def get_situation(self, hist):
        cgc = self.compute_cgc(hist)
        return self.get_grid(cgc), self.get_repeated_course_info(cgc)

    #grid_ibm = Grid.objects.get(id=3)
    #grid = DegreeGridDescription(grid_ibm.get_grid())
