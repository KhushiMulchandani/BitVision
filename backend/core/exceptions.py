from rest_framework.views import exception_handler


def api_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is None:           # unhandled -> Django's normal 500
        return None
    data = response.data
    if isinstance(data, dict) and set(data) == {"detail"}:
        response.data = {"error": str(data["detail"]), "details": None}
    else:
        response.data = {"error": "Validation failed" if response.status_code == 400 else "Request failed",
                         "details": data}
    return response