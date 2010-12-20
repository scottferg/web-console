from django.db.models import Q

import string

from console.models import Mimetype, File

class cat(object):
    def execute(self, *args):
        # Mimetype can be set magically via a metaclass, derived classes
        # will only need to set a "property" or else have no mimetype
        mimetype = Mimetype.objects.filter(Q(mimetype='text') & Q(subtype='plain'))[0]

        if mimetype and args[0]:
            try:
                file = File.objects.get(filename=args[0])
                yield string.replace(file.content, '\n', '<br />')
            except File.DoesNotExist:
                yield 'File \'%s\' not found' % args[0]
