import BaseCommand

from console.models import File

class ls(object):
    def execute(self, *args):
        for file in File.objects.all():
            yield file.filename
