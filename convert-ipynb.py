#!/usr/bin/env python
from __future__ import print_function

import os
import sys
from pandocfilters import toJSONFilter, Str, Para
import subprocess
from subprocess import check_output
from subprocess import Popen, PIPE
import errno
import nbconvert
from traitlets.config import Config
from nbconvert.exporters import HTMLExporter
try:
    from nbconvert.filters.highlight import _pygments_highlight
except ImportError:
    try:
        from IPython.nbconvert.filters.highlight import _pygments_highlight
    except ImportError:
        # IPython < 2.0
        from IPython.nbconvert.filters.highlight import _pygment_highlight as _pygments_highlight


#----------------------------------------------------------------------
# Custom highlighter:
#  instead of using class='highlight', use class='highlight-ipynb'
def custom_highlighter(source, language='ipython', metadata=None):
    formatter = HtmlFormatter(cssclass='highlight-ipynb')
    if not language:
        language = 'ipython'
    output = _pygments_highlight(source, formatter, language)
    return output.replace('<pre>', '<pre class="ipynb">')


def convert_notebook_to_content(file_name):
    # subprocess.call(["jupyter", "nbconvert", "--to", "markdown", file_name]) 

    # Create the custom notebook converter
    # Convert ipython notebook to html
    config = Config({'CSSHTMLHeaderTransformer': {'enabled': True,
                     'highlight_class': '.highlight-ipynb'}})

    template_file = 'basic'
    if os.path.exists('pelicanhtml_3.tpl'):
        template_file = 'pelicanhtml_3'
    exporter = HTMLExporter(config=config,
                            template_file=template_file,
                            filters={'highlight2html': custom_highlighter},)
    content, info = exporter.from_filename(file_name)
    # return(content.encode('utf-8').strip())
    return(content)

    # nbn = nbconvert.notebook.nbformat.read(file_name, nbconvert.notebook.nbformat.NO_CONVERT)

def write_to_file(content, file_name):
    with open(file_name.replace('ipynb', 'html'), "wb") as f:
       f.write(content.encode('utf-8').strip())

def convert_markdown_to_para(file_name):
    # e.g. file_name is ipython-notebook.ipynb.
    # ipython-notebook.ipynb -> AST
    return(file_name)

def convert_file_name_to_ast(file_name):
    # e.g. file_name is ipython-notebook.ipynb.
    # ipython-notebook.ipynb -> AST

    out = check_output(["pandoc", "-t", "json"])
    return(out)

def convert_notebook_to_para(file_name):
    content = convert_notebook_to_content(file_name)
    write_to_file(content, file_name)
    para = convert_file_name_to_ast(content)
    para = convert_markdown_to_para(file_name)
    return(para)

def notebook_convert(key, value, format, meta):
    if key == 'Para':
        sys.stderr.write("Printing Para " + str(value) + "\n")
        string_value = value[0]['c']
        if string_value[0:2] == "{%" and string_value[-2:] == "%}" and '.ipynb' in string_value:
            sys.stderr.write("Found a notebook!\n")
            file_name = string_value[2:-2]
            value[0]['c'] = convert_notebook_to_para(file_name)
        return Para(value)

if __name__ == "__main__":
    toJSONFilter(notebook_convert)

