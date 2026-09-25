from fastapi import Response


def apply_response_headers(response: Response, result) -> None:
    response.status_code = result.status
    response.headers["X-Success"] = str(result.success).lower()
    response.headers["X-Error"] = str(result.error).lower()
