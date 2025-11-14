# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
from enum import Enum
from sphinx.highlighting import lexers
import sys
import os
sys.path.insert(0, os.path.abspath('.'))
from lexer_iec61131_3 import IecstLexer


lexers['iecst'] = IecstLexer()


class Author(Enum):
    organization: str = 'ベッコフオートメーション株式会社'
    author_native: str = '市橋 卓'
    author_en: str = 'Takashi Ichihashi'

    @classmethod
    def get_strings(cls, delimiter=' '):
        return delimiter.join([e.value for e in cls])


# -- Project information -----------------------------------------------------

titles = ['BECKHOFF TwinCATテクニカルノート']

project = ' '.join(titles)
copyright = '2025, ベッコフオートメーション株式会社'
author = Author.author_native.value

# The full version, including alpha/beta/rc tags
release = '第1版'


# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'myst_parser',
    'japanesesupport',
     # 'docxbuilder',
    'sphinx.ext.githubpages',
    'sphinxcontrib.blockdiag',
    'sphinxcontrib.seqdiag',
    'sphinxcontrib.actdiag',
    'sphinxcontrib.nwdiag',
    'sphinxcontrib.youtube',
    'sphinxcontrib.applehelp'
]

source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

suppress_warnings = ["myst.header"]

docx_template = '_templates/beckhoff_document_template.docx'
exclude_patterns = []

language = 'ja'


# Config for plugins

numfig = True

# Fontpath for blockdiag (truetype font)
# blockdiag_fontpath = 'C:/Windows/fonts/YuGothM.ttc'
# Fontpath for blockdiag (truetype font)
blockdiag_fontpath = './source/assets/ipaexg.ttf'
actdiag_fontpath = './source/assets/ipaexg.ttf'
seqdiag_fontpath = './source/assets/ipaexg.ttf'
nwdiag_fontpath = './source/assets/ipaexg.ttf'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_nefertiti'

html_theme_options = {
    # "sans_serif_font": "Nunito",  # Default value.
    "documentation_font": "Montserrat",
    "documentation_font_size": "1.05rem",
    "doc_headers_font": "Montserrat",
    #"monospace_font": "Red Hat Mono",
    #"monospace_font_size": ".90rem",
    # "project_name_font": "Nunito",  # Default value.
    # "documentation_font_size": "1.0rem",  # Default value.
    # "doc_headers_font": "Georgia",  # Default value.
    # ... other options ...
    "pygments_light_style": "pastie",
    "pygments_dark_style": "dracula",
    "style_header_neutral": True,
    "show_colorset_choices": True,
    "style": "Teal",
    "header_links_in_2nd_row": False,
    "header_links": [
        {
            'text': 'BECKHOFF',
            'link': 'https://www.beckhoff.com/ja-jp/',
        },
        {
            "text": "技術情報",
            "dropdown": (
                {
                    "text": "InfoSys",
                    "link": "https://infosys.beckhoff.com/english.php?content=../content/1033/html/bkinfosys_intro.htm&id=",
                }, {
                    "text": "TwinCAT HowTo",
                    "link": "https://sites.google.com/site/twincathowto/home",
                }, {
                    "text": "YouTube",
                    "link": "https://www.youtube.com/@%E3%83%99%E3%83%83%E3%82%B3%E3%83%95%E3%82%AA%E3%83%BC%E3%83%88%E3%83%A1%E3%83%BC%E3%82%B7%E3%83%A7%E3%83%B3%E6%A0%AA%E5%BC%8F%E4%BC%9A%E7%A4%BE",
                }
            )
        }
    ],
    "repository_url": "https://github.com/Beckhoff-JP/TwinCATHowTo",
    "repository_name": "Beckhoff-JP/TwinCATHowTo"
}
'''
html_sidebars = {
    "**": [
        "search-field.html",
        "sbt-sidebar-nav.html"
        ]
}

html_theme_options = {
    "repository_url": "https://github.com/Beckhoff-JP/TwinCATHowTo",
    "use_repository_button": True,
    "home_page_in_toc": True,
}

'''

myst_enable_extensions = [
    "amsmath",
    "attrs_image",
    "colon_fence",
    "deflist",
    "dollarmath",
    "amsmath",
    "fieldlist",
    "html_admonition",
    "html_image",
    # "inv_link",
    # "linkify",
    "replacements",
    "smartquotes",
    "strikethrough",
    "substitution",
    "tasklist",
]

