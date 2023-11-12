import json
import traceback
from datetime import datetime

from HT_09.task_3 import settings


class ErrorLogger:
    def __init__(self, filepath=settings.DATABASE_ERROR):
        self.filepath = filepath
        self.errors = self.load_errors()

    def create_error_log(self):
        with open(self.filepath, 'w', encoding='utf-8') as file:
            json.dump([], file, ensure_ascii=False, indent=4)

    def load_errors(self):
        """Load an existing error file if one exists"""
        try:
            with open(self.filepath, 'r') as file:
                try:
                    return json.load(file)
                except json.decoder.JSONDecodeError:
                    print(settings.CONTACT_SUPPORT)
                    raise
        except PermissionError:
            self.create_error_log()
        except FileNotFoundError:
            self.create_error_log()
        return []

    def log_error(self, error_type, message, timestamp=None, traceback_info=None):
        """Log the error."""
        if timestamp is None:
            timestamp = datetime.now()

        if traceback_info is None:
            traceback_info = traceback.format_exc()

        formatted_timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")

        error_entry = {
            'type': error_type,
            'message': message,
            'timestamp': formatted_timestamp,
            'traceback': traceback_info
        }

        self.errors.append(error_entry)

        with open(self.filepath, 'w', encoding='utf-8') as file:
            json.dump(self.errors, file, ensure_ascii=False, indent=4)

    def get_and_parsed_errors(self):
        """Getting a list of parsed errors"""
        for error in self.errors:
            print('timestamp:', error.get('timestamp'))
            print('type error:', error.get('type'))
            print('error message:', error.get('message'))
            print('traceback:', error.get('traceback'))

        return self.errors


if __name__ == '__main__':
    logger = ErrorLogger()
    logger.get_and_parsed_errors()
