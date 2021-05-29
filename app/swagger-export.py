import argparse
from converters import *

WORKDIR = '/var/work'

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='swagger-export')
    subparsers = parser.add_subparsers(dest='command', help='application mode')
    subparsers.required = True
    pdf = subparsers.add_parser('pdf', help='')
    pdf_group = pdf.add_mutually_exclusive_group(required=True)
    pdf_group.add_argument('--url')
    pdf_group.add_argument('--file')

    html = subparsers.add_parser('html', help='')
    html_group = html.add_mutually_exclusive_group(required=True)
    html_group.add_argument('--url')
    html_group.add_argument('--file')

    args = parser.parse_args()

    converter = PdfConverter(WORKDIR) if args.command == 'pdf' else HtmlConverter(WORKDIR)
    if args.file:
        converter.convert_from_file(args.file)
    elif args.url:
        converter.convert_from_url(args.url)
