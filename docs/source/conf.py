# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/stable/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#

# -- Project information -----------------------------------------------------

project = "torchfilter"
copyright = "2020"
author = "brentyi"

# The short X.Y version
version = ""
# The full version, including alpha/beta/rc tags
release = ""


# -- General configuration ---------------------------------------------------

napoleon_numpy_docstring = False  # Force consistency, leave only Google
napoleon_use_rtype = False  # More legible

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "sphinx.ext.mathjax",
    "sphinx.ext.githubpages",
    "sphinx.ext.napoleon",
    "sphinx.ext.inheritance_diagram",
    "autoapi.extension",
    "sphinx_math_dollar",
    "sphinx.ext.viewcode",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = ".rst"

# The master toctree document.
master_doc = "index"

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path .
exclude_patterns = []

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"


# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
# html_theme_options = {}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
#
# html_sidebars = {}


# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = "torchfilter_doc"


# -- Options for Github output ------------------------------------------------

sphinx_to_github = True
sphinx_to_github_verbose = True
sphinx_to_github_encoding = "utf-8"


# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',
    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',
    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',
    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (
        master_doc,
        "torchfilter.tex",
        "torchfilter documentation",
        "brentyi",
        "manual",
    ),
]


# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [(master_doc, "torchfilter", "torchfilter documentation", [author], 1)]


# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (
        master_doc,
        "torchfilter",
        "torchfilter documentation",
        author,
        "torchfilter",
        "torchfilter documentation",
        "Miscellaneous",
    ),
]


# -- Extension configuration --------------------------------------------------

# -- Options for autoapi extension --------------------------------------------
autoapi_dirs = ["../../torchfilter"]
autoapi_root = "api"
autoapi_options = [
    "members",
    "undoc-members",
    "imported-members",
    "show-inheritance",
    "show-inheritance-diagram",
    "special-members",
    "show-module-summary",
]
autoapi_add_toctree_entry = False

# Generate inheritance aliases
def _gen_inheritance_alias():
    inheritance_alias = {}

    def recurse(module, prefixes):
        if hasattr(module, "__name__") and module.__name__.startswith("torchfilter"):
            MAX_DEPTH = 5
            if len(prefixes) > MAX_DEPTH:
                # Prevent infinite loops from cyclic imports
                return
        else:
            return

        for member_name in dir(module):
            if member_name == "torchfilter":
                continue

            member = getattr(module, member_name)
            if callable(member):
                full_name = ".".join(["torchfilter"] + prefixes + [member_name])

                shortened_name = "torchfilter"
                current = torchfilter
                success = True
                for p in prefixes + [member_name]:
                    if p.startswith("_"):
                        continue
                    if not hasattr(current, p):
                        success = False
                        break
                    current = getattr(current, p)
                    shortened_name += "." + p

                if success and shortened_name != full_name:
                    if full_name in inheritance_alias:
                        assert full_name == inheritance_alias[shortened_name], full_name
                    else:
                        inheritance_alias[full_name] = shortened_name
            elif not member_name.startswith("__"):
                recurse(member, prefixes + [member_name])

    import torchfilter

    recurse(torchfilter, prefixes=[])
    return inheritance_alias


# Set inheritance_alias setting for inheritance diagrams
inheritance_alias = _gen_inheritance_alias()
inheritance_alias["torch.nn.modules.module.Module"] = "torch.nn.Module"

# Apply our inheritance alias to autoapi base classes
def _override_class_documenter():
    import autoapi

    orig_init = autoapi.mappers.python.PythonClass.__init__

    def __init__(self, obj, **kwargs):
        bases = obj["bases"]
        for i, base in enumerate(bases):
            if base in inheritance_alias:
                bases[i] = inheritance_alias[base]
                print(bases[i])
        orig_init(self, obj, **kwargs)

    autoapi.mappers.python.PythonClass.__init__ = __init__


_override_class_documenter()

# -- Options for todo extension ----------------------------------------------

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True

# -- Enable Markdown -> RST conversion ----------------------------------------

import m2r


def docstring(app, what, name, obj, options, lines):
    md = "\n".join(lines)
    rst = m2r.convert(md)
    lines.clear()
    lines += rst.splitlines()


def setup(app):
    app.connect("autodoc-process-docstring", docstring)
