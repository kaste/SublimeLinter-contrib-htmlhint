#
# linter.py
# Linter for SublimeLinter3, a code checking framework for Sublime Text 3
#
# Written by Mark Maday
# Copyright (c) 2015 Mark Maday
#
# License: MIT
#

"""This module exports the Htmlhint plugin class."""

import re
from SublimeLinter.lint import Linter, util, persist


class Htmlhint(Linter):

    """Provides an interface to htmlhint."""

    syntax = 'html'
    cmd = 'htmlhint'
    executable = None
    version_args = '--version'
    version_re = r'(?P<version>\d+\.\d+\.\d+)'
    version_requirement = '>= 0.9.0'
    regex = r'^\s*line (?P<line>\d+), col (?P<col>\d+): (?P<message>.+)'
    tempfile_suffix = '-'
    config_file = ('--config', '.htmlhintrc', '~')

    warn_regex = (
        r'^(Doctype must be html5.'
        r'|The script tag can not be used in head'
        r'|The value of href \[ .*?\] must be'
        r'|The value of .*? can not use ad keyword.'
        r'|Alt of img tag must be set value.'
        r'|Mixed spaces and tabs in front of line'
        r'|Style tag can not be use'
        r'|The empty tag : \[ \w+ \] must closed by self.)'
    )
    warn_re = re.compile(warn_regex)

    def split_match(self, match):       
        split = super().split_match(match)
        if match:
            message = match.group('message')
            
            warn = self.warn_re.match(message)
            if warn:
                split = (split[0], split[1], split[2], False, True, split[5], split[6])
            
            persist.debug('match -- msg:"{}", split:"{}", warn: {}'.format(message, split, warn))
        return split