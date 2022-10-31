class RepositoryError(Exception):
    """
    User-defined exception for repository classes
    """
    def __int__(self, message):
        """
        Constructor for RepositoryError class
        :param message: error message
        """
        super().__init__(message)


class ValidationError(Exception):
    """
    User-defined exception for validator classes
    """
    def __init__(self, message):
        """
        Constructor for ValidationError class
        :param message: error message
        """
        super().__init__(message)


class InputError(Exception):
    """
    User-defined exception for input errors
    """
    def __init__(self, message):
        """
        Constructor for InputError class
        :param message: error message
        """
        super().__init__(message)


class UndoError(Exception):
    """
    User-defined exception for the undo/redo functionality
    """
    def __init__(self, message):
        """
        Constructor for UndoError class
        :param message: error message
        """
        super().__init__(message)


class SettingsError(Exception):
    """
    User-defined exception for the Settings class
    """
    def __init__(self, message):
        """
        Constructor for SettingsError class
        :param message: error message
        """
        super().__init__(message)
