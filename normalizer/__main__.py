import argparse
from shutil import copyfile, move
from normalizer.analyser import analyse
from normalizer.loader import load, read_titles_from_database

import sys
import os.path


def usage():
    print("usage : %s <directory>" % sys.argv[0])
    exit(1)


def _manage_actions(actions, args):
    if args.destination != '' and not args.dry:
        os.makedirs(args.destination, exist_ok=True)
    for action in actions:
        source_path = os.path.join(args.directory, action)
        destination_path = os.path.join(args.directory if args.destination == '' else args.destination, actions[action])
        if not args.dry:
            parent_directory = os.path.dirname(destination_path)
            os.makedirs(parent_directory, exist_ok=True)
        if not os.path.exists(destination_path) or args.overwrite:
            verb = 'copy' if args.copy else 'move'
            print("%s from %s to %s" % (verb, source_path, destination_path))
            if not args.dry:
                if args.copy:
                    copyfile(source_path, destination_path)
                else:
                    move(source_path, destination_path)


def main():
    parser = argparse.ArgumentParser("normalize gamecube iso files to be runnable by nintendont or dolphin")
    parser.add_argument("directory", type=str, help="the directory containing the gamecube iso files")
    parser.add_argument("-l", "--locale",
                        help="define locale used in database for titles (default:'FR').",
                        default='FR')
    parser.add_argument("-d", "--destination",
                        help="define destination directory where the normalized files will be moved/copied. \
                        (default:source directory)",
                        default='')
    parser.add_argument("--dry", help="only print the actions instead of doing them.", action="store_true")
    parser.add_argument("--copy", help="copy files instead of moving them.", action="store_true")
    args = parser.parse_args()
    if not os.path.exists(args.directory):
        print("error : directory does not exists.")
        parser.print_usage()
        exit(1)
    if not os.path.exists('database'):
        load(args.locale, 'database')
    titles = read_titles_from_database(args.locale, 'database')
    if titles is None:
        print("error : can not read the database")
        parser.print_usage()
    actions = analyse(titles, args.directory)
    _manage_actions(actions, args)


if __name__ == '__main__':
    main()
