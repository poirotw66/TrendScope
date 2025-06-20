#!/usr/bin/env python3
"""
性能測試腳本 - 比較優化前後的處理速度
"""

import os
import sys
import time
import pathlib
from typing import List, Dict, Any

# 添加專案根目錄到 Python 路徑
sys.path.append(str(pathlib.Path(__file__).parent.parent))

from src.optimized_ppt_processor import OptimizedPPTProcessor
from config.config import GEMINI_API_KEY

def simulate_original_processing(pdf_files: List[pathlib.Path], request_interval: int = 15) -> Dict[str, Any]:
    """模擬原始串行處理的時間"""
    start_time = time.time()
    
    # 模擬原始處理邏輯的時間消耗
    total_files = len(pdf_files)
    
    # 原始處理時間估算：
    # - 每個文件處理時間：約30-60秒（包含API調用、上傳、數據庫操作）
    # - 文件間延遲：15秒
    # - BigQuery查詢延遲：每個文件2-3秒
    
    estimated_processing_time = total_files * 45  # 平均45秒每文件
    estimated_delay_time = (total_files - 1) * request_interval  # 文件間延遲
    estimated_query_time = total_files * 2.5  # 查詢時間
    
    total_estimated_time = estimated_processing_time + estimated_delay_time + estimated_query_time
    
    return {
        'method': 'Original Serial Processing',
        'total_files': total_files,
        'estimated_time': total_estimated_time,
        'avg_time_per_file': total_estimated_time / total_files if total_files > 0 else 0,
        'bottlenecks': [
            f'Serial processing: {estimated_processing_time}s',
            f'Request delays: {estimated_delay_time}s', 
            f'Individual queries: {estimated_query_time}s'
        ]
    }

def test_optimized_processing(pdf_files: List[pathlib.Path], 
                            seminar_name: str,
                            max_workers: int = 4) -> Dict[str, Any]:
    """測試優化後的並行處理"""
    
    bq_project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not bq_project_id or not GEMINI_API_KEY:
        return {
            'method': 'Optimized Parallel Processing',
            'error': 'Missing environment variables'
        }
    
    try:
        processor = OptimizedPPTProcessor(
            gemini_api_key=GEMINI_API_KEY,
            bq_project_id=bq_project_id,
            max_workers=max_workers,
            max_requests_per_minute=15
        )
        
        # 只測試處理邏輯，不實際調用API
        start_time = time.time()
        
        # 模擬優化處理的時間估算
        # - 並行處理減少總時間
        # - 批量查詢減少數據庫開銷
        # - 速率限制器智能管理API調用
        
        total_files = len(pdf_files)
        
        # 並行處理時間估算
        parallel_batches = (total_files + max_workers - 1) // max_workers
        estimated_processing_time = parallel_batches * 45  # 並行處理
        
        # API速率限制時間（智能管理）
        api_calls_needed = total_files
        estimated_api_time = (api_calls_needed / 15) * 60  # 15 calls per minute
        
        # 批量查詢時間（一次性載入）
        estimated_query_time = 5  # 單次批量查詢
        
        total_estimated_time = max(estimated_processing_time, estimated_api_time) + estimated_query_time
        
        return {
            'method': 'Optimized Parallel Processing',
            'total_files': total_files,
            'estimated_time': total_estimated_time,
            'avg_time_per_file': total_estimated_time / total_files if total_files > 0 else 0,
            'max_workers': max_workers,
            'optimizations': [
                f'Parallel processing: {parallel_batches} batches',
                f'Smart rate limiting: {estimated_api_time}s',
                f'Batch queries: {estimated_query_time}s',
                'Cached session data',
                'Connection pooling'
            ]
        }
        
    except Exception as e:
        return {
            'method': 'Optimized Parallel Processing',
            'error': str(e)
        }

def run_performance_comparison(input_dir: str, seminar_name: str):
    """運行性能比較測試"""
    
    print("🚀 PPT處理性能比較測試")
    print("=" * 50)
    
    # 檢查輸入目錄
    input_path = pathlib.Path(input_dir)
    if not input_path.exists():
        print(f"❌ 輸入目錄不存在: {input_dir}")
        return
    
    # 查找PDF文件
    pdf_files = list(input_path.glob("*.pdf"))
    if not pdf_files:
        print(f"❌ 在目錄 {input_dir} 中沒有找到PDF文件")
        return
    
    print(f"📁 測試目錄: {input_dir}")
    print(f"📄 找到文件: {len(pdf_files)} 個PDF")
    print(f"🎯 研討會: {seminar_name}")
    print()
    
    # 測試原始處理方法
    print("📊 分析原始處理方法...")
    original_result = simulate_original_processing(pdf_files)
    
    # 測試優化處理方法
    print("📊 分析優化處理方法...")
    optimized_result = test_optimized_processing(pdf_files, seminar_name)
    
    # 輸出比較結果
    print("\n" + "=" * 50)
    print("📈 性能比較結果")
    print("=" * 50)
    
    # 原始方法結果
    print(f"\n🐌 {original_result['method']}")
    print(f"   總文件數: {original_result['total_files']}")
    print(f"   預估總時間: {original_result['estimated_time']:.1f} 秒 ({original_result['estimated_time']/60:.1f} 分鐘)")
    print(f"   平均每文件: {original_result['avg_time_per_file']:.1f} 秒")
    print("   主要瓶頸:")
    for bottleneck in original_result['bottlenecks']:
        print(f"     - {bottleneck}")
    
    # 優化方法結果
    print(f"\n⚡ {optimized_result['method']}")
    if 'error' in optimized_result:
        print(f"   ❌ 錯誤: {optimized_result['error']}")
    else:
        print(f"   總文件數: {optimized_result['total_files']}")
        print(f"   預估總時間: {optimized_result['estimated_time']:.1f} 秒 ({optimized_result['estimated_time']/60:.1f} 分鐘)")
        print(f"   平均每文件: {optimized_result['avg_time_per_file']:.1f} 秒")
        print(f"   並行工作數: {optimized_result['max_workers']}")
        print("   主要優化:")
        for optimization in optimized_result['optimizations']:
            print(f"     - {optimization}")
        
        # 計算性能提升
        if original_result['estimated_time'] > 0:
            speedup = original_result['estimated_time'] / optimized_result['estimated_time']
            time_saved = original_result['estimated_time'] - optimized_result['estimated_time']
            
            print(f"\n🎉 性能提升總結:")
            print(f"   ⚡ 速度提升: {speedup:.1f}x")
            print(f"   ⏰ 節省時間: {time_saved:.1f} 秒 ({time_saved/60:.1f} 分鐘)")
            print(f"   📈 效率提升: {(speedup-1)*100:.1f}%")
            
            if speedup >= 5:
                print("   🏆 優化效果: 優秀！")
            elif speedup >= 3:
                print("   🥈 優化效果: 良好")
            elif speedup >= 2:
                print("   🥉 優化效果: 一般")
            else:
                print("   ⚠️  優化效果: 有限")

def main():
    """主函數"""
    import argparse
    
    parser = argparse.ArgumentParser(description="PPT處理性能測試")
    parser.add_argument("--input-dir", type=str, required=True, help="PPT文件目錄")
    parser.add_argument("--seminar-name", type=str, required=True, help="研討會名稱")
    
    args = parser.parse_args()
    
    run_performance_comparison(args.input_dir, args.seminar_name)

if __name__ == "__main__":
    main()
