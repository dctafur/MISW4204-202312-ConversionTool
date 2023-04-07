from werkzeug.exceptions import HTTPException
from jsonschema import ValidationError


def http_exception_handler(error: HTTPException):
    if isinstance(error.description, ValidationError):
        original_error = error.description
        return {'message': original_error.message}, 400
    return {'message': error.description}, error.code
