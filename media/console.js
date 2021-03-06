// Copyright (c) 2011, Scott Ferguson
// All rights reserved.
// 
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions are met:
//     * Redistributions of source code must retain the above copyright
//       notice, this list of conditions and the following disclaimer.
//     * Redistributions in binary form must reproduce the above copyright
//       notice, this list of conditions and the following disclaimer in the
//       documentation and/or other materials provided with the distribution.
//     * Neither the name of the software nor the
//       names of its contributors may be used to endorse or promote products
//       derived from this software without specific prior written permission.
// 
// THIS SOFTWARE IS PROVIDED BY SCOTT FERGUSON ''AS IS'' AND ANY
// EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
// WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
// DISCLAIMED. IN NO EVENT SHALL SCOTT FERGUSON BE LIABLE FOR ANY
// DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
// (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
// LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
// ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
// (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
// SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

function Console() {
    this.command_buffer = [];
    this.command_index = 0;

    this.bindHotKeys();
    this.initCommandline();
}

Console.prototype.bindHotKeys = function() {
    var that = this;

    jQuery(document).keydown(function(event) {
        switch(event.keyCode) {
            case 38: /* up */
                that.getPreviousCommand();
                break;
            case 40: /* down */
                that.getNextCommand();
                break;
            case 13:
                that.submitCommand();
                break;
        }
    });
};

Console.prototype.initCommandline = function() {
    var that = this;

    jQuery(document).ready(function() {
        that.hostname = jQuery('span.hostname').first().html();
        that.command_line = jQuery('input[name="console-input"]').first();
        that.command_line.focus();

        var buffer_content = jQuery(jQuery('div#main-content').first());

        buffer_content.html(parseBBCodes(buffer_content.html()));
    });
};

Console.prototype.getPreviousCommand = function() {
    if (this.command_index > 0) {
        this.command_line.val(this.command_buffer[this.command_index - 1]);
        this.command_index--;
    }
};

Console.prototype.getNextCommand = function() {
    this.command_line.val(this.command_buffer[this.command_index + 1]);

    if (this.command_index < this.command_buffer.length) {
        this.command_index++;
    }
};

Console.prototype.submitCommand = function() {
    var command = this.command_line.val();
    var buffer = jQuery('div#main-content').first();

    if (command == '') {
        this.appendResponse(buffer, {'message': ''});
        return;
    }

    this.command_buffer[this.command_index] = command;
    this.command_index++;

    var that = this;

    jQuery.getJSON('/submit/', 
        {
            'action': command,
        },
        function(response) {
            that.processResponse(buffer, response);
        });
};

Console.prototype.processResponse = function(buffer, response) {
    switch (response.type) {
        case 'content':
            this.appendResponse(buffer, response);
            break;  
        case 'update':
            this.updateBuffer(buffer, response);
            break;
    }

    this.command_line.val('');

    jQuery(document).scrollTop(jQuery(document).height());
};

Console.prototype.appendResponse = function(buffer, response) {
    var buffer_content = buffer.html();

    buffer_content += '<br /><span class="hostname">' + this.hostname 
        + '</span>&nbsp;' + this.command_line.val();
    buffer_content += parseBBCodes(response.message);

    buffer.html(buffer_content);
};

Console.prototype.updateBuffer = function(buffer, response) {
    buffer.html(response.message);
};