docx_documents = [
    ('index', 'BeckhoffTechnologyDocuments.docx', {'title': 'Beckhoff Technology documents',
     'creator': 'Beckhoff Automation K.K.', 'subject': 'A technical documents for TwinCAT system', }, True),
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


# latex_docclass = {'manual': 'jsbook'}

latex_elements = {
    # Latex figure (float) alignment
    #
    'figure_align': 'H',
    'sphinxsetup': "verbatimforcewraps, verbatimmaxunderfull=0"
}


latex_engine = 'lualatex'

latex_docclass = {'manual': 'ltjsbook'}

# 改行コマンド `\\` を挟んで連結する(A)
my_latex_title_lines = '\\\\'.join(titles)

latex_elements = {
    # (C) Polyglossiaパッケージを読み込まないようにする
    'polyglossia': '',
    'fontpkg': r'''
        \setmainfont{DejaVu Serif}
        \setsansfont{DejaVu Sans}
        \setmonofont{DejaVu Sans Mono}
        ''',
    'preamble': r'''

        % my_latex_title_linesをLaTeXの世界に持ち込む
        \newcommand{\mylatextitlelines}{''' + my_latex_title_lines + r'''}
        \newcommand{\mylatexauthorlines}{''' + Author.get_strings('\\\\') + r'''}

        % 表紙テンプレート内でアットマークが使われているため、アットマークを通常の文字として扱う
        \makeatletter

        % 表紙テンプレートを再定義(B)
        \renewcommand{\sphinxmaketitle}{%
            \let\sphinxrestorepageanchorsetting\relax
            \ifHy@pageanchor\def\sphinxrestorepageanchorsetting{\Hy@pageanchortrue}\fi
            \hypersetup{pageanchor=false}% avoid duplicate destination warnings
            \begin{titlepage}%
                \let\footnotesize\small
                \let\footnoterule\relax
                \noindent\rule{\textwidth}{1pt}\par
                \begingroup % for PDF information dictionary
                \def\endgraf{ }\def\and{\& }%
                \pdfstringdefDisableCommands{\def\\{, }}% overwrite hyperref setup
                \hypersetup{pdfauthor={\@author}, pdftitle={\@title}}%
                \endgroup
                \begin{flushright}%
                \sphinxlogo
                \py@HeaderFamily
                {\Huge \mylatextitlelines \par} % <--- ここで\mylatextitlelinesを使用(C)
                {\itshape\LARGE \py@release\releaseinfo \par}
                \vfill
                {\LARGE
                    \begin{tabular}[t]{l}
                    \mylatexauthorlines
                    %\@author
                    \end{tabular}\kern-\tabcolsep
                    \par}
                \vfill\vfill
                {\large
                \@date \par
                \vfill
                \py@authoraddress \par
                }%
                \end{flushright}%\par
                \@thanks
            \end{titlepage}%
            \setcounter{footnote}{0}%
            \let\thanks\relax\let\maketitle\relax
            %\gdef\@thanks{}\gdef\@author{}\gdef\@title{}
            \clearpage
            \ifdefined\sphinxbackoftitlepage\sphinxbackoftitlepage\fi
            \if@openright\cleardoublepage\else\clearpage\fi
            \sphinxrestorepageanchorsetting
        } % 表紙スタイル終わり
        % アットマークを特殊文字に戻す
        \makeatother

        \setcounter{tocdepth}{1}
        \usepackage[titles]{tocloft}
        %\usepackage[OT1]{fontenc}
        \cftsetpnumwidth {1.25cm}\cftsetrmarg{1.5cm}
        \setlength{\cftchapnumwidth}{1.5cm}
        \setlength{\cftsecindent}{\cftchapnumwidth}
        \setlength{\cftsecnumwidth}{1.25cm}
        \addtolength{\footskip}{0mm}
        ''',
    'fncychap': r'\usepackage[Bjornstrup]{fncychap}',
    'printindex': r'\footnotesize\raggedright\printindex'
}


latex_show_urls = 'footnote'


# for epub


epub_title = project
epub_author = author
epub_basename = 'twincat_howto'
epub_language = 'ja'
epub_publisher = author
# epub_identifier = u'http://ascii.asciimw.jp/books/books/detail/978-4-04-868629-7.shtml'
epub_scheme = 'URL'
epub_tocdepth = 3
