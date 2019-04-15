from django.test import TestCase, Client
from django.contrib.auth.models import User
from submission.models import Submission
from educator.models import Educator
from degree.models import Degree
import os

class SubmissionMixin(object):
    def createSubmission(self, degree_id):
        # trying to submit data for analysis
        basePath = os.path.dirname(os.path.abspath(__file__))
        historico_path = basePath + '/analysis/test/historico.xls'
        matricula_path = basePath + '/analysis/test/matricula.xls'

        historico = open(historico_path, 'rb') 
        matricula = open(matricula_path, 'rb')
        report_data = {
                        'historico': historico,
                        'matricula': matricula,
                        'relative_year': '2019',
                        'relative_semester': '1',
                        'semester_status': '0',
                        'degree': str(degree_id)
                      }
        response = self.client.post('/submission/create/', report_data, follow=True)

        self.assertEqual(response.status_code, 200) # if ne, failed to submit report to /submission/create/
    
        return response

    def deleteSubmission(self, a_id):
        # get number of objects
        count = len(Submission.objects.all())
        
        # destroying submission via /submission/delete/id
        response = self.client.post('/submission/delete/' + a_id, follow=True)
        self.assertEqual(len(Submission.objects.all()), count-1) # if ne, failed to delete submission
        
        return response

    def getSubmissionId(self):
        analysis = Submission.objects.first()
        self.assertEqual(analysis.analysis_status, 1) # if ne, failed to analyze submission 

        return str(analysis.id)

class SubmissionTest(TestCase, SubmissionMixin):
    @classmethod
    def setUpTestData(cls):
        # instantiate a Client to make requests
        cls.client = Client(HTTP_USER_AGENT='Mozilla/5.0')

        # create user
        cls.credentials = {"username":"testuser","email":"testuser@user.com","password":"secret"}
        cls.user = User.objects.create_user(**cls.credentials)
        cls.user.save()

        # create a degree
        cls.degree = Degree.objects.create(name="Curso ficticio", code="00A", manager_id=cls.user.id)
        cls.degree.save()
        
        # create an educator
        cls.educator = Educator.objects.create(user_id=cls.user.id)
        cls.educator.save()
        cls.educator.degree.add(cls.degree)
        cls.educator.save()

        # login data
        cls.login_data = {
                'email': 'testuser@user.com', 
                'password': 'secret'
               }

    def testSubmissionRoutes(self): 
        # logging in
        response = self.client.post('/public/', self.login_data, follow=True)

        # trying to access /submission/ after logging in
        response = self.client.get('/submission/')
        self.assertEqual(response.status_code, 200) # if ne, failed to access /submission/
        
        # trying to access /submission/create
        response = self.client.get('/submission/create/')
        self.assertEqual(response.status_code, 200) # if ne, failed to access /submission/create
        
        # trying to submit data for analysis
        response = self.createSubmission(self.degree.id)
        self.assertEqual(response.status_code, 200) # if ne, failed to submit report to /submission/create/

        # checks if submission was properly analyzed and gets its id
        a_id = self.getSubmissionId()

        # deletes submission
        self.deleteSubmission(a_id)