import pytest

from ingenialogger import get_logger


def generate_fields_text(custom_fields):
    if custom_fields == {}:
        return ""
    else:
        fields_order = ["axis", "drive", "category", "code_error"]
        fields_str = '({}) '.format(
            ", ".join(['{}="{}"'.format(key, custom_fields[key]) for key in fields_order if key in custom_fields])
        )
        return fields_str


@pytest.mark.parametrize("custom_fields, message",
                         [
                             ({"axis": 1, "drive": "my_drive", "code_error": "0x3"}, "Hello"),
                             ({"axis": 3}, "Bye"),
                             ({"drive": "my_drive", "code_error": "An error"}, "Message with spaces"),
                             ({"axis": 0, "code_error": "0"}, "Enter de Gungeon"),
                             ({}, "Empty"),
                             ({"code_error": "0x3", "drive": "my_drive", "axis": 1}, "olleH"),
                             ({"category": "Generic", "drive": "my_drive", "axis": 1}, "Hi")
                         ])
def test_get_logger_single_logger(caplog, custom_fields, message):
    logger = get_logger("test", **custom_fields)
    logger.warning(message)
    fields_str = generate_fields_text(custom_fields)
    for record in caplog.records:
        assert record.msg == '{}{}'.format(fields_str, message)


@pytest.mark.parametrize("loggers_name, custom_fields, messages",
                         [
                             (["logger 1", "logger 2"],
                              [{"axis": 1, "drive": "my_drive", "code_error": "0x3"}, {"axis": 3}],
                              ["mes", "sage"]),
                             (["logger 1", "logger 2", "log3"],
                              [{"axis": 1, "drive": "my_drive", "code_error": "0x3"}, {"axis": 3}, {}],
                              ["mes", "sage", "any"]),
                             (["name", "same name", "same name"],
                              [{"axis": 1, "drive": "my_drive", "code_error": "0x3"}, {"axis": 3}, {}],
                              ["mes", "sage", "any"]),
                             (["3", "2", "1"],
                              [{}, {"axis": 1, "drive": "my_drive", "code_error": "0x3"}, {"axis": 3}],
                              ["empty", "message with spaces", 'message with ( )) and " ```++´´ "']),
                         ])
def test_get_logger_multiple_logger(caplog, loggers_name, custom_fields, messages):
    loggers = [get_logger(name, **custom_fields[index]) for index, name in enumerate(loggers_name)]
    for index, msg in enumerate(messages):
        loggers[index].warning(msg)
    fields_str = [generate_fields_text(c_f) for c_f in custom_fields]
    for index, record in enumerate(caplog.records):
        assert record.msg == '{}{}'.format(fields_str[index], messages[index])


@pytest.mark.parametrize("custom_fields, message",
                         [
                             ({"axis": 1, "drive": "my_drive", "code_error": "0x3"}, "Hello"),
                             ({"axis": 3}, "Bye"),
                             ({"drive": "my_drive", "code_error": "An error"}, "Message with spaces"),
                             ({"axis": 0, "code_error": "0"}, "Enter de Gungeon"),
                             ({}, "Empty"),
                             ({"code_error": "0x3", "drive": "my_drive", "axis": 1}, "olleH"),
                             ({"category": "Configuration"}, "Good day sir")
                         ])
def test_get_logger_override_fields(caplog, custom_fields, message):
    init_fields = {"axis": 0, "drive": "No drive", "code_error": "No error", "category": "Generic"}
    logger = get_logger("test", **init_fields)
    logger.warning(message, **custom_fields)
    fields = init_fields.copy()
    fields.update(custom_fields)
    fields_str = generate_fields_text(fields)
    for record in caplog.records:
        assert record.msg == '{}{}'.format(fields_str, message)
