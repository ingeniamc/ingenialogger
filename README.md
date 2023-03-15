Ingenialogger
=============

Module to unify libraries, script and programs logs.

How to use it
-------------

### Module and libraries

```python
import ingenialogger

logger = ingenialogger.get_logger(__name__)

logger.info("Info log", axis=1, drive="EVE-XCR (192.168.2.22)")

logger.user_warning("User Warning log", code_error="0x2342")
```

### Final application

```python
import ingenialogger

log_queue = ingenialogger.configure_logger(level=ingenialogger.LoggingLevel.INFO, queue=True)
logger = ingenialogger.get_logger(__name__)
logger.user_info("User Info log", axis=2, drive="My drive")

log_msg = log_queue.get().msg
print(ingenialogger.LogParser.parse_log(log_msg))
```
