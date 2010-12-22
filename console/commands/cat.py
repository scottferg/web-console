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
from command import command, MimetypeError

class cat(object):
    __metaclass__ = command

    mimetypes = ['text/plain',]

    manpage = '''
    [b]NAME[/b]
       cat -- Displays the contents of a file

    [b]SYNOPSIS[/b]
       cat [file]

    [b]DESCRIPTION[/b]
       Displays the contents of a text file. Works for all files with a
       text base mimetype.  Honors BBCode styling for content.
    '''

    def execute(self, *args):
        if args[0]:
            try:
                file = File.objects.get(filename=args[0])

                if not file.mimetype in self.mimetypes:
                    raise MimetypeError

                message = file.content
            except File.DoesNotExist:
                message = '<br /> File \'%s\' not found' % args[0]
            except MimetypeError:
                message = '<br /> File is not a textfile'

            return {
                'type'   : 'content',
                'message': message,
            }
