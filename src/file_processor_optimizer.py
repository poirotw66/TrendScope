"""
文件處理優化器
優化文件讀取、上傳和處理的效率
"""

import os
import hashlib
import mimetypes
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import logging
import time
from dataclasses import dataclass
import json

logger = logging.getLogger(__name__)

@dataclass
class FileInfo:
    """文件信息"""
    path: Path
    size: int
    hash: str
    mime_type: str
    last_modified: float

@dataclass
class UploadResult:
    """上傳結果"""
    success: bool
    file_id: Optional[str] = None
    error: Optional[str] = None
    upload_time: float = 0.0
    cached: bool = False

class FileCache:
    """文件緩存管理器"""
    
    def __init__(self, cache_dir: Path = Path(".cache")):
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(exist_ok=True)
        self.cache_file = self.cache_dir / "file_cache.json"
        self.cache_data = self._load_cache()
    
    def _load_cache(self) -> Dict:
        """載入緩存數據"""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"載入緩存失敗: {e}")
        return {}
    
    def _save_cache(self):
        """保存緩存數據"""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"保存緩存失敗: {e}")
    
    def get_cached_upload(self, file_hash: str) -> Optional[str]:
        """獲取緩存的上傳ID"""
        return self.cache_data.get(file_hash, {}).get('file_id')
    
    def cache_upload(self, file_hash: str, file_id: str, file_path: str):
        """緩存上傳結果"""
        self.cache_data[file_hash] = {
            'file_id': file_id,
            'file_path': file_path,
            'cached_at': time.time()
        }
        self._save_cache()
    
    def cleanup_old_cache(self, max_age_days: int = 7):
        """清理過期緩存"""
        current_time = time.time()
        max_age_seconds = max_age_days * 24 * 3600
        
        to_remove = []
        for file_hash, data in self.cache_data.items():
            if current_time - data.get('cached_at', 0) > max_age_seconds:
                to_remove.append(file_hash)
        
        for file_hash in to_remove:
            del self.cache_data[file_hash]
        
        if to_remove:
            logger.info(f"清理 {len(to_remove)} 個過期緩存項")
            self._save_cache()

