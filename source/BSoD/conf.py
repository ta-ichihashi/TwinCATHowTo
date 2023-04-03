# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Beckhoff Automation Japan White Paper'
copyright = '2022, Takashi Ichihashi'
author = 'Takashi Ichihashi'

# docx settings

docx_documents = [
  ('index', 'measurement_to_BSoD_for_IPC.docx', { 'title': 'Countermeasure to BSoD for IPC', 'creator': 'Beckhoff Automation K.K.', 'subject': 'A technical white paper for TwinCAT system', }, True),
]

docx_style = '_templates/beckhoff_document_template.docx'

docx_coverpage = True 
docx_pagebreak_before_section = 1 
docx_pagebreak_after_table_of_contents = 0
docx_table_options = {
  'landscape_columns': 6,      # 
  'in_single_page': True,      #
  'row_splittable': True,      # 
  'header_in_all_page': True,  # 
}

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinxcontrib.blockdiag',
    'sphinxcontrib.seqdiag',
    'sphinxcontrib.actdiag',
    'sphinxcontrib.nwdiag',
    'sphinxcontrib.rackdiag',
    'sphinxcontrib.packetdiag',
    'docxbuilder',
    'sphinx.ext.mathjax'
]

templates_path = ['_templates']
exclude_patterns = []

language = 'ja'
numfig = True

source_suffix = ['.rst', '.md']
source_parsers = {
    '.md': 'recommonmark.parser.CommonMarkParser',
}

exclude_patterns = ['**.ipynb_checkpoints']

# -- Options for HTML output -------------------------------------------------
# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#

#import sphinx_rtd_theme
#html_theme = "sphinx_rtd_theme"
#html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]


html_theme = 'nature'
html_theme_path = ["."]

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# -- Block diag -------------------------------------------------
blockdiag_html_image_format = 'SVG'
seqdiag_html_image_format = 'SVG'
actdiag_html_image_format = 'SVG'
nwdiag_html_image_format = 'SVG'
rackiag_html_image_format = 'SVG'
packetdiag_html_image_format = 'SVG'

blockdiag_latex_image_format = 'PDF'
seqdiag_latex_image_format = 'PDF'
actdiag_latex_image_format = 'PDF'
nwdiag_latex_image_format = 'PDF'
rackiag_latex_image_format = 'PDF'
packetdiag_latex_image_format = 'PDF'

# Fontpath for blockdiag (truetype font)
blockdiag_fontpath = 'c:/windows/fonts/YuGothM.ttc'
actdiag_fontpath = 'c:/windows/fonts/YuGothM.ttc'

#latex_docclass = {'manual': 'jsbook'}

latex_elements = {
    # Latex figure (float) alignment
    #
    'figure_align': 'H',
}


latex_engine = 'lualatex'

# (B) LaTeX�h�L�������g�N���X�Ƃ���ltjsbook���g�p����
latex_docclass = {'manual': 'ltjsbook'}

latex_elements = {
    'polyglossia': '',  #polyglossia��ǂݍ��܂Ȃ� (��ʃG���[�΍�)
    'fontpkg': r'''
        \setmainfont{DejaVu Serif}
        \setsansfont{DejaVu Sans}
        \setmonofont{DejaVu Sans Mono}
        ''',
    'preamble': r'''
        \usepackage[titles]{tocloft}
        \cftsetpnumwidth {1.25cm}\cftsetrmarg{1.5cm}
        \setlength{\cftchapnumwidth}{1.5cm}
        \setlength{\cftsecindent}{\cftchapnumwidth}
        \setlength{\cftsecnumwidth}{1.25cm}
        \addtolength{\footskip}{-3mm}
        ''',
    'fncychap': r'\usepackage[Bjornstrup]{fncychap}',
   'printindex': r'\footnotesize\raggedright\printindex',
    #'preamble': r"""\protected\def\sphinxtablecontinued#1{}"""
}

latex_show_urls = 'footnote'
