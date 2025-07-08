"""
Google Cloud Storage 客戶端
提供與 Google Cloud Storage 交互的功能
"""
import os
import pathlib
import logging
from typing import Optional, Dict, Any
from google.cloud import storage
from google.oauth2 import service_account

logger = logging.getLogger("trendscope-api")

class GCSClient:
    """
    Google Cloud Storage 客戶端類
    提供與 Google Cloud Storage 交互的方法
    """
    
    def __init__(self, credentials_path: Optional[str] = None, project_id: Optional[str] = None):
        """
        初始化 GCS 客戶端
        
        Args:
            credentials_path (str, optional): 服務帳戶憑證文件路徑，如果未提供，
                                             則嘗試從環境變量 GOOGLE_APPLICATION_CREDENTIALS 獲取
            project_id (str, optional): Google Cloud 項目 ID，如果未提供，則從憑證中獲取
        """
        self.credentials_path = credentials_path or os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
        
        if not self.credentials_path:
            raise ValueError("必須提供憑證路徑或設置 GOOGLE_APPLICATION_CREDENTIALS 環境變量")
        
        self.credentials = service_account.Credentials.from_service_account_file(
            self.credentials_path
        )
        
        self.project_id = project_id or self.credentials.project_id
        
        if not self.project_id:
            raise ValueError("必須提供項目 ID 或確保憑證中包含項目 ID")
        
        self.client = storage.Client(
            credentials=self.credentials,
            project=self.project_id
        )
        
    def upload_file(self, local_file_path: str, bucket_name: str, 
                   destination_blob_name: str, make_public: bool = True) -> Dict[str, Any]:
        """
        上傳文件到 Google Cloud Storage
        
        Args:
            local_file_path (str): 本地文件路徑
            bucket_name (str): GCS bucket 名稱
            destination_blob_name (str): 目標 blob 名稱（GCS 中的文件路徑）
            make_public (bool): 是否設置為公開可訪問，默認為 True
            
        Returns:
            Dict[str, Any]: 包含上傳結果的字典
                - success (bool): 上傳是否成功
                - blob_name (str): blob 名稱
                - public_url (str): 公開訪問 URL（如果設置為公開）
                - gs_url (str): GCS URL
                - size (int): 文件大小（字節）
                - error (str): 錯誤信息（如果失敗）
        """
        try:
            # 檢查本地文件是否存在
            local_path = pathlib.Path(local_file_path)
            if not local_path.exists():
                return {
                    "success": False,
                    "error": f"本地文件不存在: {local_file_path}"
                }
            
            # 獲取 bucket
            bucket = self.client.bucket(bucket_name)
            
            # 創建 blob
            blob = bucket.blob(destination_blob_name)
            
            # 上傳文件
            logger.info(f"開始上傳文件到 GCS: {local_file_path} -> gs://{bucket_name}/{destination_blob_name}")
            
            with open(local_file_path, 'rb') as file_obj:
                blob.upload_from_file(file_obj)
            
            # 設置文件為公開可訪問（如果需要）
            public_url = None
            if make_public:
                blob.make_public()
                public_url = blob.public_url
                logger.info(f"文件已設置為公開可訪問: {public_url}")
            
            # 構建結果
            result = {
                "success": True,
                "blob_name": destination_blob_name,
                "gs_url": f"gs://{bucket_name}/{destination_blob_name}",
                "size": local_path.stat().st_size
            }
            
            if public_url:
                result["public_url"] = public_url
            
            logger.info(f"文件上傳成功: {local_file_path} -> {result['gs_url']}")
            return result
            
        except Exception as e:
            error_msg = f"上傳文件到 GCS 失敗: {str(e)}"
            logger.error(error_msg)
            return {
                "success": False,
                "error": error_msg
            }
    
    def upload_zip_file(self, local_zip_path: str, bucket_name: str, 
                       folder_prefix: str = "seminar_report/") -> Dict[str, Any]:
        """
        上傳 ZIP 文件到 GCS 的指定目錄
        
        Args:
            local_zip_path (str): 本地 ZIP 文件路徑
            bucket_name (str): GCS bucket 名稱
            folder_prefix (str): GCS 中的目錄前綴，默認為 "seminar_report/"
            
        Returns:
            Dict[str, Any]: 上傳結果
        """
        try:
            local_path = pathlib.Path(local_zip_path)
            if not local_path.exists():
                return {
                    "success": False,
                    "error": f"ZIP 文件不存在: {local_zip_path}"
                }
            
            # 構建目標路徑：folder_prefix + 文件名
            destination_blob_name = f"{folder_prefix.rstrip('/')}/{local_path.name}"
            
            # 上傳文件
            result = self.upload_file(
                local_file_path=local_zip_path,
                bucket_name=bucket_name,
                destination_blob_name=destination_blob_name,
                make_public=True
            )
            
            if result["success"]:
                logger.info(f"ZIP 文件上傳成功: {local_zip_path} -> {result['gs_url']}")
            
            return result
            
        except Exception as e:
            error_msg = f"上傳 ZIP 文件失敗: {str(e)}"
            logger.error(error_msg)
            return {
                "success": False,
                "error": error_msg
            }
    
    def check_bucket_exists(self, bucket_name: str) -> bool:
        """
        檢查 bucket 是否存在
        
        Args:
            bucket_name (str): bucket 名稱
            
        Returns:
            bool: bucket 是否存在
        """
        try:
            bucket = self.client.bucket(bucket_name)
            bucket.reload()
            return True
        except Exception as e:
            logger.warning(f"Bucket {bucket_name} 不存在或無法訪問: {e}")
            return False
    
    def list_files(self, bucket_name: str, prefix: str = "") -> list:
        """
        列出 bucket 中的文件
        
        Args:
            bucket_name (str): bucket 名稱
            prefix (str): 文件前綴過濾器
            
        Returns:
            list: 文件列表
        """
        try:
            bucket = self.client.bucket(bucket_name)
            blobs = bucket.list_blobs(prefix=prefix)
            return [blob.name for blob in blobs]
        except Exception as e:
            logger.error(f"列出文件失敗: {e}")
            return []


def get_gcs_client() -> Optional[GCSClient]:
    """
    獲取 GCS 客戶端實例
    
    Returns:
        Optional[GCSClient]: GCS 客戶端實例，如果初始化失敗則返回 None
    """
    try:
        credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
        
        if not credentials_path:
            logger.warning("未設置 GOOGLE_APPLICATION_CREDENTIALS 環境變量")
            return None
        
        return GCSClient(credentials_path=credentials_path, project_id=project_id)
    except Exception as e:
        logger.error(f"初始化 GCS 客戶端失敗: {str(e)}")
        return None
