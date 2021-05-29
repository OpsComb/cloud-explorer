import logging

logger = logging.getLogger(__name__)


def error_handling_decorator(func):
    def wrapper(*args, **kwargs):
        logger.debug(f"Function - {func.__qualname__} called with args - {args} and kwargs - {kwargs}")
        response = {
            "Response": None,
            "Error": None
        }
        try:
            output = func(*args, **kwargs)
            logger.debug(f"Response for function {func} is {output}")

            # format exception
            response["Response"] = output
        except Exception as e:
            response["Error"] = str(e)
        return response

    return wrapper
