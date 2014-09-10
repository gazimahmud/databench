#!/usr/bin/env python
"""Databench command line executable. Run to create a server that serves
the analyses pages and runs the python backend."""


import os
import logging
import argparse
import werkzeug.serving

from .app import App
from . import __version__ as DATABENCH_VERSION


def main():
    """Entry point to run databench."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--version', action='version',
                        version='%(prog)s '+DATABENCH_VERSION)
    parser.add_argument('--log', dest='loglevel', default="NOTSET",
                        help='set log level')
    parser.add_argument('--host', dest='host',
                        default=os.environ.get('HOST', 'localhost'),
                        help='set host for webserver')
    parser.add_argument('--port', dest='port',
                        type=int, default=int(os.environ.get('PORT', 5000)),
                        help='set port for webserver')
    delimiter_args = parser.add_argument_group('delimiters')
    delimiter_args.add_argument('--variable_start_string',
                                help='delimiter for variable start')
    delimiter_args.add_argument('--variable_end_string',
                                help='delimiter for variable end')
    delimiter_args.add_argument('--block_start_string',
                                help='delimiter for block start')
    delimiter_args.add_argument('--block_end_string',
                                help='delimiter for block end')
    delimiter_args.add_argument('--comment_start_string',
                                help='delimiter for comment start')
    delimiter_args.add_argument('--comment_end_string',
                                help='delimiter for comment end')
    args = parser.parse_args()

    # log
    if args.loglevel != 'NOTSET':
        print 'Setting loglevel to '+args.loglevel+'.'
        logging.basicConfig(level=getattr(logging, args.loglevel))

    # delimiters
    delimiters = {
        'variable_start_string': '[[',
        'variable_end_string': ']]',
    }
    if args.variable_start_string:
        delimiters['variable_start_string'] = args.variable_start_string
    if args.variable_end_string:
        delimiters['variable_end_string'] = args.variable_end_string
    if args.block_start_string:
        delimiters['block_start_string'] = args.block_start_string
    if args.block_end_string:
        delimiters['block_end_string'] = args.block_end_string
    if args.comment_start_string:
        delimiters['comment_start_string'] = args.comment_start_string
    if args.comment_end_string:
        delimiters['comment_end_string'] = args.comment_end_string

    print '--- databench v'+DATABENCH_VERSION+' ---'
    logging.info('host='+str(args.host)+', port='+str(args.port))
    logging.info('delimiters='+str(delimiters))

    @werkzeug.serving.run_with_reloader
    def reloader():
        app = App(__name__, host=args.host, port=args.port,
                  delimiters=delimiters)
        app.run()
        return app
    return reloader()


if __name__ == '__main__':
    main()