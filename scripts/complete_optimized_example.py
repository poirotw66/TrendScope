#!/usr/bin/env python3
"""
完整的優化PPT處理示例
展示所有優化功能的使用方法
"""

import os
import sys
import pathlib
import argparse
import time
from typing import List

# 添加專案根目錄到 Python 路徑
sys.path.append(str(pathlib.Path(__file__).parent.parent))

from src.optimized_ppt_processor import OptimizedPPTProcessor
from src.performance_monitor import PerformanceMonitor
from src.file_processor_optimizer import OptimizedFileProcessor
from config.config import GEMINI_API_KEY

def main():
    """主函數 - 完整的優化處理流程"""
    parser = argparse.ArgumentParser(description="完整優化PPT處理示例")
    parser.add_argument("--input-dir", type=str, required=True, help="PPT文件目錄")
    parser.add_argument("--seminar-name", type=str, required=True, help="研討會名稱")
    parser.add_argument("--max-workers", type=int, default=4, help="最大並行工作數")
    parser.add_argument("--rate-limit", type=int, default=15, help="每分鐘最大API請求數")
    parser.add_argument("--enable-cache", action="store_true", help="啟用文件緩存")
    parser.add_argument("--performance-report", type=str, help="性能報告輸出文件")
    parser.add_argument("--dry-run", action="store_true", help="只分析不實際處理")
    
    args = parser.parse_args()
    
    print("🚀 完整優化PPT處理系統")
    print("=" * 60)
    
    # 檢查環境變數
    bq_project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not bq_project_id:
        print("❌ 請設置 GOOGLE_CLOUD_PROJECT 環境變數")
        return 1
    
    if not GEMINI_API_KEY:
        print("❌ 請設置 GEMINI_API_KEY")
        return 1
    
    # 檢查輸入目錄
    input_dir = pathlib.Path(args.input_dir)
    if not input_dir.exists():
        print(f"❌ 輸入目錄不存在: {input_dir}")
        return 1
    
    # 初始化性能監控
    print("📊 初始化性能監控...")
    monitor = PerformanceMonitor(monitoring_interval=0.5)
    
    try:
        with monitor.monitor_operation("complete_processing", 
                                     input_dir=str(input_dir),
                                     seminar_name=args.seminar_name):
            
            # 步驟1: 文件分析和優化
            print("\n📁 步驟1: 文件分析和優化")
            print("-" * 40)
            
            with monitor.monitor_operation("file_analysis"):
                file_processor = OptimizedFileProcessor(cache_enabled=args.enable_cache)
                
                # 查找所有PDF文件
                pdf_files = list(input_dir.glob("*.pdf"))
                if not pdf_files:
                    print(f"❌ 沒有找到PDF文件")
                    return 1
                
                print(f"📄 找到 {len(pdf_files)} 個PDF文件")
                
                # 批量獲取文件信息
                file_infos = file_processor.batch_get_file_info(pdf_files)
                
                # 文件過濾
                filtered_files = file_processor.filter_files_by_size(
                    file_infos, 
                    min_size=1024,  # 1KB
                    max_size=50 * 1024 * 1024  # 50MB
                )
                
                # 優化處理順序
                optimized_files = file_processor.optimize_upload_order(filtered_files)
                
                # 獲取處理統計
                stats = file_processor.get_processing_stats(optimized_files)
                
                print(f"✅ 文件分析完成:")
                print(f"   - 有效文件: {stats['total_files']}")
                print(f"   - 總大小: {stats['total_size_mb']:.1f} MB")
                print(f"   - 平均大小: {stats['avg_size_mb']:.1f} MB")
                print(f"   - 預估上傳時間: {stats['estimated_upload_time']:.1f} 秒")
                print(f"   - 大小分布: 小({stats['size_distribution']['small']}) "
                      f"中({stats['size_distribution']['medium']}) "
                      f"大({stats['size_distribution']['large']})")
            
            if args.dry_run:
                print("\n🔍 乾運行模式 - 僅分析，不實際處理")
                return 0
            
            # 步驟2: 初始化PPT處理器
            print("\n⚡ 步驟2: 初始化優化處理器")
            print("-" * 40)
            
            with monitor.monitor_operation("processor_initialization"):
                processor = OptimizedPPTProcessor(
                    gemini_api_key=GEMINI_API_KEY,
                    bq_project_id=bq_project_id,
                    max_workers=args.max_workers,
                    max_requests_per_minute=args.rate_limit
                )
                
                print(f"✅ 處理器初始化完成:")
                print(f"   - 並行工作數: {args.max_workers}")
                print(f"   - API速率限制: {args.rate_limit}/分鐘")
                print(f"   - 文件緩存: {'啟用' if args.enable_cache else '禁用'}")
            
            # 步驟3: 執行優化處理
            print("\n🔄 步驟3: 執行優化處理")
            print("-" * 40)
            
            with monitor.monitor_operation("ppt_processing"):
                # 使用優化的文件路徑列表
                optimized_paths = [info.path for info in optimized_files]
                
                # 選擇處理模式
                if len(optimized_paths) <= 20:
                    print("使用目錄處理模式")
                    stats = processor.process_directory(
                        input_dir=input_dir,
                        seminar_name=args.seminar_name,
                        file_pattern="*.pdf"
                    )
                else:
                    print("使用分批處理模式")
                    stats = processor.process_files_batch(
                        pdf_files=optimized_paths,
                        seminar_name=args.seminar_name,
                        batch_size=10
                    )
                
                print(f"\n✅ 處理完成:")
                print(f"   - 總文件數: {stats.total_files}")
                print(f"   - 成功: {stats.successful}")
                print(f"   - 失敗: {stats.failed}")
                print(f"   - 成功率: {stats.successful/stats.total_files*100:.1f}%")
                print(f"   - 總耗時: {stats.total_time:.1f} 秒")
                print(f"   - 平均每文件: {stats.avg_time_per_file:.1f} 秒")
            
            # 步驟4: 性能分析
            print("\n📈 步驟4: 性能分析")
            print("-" * 40)
            
            # 獲取性能摘要
            perf_summary = monitor.get_metrics_summary(last_n_minutes=10)
            op_summary = monitor.get_operation_summary()
            
            if perf_summary:
                print(f"系統性能:")
                print(f"   - CPU平均使用率: {perf_summary['cpu']['avg']:.1f}%")
                print(f"   - CPU峰值使用率: {perf_summary['cpu']['max']:.1f}%")
                print(f"   - 內存平均使用率: {perf_summary['memory']['avg']:.1f}%")
                print(f"   - 當前內存使用: {perf_summary['memory']['current_used_mb']:.1f} MB")
            
            if op_summary:
                print(f"操作統計:")
                print(f"   - 總操作數: {op_summary['total_operations']}")
                print(f"   - 成功率: {op_summary['success_rate']:.1f}%")
                if 'timing' in op_summary:
                    print(f"   - 平均耗時: {op_summary['timing']['avg_duration']:.2f} 秒")
                    print(f"   - 總耗時: {op_summary['timing']['total_duration']:.1f} 秒")
            
            # 計算效率提升
            if stats.total_files > 0:
                # 估算原始串行處理時間
                original_time = stats.total_files * 45 + (stats.total_files - 1) * 15
                speedup = original_time / stats.total_time if stats.total_time > 0 else 1
                
                print(f"\n🎉 效率提升:")
                print(f"   - 原始預估時間: {original_time:.1f} 秒 ({original_time/60:.1f} 分鐘)")
                print(f"   - 優化後實際時間: {stats.total_time:.1f} 秒 ({stats.total_time/60:.1f} 分鐘)")
                print(f"   - 速度提升: {speedup:.1f}x")
                print(f"   - 節省時間: {original_time - stats.total_time:.1f} 秒")
        
        # 導出性能報告
        if args.performance_report:
            print(f"\n📋 導出性能報告到: {args.performance_report}")
            monitor.export_report(pathlib.Path(args.performance_report))
        
        print(f"\n🎊 處理完成！")
        return 0
        
    except KeyboardInterrupt:
        print("\n⚠️ 用戶中斷處理")
        return 1
    except Exception as e:
        print(f"\n❌ 處理過程中發生錯誤: {e}")
        return 1
    finally:
        # 停止性能監控
        monitor.stop_monitoring()

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
