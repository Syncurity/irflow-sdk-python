import os
import os.path
import pypandoc
import codecs

# Navigation table appended to the end of every page
_BOTTOM_TABLE = 'Indices and Tables\n'\
                '==================\n\n'\
                '* :ref:`genindex`\n'\
                '* :ref:`modindex`\n'\
                '* :ref:`search`\n'\
                '* :ref:`class`\n'\
                '* :ref:`examples`\n'


def _generate_example_page(title, name, file_in, file_out, lexer):
    """Helper function to generate a page for an individual example file

    Args:
        title (str): The page title
        name (str): The resource name used for linking docs pages
        file_in (str): The file for which to generate a docs page
        file_out (str): The resulting docs page filepath
        lexer (str): The type of lexer to apply to the code-block made from the file_in arg
    """

    file_text = ''
    file_text += '.. _' + name + ':\n\n'
    file_text += title + '\n'
    file_text += '=' * len(title) + '\n\n'
    file_text += '.. toctree::\n'
    file_text += '   :maxdepth: 2\n'
    file_text += '   :caption: Contents:\n\n'

    file_text += '.. code:: ' + lexer + '\n\n'

    try:
        with codecs.open(file_in, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f.readlines():
                file_text += '   ' + line
    except BaseException as e:
        print('Error reading file: ' + file_in + ' - ' + str(e))
        return

    file_text += '\n' + _BOTTOM_TABLE

    print(title + ' documentation page generated')

    try:
        with open(file_out, 'w') as f:
            f.write(file_text)
            print('File: ' + file_out + ' Written successfully')
    except BaseException as e:
        print('Failed to create file: ' + file_out)


def _generate_docs_from_readme(name, file_in):
    """Helper function to generate RST documentation pages from README MD files

    Args:
        name (str): The name to use for the resulting file
        file_in (str): Filepath for the MD file to be converted
        file_out (str): Filepath for the resulting RST to be created
    """
    readme_rst = pypandoc.convert_file(file_in, 'rst', format='md')
    readme_rst = '.. _' + name + ':\n\n' + readme_rst + '\n' + _BOTTOM_TABLE

    with open(name + '.rst', 'w') as f:
        f.write(readme_rst)

    print('Generated README documentation: ' + name)


def _generate_index():
    """Helper function to generate the index page from `main_readme.rst`"""
    with codecs.open('main_readme.rst', 'r', encoding='utf-8', errors='ignore') as f:
        main_readme = f.read()

    index_rst = ''
    index_rst += '.. Syncurity SDK documentation master file, created by\n'
    index_rst += '   sphinx-quickstart on Fri Oct 27 14:18:07 2017.\n\n'

    index_rst += 'Welcome to Syncurity SDK\'s documentation!\n'
    index_rst += '=========================================\n\n'

    index_rst += '.. toctree::\n'
    index_rst += '   :maxdepth: 2\n'
    index_rst += '   :caption: Contents:\n\n'

    index_rst += main_readme

    with open('index.rst', 'w') as f:
        f.write(index_rst)

    print('Generated documentation index')


def generate_docs():
    """Generate documentation pages for all relevant examples and README files"""

    _generate_example_page('Run All API Calls', 'example_01', '../../examples/01_run_all_api_calls.py',
                           'example_01.rst', 'python')
    _generate_example_page('CSV To Alerts', 'example_02', '../../examples/02_csv_to_alerts.py',
                           'example_02.rst', 'python')
    _generate_example_page('API Conf Template', 'example_api_conf', '../../examples/api.conf.template',
                           'example_api_conf.rst', '')

    _generate_docs_from_readme('example_readme', '../../examples/README.md')
    _generate_docs_from_readme('main_readme', '../../README.md')

    _generate_index()
