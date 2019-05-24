from django.test import TestCase, Client
from django.contrib.auth.models import User
from submission.models import Submission
from educator.models import Educator
from degree.models import Degree
import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../submission/')
from tests import SubmissionMixin

class StudentTest(TestCase, SubmissionMixin):
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
        
    def testStudentRoutes(self): 
        # logging in
        response = self.client.post('/public/', self.login_data, follow=True)

        # submitting report
        response = self.createSubmission(self.degree.id)

        # checks if submission was properly analyzed and gets its id
        a_id = self.getSubmissionId()
        
        # trying to access /student/id/
        response = self.client.get('/student/' + a_id + '/')
        self.assertEqual(response.status_code, 200) # if ne, failed to access /student/id/

        # trying to access /student/id/GRR/
        response = self.client.get('/student/' + a_id + '/GRR20130000/')
        self.assertEqual(response.status_code, 200) # if ne, failed to access /student/id/GRR/

        # deletes submission
        self.deleteSubmission(a_id)