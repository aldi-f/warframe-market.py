from warframe_market.exceptions import (
    WFMApiError,
    WFMRateLimitError,
    WFMTooManyConnectionsError,
    WFMValidationError,
    WFMAuthError,
    WFMNotFoundError,
    WFMServerError,
)


class TestExceptionHierarchy:
    def test_all_inherit_from_wfm_api_error(self):
        assert issubclass(WFMRateLimitError, WFMApiError)
        assert issubclass(WFMTooManyConnectionsError, WFMApiError)
        assert issubclass(WFMValidationError, WFMApiError)
        assert issubclass(WFMAuthError, WFMApiError)
        assert issubclass(WFMNotFoundError, WFMApiError)
        assert issubclass(WFMServerError, WFMApiError)

    def test_api_error_basic(self):
        err = WFMApiError(status=400, message="bad request", body="{}")
        assert err.status == 400
        assert str(err) == "bad request"
        assert err.body == "{}"

    def test_api_error_default_message(self):
        err = WFMApiError(status=418)
        assert str(err) == "API error 418"

    def test_rate_limit(self):
        err = WFMRateLimitError()
        assert err.status == 429
        assert "Rate limited" in str(err)

    def test_rate_limit_with_body(self):
        err = WFMRateLimitError(body='{"error": "too many requests"}')
        assert err.status == 429
        assert err.body is not None

    def test_too_many_connections(self):
        err = WFMTooManyConnectionsError()
        assert err.status == 509
        assert "Too many" in str(err)

    def test_validation_error(self):
        err = WFMValidationError(
            status=422,
            request_errors=["app.errors.unauthorized"],
            input_errors={"platinum": "app.field.tooSmall"},
        )
        assert "unauthorized" in str(err)
        assert err.request_errors == ["app.errors.unauthorized"]
        assert err.input_errors == {"platinum": "app.field.tooSmall"}
        assert err.status == 422

    def test_validation_error_without_fields(self):
        err = WFMValidationError(status=400)
        assert err.request_errors == []
        assert err.input_errors == {}
        assert str(err) == "Validation error"

    def test_auth_error_401(self):
        err = WFMAuthError()
        assert err.status == 401
        assert "Authentication" in str(err)

    def test_auth_error_403(self):
        err = WFMAuthError(status=403)
        assert err.status == 403

    def test_not_found(self):
        err = WFMNotFoundError()
        assert err.status == 404
        assert "not found" in str(err).lower()

    def test_server_error(self):
        err = WFMServerError(status=503)
        assert err.status == 503
        assert "503" in str(err)