class OptimizedFileProcessor:
    """優化的文件處理器"""
    
    def __init__(self, cache_enabled: bool = True):
        self.cache_enabled = cache_enabled
        self.file_cache = FileCache() if cache_enabled else None
        self.file_info_cache: Dict[str, FileInfo] = {}
        
        logger.info(f"初始化文件處理器，緩存: {'啟用' if cache_enabled else '禁用'}")
    
    def get_file_info(self, file_path: Path) -> FileInfo:
        """獲取文件信息（帶緩存）"""
        file_key = str(file_path.absolute())
        
        # 檢查內存緩存
        if file_key in self.file_info_cache:
            cached_info = self.file_info_cache[file_key]
            # 檢查文件是否被修改
            if file_path.stat().st_mtime == cached_info.last_modified:
                return cached_info
        
        # 計算文件信息
        stat = file_path.stat()
        file_size = stat.st_size
        last_modified = stat.st_mtime
        
        # 計算文件哈希
        file_hash = self._calculate_file_hash(file_path)
        
        # 獲取MIME類型
        mime_type, _ = mimetypes.guess_type(str(file_path))
        if not mime_type:
            mime_type = 'application/octet-stream'
        
        file_info = FileInfo(
            path=file_path,
            size=file_size,
            hash=file_hash,
            mime_type=mime_type,
            last_modified=last_modified
        )
        
        # 緩存到內存
        self.file_info_cache[file_key] = file_info
        
        return file_info
    
    def _calculate_file_hash(self, file_path: Path, chunk_size: int = 8192) -> str:
        """計算文件哈希值"""
        hash_md5 = hashlib.md5()
        
        try:
            with open(file_path, "rb") as f:
                while chunk := f.read(chunk_size):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            logger.error(f"計算文件哈希失敗 {file_path}: {e}")
            return ""
    
    def batch_get_file_info(self, file_paths: List[Path]) -> List[FileInfo]:
        """批量獲取文件信息"""
        logger.info(f"批量獲取 {len(file_paths)} 個文件信息")
        
        file_infos = []
        for file_path in file_paths:
            try:
                file_info = self.get_file_info(file_path)
                file_infos.append(file_info)
            except Exception as e:
                logger.error(f"獲取文件信息失敗 {file_path}: {e}")
        
        return file_infos
    
    def filter_files_by_size(self, file_infos: List[FileInfo], 
                           min_size: int = 1024, 
                           max_size: int = 100 * 1024 * 1024) -> List[FileInfo]:
        """根據文件大小過濾文件"""
        filtered = []
        skipped_small = 0
        skipped_large = 0
        
        for file_info in file_infos:
            if file_info.size < min_size:
                skipped_small += 1
                logger.debug(f"跳過小文件: {file_info.path.name} ({file_info.size} bytes)")
            elif file_info.size > max_size:
                skipped_large += 1
                logger.warning(f"跳過大文件: {file_info.path.name} ({file_info.size / 1024 / 1024:.1f} MB)")
            else:
                filtered.append(file_info)
        
        if skipped_small > 0:
            logger.info(f"跳過 {skipped_small} 個小文件 (< {min_size} bytes)")
        if skipped_large > 0:
            logger.info(f"跳過 {skipped_large} 個大文件 (> {max_size / 1024 / 1024:.1f} MB)")
        
        return filtered
    
    def optimize_upload_order(self, file_infos: List[FileInfo]) -> List[FileInfo]:
        """優化上傳順序 - 小文件優先"""
        return sorted(file_infos, key=lambda x: x.size)
    
    def simulate_upload_with_cache(self, file_info: FileInfo) -> UploadResult:
        """模擬帶緩存的文件上傳"""
        start_time = time.time()
        
        # 檢查緩存
        if self.cache_enabled and self.file_cache:
            cached_file_id = self.file_cache.get_cached_upload(file_info.hash)
            if cached_file_id:
                logger.info(f"使用緩存上傳: {file_info.path.name}")
                return UploadResult(
                    success=True,
                    file_id=cached_file_id,
                    upload_time=time.time() - start_time,
                    cached=True
                )
        
        # 模擬上傳時間（基於文件大小）
        # 假設上傳速度：1MB/s
        upload_time = max(1.0, file_info.size / (1024 * 1024))  # 最少1秒
        time.sleep(min(upload_time, 0.1))  # 實際測試時只等待很短時間
        
        # 模擬成功上傳
        fake_file_id = f"file_{file_info.hash[:8]}"
        
        # 緩存結果
        if self.cache_enabled and self.file_cache:
            self.file_cache.cache_upload(
                file_info.hash, 
                fake_file_id, 
                str(file_info.path)
            )
        
        return UploadResult(
            success=True,
            file_id=fake_file_id,
            upload_time=time.time() - start_time,
            cached=False
        )
    
    def get_processing_stats(self, file_infos: List[FileInfo]) -> Dict:
        """獲取處理統計信息"""
        if not file_infos:
            return {}
        
        total_size = sum(f.size for f in file_infos)
        avg_size = total_size / len(file_infos)
        
        size_distribution = {
            'small': len([f for f in file_infos if f.size < 1024 * 1024]),  # < 1MB
            'medium': len([f for f in file_infos if 1024 * 1024 <= f.size < 10 * 1024 * 1024]),  # 1-10MB
            'large': len([f for f in file_infos if f.size >= 10 * 1024 * 1024])  # >= 10MB
        }
        
        return {
            'total_files': len(file_infos),
            'total_size_mb': total_size / 1024 / 1024,
            'avg_size_mb': avg_size / 1024 / 1024,
            'size_distribution': size_distribution,
            'estimated_upload_time': total_size / (1024 * 1024),  # 假設1MB/s
        }
    
    def cleanup_cache(self):
        """清理緩存"""
        if self.cache_enabled and self.file_cache:
            self.file_cache.cleanup_old_cache()
        
        # 清理內存緩存
        self.file_info_cache.clear()
        logger.info("緩存清理完成")
