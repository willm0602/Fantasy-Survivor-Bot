
class CommandInputException(Exception):
    pass

class InvalidBetException(CommandInputException):
    pass

class ModelInstanceDoesNotExist(Exception):
    pass

class CommandInvalidAccessException(
    CommandInputException
):
    pass

class UserInputInvalidBetException(
    CommandInputException,
    InvalidBetException
):
    pass
