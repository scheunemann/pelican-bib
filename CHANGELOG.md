# Changelog

All notable changes to this project will be documented in this file. This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.3.0] - 2020-04-06

### Added

- Custom `pybtex` styles by [@eginhard](https://github.com/eginhard).
- Add this changelog.

### Changed

- Package description.

### Fixed

- Add `pybtex` to requirements [[@lpirl](https://github.com/lpirl)].
- Fix install explanation.

## [0.2.7] - 2018-12-17

### Added

- A pelican package to organize scientific publications with BibTeX in Pelican. [Pelican-bibtex](https://github.com/vene/pelican-bibtex) and [PR](https://github.com/vene/pelican-bibtex/pull/13) serve as a base for this new package [pelican-bib](https://pypi.org/project/pelican-bib/).
- Sort or group publications by a BibTeX field such as `year`.
- Group publications by categories such as "conferences" or "peer reviewed" from a custom BibTeX field (e.g. `tags`).

[unreleased]: https://github.com/scheunemann/pelican-bib/compare/0.3.0...HEAD
[0.3.0]: https://github.com/scheunemann/pelican-bib/compare/v0.2.7...v0.3.0
[0.2.7]: https://github.com/scheunemann/pelican-bib/releases/tag/0.2.7