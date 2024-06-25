import datetime

class Logger:
    console_enabled = True  # Class variable to control output

    @staticmethod
    def print(message, level="INFO"):
        if Logger.console_enabled:
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{now}] [{level}] - {message}")

    @staticmethod
    def set_console_output(enable=True):
        Logger.console_enabled = enable  # Set the class variable based on the input

    @staticmethod
    def info(message):
        Logger.print(message, "INFO")

    @staticmethod
    def debug(message):
        Logger.print(message, "DEBUG")

    @staticmethod
    def error(message):
        Logger.print(message, "ERROR")

    @staticmethod
    def section_header(title):
        if Logger.console_enabled:
            print("\n" + "-"*50)
        Logger.info(title)
        if Logger.console_enabled:
            print("-"*50)

    @staticmethod
    def section_footer():
        if Logger.console_enabled:
            print("-"*50 + "\n")
