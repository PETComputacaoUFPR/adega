from django.core.management.base import BaseCommand
from submission.models import Submission
from degree.models import Degree

from submission.analysis.main import analyze


class Command(BaseCommand):
    help = ' Reexecute last analyze of all degree'

    def handle(self, *args, **options):

        degrees = Degree.objects.all()
        submissions = Submission.objects.all()

        to_analyze = []
        # for each degree, get last submission with sucessful and re execute
        for degree in degrees:
            # get all submissions of degree
            submissions = Submission.objects.filter(degree=degree, analysis_status=Submission.STATUS_FINISHED)
            # check if degree has submissions
            if len(submissions) > 0:
                # sort reverse submission by timestamp and the most recent submission
                submission = submissions.order_by('timestamp').reverse()[0]
                submission.set_executing()
                to_analyze.append(submission)

        # Execute each analyze in chronological order
        for submission in to_analyze:
            analyze(submission)