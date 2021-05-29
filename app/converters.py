from abc import ABC, abstractmethod
import os
import ssl
import tempfile
import urllib.request


ssl._create_default_https_context = ssl._create_unverified_context


class IConverter(ABC):
    @abstractmethod
    def convert_from_url(self, url):
        raise NotImplementedError

    @abstractmethod
    def convert_from_file(self, file):
        raise NotImplementedError


class HtmlConverter(IConverter):
    def __init__(self, work_dir):
        self.work_dir = work_dir

    def convert_from_url(self, url):
        with tempfile.TemporaryDirectory() as tmp:
            definition_file = os.path.join(tmp, 'swagger.json')
            urllib.request.urlretrieve(url, definition_file)
            self.convert_from_file(definition_file)

    def convert_from_file(self, file):
        input_file = os.path.join(self.work_dir, file) if not os.path.isabs(file) else file
        output_dir = os.path.join(self.work_dir, 'html')
        os.system('java -jar swagger-codegen-cli.jar generate -i {} -l html2 -o {}'.format(input_file, output_dir))


class PdfConverter(IConverter):
    asciidocs = ('overview', 'security', 'paths', 'definitions')

    def __init__(self, work_dir):
        self.work_dir = work_dir

    def convert_from_url(self, url):
        with tempfile.TemporaryDirectory() as tmp:
            definition_file = os.path.join(tmp, 'swagger.json')
            urllib.request.urlretrieve(url, definition_file)
            self.convert_from_file(definition_file)

    def convert_from_file(self, file):
        input_file = os.path.join(self.work_dir, file) if not os.path.isabs(file) else file
        output_file = os.path.join(self.work_dir, 'output.pdf')
        with tempfile.TemporaryDirectory() as tmp:
            self.__generate_asciidoc(input_file, tmp)
            self.__generate_pdf(tmp, output_file)

    def __generate_asciidoc(self, input_file, output_dir):
        os.system('java -jar swagger2markup-cli.jar convert -i {} -d {}'.format(input_file, output_dir))

    def __generate_pdf(self, work_dir, output_file):
        expected_ascii_docs = list(os.path.join(work_dir, name + '.adoc') for name in self.asciidocs)
        expected_ascii_docs = list(file for file in expected_ascii_docs if os.path.exists(file))
        os.system('asciidoctor-pdf {}'.format(' '.join(expected_ascii_docs)))

        expected_pdf_files = (os.path.join(work_dir, name + '.pdf') for name in self.asciidocs)
        expected_pdf_files = list(file for file in expected_pdf_files if os.path.exists(file))
        os.system('pdftk {} cat output {}'.format(' '.join(expected_pdf_files), output_file))
