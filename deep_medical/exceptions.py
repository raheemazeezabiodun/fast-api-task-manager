class AppException(Exception):
    pass


class NotFoundException(AppException):
    pass


class InvalidDataException(AppException):
    pass
