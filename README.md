# Pelican Bib

Organize your scientific publications with BibTeX in Pelican. The package is based on Vlad's [pelican-bibtex](https://github.com/vene/pelican-bibtex). The current version is backward compatible and can replace the `pelican-bibtex` install of your current project.

## Installation

`pelican_bib` requires `pybtex`.

    pip install pybtex

You can either install Pelican Bib using _pip_ or as a _submodule_:

### Using pip

    pip install pelican-bib

Add the plugin to the `PLUGINS` variable (in your Pelican config, e.g. `pelicanconf.py`):

    PLUGINS = ['pelican_bib', ...]

### As a Submodule

In your Pelican site:

    $ mkdir plugins
    $ git submodule add https://github.com/scheunemann/pelican-bib plugins/pelican-bib

Register the plugin folder and add the plugin to the `PLUGINS` variable (in your Pelican config, e.g. `pelicanconf.py`):

    PLUGIN_PATHS = ['plugins/pelican-bib', ...]
    PLUGINS = ['pelican_bib', ...]
    
## How to Use

This plugin reads a user-specified BibTeX file and populates the context with
a list of publications, ready to be used in your Jinja2 template.

Configuration is simply:

    PUBLICATIONS_SRC = 'content/pubs.bib'


If the file is present and readable, you will be able to find the `publications`
variable in all templates.  It is a list of dictionaries with the following keys:

1. `key` is the BibTeX key (identifier) of the entry.
2. `year` is the year when the entry was published.  Useful for grouping by year in templates using Jinja's `groupby`
3. `text` is the HTML formatted entry, generated by `pybtex`.
4. `bibtex` is a string containing BibTeX code for the entry, useful to make it
available to people who want to cite your work.
5. `pdf`, `slides`, `poster`: in your BibTeX file, you can add these special fields,
for example:

    ```
    @article{
       foo13
       ...
       pdf = {/papers/foo13.pdf},
       slides = {/slides/foo13.html}
    }
    ```


This plugin will take all defined fields and make them available in the template.
If a field is not defined, the tuple field will be `None`.  Furthermore, the
fields are stripped from the generated BibTeX (found in the `bibtex` field).

### Split into lists of publications

You can add an extra field to each bibtex entry. This value of that field is a comma seperated list.
These values will become the keys of a list `publications_lists` containing the associated bibtex entries in your template.

For example, if you want to associate an entry with two different tags (`foo-tag`, `bar-tag`), 
you add the following field to the bib entry:


    @article{
       foo13
       ...
       tags = {foo-tag, bar-tag}
    }


In your `pelicanconf.py` you'll need to set:

    PUBLICATIONS_SPLIT_BY = 'tags'


In your template you can then access these lists with the variables `publications_lists['foo-tag']` and `publications_lists['bar-tag']`.

If you want to assign all untagged entries (i.e. entries without 
the field defined in `PUBLICATIONS_SPLIT_BY`) to a tag named `others`, set: 

    PUBLICATIONS_UNTAGGED_TITLE = 'others'

### Styling generated entries with CSS

If you set the configuration variable `PUBLICATIONS_DECORATE_HTML` to `true`, the parts of a HTML formatted entry generated by `pybtex` (e.g. title, author list, volume & series) will be surrounded by `span` tags with a corresponding `class` attribute.

    PUBLICATIONS_DECORATE_HTML = True

Available parts / CSS classes are (according to the `format_*` function names of `pybtex.style.formatting.unsrt`): 
_bib-names_, 
_bib-article_, 
_bib-author_or_editor_, 
_bib-editor_, 
_bib-volume_and_series_, 
_bib-chapter_and_pages_, 
_bib-edition_, 
_bib-title_, 
_bib-btitle_, 
_bib-address_organization_publisher_date_, 
_bib-book_, 
_bib-booklet_, 
_bib-inbook_, 
_bib-incollection_, 
_bib-inproceedings_, 
_bib-manual_, 
_bib-mastersthesis_, 
_bib-misc_, 
_bib-phdthesis_, 
_bib-proceedings_, 
_bib-techreport_, 
_bib-unpublished_, 
_bib-web_refs_, 
_bib-url_, 
_bib-pubmed_, 
_bib-doi_, 
_bib-eprint_.

### Custom pybtex styles

By default, the `pybtex.style.formatting.plain` style is applied to the list
of publications, but it is also possible to supply custom pybtex styles. Here
is a simple example that will highlight the name of the website's author. Add
the following to your Pelican config:

```python
PUBLICATIONS_CUSTOM_STYLE = True
PUBLICATIONS_STYLE_ARGS = {'site_author': AUTHOR}
```

Then create the file `plugins/pybtex_plugins.py` with the following content:

```python
from pybtex.database import Person
from pybtex.style.formatting import unsrt
from pybtex.style.template import tag

class PelicanStyle(unsrt.Style):

    def __init__(self, site_author='', **kwargs):
        super().__init__(**kwargs)
        self.site_author = Person(site_author)

        # Allows to apply special formatting to a specific author.
        def format(person, abbr=False):
            if person == self.site_author:
                return tag('strong') [ self.name_style.format(person, abbr) ]
            else:
                return self.name_style.format(person, abbr)

        self.format_name = format
```

