import os
import os.path
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


def generate_example_docs():
    """Generate documentation pages for all relevant examples except README files"""

    _generate_example_page('Run All API Calls', 'example_01', '../../examples/01_run_all_api_calls.py',
                           'example_01.rst', 'python')
    _generate_example_page('CSV To Alerts', 'example_02', '../../examples/02_csv_to_alerts.py',
                           'example_02.rst', 'python')
    _generate_example_page('API Conf Template', 'example_api_conf', '../../examples/api.conf.template',
                           'example_api_conf.rst', '')
