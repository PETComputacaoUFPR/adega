from django.core.management.base import BaseCommand
from grid.models import Grid

from grid.generate_grid import generate_grid


class Command(BaseCommand):
    help = 'Makes one specific analysis'

    def add_arguments(self, parser):
        parser.add_argument('grid_id', type=int)

    def handle(self, *args, **options):
        id = options['grid_id']

        grid = Grid.objects.get(pk=id)

        generate_grid(grid, False)
