from logging import getLogger


def get_logger(name):
    """
    Function to be used instead of the standard logging.getLogger in order to ensure proper
    logger configuration load order
    """
    return getLogger(name)


def configure_logger():
    """
    Logger configuration goes here, for instance:

    print(f'Logging configuration file path: "logging.conf"')

    if not os.path.exists("log"):
        print(f'Creating logs directory: /log')
        os.mkdir("log")

    fileConfig(
        "logging.conf",
        disable_existing_loggers=False,
    )
    """
    pass
