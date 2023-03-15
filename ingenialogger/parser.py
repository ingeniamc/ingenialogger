import re

REGEX_PARSER_LOG_STR = r"([^|]+) \| ([^|]+) \| ([^|]+) \| ([^|]+)"
REGEX_PARSER_LOG = re.compile(REGEX_PARSER_LOG_STR)
REGEX_PARSER_MSG_STR = r'(?:\(((?:\w+="[^"]+",? ?)+)\) )?(.+)'
REGEX_PARSER_MSG = re.compile(REGEX_PARSER_MSG_STR, re.DOTALL)
REGEX_PARSER_FIELDS_STR = r'(\w+)="([^"]+)"'
REGEX_PARSER_FIELDS = re.compile(REGEX_PARSER_FIELDS_STR)


class LogParser:
    @staticmethod
    def parse_log(log):
        """
        From a target log line, return a dict with logs timestamp, logger name, level, message and custom fields.

        Args:
            log (str): log line string.

        Returns:
            dict: Dictionary with all the log fields. Example:

            .. code-block:: python

                {
                    'timestamp': '2021-03-24 13:16:29,335',
                    'logger': 'root',
                    'level': 'INFO',
                    'message': 'Example log'
                    'fields': {
                        'axis': 1
                    }
                }
        """
        log_match = REGEX_PARSER_LOG.match(log)
        if log_match is None:
            return
        log_dict = {
            "timestamp": log_match.group(1),
            "logger": log_match.group(2),
            "level": log_match.group(3),
        }
        msg_dict = LogParser.parse_message(log_match.group(4))
        return {**log_dict, **msg_dict}

    @staticmethod
    def parse_message(msg):
        """
        From a target log message, return a dict with message and custom fields.

        Args:
            msg (str): log message.

        Returns:
            dict: Dictionary with log message and custom fields. Example:

            .. code-block:: python

                {
                    'message': 'Example log'
                    'fields': {
                        'axis': 1
                    }
                }
        """
        msg_match = REGEX_PARSER_MSG.match(msg)
        return {"message": msg_match.group(2), "fields": LogParser.parse_fields(msg_match.group(1))}

    @staticmethod
    def parse_fields(fields_str):
        """
        From a target log fields, return a dict with fields.

        Args:
            fields_str (str): string with log custom fields.

        Returns:
            dict: Dictionary with log custom fields. Example:

            .. code-block:: python

                {
                    axis': 1
                }
        """
        fields = {}
        if fields_str is not None:
            field_matches = REGEX_PARSER_FIELDS.finditer(fields_str)
            for match in field_matches:
                fields[match.group(1)] = match.group(2)
        return fields
