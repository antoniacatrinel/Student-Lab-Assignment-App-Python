class RepositoryError(Exception):
    """
    User-defined exception for all repository classes
    """
    pass


class ValidationError(Exception):
    """
    User-defined exception for all validator classes
    """
    pass


class InputError(Exception):
    """
    User-defined exception for all input errors
    """
    pass


class UndoError(Exception):
    """
    User-defined exception for the undo/redo functionality
    """
    pass


class SettingsError(Exception):
    """
    User-defined exception for the Settings class
    """
    pass
