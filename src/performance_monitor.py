"""
性能監控模組
提供詳細的性能監控和日誌記錄功能
"""

import time
import psutil
import threading
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
import logging
import json
from pathlib import Path
from contextlib import contextmanager

logger = logging.getLogger(__name__)

@dataclass
class PerformanceMetrics:
    """性能指標"""
    timestamp: float
    cpu_percent: float
    memory_percent: float
    memory_used_mb: float
    disk_io_read_mb: float
    disk_io_write_mb: float
    network_sent_mb: float
    network_recv_mb: float

@dataclass
class OperationStats:
    """操作統計"""
    operation_name: str
    start_time: float
    end_time: Optional[float] = None
    duration: Optional[float] = None
    success: bool = True
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

class PerformanceMonitor:
    """性能監控器"""
    
    def __init__(self, 
                 monitoring_interval: float = 1.0,
                 log_file: Optional[Path] = None,
                 auto_start: bool = True):
        
        self.monitoring_interval = monitoring_interval
        self.log_file = log_file
        self.is_monitoring = False
        self.monitoring_thread: Optional[threading.Thread] = None
        
        # 性能數據存儲
        self.metrics_history: List[PerformanceMetrics] = []
        self.operation_stats: List[OperationStats] = []
        
        # 基線性能數據
        self.baseline_metrics: Optional[PerformanceMetrics] = None
        
        # 鎖
        self.lock = threading.Lock()
        
        # 初始化系統信息
        self.system_info = self._get_system_info()
        
        if auto_start:
            self.start_monitoring()
    
    def _get_system_info(self) -> Dict[str, Any]:
        """獲取系統信息"""
        try:
            return {
                'cpu_count': psutil.cpu_count(),
                'cpu_count_logical': psutil.cpu_count(logical=True),
                'memory_total_gb': psutil.virtual_memory().total / 1024**3,
                'disk_total_gb': psutil.disk_usage('/').total / 1024**3,
                'python_version': f"{psutil.version_info}",
                'platform': psutil.WINDOWS if psutil.WINDOWS else 'Unix-like'
            }
        except Exception as e:
            logger.error(f"獲取系統信息失敗: {e}")
            return {}
    
    def _collect_metrics(self) -> PerformanceMetrics:
        """收集當前性能指標"""
        try:
            # CPU使用率
            cpu_percent = psutil.cpu_percent(interval=0.1)
            
            # 內存使用情況
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_used_mb = memory.used / 1024**2
            
            # 磁盤I/O
            disk_io = psutil.disk_io_counters()
            disk_io_read_mb = disk_io.read_bytes / 1024**2 if disk_io else 0
            disk_io_write_mb = disk_io.write_bytes / 1024**2 if disk_io else 0
            
            # 網絡I/O
            network_io = psutil.net_io_counters()
            network_sent_mb = network_io.bytes_sent / 1024**2 if network_io else 0
            network_recv_mb = network_io.bytes_recv / 1024**2 if network_io else 0
            
            return PerformanceMetrics(
                timestamp=time.time(),
                cpu_percent=cpu_percent,
                memory_percent=memory_percent,
                memory_used_mb=memory_used_mb,
                disk_io_read_mb=disk_io_read_mb,
                disk_io_write_mb=disk_io_write_mb,
                network_sent_mb=network_sent_mb,
                network_recv_mb=network_recv_mb
            )
            
        except Exception as e:
            logger.error(f"收集性能指標失敗: {e}")
            return PerformanceMetrics(
                timestamp=time.time(),
                cpu_percent=0, memory_percent=0, memory_used_mb=0,
                disk_io_read_mb=0, disk_io_write_mb=0,
                network_sent_mb=0, network_recv_mb=0
            )
    
    def _monitoring_loop(self):
        """監控循環"""
        logger.info("性能監控開始")
        
        while self.is_monitoring:
            try:
                metrics = self._collect_metrics()
                
                with self.lock:
                    self.metrics_history.append(metrics)
                    
                    # 保持最近1000個數據點
                    if len(self.metrics_history) > 1000:
                        self.metrics_history = self.metrics_history[-1000:]
                
                time.sleep(self.monitoring_interval)
                
            except Exception as e:
                logger.error(f"監控循環錯誤: {e}")
                time.sleep(self.monitoring_interval)
    
    def start_monitoring(self):
        """開始監控"""
        if self.is_monitoring:
            return
        
        self.is_monitoring = True
        self.baseline_metrics = self._collect_metrics()
        
        self.monitoring_thread = threading.Thread(
            target=self._monitoring_loop,
            daemon=True
        )
        self.monitoring_thread.start()
        
        logger.info("性能監控已啟動")
    
    def stop_monitoring(self):
        """停止監控"""
        if not self.is_monitoring:
            return
        
        self.is_monitoring = False
        
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        
        logger.info("性能監控已停止")
    
    @contextmanager
    def monitor_operation(self, operation_name: str, **metadata):
        """監控操作的上下文管理器"""
        start_time = time.time()
        operation = OperationStats(
            operation_name=operation_name,
            start_time=start_time,
            metadata=metadata
        )
        
        try:
            yield operation
            operation.success = True
        except Exception as e:
            operation.success = False
            operation.error_message = str(e)
            raise
        finally:
            operation.end_time = time.time()
            operation.duration = operation.end_time - operation.start_time
            
            with self.lock:
                self.operation_stats.append(operation)
            
            # 記錄操作日誌
            status = "成功" if operation.success else "失敗"
            logger.info(f"操作 '{operation_name}' {status}, 耗時: {operation.duration:.2f}秒")
    
    def get_current_metrics(self) -> Optional[PerformanceMetrics]:
        """獲取當前性能指標"""
        with self.lock:
            return self.metrics_history[-1] if self.metrics_history else None
    
    def get_metrics_summary(self, last_n_minutes: int = 5) -> Dict[str, Any]:
        """獲取性能指標摘要"""
        cutoff_time = time.time() - (last_n_minutes * 60)
        
        with self.lock:
            recent_metrics = [
                m for m in self.metrics_history 
                if m.timestamp >= cutoff_time
            ]
        
        if not recent_metrics:
            return {}
        
        # 計算統計信息
        cpu_values = [m.cpu_percent for m in recent_metrics]
        memory_values = [m.memory_percent for m in recent_metrics]
        
        return {
            'time_range_minutes': last_n_minutes,
            'data_points': len(recent_metrics),
            'cpu': {
                'avg': sum(cpu_values) / len(cpu_values),
                'max': max(cpu_values),
                'min': min(cpu_values)
            },
            'memory': {
                'avg': sum(memory_values) / len(memory_values),
                'max': max(memory_values),
                'min': min(memory_values),
                'current_used_mb': recent_metrics[-1].memory_used_mb
            },
            'baseline_comparison': self._compare_with_baseline(recent_metrics[-1]) if self.baseline_metrics else None
        }
    
    def _compare_with_baseline(self, current: PerformanceMetrics) -> Dict[str, float]:
        """與基線性能比較"""
        if not self.baseline_metrics:
            return {}
        
        return {
            'cpu_increase': current.cpu_percent - self.baseline_metrics.cpu_percent,
            'memory_increase': current.memory_percent - self.baseline_metrics.memory_percent,
            'memory_mb_increase': current.memory_used_mb - self.baseline_metrics.memory_used_mb
        }
    
    def get_operation_summary(self, operation_name: Optional[str] = None) -> Dict[str, Any]:
        """獲取操作統計摘要"""
        with self.lock:
            if operation_name:
                ops = [op for op in self.operation_stats if op.operation_name == operation_name]
            else:
                ops = self.operation_stats.copy()
        
        if not ops:
            return {}
        
        successful_ops = [op for op in ops if op.success]
        failed_ops = [op for op in ops if not op.success]
        
        durations = [op.duration for op in ops if op.duration is not None]
        
        summary = {
            'total_operations': len(ops),
            'successful': len(successful_ops),
            'failed': len(failed_ops),
            'success_rate': len(successful_ops) / len(ops) * 100 if ops else 0
        }
        
        if durations:
            summary['timing'] = {
                'avg_duration': sum(durations) / len(durations),
                'max_duration': max(durations),
                'min_duration': min(durations),
                'total_duration': sum(durations)
            }
        
        return summary
    
    def export_report(self, output_file: Path):
        """導出性能報告"""
        try:
            report = {
                'timestamp': datetime.now().isoformat(),
                'system_info': self.system_info,
                'monitoring_duration': time.time() - self.baseline_metrics.timestamp if self.baseline_metrics else 0,
                'metrics_summary': self.get_metrics_summary(),
                'operation_summary': self.get_operation_summary(),
                'detailed_operations': [
                    {
                        'name': op.operation_name,
                        'duration': op.duration,
                        'success': op.success,
                        'error': op.error_message,
                        'metadata': op.metadata
                    }
                    for op in self.operation_stats
                ]
            }
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            logger.info(f"性能報告已導出到: {output_file}")
            
        except Exception as e:
            logger.error(f"導出性能報告失敗: {e}")
    
    def clear_history(self):
        """清除歷史數據"""
        with self.lock:
            self.metrics_history.clear()
            self.operation_stats.clear()
        
        logger.info("性能監控歷史數據已清除")