`PelicanStyle` must be a subclass of `pybtex.style.formatting.BaseStyle`. An
alternative path to the `pybtex_plugins.py` file can be provided via
`PUBLICATIONS_PLUGIN_PATH` in the Pelican config.

## Page with a list of publications

To generate a page displaying the publications with one of the methods below, you need to add a template file and a page.

1.) place the template file as `publications.html` in `content/templates` and add it as direct template to your webpage. Add in your `pelicanconf.py`:


    THEME_TEMPLATES_OVERRIDES.append('templates')


2.) Create a page in your page folder, e.g., 'content/pages/publications.rst' with the following metadata in your content:


    Publications
    ############
    
    :template: publications



## Example templates

Example content of the `publications.html` template:

    {% extends "base.html" %}
    {% block title %}Publications{% endblock %}
    {% block content %}
    
    <script type="text/javascript">
        function disp(s) {
            var win;
            var doc;
            win = window.open("", "WINDOWID");
            doc = win.document;
            doc.open("text/plain");
            doc.write("<pre>" + s + "</pre>");
            doc.close();
        }
    </script>
    <section id="content" class="body">
        <h1 class="entry-title">Publications</h1>
        <ul>
            {% for publication in publications %}
              <li id="{{ publication.key }}">{{ publication.text }}
              [&nbsp;<a href="javascript:disp('{{ publication.bibtex|replace('\n', '\\n')|escape|forceescape }}');">Bibtex</a>&nbsp;]
              {% for label, target in [('PDF', publication.pdf), ('Slides', publication.slides), ('Poster', publication.poster)] %}
                {{ "[&nbsp;<a href=\"%s\">%s</a>&nbsp;]" % (target, label) if target }}
              {% endfor %}
              </li>
            {% endfor %}
        </ul>
    </section>
    {% endblock %}

_(Note: that we are escaping the BibTeX string twice in order to properly display it. 
This can be achieved using `forceescape`)_

### Sorting entries

The entries can be sorted by one of the attributes, for example, if you want to sort the entries by date, your unordered list would look like the following:


    ...
        <ul>
            {% for publication in publications|sort(True, attribute='year') %}
              <li id="{{ publication.key }}">{{ publication.text }}
              [&nbsp;<a href="javascript:disp('{{ publication.bibtex|replace('\n', '\\n')|escape|forceescape }}');">Bibtex</a>&nbsp;]
              {% for label, target in [('PDF', publication.pdf), ('Slides', publication.slides), ('Poster', publication.poster)] %}
                {{ "[&nbsp;<a href=\"%s\">%s</a>&nbsp;]" % (target, label) if target }}
              {% endfor %}
              </li>
            {% endfor %}
        </ul>
    ...


The [sort builtin filter](http://jinja.pocoo.org/docs/2.10/templates/#sort) was added in version 2.6 of jinja2. 

### Grouping entries

To group entries by year,


    ...
    <ul>
      {% for grouper, publist in publications|groupby('year')|reverse %}
      <li> {{grouper}}
        <ul>
        {% for publication in publist %}
          <li id="{{ publication.key }}">{{ publication.text }}
          [&nbsp;<a href="javascript:disp('{{ publication.bibtex|replace('\n', '\\n')|escape|forceescape }}');">Bibtex</a>&nbsp;]
          {% for label, target in [('PDF', publication.pdf), ('Slides', publication.slides), ('Poster', publication.poster)] %}
            {{ "[&nbsp;<a href=\"%s\">%s</a>&nbsp;]" % (target, label) if target }}
          {% endfor %}
          </li>
        {% endfor %}
        </ul></li>
      {% endfor %}
    </ul>
    ...


### Using lists of publications

As described above, lists of publications are stored in `publications_lists`.
You can replace `publications` from the previous example with `publications_lists['foo-tag']` to only show the publications with tagged with `foo-tag`. 

You can also iterate over the map and present all bib entries of each list.
The section of the previous example changes to:

    ...
    <section id="content" class="body">
        <h1 class="entry-title">Publications</h1>
        {% for tag in publications_lists %}
            {% if publications_lists|length > 1 %}
                <h2>{{tag}}</h2>
            {% endif %}
    	       <ul>
    	       {% for publication  in  publications_lists[tag] %}
                <li id="{{ publication.bibkey }}">{{ publication.text }}
                [&nbsp;<a href="javascript:disp('{{ publication.bibtex|replace('\n', '\\n')|escape|forceescape }}');">Bibtex</a>&nbsp;]
                {% for label, target in [('PDF', publication.pdf), ('Slides', publication.slides), ('Poster', publication.poster)] %}
                    {{ "[&nbsp;<a href=\"%s\">%s</a>&nbsp;]" % (target, label) if target }}
                {% endfor %}
                </li>
    	       {% endfor %}
    	       </ul>
    	   {% endfor %}
    </section>
    ...
