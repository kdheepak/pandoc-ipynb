#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Convert notebooks to markdown to use with pelican
"""

from __future__ import print_function

import os
import sys
from pandocfilters import toJSONFilter, Str, Para, Div
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

    if key == 'Div':
        sys.stderr.write("key = "+str(key)+"\t")
        sys.stderr.write("value = "+str(type(value))+"\t")
        sys.stderr.write(unicode(value).encode('ascii', 'ignore')+'\n')

    if key == 'Para' and value[0]['c'][0:2] == '{%' and value[0]['c'][-2:] == '%}':
        sys.stderr.write("Inside notebook convert\n")
        return Div([u'notebook', [u'border-box-sizing'], [[u'tabindex', u'-1']]],
[{u'c': [[u'notebook-container', [u'container'], []], [{u'c': [[u'', [u'cell', u'border-box-sizing', u'text_cell', u'rendered'], []], [{u'c': [[u'', [u'prompt', u'input_prompt'], []], []], u't': u'Div'}, {u'c': [[u'', [u'inner_cell'], []], [{u'c': [[u'', [u'text_cell_render', u'border-box-sizing', u'rendered_html'], []], [{u'c': [1, [u'Notebook', [], []], [{u'c': u'Notebook', u't': u'Str'}, {u'c': [[{u'c': u'\xb6', u't': u'Str'}], [u'#Notebook', u'']], u't': u'Link'}]], u't': u'Header'}]], u't': u'Div'}]], u't': u'Div'}]], u't': u'Div'}, {u'c': [[u'', [u'cell', u'border-box-sizing', u'code_cell', u'rendered'], []], [{u'c': [[u'', [u'input'], []], [{u'c': [[u'', [u'prompt', u'input_prompt'], []], [{u'c': [{u'c': u'In\xa0[2]:', u't': u'Str'}], u't': u'Plain'}]], u't': u'Div'}, {u'c': [[u'', [u'inner_cell'], []], [{u'c': [[u'', [u'input_area'], []], [{u'c': [[u'', [u'highlight', u'hl-ipython2'], []], [{u'c': [[u'', [], []], u"print('Hello')"], u't': u'CodeBlock'}]], u't': u'Div'}]], u't': u'Div'}]], u't': u'Div'}]], u't': u'Div'}, {u'c': [[u'', [u'output_wrapper'], []], [{u'c': [[u'', [u'output'], []], [{u'c': [[u'', [u'output_area'], []], [{u'c': [[u'', [u'prompt'], []], []], u't': u'Div'}, {u'c': [[u'', [u'output_subarea', u'output_stream', u'output_stdout', u'output_text'], []], [{u'c': [[u'', [], []], u'Hello'], u't': u'CodeBlock'}]], u't': u'Div'}]], u't': u'Div'}]], u't': u'Div'}]], u't': u'Div'}]], u't': u'Div'}, {u'c': [[u'', [u'cell', u'border-box-sizing', u'text_cell', u'rendered'], []], [{u'c': [[u'', [u'prompt', u'input_prompt'], []], []], u't': u'Div'}, {u'c': [[u'', [u'inner_cell'], []], [{u'c': [[u'', [u'text_cell_render', u'border-box-sizing', u'rendered_html'], []], [{u'c': [{u'c': u'Testing', u't': u'Str'}, {u'c': [], u't': u'Space'}, {u'c': u'markdown', u't': u'Str'}, {u'c': [], u't': u'Space'}, {u'c': u'cell', u't': u'Str'}], u't': u'Para'}]], u't': u'Div'}]], u't': u'Div'}]], u't': u'Div'}]], u't': u'Div'}]
)
        # return Str("Hello")
    
if __name__ == "__main__":
    toJSONFilter(notebook_convert)

