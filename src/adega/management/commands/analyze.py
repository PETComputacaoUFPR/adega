from django.core.management.base import BaseCommand
from submission.models import Submission

from submission.analysis.main import analyze


class Command(BaseCommand):
    help = 'Makes one specific analysis'

    def add_arguments(self, parser):
        parser.add_argument('submission_id', type=int)

    def handle(self, *args, **options):
        id = options['submission_id']

        submission = Submission.objects.get(pk=id)

        analyze(submission)
