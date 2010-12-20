from django.http import HttpResponse
from django.shortcuts import render_to_response

from django.contrib.auth.models import User

from models import *

def tty_styling(function):
    return '<span class="hostname">%s:/></span>' % function()

@tty_styling
def hostname():
    return 'user@ferg-console'

def parse_command(command):
    return command.split(' ')

def load_command(command):
    mod = __import__('commands.%s' % command, globals(), locals(), [command])
    return getattr(mod, command)

def index(request):
    return render_to_response('console.html',
        {
            'hostname': hostname,
        })

def submit(request):
    buffer = request.REQUEST['buffer']
    action = request.REQUEST['action']

    if buffer:
        buffer = buffer + '<br />' + hostname + ' ' + action
    else:
        buffer = hostname + ' ' + action

    parsed_command = parse_command(action)

    try:
        command_class = load_command(parsed_command[0])
        args = parsed_command[1:]
    except ImportError:
        buffer = buffer + '<br />' + '-bash: %s: command not found' % parsed_command[0]
        return HttpResponse(buffer)

    command = command_class()

    for result in command.execute(*args):
        buffer = buffer + '<br />' + result

    return HttpResponse(buffer)
