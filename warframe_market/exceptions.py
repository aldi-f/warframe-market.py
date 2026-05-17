class WFMApiError(Exception):
    def __init__(self, status: int, message: str = "", body: str | None = None):
        self.status = status
        self.body = body
        super().__init__(message or f"API error {status}")


class WFMRateLimitError(WFMApiError):
    def __init__(self, status: int = 429, body: str | None = None):
        super().__init__(status, "Rate limited by Warframe Market API", body)


class WFMTooManyConnectionsError(WFMApiError):
    def __init__(self, status: int = 509, body: str | None = None):
        super().__init__(status, "Too many concurrent connections from this IP", body)


class WFMValidationError(WFMApiError):
    def __init__(self, status: int, request_errors: list[str] | None = None, input_errors: dict[str, str] | None = None, body: str | None = None):
        self.request_errors = request_errors or []
        self.input_errors = input_errors or {}
        msg = "; ".join(self.request_errors)
        if self.input_errors:
            msg += " | " if msg else ""
            msg += str(self.input_errors)
        super().__init__(status, msg or "Validation error", body)


class WFMAuthError(WFMApiError):
    def __init__(self, status: int = 401, body: str | None = None):
        super().__init__(status, "Authentication required or failed", body)


class WFMNotFoundError(WFMApiError):
    def __init__(self, status: int = 404, body: str | None = None):
        super().__init__(status, "Resource not found", body)


class WFMServerError(WFMApiError):
    def __init__(self, status: int = 500, body: str | None = None):
        super().__init__(status, f"Server error {status}", body)