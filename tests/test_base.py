import pytest
import msgspec
from warframe_market.common.base import Base, BaseRequest
from warframe_market.common import BASE_URL, LanguageCode
from warframe_market.exceptions import WFMValidationError


class DummyRequest(BaseRequest):
    __endpoint__ = "/test"
    data: str | None = None


class TestBaseCheckError:
    def test_good_response_no_error(self):
        resp = '{"apiVersion": "x.x.x", "data": "ok", "error": null}'
        Base._check_error(resp)

    def test_good_response_with_data(self):
        resp = '{"apiVersion": "x.x.x", "data": [1,2,3], "error": null}'
        Base._check_error(resp)

    def test_error_response_raises(self):
        resp = '{"apiVersion": "x.x.x", "data": null, "error": {"request": ["app.errors.unauthorized"], "inputs": {}}}'
        with pytest.raises(WFMValidationError) as exc_info:
            Base._check_error(resp)
        assert "unauthorized" in str(exc_info.value)
        assert exc_info.value.status == 422

    def test_error_with_input_errors(self):
        resp = '{"apiVersion": "x.x.x", "data": null, "error": {"request": [], "inputs": {"platinum": "app.field.tooSmall"}}}'
        with pytest.raises(WFMValidationError) as exc_info:
            Base._check_error(resp)
        assert "tooSmall" in str(exc_info.value)

    def test_malformed_json_does_not_raise(self):
        resp = "not-json"
        Base._check_error(resp)

    def test_error_missing_request_field(self):
        resp = '{"apiVersion": "x.x.x", "data": null, "error": {}}'
        Base._check_error(resp)


class TestDecodeIntegration:
    def test_decode_good_response(self):
        resp = '{"apiVersion": "x.x.x", "data": "hello", "error": null}'
        result = DummyRequest._decode(resp)
        assert result.api_version == "x.x.x"
        assert result.data == "hello"

    def test_decode_raises_on_error(self):
        resp = '{"apiVersion": "x.x.x", "data": null, "error": {"request": ["error"], "inputs": {}}}'
        with pytest.raises(WFMValidationError):
            DummyRequest._decode(resp)

    def test_decode_preserves_encoded_date(self):
        class WithDate(Base):
            data: str | None = None

        resp = '{"apiVersion": "x.x.x", "data": null, "error": null}'
        obj = msgspec.json.decode(resp, type=WithDate)
        assert obj.api_version == "x.x.x"