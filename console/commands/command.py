# Copyright (c) 2011, Scott Ferguson
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the software nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY SCOTT FERGUSON ''AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL SCOTT FERGUSON BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from django.db.models import Q
from console.models import Mimetype, File

import sys

class MimetypeError(Exception):
    def __str__(self):
        return repr('')

class command(type):
    def __new__(meta, classname, bases, class_dict):
        if not class_dict.has_key('manpage'):
			class_dict['manpage'] = 'No man page entry for this command.'

        if class_dict.has_key('mimetypes'):
            for index,mimetype in enumerate(class_dict['mimetypes']):
                mimetype = mimetype.split('/')
                mimetype = Mimetype.objects.get(Q(mimetype = mimetype[0]) & Q(subtype = mimetype[1]))

                class_dict['mimetypes'][index] = mimetype
        else:
            class_dict['mimetypes'] = []

        return type.__new__(meta, classname, bases, class_dict)

def load_command(command):
    __import__('console.commands.commands', globals(), locals())
    mod = sys.modules['console.commands.commands']
    return getattr(mod, command)
