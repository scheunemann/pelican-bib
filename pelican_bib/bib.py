# -*- coding: utf-8 -*-

"""
Pelican Bib
===========

A Pelican plugin that populates the context with a list of formatted
citations, loaded from a BibTeX file at a configurable path.

The use case for now is to generate a ``Publications'' page for academic
websites.

Configuration
-------------
generator.settings['PUBLICATIONS_SRC']:
    Local path to the BibTeX file to read.
    Each generator contains this list of publications.

generator.settings['PUBLICATIONS_SPLIT_BY']:
    The name of the bibtex field used for splitting the publications.
    No splitting if title is not provided.

generator.settings['PUBLICATIONS_UNTAGGED_TITLE']:
    The title of the header for all untagged entries.
    No such list if title is not provided.

generator.settings['PUBLICATIONS_DECORATE_HTML']:
    If set to True, elements of a publication entry (e.g. names, title)
    will be decorated with a <span> tag with a specific class name

generator.settings['PUBLICATIONS_DEFAULT_TEMPLATE']:
    The name of the template used as default if there is no
    template name argument present in the `bibliography` directive.
    `bibliography` if no value provided.

"""
# Author: Vlad Niculae <vlad@vene.ro>
# Unlicense (see UNLICENSE for details)

import logging
logger = logging.getLogger(__name__)

import os
import re as regex

from pelican import signals
from jinja2 import Template
from docutils.parsers.rst import directives, Directive
from docutils import nodes, utils

from .tagdecorator import *


def generator_init(generator):
    """ Populates context with a list of BibTeX publications.

    generator.settings['PUBLICATIONS_SRC']:
        Local path to the BibTeX file to read.

    Output
    ------
    generator.context['publications_lists']:
        A map with keys retrieved from the field named in PUBLICATIONS_SPLIT_TAG.
        Values are lists of tuples (key, year, text, bibtex, pdf, slides, poster)
        See Readme.md for more details.

    generator.context['publications']:
        Contains all publications as a list of tuples
        (key, year, text, bibtex, pdf, slides, poster).
        See Readme.md for more details.
    """
    if 'PUBLICATIONS_SRC'in generator.settings:
        refs_file = generator.settings['PUBLICATIONS_SRC']
        add_publications_to_context(generator,generator.context,refs_file)


