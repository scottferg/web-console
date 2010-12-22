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

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.utils import simplejson

import sys

from models import *

INTRO_TEXT = """
Welcome to ferg-console!<br /><br />

Some basic commands:<br />
[color="orange"]ls  - List contents of a directory[/color]<br />
[color="orange"]cat - Display the contents of a text-based file[/color]<br /><br />

"""

def parse_command(command):
    return command.split(' ')

def load_command(command):
    __import__('console.commands.%s' % command, globals(), locals())
    mod = sys.modules['console.commands.%s' % command]
    return getattr(mod, command)

def index(request):
    return render_to_response('console.html',
        {
            'hostname': Hostname(request.META['SERVER_NAME'])(),
            'intro_text': INTRO_TEXT,
        })

def submit(request):
    action = request.REQUEST['action']

    parsed_command = parse_command(action)

    try:
        command_class = load_command(parsed_command[0])
        args = parsed_command[1:]
        command = command_class()

        result = simplejson.dumps(command.execute(*args))
    except ImportError:
        result = simplejson.dumps({
            'type'   : 'content',
            'message': '<br />' + '-bash: %s: command not found' % parsed_command[0],
        })

    return HttpResponse(result)
