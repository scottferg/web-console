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

from commands import command as command_mod
from models import *

import string

INTRO_TEXT = """
Welcome to ferg-console!<br /><br />

Some basic commands:<br />
[color="orange"]ls    - List contents of a directory[/color]<br />
[color="orange"]cat   - Display the contents of a text-based file[/color]<br />
[color="orange"]clear - Clear the current console buffer[/color]<br /><br />

"""

response_types = ['message',]

def format_response(response):
    '''
    Pieces together the response message after washing it through several
    preliminary text/formatting filters
    '''
    if response['message'][0:6] != '<br />':
        response['message'] = '<br />' + response['message']

    response['message'] = string.replace(response['message'], '\t', '&nbsp;&nbsp;&nbsp;&nbsp;')
    response['message'] = string.replace(response['message'], '\n', '<br />')

    return response

def parse_command(command):
    return command.split(' ')

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
        command_class = command_mod.load_command(parsed_command[0])
        args = parsed_command[1:]
        command = command_class()

        result = simplejson.dumps(format_response(command.execute(*args)))
    except ImportError:
        result = simplejson.dumps({
            'type'   : 'content',
            'message': '<br />' + '-bash: %s: command not found' % parsed_command[0],
        })

    return HttpResponse(result)
