"""
統一錯誤處理中間件
提供全局異常處理和統一的錯誤響應格式
"""
import logging
from typing import Union
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from google.cloud.exceptions import GoogleCloudError
from google.api_core.exceptions import GoogleAPIError

logger = logging.getLogger("NeoTrendHub-api")


class APIError(Exception):
    """自定義 API 錯誤基類"""
    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail: Union[str, dict] = None,
        error_code: str = None
    ):
        self.message = message
        self.status_code = status_code
        self.detail = detail or message
        self.error_code = error_code or f"ERR_{status_code}"
        super().__init__(self.message)


class BigQueryError(APIError):
    """BigQuery 相關錯誤"""
    def __init__(self, message: str, detail: Union[str, dict] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=detail,
            error_code="BIGQUERY_ERROR"
        )


class ValidationError(APIError):
    """驗證錯誤"""
    def __init__(self, message: str, detail: Union[str, dict] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
            error_code="VALIDATION_ERROR"
        )


class NotFoundError(APIError):
    """資源未找到錯誤"""
    def __init__(self, message: str, detail: Union[str, dict] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
            error_code="NOT_FOUND"
        )


def create_error_response(
    status_code: int,
    message: str,
    detail: Union[str, dict] = None,
    error_code: str = None,
    include_traceback: bool = False
) -> JSONResponse:
    """
    創建統一的錯誤響應
    
    Args:
        status_code: HTTP 狀態碼
        message: 錯誤訊息
        detail: 詳細資訊
        error_code: 錯誤代碼
        include_traceback: 是否包含堆疊追蹤（僅開發環境）
    
    Returns:
        JSONResponse: 統一的錯誤響應
    """
    response_data = {
        "error": {
            "code": error_code or f"ERR_{status_code}",
            "message": message,
            "detail": detail or message
        }
    }
    
    # 僅在開發環境包含堆疊追蹤
    if include_traceback:
        import traceback as tb
        response_data["error"]["traceback"] = tb.format_exc()
    
    return JSONResponse(
        status_code=status_code,
        content=response_data
    )


async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    全局異常處理器
    捕獲所有未處理的異常並返回統一的錯誤響應
    """
    # 記錄完整的錯誤資訊
    logger.error(
        "未處理的異常: %s",
        type(exc).__name__,
        exc_info=True,
        extra={
            "path": request.url.path,
            "method": request.method,
            "error_type": type(exc).__name__,
            "error_message": str(exc)
        }
    )
    
    # Google Cloud 相關錯誤
    if isinstance(exc, (GoogleCloudError, GoogleAPIError)):
        return create_error_response(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            message="Google Cloud 服務暫時不可用",
            detail=str(exc),
            error_code="GOOGLE_CLOUD_ERROR"
        )
    
    # 自定義 API 錯誤
    if isinstance(exc, APIError):
        return create_error_response(
            status_code=exc.status_code,
            message=exc.message,
            detail=exc.detail,
            error_code=exc.error_code
        )
    
    # 預設：500 內部伺服器錯誤
    return create_error_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message="內部伺服器錯誤",
        detail="發生未預期的錯誤，請聯繫管理員",
        error_code="INTERNAL_ERROR",
        include_traceback=False  # 生產環境不暴露堆疊追蹤
    )


async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    """
    HTTP 異常處理器
    處理 FastAPI 的 HTTPException
    """
    logger.warning(
        "HTTP 異常: %s - %s",
        exc.status_code,
        exc.detail,
        extra={
            "path": request.url.path,
            "method": request.method,
            "status_code": exc.status_code
        }
    )
    
    return create_error_response(
        status_code=exc.status_code,
        message=exc.detail,
        detail=exc.detail,
        error_code=f"HTTP_{exc.status_code}"
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """
    請求驗證異常處理器
    處理 Pydantic 驗證錯誤
    """
    errors = exc.errors()
    logger.warning(
        "請求驗證失敗: %s 個錯誤",
        len(errors),
        extra={
            "path": request.url.path,
            "method": request.method,
            "errors": errors
        }
    )
    
    # 格式化驗證錯誤
    error_details = []
    for error in errors:
        field = " -> ".join(str(loc) for loc in error.get("loc", []))
        error_details.append({
            "field": field,
            "message": error.get("msg"),
            "type": error.get("type")
        })
    
    return create_error_response(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        message="請求驗證失敗",
        detail={
            "validation_errors": error_details,
            "raw_errors": errors
        },
        error_code="VALIDATION_ERROR"
    )
