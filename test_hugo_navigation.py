#!/usr/bin/env python3
"""
測試 Hugo 靜態網站生成器的完整三階層導航系統
"""

import os
import sys
import tempfile
import pathlib
import logging
from datetime import datetime

# 添加項目根目錄到 Python 路徑
sys.path.append(os.path.join(os.path.dirname(__file__)))

from base.api.modules.hugo_report import HugoReportGenerator, ReportMetadata

# 設置日誌
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_test_markdown_files(md_dir: pathlib.Path):
    """創建測試用的 Markdown 文件"""
    
    # 創建測試數據
    test_reports = [
        {
            "title": "AI 大模型技術發展趨勢",
            "seminar": "QCon Beijing 2024",
            "category": "主題演講",
            "trends": ["人工智能", "大語言模型", "機器學習"],
            "content": """
# AI 大模型技術發展趨勢

## 技術背景
大語言模型（LLM）正在重塑整個 AI 領域，從 GPT 系列到各種開源模型，技術發展日新月異。

## 核心洞察
- **模型規模持續增長**：參數量從億級發展到萬億級
- **多模態融合**：文本、圖像、音頻的統一處理
- **推理能力提升**：從簡單對話到複雜推理

## 實踐經驗
企業在部署大模型時需要考慮成本、效率和安全性的平衡。
            """
        },
        {
            "title": "雲原生架構最佳實踐",
            "seminar": "KubeCon China 2024",
            "category": "技術分享",
            "trends": ["雲原生", "Kubernetes", "微服務"],
            "content": """
# 雲原生架構最佳實踐

## 技術背景
雲原生技術棧已成為現代應用開發的標準，Kubernetes 生態系統不斷完善。

## 核心洞察
- **容器化部署**：標準化的應用打包和部署
- **服務網格**：微服務間通信的統一管理
- **可觀測性**：全鏈路監控和故障排查

## 實踐經驗
從單體應用到微服務的遷移需要循序漸進，避免過度拆分。
            """
        },
        {
            "title": "前端框架演進與選型",
            "seminar": "JSConf China 2024",
            "category": "技術分享",
            "trends": ["前端開發", "React", "Vue.js", "性能優化"],
            "content": """
# 前端框架演進與選型

## 技術背景
前端技術生態快速發展，新框架和工具層出不窮。

## 核心洞察
- **組件化開發**：可復用的 UI 組件庫
- **狀態管理**：複雜應用的數據流控制
- **性能優化**：首屏加載和運行時性能

## 實踐經驗
選擇前端框架需要考慮團隊技能、項目需求和長期維護。
            """
        },
        {
            "title": "數據庫技術新趨勢",
            "seminar": "QCon Beijing 2024",
            "category": "深度技術",
            "trends": ["數據庫", "分佈式系統", "OLAP"],
            "content": """
# 數據庫技術新趨勢

## 技術背景
數據庫技術正在向分佈式、雲原生方向發展。

## 核心洞察
- **分佈式架構**：水平擴展和高可用
- **多模型支持**：關係型、文檔、圖數據庫融合
- **實時分析**：OLTP 和 OLAP 的統一

## 實踐經驗
選擇數據庫需要根據業務場景和數據特點進行權衡。
            """
        },
        {
            "title": "DevOps 文化與實踐",
            "seminar": "DevOpsDays Shanghai 2024",
            "category": "文化實踐",
            "trends": ["DevOps", "CI/CD", "自動化"],
            "content": """
# DevOps 文化與實踐

## 技術背景
DevOps 不僅是技術實踐，更是組織文化的變革。

## 核心洞察
- **持續集成**：自動化的代碼集成和測試
- **持續部署**：快速、可靠的發布流程
- **監控反饋**：生產環境的實時監控

## 實踐經驗
DevOps 轉型需要技術、流程和文化的全面配合。
            """
        }
    ]
    
    # 創建 Markdown 文件
    for i, report in enumerate(test_reports):
        filename = f"report_{i+1:03d}.md"
        filepath = md_dir / filename
        
        # 創建 front matter
        front_matter = f"""---
title: "{report['title']}"
seminar: "{report['seminar']}"
category: "{report['category']}"
date: "{datetime.now().strftime('%Y-%m-%d')}"
trends: {report['trends']}
tags: ["技術分析", "會議報告"]
---
{report['content']}
"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(front_matter)
        
        logger.info(f"✅ 創建測試文件: {filename}")

def test_hugo_navigation_system():
    """測試 Hugo 導航系統"""
    logger.info("🚀 開始測試 Hugo 三階層導航系統...")
    
    # 創建臨時目錄
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = pathlib.Path(temp_dir)
        md_dir = temp_path / "markdown"
        html_dir = temp_path / "html"
        
        # 創建目錄
        md_dir.mkdir(parents=True)
        html_dir.mkdir(parents=True)
        
        # 創建測試 Markdown 文件
        logger.info("📝 創建測試 Markdown 文件...")
        create_test_markdown_files(md_dir)
        
        # 初始化 Hugo 生成器
        logger.info("🏗️ 初始化 Hugo 生成器...")
        generator = HugoReportGenerator()
        
        # 生成 Hugo 靜態網站
        logger.info("🌐 生成 Hugo 靜態網站...")
        result = generator.generate_hugo_site(
            md_dir=str(md_dir),
            html_dir=str(html_dir),
            template_style="professional",
            create_offline_package=True
        )
        
        # 檢查生成結果
        logger.info("🔍 檢查生成結果...")
        
        # 檢查 HTML 文件
        html_files = list(html_dir.rglob("*.html"))
        logger.info(f"📄 生成了 {len(html_files)} 個 HTML 文件")
        
        # 檢查關鍵文件
        key_files = [
            "index.html",  # 首頁
            "trends/index.html",  # 技術趨勢列表
            "seminars/index.html",  # 研討會列表
            "sessions/index.html",  # 會議報告列表
        ]
        
        for key_file in key_files:
            file_path = html_dir / key_file
            if file_path.exists():
                logger.info(f"✅ 關鍵文件存在: {key_file}")
                
                # 檢查文件內容
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 檢查導航元素
                navigation_elements = [
                    'class="site-header"',  # 主導航
                    'class="breadcrumb"',   # 麵包屑（非首頁）
                    'class="nav-buttons"',  # 上一頁/下一頁
                    'class="related-content"',  # 相關內容
                    'class="back-to-top"',  # 返回頂部（JavaScript 生成）
                ]
                
                found_elements = []
                for element in navigation_elements:
                    if element in content:
                        found_elements.append(element)
                
                logger.info(f"   📋 {key_file} 包含導航元素: {len(found_elements)}/{len(navigation_elements)}")
                
                # 檢查連結
                link_patterns = [
                    'href="/',  # 內部連結
                    'class="nav-link"',  # 導航連結
                    'class="trend-tag"',  # 趨勢標籤連結
                    'class="seminar-link"',  # 研討會連結
                ]
                
                found_links = []
                for pattern in link_patterns:
                    if pattern in content:
                        found_links.append(pattern)
                
                logger.info(f"   🔗 {key_file} 包含連結類型: {len(found_links)}/{len(link_patterns)}")
                
            else:
                logger.warning(f"❌ 關鍵文件缺失: {key_file}")
        
        # 檢查靜態資源
        css_files = list(html_dir.rglob("*.css"))
        js_files = list(html_dir.rglob("*.js"))
        
        logger.info(f"🎨 CSS 文件: {len(css_files)}")
        logger.info(f"⚡ JavaScript 文件: {len(js_files)}")
        
        # 檢查離線包
        if "zip_file" in result:
            logger.info(f"📦 離線包已創建: {result['zip_file']}")
        
        if "launcher_file" in result:
            logger.info(f"🚀 啟動器已創建: {result['launcher_file']}")
        
        # 輸出結果摘要
        logger.info("📊 測試結果摘要:")
        logger.info(f"   📂 輸出目錄: {html_dir}")
        logger.info(f"   📄 HTML 文件數: {len(html_files)}")
        logger.info(f"   🎨 CSS 文件數: {len(css_files)}")
        logger.info(f"   ⚡ JS 文件數: {len(js_files)}")
        
        # 保存測試結果到用戶可訪問的位置
        user_output_dir = pathlib.Path.home() / "Desktop" / "hugo_navigation_test"
        if user_output_dir.exists():
            import shutil
            shutil.rmtree(user_output_dir)
        
        import shutil
        shutil.copytree(html_dir, user_output_dir)
        logger.info(f"💾 測試結果已保存到: {user_output_dir}")
        
        return result

if __name__ == "__main__":
    try:
        result = test_hugo_navigation_system()
        logger.info("✅ Hugo 三階層導航系統測試完成!")
        
        # 提示用戶如何查看結果
        output_dir = pathlib.Path.home() / "Desktop" / "hugo_navigation_test"
        logger.info(f"🌐 請打開瀏覽器訪問: file://{output_dir}/index.html")
        
    except Exception as e:
        logger.error(f"❌ 測試失敗: {e}")
        import traceback
        traceback.print_exc()
