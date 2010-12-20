from django.db import models

class Mimetype(models.Model):
    mimetype = models.CharField(max_length = 25)
    subtype = models.CharField(max_length = 25)

    def __str__(self):
        return '%s/%s' % (self.mimetype, self.subtype)

class File(models.Model):
    mimetype = models.ForeignKey(Mimetype)
    filename = models.CharField(max_length = 250)
    content = models.TextField()

    def __str__(self):
        return self.filename
