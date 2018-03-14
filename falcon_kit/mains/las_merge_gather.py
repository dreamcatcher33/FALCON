"""Not sure anything uses the fopfn anymore.
"""
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

#from future.utils import viewitems
import argparse
import logging
import os
import sys
from .. import io

LOG = logging.getLogger()


def run(gathered_fn, las_fn, p_id2las_fn):
    gathered = io.deserialize(gathered_fn)
    p_id2las = dict()
    for desc in gathered:
        p_id_fn = desc['p_id']
        p_id = int(open(p_id_fn).read()) #io.deserialize(p_id_fn) # someday? requires file-extension
        p_id2las[p_id] = desc['merged_las']
    io.serialize(p_id2las_fn, p_id2las)
    io.serialize(las_fn, list(p_id2las.values()))


class HelpF(argparse.RawTextHelpFormatter, argparse.ArgumentDefaultsHelpFormatter):
    pass


def parse_args(argv):
    description = 'Turn gathered file into .las FOFN (and FOPFN).'
    epilog = ''
    parser = argparse.ArgumentParser(
        description=description,
        epilog=epilog,
        formatter_class=HelpF,
    )
    parser.add_argument(
        '--gathered-fn',
        help='Input. JSON list of output dicts.')
    parser.add_argument(
        '--las-fn',
        help='Output. JSON list of las paths.')
    parser.add_argument(
        '--p-id2las-fn',
        help='Output. JSON dict of p_id to las.')
    args = parser.parse_args(argv[1:])
    return args


def main(argv=sys.argv):
    args = parse_args(argv)
    logging.basicConfig(level=logging.INFO)
    run(**vars(args))


if __name__ == '__main__':  # pragma: no cover
    main()
