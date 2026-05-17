import msgspec
from datetime import datetime
from typing import TypeVar, ClassVar, Type, Optional, Any, List

from ..exceptions import WFMValidationError


def _dec_hook(type: Type, obj: Any) -> Any:
    if isinstance(type, datetime) and isinstance(obj, str):
        return datetime.fromisoformat(obj.strip("Z"))
    return obj


class Base(msgspec.Struct, kw_only=True):
    api_version: str = msgspec.field(name="apiVersion")
    error: Optional[Any] = None

    @classmethod
    def _check_error(cls, response: str) -> None:
        try:
            parsed = msgspec.json.decode(response)
            if parsed.get("data") is None and parsed.get("error") is not None:
                err = parsed["error"]
                request_errors = err.get("request") if isinstance(err, dict) else None
                input_errors = err.get("inputs") if isinstance(err, dict) else None
                if request_errors or input_errors:
                    raise WFMValidationError(
                        status=422,
                        request_errors=request_errors,
                        input_errors=input_errors,
                        body=response,
                    )
        except WFMValidationError:
            raise
        except Exception:
            pass


T = TypeVar("T", bound=Base)


class BaseRequest(Base):
    __endpoint__: ClassVar[str]
    __params__: ClassVar[List[str]] = []
    __slug__: ClassVar[bool] = False

    @classmethod
    def _decode(cls: Type[T], response: str) -> T:
        cls._check_error(response)
        return msgspec.json.decode(response, type=cls, dec_hook=_dec_hook)

    @classmethod
    def _get_endpoint(cls, slug: Optional[str] = None, **kwargs) -> str:
        endpoint = cls.__endpoint__
        if cls.__slug__ and slug:
            endpoint = endpoint.format(slug=slug)
        if cls.__params__:
            params = "&".join(
                f"{k}={v}" for k, v in kwargs.items() if k in cls.__params__ and v is not None
            )
            if params:
                endpoint += f"?{params}"
        return endpoint