import datetime

class Logger:
    @staticmethod
    def print(message, level="INFO"):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{now}] [{level}] - {message}")

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
        print("\n" + "-"*50)
        Logger.info(f"{title}")
        print("-"*50)

    @staticmethod
    def section_footer():
        print("-"*50 + "\n")
