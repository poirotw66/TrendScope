"""
共享任務管理模組
用於在不同路由模組之間共享任務狀態
"""
from typing import Dict, Any

# 全域任務字典，用於存儲所有類型的任務
tasks: Dict[str, Dict[str, Any]] = {}

def get_tasks() -> Dict[str, Dict[str, Any]]:
    """獲取所有任務"""
    return tasks

def get_task(task_id: str) -> Dict[str, Any]:
    """獲取特定任務"""
    return tasks.get(task_id, {})

def set_task(task_id: str, task_data: Dict[str, Any]) -> None:
    """設置任務數據"""
    tasks[task_id] = task_data

def update_task(task_id: str, updates: Dict[str, Any]) -> None:
    """更新任務數據"""
    if task_id in tasks:
        tasks[task_id].update(updates)

def delete_task(task_id: str) -> None:
    """刪除任務"""
    if task_id in tasks:
        del tasks[task_id]

def task_exists(task_id: str) -> bool:
    """檢查任務是否存在"""
    return task_id in tasks
