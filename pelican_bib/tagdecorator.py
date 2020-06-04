from pybtex.style.template import tag
from pybtex.database import Person

def get_style_class(cls,decorate_html):
    """
    Overrides `format_*` methods and surrounds the result with a
    format-method-specific html tag, e.g 
        `format_names(abc)` will result in `<:bib-names>abc</:bib-names>`
    Attention: These tags need to be updated later, e.g. 
        `<:bib-xyz>abc</:bib-xyz>` => `<span class="bib-xyz">abc</span>`
    """

    if not decorate_html:
        return cls

    class HtmlDecorator(cls):

        def format_names(self, role, as_sentence=True): 
            return tag(':bib-names') [ super().format_names(role, as_sentence) ]

        def format_article(self, e): 
            return tag(':bib-article') [ super()._format_article(e) ]

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

        def format_book(self, e): 
            return tag(':bib-book') [ super().format_book(e) ]

        def format_booklet(self, e): 
            return tag(':bib-booklet') [ super().format_booklet(e) ]

        def format_inbook(self, e): 
            return tag(':bib-inbook') [ super().format_inbook(e) ]

        def format_incollection(self, e): 
            return tag(':bib-incollection') [ super().format_incollection(e) ]

        def format_inproceedings(self, e): 
            return tag(':bib-inproceedings') [ super().format_inproceedings(e) ]

        def format_manual(self, e): 
            return tag(':bib-manual') [ super().format_manual(e) ]

        def format_mastersthesis(self, e): 
            return tag(':bib-mastersthesis') [ super().format_mastersthesis(e) ]

        def format_misc(self, e): 
            return tag(':bib-misc') [ super().format_misc(e) ]

        def format_phdthesis(self, e): 
            return tag(':bib-phdthesis') [ super().format_phdthesis(e) ]

        def format_proceedings(self, e): 
            return tag(':bib-proceedings') [ super().format_proceedings(e) ]

        def format_techreport(self, e): 
            return tag(':bib-techreport') [ super().format_techreport(e) ]

        def format_unpublished(self, e): 
            return tag(':bib-unpublished') [ super().format_unpublished(e) ]

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

    return HtmlDecorator