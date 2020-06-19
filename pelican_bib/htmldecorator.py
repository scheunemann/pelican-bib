from pybtex.style.template import tag
from pybtex.database import Person

def get_style_type(cls,decorate_html):
    """
    Overrides `format_*` and `get_*_template` methods and surrounds the result 
    with a format-method-specific html tag, e.g 
        `format_names(abc)` will result in `<:bib-names>abc</:bib-names>`
    Attention: These tags need to be updated later, e.g. 
        `<:bib-xyz>abc</:bib-xyz>` => `<span class="bib-xyz">abc</span>`
    """

    if not decorate_html:
        return cls

    class HtmlDecorator(cls):

        def format_names(self, role, as_sentence=True):
            return tag(':bib-names') [ super().format_names(role, as_sentence) ]

        def get_article_template(self, e):
            return tag(':bib-article') [ super().get_article_template(e) ]

        def format_author_or_editor(self, e):
            return tag(':bib-author_or_editor') [ super().format_author_or_editor(e) ]

        def format_editor(self, e, as_sentence=True):
            return tag(':bib-editor') [ super().format_editor(e, as_sentence) ]

        def format_volume_and_series(self, e, as_sentence=True):
            return tag(':bib-volume_and_series') [ super().format_volume_and_series(e, as_sentence) ]

        def format_chapter_and_pages(self, e):
            return tag(':bib-chapter_and_pages') [ super().format_chapter_and_pages(e) ]

        def format_edition(self, e):
            return tag(':bib-edition') [ super().format_edition(e) ]

        def format_title(self, e, which_field, as_sentence=True):
            return tag(':bib-title') [ super().format_title(e, which_field, as_sentence) ]

        def format_btitle(self, e, which_field, as_sentence=True):
            return tag(':bib-btitle') [ super().format_btitle(e, which_field, as_sentence) ]

        def format_address_organization_publisher_date(self, e, include_organization=True):
            return tag(':bib-address_organization_publisher_date') [ super().format_address_organization_publisher_date(e, include_organization) ]

        def get_book_template(self, e):
            return tag(':bib-book') [ super().get_book_template(e) ]

        def get_booklet_template(self, e):
            return tag(':bib-booklet') [ super().get_booklet_template(e) ]

        def get_inbook_template(self, e):
            return tag(':bib-inbook') [ super().get_inbook_template(e) ]

        def get_incollection_template(self, e):
            return tag(':bib-incollection') [ super().get_incollection_template(e) ]

        def get_inproceedings_template(self, e):
            return tag(':bib-inproceedings') [ super().get_inproceedings_template(e) ]

        def get_manual_template(self, e):
            return tag(':bib-manual') [ super().get_manual_template(e) ]

        def get_mastersthesis_template(self, e):
            return tag(':bib-mastersthesis') [ super().get_mastersthesis_template(e) ]

        def get_misc_template(self, e):
            return tag(':bib-misc') [ super().get_misc_template(e) ]

        def get_phdthesis_template(self, e):
            return tag(':bib-phdthesis') [ super().get_phdthesis_template(e) ]

        def get_proceedings_template(self, e):
            return tag(':bib-proceedings') [ super().get_proceedings_template(e) ]

        def get_techreport_template(self, e):
            return tag(':bib-techreport') [ super().get_techreport_template(e) ]

        def get_unpublished_template(self, e):
            return tag(':bib-unpublished') [ super().get_unpublished_template(e) ]

        def format_web_refs(self, e):
            return tag(':bib-web_refs') [ super().format_web_refs(e) ]

        def format_url(self, e):
            return tag(':bib-url') [ super().format_url(e) ]

        def format_pubmed(self, e):
            return tag(':bib-pubmed') [ super().format_pubmed(e) ]

        def format_doi(self, e):
            return tag(':bib-doi') [ super().format_doi(e) ]

        def format_eprint(self, e):
            return tag(':bib-eprint') [ super().format_eprint(e) ]

        def format_isbn(self, e):
            return tag(':bib-isbn') [ super().format_isbn(e) ]

    return HtmlDecorator