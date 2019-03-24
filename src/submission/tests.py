from django.test import TestCase, Client
from django.contrib.auth.models import User
from submission.models import Submission
from educator.models import Educator
from degree.models import Degree

class SubmissionTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # instantiate a Client to make requests
        cls.client = Client(HTTP_USER_AGENT='Mozilla/5.0')

        # create user
        cls.credentials = {"username":"testuser","email":"testuser@user.com","password":"secret"}
        cls.user = User.objects.create_user(**cls.credentials)
        cls.user.save()

        # creates a degree
        cls.degree = Degree.objects.create(name="Curso ficticio", code="00A", manager_id=cls.user.id)
        cls.degree.save()
        
        # create an educator
        cls.educator = Educator.objects.create(user_id=cls.user.id)
        cls.educator.save()
        cls.educator.degree.add(cls.degree)
        cls.educator.save()

    def testSubmissionRoutes(self): 
        # login
        login_data = {
                'email': 'testuser@user.com', 
                'password': 'secret'
               }
        
        response = self.client.post('/public/', login_data, follow=True)
        
        # trying to access /submission/ after logging in
        response = self.client.get('/submission/')
        self.assertEqual(response.status_code,200) # if ne, failed to access /submission/
        
        # trying to access /submission/create
        response = self.client.get('/submission/create/')
        self.assertEqual(response.status_code, 200) # if ne, failed to access /submission/create

        # trying to submit data for analysis
        historico_path = '/adega/src/submission/analysis/test/historico.xls'
        matricula_path = '/adega/src/submission/analysis/test/matricula.xls'

        historico = open(historico_path, 'rb') 
        matricula = open(matricula_path, 'rb')
        report_data = {
                        'historico': historico,
                        'matricula': matricula,
                        'relative_year': '2019',
                        'relative_semester': '1',
                        'semester_status': '0',
                        'degree': '1'
                      }
        response = self.client.post('/submission/create/', report_data, follow=True)

        self.assertEqual(response.status_code, 200) # if ne, failed to submit report to /submission/create/
        
        # checking if the submission was properly analyzed
        analysis = Submission.objects.first()
        self.assertEqual(analysis.analysis_status, 1) # if ne, failed to analyze report 
        
        # store for use in the following tests
        a_id = str(analysis.id)
        
        # trying to access /degree/id/
        response = self.client.get('/degree/' + a_id + '/')
        self.assertEqual(response.status_code, 200) # if ne, failed to access /degree/id/

        # trying to access /student/id/
        response = self.client.get('/student/' + a_id + '/')
        self.assertEqual(response.status_code, 200) # if ne, failed to access /student/id/

        # trying to access /student/id/GRR/
        
        response = self.client.get('/student/' + a_id + '/GRR20130000/')
        self.assertEqual(response.status_code, 200) # if ne, failed to access /student/id/GRR/

        # trying to access /course/id/
        response = self.client.get('/course/' + a_id + '/')
        self.assertEqual(response.status_code, 200) # if ne, failed to access /course/id/
        
        # trying to access /course/id/DIS/
        response = self.client.get('/course/' + a_id + '/Dis1/')
        self.assertEqual(response.status_code, 200) # if ne, failed to access /course/id/DIS/
        
        # trying to access /course/id/compare/
        response = self.client.get('/course/' + a_id + '/compare/')
        self.assertEqual(response.status_code, 200) # if ne, failed to access /course/id/compare/
        
        # trying to access /admission/id/
        response = self.client.get('/admission/' + a_id + '/')
        self.assertEqual(response.status_code, 200) # if ne, failed to access /admission/id/
        
        # trying to access /admission/id/YEAR/SEMESTER
        response = self.client.get('/admission/' + a_id + '/2012/1/')
        self.assertEqual(response.status_code, 200) # if ne, failed to access /admission/id/YEAR/SEMESTER

        # leave for last, destroying submission via /submission/delete/id
        response = self.client.post('/submission/delete/' + a_id, follow=True)
        self.assertEqual(len(Submission.objects.all()),0) # if ne, failed to delete submission
        