def add_publications_to_context(generator,generator_context,refs_file):
    """ Populates context with a list of BibTeX publications. """
    try:
        from StringIO import StringIO
    except ImportError:
        from io import StringIO
    try:
        from pybtex.database.input.bibtex import Parser
        from pybtex.database.output.bibtex import Writer
        from pybtex.database import BibliographyData, PybtexError
        from pybtex.backends import html
        from pybtex.style.formatting import BaseStyle, plain
    except ImportError:
        logger.warn('`pelican_bib` failed to load dependency `pybtex`')
        return

    decorate_html = generator.settings.get('PUBLICATIONS_DECORATE_HTML', False)

    plugin_path = generator.settings.get('PUBLICATIONS_PLUGIN_PATH', 'plugins')
    import sys
    sys.path.append(plugin_path)

    style = get_style_class(plain.Style,decorate_html)()
    if generator.settings.get('PUBLICATIONS_CUSTOM_STYLE', False):
        try:
            from pybtex_plugins import PelicanStyle
            if not isinstance(PelicanStyle, type) or not issubclass(PelicanStyle, BaseStyle):
                raise TypeError()
            kwargs = generator.settings.get('PUBLICATIONS_STYLE_ARGS', {})
            style = get_style_class(PelicanStyle,decorate_html)(**kwargs)
        except ImportError as e:
            logger.warn(str(e))
            logger.warn('pybtex_plugins.PelicanStyle not found, using Pybtex plain style')
        except TypeError:
            logger.warn('PelicanStyle must be a subclass of pybtex.style.formatting.BaseStyle')


    try:
        bibdata_all = Parser().parse_file(refs_file)
    except PybtexError as e:
        logger.warn('`pelican_bib` failed to parse file %s: %s' % (
            refs_file,
            str(e)))
        return

    publications = []
    publications_lists = {}
    publications_untagged = []

    split_by = generator.settings.get('PUBLICATIONS_SPLIT_BY', None)
    untagged_title = generator.settings.get('PUBLICATIONS_UNTAGGED_TITLE', None)

    # format entries
    html_backend = html.Backend()
    formatted_entries = style.format_entries(bibdata_all.entries.values())

    for formatted_entry in formatted_entries:
        key = formatted_entry.key
        entry = bibdata_all.entries[key]
        year = entry.fields.get('year')
        # This shouldn't really stay in the field dict
        # but new versions of pybtex don't support pop
        pdf = entry.fields.get('pdf', None)
        slides = entry.fields.get('slides', None)
        poster = entry.fields.get('poster', None)

        tags = []
        if split_by:
            tags = entry.fields.get(split_by, [])

            # parse to list, and trim each string
            if tags:

                tags = [tag.strip() for tag in tags.split(',')]

                # create keys in publications_lists if at least one
                # tag is given
                for tag in tags:
                    publications_lists[tag] = publications_lists.get(tag, [])


        #render the bibtex string for the entry
        bib_buf = StringIO()
        bibdata_this = BibliographyData(entries={key: entry})
        Writer().write_stream(bibdata_this, bib_buf)

        # convert decorated html tags
        # `<:bib-xyz>abc</:bib-xyz>` => `<span class="bib-xyz">abc</span>`
        text = formatted_entry.text.render(html_backend)
        text = regex.sub(r'<:([^>]*)>',r'<span class="\1">',text)
        text = regex.sub(r'</:([^>]*)>',r'</span>',text)

        entry_tuple = {'key': key,
                       'year': year,
                       'text': text,
                       'bibtex': bib_buf.getvalue(),
                       'pdf': pdf,
                       'slides': slides,
                       'poster': poster}

        publications.append(entry_tuple)

        for tag in tags:
            publications_lists[tag].append(entry_tuple)

        if not tags and untagged_title:
            publications_untagged.append(entry_tuple)

    # append untagged list if title is given
    if untagged_title and publications_untagged:
        publications_lists[untagged_title] = publications_untagged


    # output
    generator_context['publications'] = publications
    generator_context['publications_lists'] = publications_lists


current_generator = None

class Bibliography(Directive):
    """ 
    Directive to embed bibliographies into articles/posts.

    Usage:
        .. bibliography:: PUBLICATIONS_SRC
        .. bibliography:: PUBLICATIONS_SRC TEMPLATE_NAME
    e.g.
        .. bibliography:: osm.bib
        .. bibliography:: osm.bib publications_by_year

    PUBLICATIONS_SRC
        Local path to the BibTeX file to read
        (required)

    TEMPLATE_NAME
        Name of the template used for rendering the bibliography.
        (optional, default is `bibliography`)
    """
    required_arguments = 1
    optional_arguments = 1
    final_argument_whitespace = False
    has_content = False

    def run(self):

        default_template = current_generator.settings.get('PUBLICATIONS_DEFAULT_TEMPLATE', 'bibliography')

        # get (required) arguments
        refs_file = directives.path(self.arguments[0])
        try:
            template_name = directives.unchanged_required(self.arguments[1])
        except:
            template_name = default_template

        # determine actual absolute path to BibTeX file
        if refs_file.startswith('/') or refs_file.startswith(os.sep):
            # absolute path => relative to Pelican working directory
            refs_file = os.path.join(current_generator.path, refs_file[1:])
        else:
            # relative path => relative to directory of 
            # source file using the directive
            source,line = self.state_machine.get_source_and_line(self.lineno)
            source_dir = os.path.dirname(os.path.abspath(source))
            refs_file = os.path.join(source_dir, refs_file)
        refs_file = nodes.reprunicode(refs_file)
        refs_file = os.path.abspath(refs_file)

        # create a copy of generator context & add publications
        generator_context = current_generator.context.copy()
        add_publications_to_context(current_generator,generator_context,refs_file)

        # find template & generate HTML
        template = current_generator.get_template(template_name)
        html = template.render(generator_context)
        
        node = nodes.raw('', html, format='html')
        return [ node ]


def generator_preread(generator):
    global current_generator
    current_generator = generator


def register():
    signals.generator_init.connect(generator_init)

    signals.article_generator_preread.connect(generator_preread)
    signals.page_generator_preread.connect(generator_preread)
    signals.static_generator_preread.connect(generator_preread)

    directives.register_directive('bibliography', Bibliography)