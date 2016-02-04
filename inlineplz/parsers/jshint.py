# -*- coding: utf-8 -*-
from __future__ import absolute_import

import xmltodict

from inlineplz.parsers.base import ParserBase


class JSHintParser(ParserBase):
    """Parse json jshint output."""

    def parse(self, lint_data):
        messages = set()
        obj = xmltodict.parse(lint_data)
        if 'file' in obj['checkstyle']:
            # handle single file
            try:
                path = obj['checkstyle']['file']['@name']
                for errordata in obj['checkstyle']['file']['error']:
                    self.create_message_from_error(messages, path, errordata)
            # handle many files
            except TypeError:
                for filedata in obj['checkstyle']['file']:
                    for errordata in filedata['error']:
                        try:
                            path = filedata['@name']
                            self.create_message_from_error(messages, path, errordata)
                        except (AttributeError, TypeError):
                            pass
        return messages

    def create_message_from_error(self, messages, path, errordata):
        line = int(errordata['@line'])
        msgbody = errordata['@message']
        messages.add((path, line, msgbody))
