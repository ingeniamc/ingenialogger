# Changelog

## [Unreleased]
### Added
- configure_file_handler and configure_queue_handler
- clean_ingenia_handlers

### Changed
- Now, configure_logger just configure the StreamHandler

## [0.2.1] - 2021-06-15
### Added
- Python 3.6 and newer compatibility

## [0.2.0] - 2021-05-05
### Added
- Add default values for custom_fields in get_logger function
- Add pytest
- Add category custom field
- Add PUBLIC_FAULT log level

### Changed
- Changed configure_logger method to configure the logger only once, handlers are not duplicated
- Changed USER log levels to PUBLIC

## [0.1.0] - 2021-03-29
### Added
- First version
