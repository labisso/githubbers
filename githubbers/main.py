#!/usr/bin/env python

import optparse

import yaml
import jinja2

import hubbers

_USAGE = "%prog -c CONFIG [-o OUTPUT]"

_DESCRIPTION = """
Queries Github contributors for a project and populates a template.
"""

def build_parser():
    parser = optparse.OptionParser(usage=_USAGE, description=_DESCRIPTION)

    parser.add_option('-c', '--config', dest='config', metavar='FILE',
            help='Configuration file')
    parser.add_option('-o', '--output', dest='output', metavar='FILE',
            help='Output file. If unspecified, output is written to stdout.')
    return parser

def main():

    parser = build_parser()
    opts, args = parser.parse_args()

    if not opts.config:
        parser.error('A config file must be specified')

    config_string = open(opts.config).read()

    if opts.output:
        output = open(opts.output,'w')
    else:
        output = None

    config = yaml.load(config_string)
    user = config['user']
    repo = config['repository']

    ignore = config.get('ignore')
    if ignore:
        ignore_logins = ignore.get('logins') or []
        ignore_names = ignore.get('names') or []

    template = jinja2.Template(config['template'])

    all = hubbers.get_hubbers(user, repo)
    if ignore_logins or ignore_names:
        contributors = [u for u in all if u.login not in ignore_logins and 
                u.name not in ignore_names]
    else:
        contributors = all
    
    print >>output, template.render(contributors=contributors)

if __name__ == '__main__':
    main()
