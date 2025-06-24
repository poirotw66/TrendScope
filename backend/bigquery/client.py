"""
BigQuery 客戶端
提供與 Google BigQuery 交互的功能
"""
from google.cloud import bigquery
from google.oauth2 import service_account
import os

class BigQueryClient:
    """
    BigQuery 客戶端類
    提供與 Google BigQuery 交互的方法
    """
    
    def __init__(self, credentials_path=None, project_id=None):
        """
        初始化 BigQuery 客戶端
        
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
        
        self.client = bigquery.Client(
            credentials=self.credentials,
            project=self.project_id
        )
        
    def create_dataset_if_not_exists(self, dataset_id):
        """
        如果數據集不存在，則創建
        
        Args:
            dataset_id (str): 數據集 ID
            
        Returns:
            google.cloud.bigquery.dataset.Dataset: 創建或獲取的數據集
        """
        dataset_ref = self.client.dataset(dataset_id)
        
        try:
            dataset = self.client.get_dataset(dataset_ref)
            print(f"數據集 {dataset_id} 已存在")
        except Exception:
            # 數據集不存在，創建它
            dataset = bigquery.Dataset(dataset_ref)
            dataset.location = "asia-east1"  # 可根據需要更改位置
            dataset = self.client.create_dataset(dataset)
            print(f"已創建數據集 {dataset_id}")
            
        return dataset
        
    def create_table_if_not_exists(self, dataset_id, table_id, schema):
        """
        如果表不存在，則創建
        
        Args:
            dataset_id (str): 數據集 ID
            table_id (str): 表 ID
            schema (list): BigQuery 表結構
            
        Returns:
            google.cloud.bigquery.table.Table: 創建或獲取的表
        """
        table_ref = self.client.dataset(dataset_id).table(table_id)
        
        try:
            table = self.client.get_table(table_ref)
            print(f"表 {dataset_id}.{table_id} 已存在")
        except Exception:
            # 表不存在，創建它
            table = bigquery.Table(table_ref, schema=schema)
            table = self.client.create_table(table)
            print(f"已創建表 {dataset_id}.{table_id}")
            
        return table
        
    def upload_data_to_table(self, dataset_id, table_id, data, schema=None):
        """
        將數據上傳到 BigQuery 表
        
        Args:
            dataset_id (str): 數據集 ID
            table_id (str): 表 ID
            data (list): 要上傳的數據列表，每個元素為一個字典
            schema (list, optional): BigQuery 表結構，如果未提供，則使用現有表的結構
            
        Returns:
            google.cloud.bigquery.job.LoadJob: 上傳作業
        """
        table_ref = self.client.dataset(dataset_id).table(table_id)
        
        # 確保表存在
        if schema:
            table = self.create_table_if_not_exists(dataset_id, table_id, schema)
        else:
            # 獲取現有表的結構
            try:
                table = self.client.get_table(table_ref)
                schema = table.schema
            except Exception as e:
                print(f"無法獲取表結構: {str(e)}")
                return None
        
        # 準備上傳作業
        job_config = bigquery.LoadJobConfig()
        job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
        
        # 始終使用表結構上傳，避免 schema mismatch
        job_config.schema = schema
        
        # 開始上傳作業
        job = self.client.load_table_from_json(
            data,
            table_ref,
            job_config=job_config
        )
        
        # 等待作業完成
        job.result()
        
        print(f"已上傳 {len(data)} 條記錄到 {dataset_id}.{table_id}")
        
        return job
        
    def query(self, query_string):
        """
        執行 SQL 查詢
        
        Args:
            query_string (str): SQL 查詢字符串
            
        Returns:
            google.cloud.bigquery.table.RowIterator: 查詢結果
        """
        query_job = self.client.query(query_string)
        return query_job.result()
