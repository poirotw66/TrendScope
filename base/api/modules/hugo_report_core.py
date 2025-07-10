#!/usr/bin/env python3
"""
Hugo 報告生成器核心功能
包含元數據提取、內容創建、構建等核心方法
"""

import pathlib
import subprocess
import zipfile
import logging
import re
import unicodedata
from typing import List, Dict, Any, Optional
from datetime import datetime
from dataclasses import asdict

logger = logging.getLogger(__name__)

class HugoReportCore:
    """Hugo 報告生成器核心功能類"""
    
    def _extract_metadata_from_content(self, content: str, filename: str):
        """從內容中提取元數據"""
        import re
        from .hugo_report import ReportMetadata

        # 嘗試從內容中提取標題
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else filename

        # 嘗試從內容中提取研討會信息
        seminar_match = re.search(r'研討會[：:]\s*\*?\*?(.+?)\*?\*?$', content, re.MULTILINE)
        seminar = seminar_match.group(1).strip() if seminar_match else "未知研討會"

        # 嘗試從內容中提取類型信息
        category_match = re.search(r'類型[：:]\s*\*?\*?(.+?)\*?\*?$', content, re.MULTILINE)
        category = category_match.group(1).strip() if category_match else "主題演講"

        # 嘗試從內容中提取 URL
        url_match = re.search(r'來源[：:]\s*\[(.+?)\]\((.+?)\)', content)
        url = url_match.group(2) if url_match else ""

        # 生成標籤和趨勢
        tags = self._generate_tags_from_content(content, seminar, category)
        trends = self._extract_trends_from_content(content)

        return ReportMetadata(
            title=title,
            seminar=seminar,
            category=category,
            url=url,
            session_id=filename,
            tags=tags,
            trends=trends
        )

    def _generate_tags_from_content(self, content: str, seminar: str, category: str) -> List[str]:
        """從內容生成標籤"""
        tags = []

        # 添加研討會作為標籤
        if seminar and seminar != "未知研討會":
            tags.append(seminar)

        # 添加類型作為標籤
        if category:
            tags.append(category)

        # 從內容中提取技術關鍵詞
        tech_keywords = [
            "AI", "人工智慧", "機器學習", "深度學習", "神經網路",
            "雲端", "雲計算", "容器", "微服務", "Kubernetes",
            "區塊鏈", "加密貨幣", "NFT", "Web3",
            "大數據", "數據分析", "數據科學", "數據庫",
            "前端", "後端", "全端", "React", "Vue", "Angular",
            "Python", "JavaScript", "Java", "Go", "Rust",
            "DevOps", "CI/CD", "自動化", "測試",
            "安全", "資安", "隱私", "加密",
            "物聯網", "IoT", "邊緣計算", "5G"
        ]

        for keyword in tech_keywords:
            if keyword in content:
                tags.append(keyword)

        # 限制標籤數量並去重
        return list(set(tags))[:10]

    def _extract_trends_from_content(self, content: str) -> List[str]:
        """從內容中提取技術趨勢"""
        trends = []

        # 技術趨勢關鍵詞映射
        trend_keywords = {
            "人工智能": ["AI", "人工智能", "機器學習", "深度學習", "神經網絡", "大模型", "LLM", "GPT"],
            "雲原生": ["雲原生", "Cloud Native", "Kubernetes", "Docker", "容器", "微服務", "服務網格"],
            "前端開發": ["前端", "React", "Vue", "Angular", "JavaScript", "TypeScript", "Web開發"],
            "數據庫": ["數據庫", "MySQL", "PostgreSQL", "MongoDB", "Redis", "分佈式數據庫", "OLAP", "OLTP"],
            "DevOps": ["DevOps", "CI/CD", "持續集成", "持續部署", "自動化", "監控"],
            "大數據": ["大數據", "Spark", "Hadoop", "數據分析", "數據挖掘", "數據科學"],
            "區塊鏈": ["區塊鏈", "比特幣", "以太坊", "智能合約", "DeFi", "NFT"],
            "物聯網": ["物聯網", "IoT", "邊緣計算", "傳感器", "智能設備"],
            "安全": ["網絡安全", "信息安全", "加密", "身份認證", "零信任"],
            "性能優化": ["性能優化", "性能調優", "緩存", "負載均衡", "高並發"]
        }

        content_lower = content.lower()
        for trend, keywords in trend_keywords.items():
            if any(keyword.lower() in content_lower for keyword in keywords):
                trends.append(trend)

        return list(set(trends))  # 去重

    def _create_hugo_content(self, content: str, metadata) -> str:
        """創建 Hugo 內容文件"""
        # 創建 Front Matter
        front_matter = {
            "title": metadata.title,
            "date": metadata.date,
            "draft": False,
            "seminar": metadata.seminar,
            "category": metadata.category,
            "tags": metadata.tags,
            "trends": metadata.trends
        }

        if metadata.url:
            front_matter["url"] = metadata.url

        # 轉換為 YAML 格式
        import yaml
        front_matter_yaml = yaml.dump(front_matter, default_flow_style=False, allow_unicode=True)

        # 移除內容中的原始元數據行
        content_lines = content.split('\n')
        filtered_lines = []
        
        for line in content_lines:
            # 跳過包含元數據的行
            if not any(keyword in line for keyword in ['研討會：', '類型：', '來源：', '講者：']):
                filtered_lines.append(line)

        clean_content = '\n'.join(filtered_lines).strip()

        # 組合最終內容
        hugo_content = f"---\n{front_matter_yaml}---\n\n{clean_content}"
        
        return hugo_content

    def _slugify(self, text: str) -> str:
        """將文本轉換為 URL 友好的 slug"""
        import re
        import unicodedata

        # 移除特殊字符，保留中文、英文、數字
        text = re.sub(r'[^\w\s-]', '', text)
        text = re.sub(r'[-\s]+', '-', text)
        text = text.strip('-').lower()
        
        return text or "unknown"

    def _build_hugo_site(self, site_dir: pathlib.Path, output_dir: str) -> bool:
        """構建 Hugo 靜態網站"""
        try:
            # 確保輸出目錄存在
            output_path = pathlib.Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)

            if not self.hugo_binary:
                logger.warning("Hugo 二進制文件不可用，跳過 Hugo 構建")
                return False

            # 執行 Hugo 構建命令
            cmd = [
                self.hugo_binary,
                "--source", str(site_dir),
                "--destination", str(output_path),
                "--minify",
                "--gc"
            ]

            logger.info(f"🔨 執行 Hugo 構建: {' '.join(cmd)}")
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=site_dir,
                timeout=300  # 5分鐘超時
            )

            if result.returncode == 0:
                logger.info("✅ Hugo 網站構建成功")
                logger.info(f"Hugo 輸出: {result.stdout}")
                return True
            else:
                logger.error(f"❌ Hugo 構建失敗: {result.stderr}")
                return False

        except subprocess.TimeoutExpired:
            logger.error("❌ Hugo 構建超時")
            return False
        except Exception as e:
            logger.error(f"❌ Hugo 構建過程中發生錯誤: {e}")
            return False

    def _generate_static_files_fallback(self, site_dir: pathlib.Path, output_dir: str):
        """備用靜態文件生成方法（當 Hugo 不可用時）"""
        try:
            logger.info("🔄 使用備用方法生成靜態文件...")
            
            output_path = pathlib.Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            
            # 複製靜態資源
            static_dir = site_dir / "static"
            if static_dir.exists():
                import shutil
                for item in static_dir.iterdir():
                    if item.is_file():
                        shutil.copy2(item, output_path / item.name)
                    elif item.is_dir():
                        shutil.copytree(item, output_path / item.name, dirs_exist_ok=True)
            
            # 生成基本的 HTML 文件
            self._generate_basic_html_files(site_dir, output_path)
            
            logger.info("✅ 備用靜態文件生成完成")
            
        except Exception as e:
            logger.error(f"❌ 備用靜態文件生成失敗: {e}")

    def _generate_basic_html_files(self, site_dir: pathlib.Path, output_path: pathlib.Path):
        """生成基本的 HTML 文件"""
        try:
            content_dir = site_dir / "content"
            
            # 生成首頁
            index_html = """<!DOCTYPE html>
<html lang="zh-tw">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TrendScope 技術趨勢分析</title>
    <link rel="stylesheet" href="css/styles.css">
</head>
<body>
    <header class="site-header">
        <div class="container">
            <nav class="navbar">
                <div class="nav-brand">
                    <a href="/">TrendScope</a>
                </div>
            </nav>
        </div>
    </header>
    
    <main>
        <div class="container">
            <section class="hero">
                <h1 class="hero-title">TrendScope 技術趨勢分析</h1>
                <p class="hero-subtitle">深度技術趨勢分析與會議洞察</p>
            </section>
            
            <section class="content-section">
                <h2 class="section-title">歡迎使用 TrendScope</h2>
                <p>探索最新的技術趨勢，深入了解行業發展動向。</p>
            </section>
        </div>
    </main>
    
    <footer class="site-footer">
        <div class="container">
            <p>&copy; 2025 TrendScope. 由 TrendScope 技術趨勢分析系統生成。</p>
        </div>
    </footer>
    
    <script src="js/main.js"></script>
</body>
</html>"""
            
            with open(output_path / "index.html", 'w', encoding='utf-8') as f:
                f.write(index_html)
            
            logger.info("✅ 基本 HTML 文件生成完成")
            
        except Exception as e:
            logger.error(f"❌ 基本 HTML 文件生成失敗: {e}")

    def _fix_offline_paths(self, output_dir: str):
        """修復離線瀏覽的路徑問題 - 增強版"""
        try:
            output_path = pathlib.Path(output_dir)
            logger.info("開始修復離線瀏覽路徑...")

            # 遍歷所有 HTML 文件
            for html_file in output_path.rglob("*.html"):
                if html_file.is_file():
                    # 計算相對於根目錄的深度
                    relative_path = html_file.relative_to(output_path)
                    depth = len(relative_path.parts) - 1
                    
                    success = self._fix_html_file_paths(html_file, depth)
                    if success:
                        logger.debug(f"✅ 修復路徑: {relative_path}")

            logger.info("✅ 離線瀏覽路徑修復完成")

        except Exception as e:
            logger.error(f"❌ 修復離線瀏覽路徑失敗: {e}")
            raise

    def _fix_html_file_paths(self, html_file: pathlib.Path, depth: int) -> bool:
        """修復單個 HTML 文件的路徑 - 增強版"""
        try:
            # 讀取文件內容
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # 生成相對路徑前綴
            if depth == 0:
                path_prefix = ""
            else:
                path_prefix = "../" * depth

            # 修復各種類型的路徑
            # 1. CSS 文件路徑
            content = re.sub(
                r'href=["\']/?css/',
                f'href="{path_prefix}css/',
                content
            )

            # 2. JavaScript 文件路徑
            content = re.sub(
                r'src=["\']/?js/',
                f'src="{path_prefix}js/',
                content
            )

            # 3. 圖片文件路徑
            content = re.sub(
                r'src=["\']/?images/',
                f'src="{path_prefix}images/',
                content
            )

            # 4. 內部頁面連結
            content = re.sub(
                r'href=["\']/',
                f'href="{path_prefix}',
                content
            )

            # 寫回文件
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)

            return True

        except Exception as e:
            logger.error(f"❌ 修復 HTML 文件路徑失敗 {html_file}: {e}")
            return False

    def _collect_site_info(self, md_dir: str, output_dir: str, html_files: List[str]) -> Dict[str, Any]:
        """收集網站信息"""
        try:
            md_path = pathlib.Path(md_dir)
            output_path = pathlib.Path(output_dir)

            # 統計信息
            total_files = len(list(output_path.rglob("*"))) if output_path.exists() else 0
            html_count = len(html_files)
            css_files = len(list(output_path.rglob("*.css"))) if output_path.exists() else 0
            js_files = len(list(output_path.rglob("*.js"))) if output_path.exists() else 0

            # 計算總大小
            total_size = 0
            if output_path.exists():
                for file_path in output_path.rglob("*"):
                    if file_path.is_file():
                        total_size += file_path.stat().st_size

            site_info = {
                "title": "TrendScope 技術趨勢分析",
                "description": "深度技術趨勢分析與會議洞察",
                "generated_at": datetime.now().isoformat(),
                "source_dir": str(md_path),
                "output_dir": str(output_path),
                "statistics": {
                    "total_files": total_files,
                    "html_files": html_count,
                    "css_files": css_files,
                    "js_files": js_files,
                    "total_size_bytes": total_size,
                    "total_size_mb": round(total_size / (1024 * 1024), 2)
                },
                "html_files": html_files
            }

            return site_info

        except Exception as e:
            logger.error(f"❌ 收集網站信息失敗: {e}")
            return {
                "title": "TrendScope 技術趨勢分析",
                "description": "深度技術趨勢分析與會議洞察",
                "generated_at": datetime.now().isoformat(),
                "error": str(e)
            }

    def _create_offline_zip_package(self, output_dir: str, site_info: Dict[str, Any]) -> str:
        """創建離線 ZIP 分享包"""
        try:
            output_path = pathlib.Path(output_dir)
            parent_dir = output_path.parent

            # 生成 ZIP 文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            zip_filename = f"TrendScope-會議報告-{timestamp}.zip"
            zip_file_path = parent_dir / zip_filename

            logger.info(f"📦 創建離線 ZIP 包: {zip_filename}")

            # 使用 Python 內建的 zipfile 模組
            with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # 遍歷輸出目錄中的所有文件
                for file_path in output_path.rglob('*'):
                    if file_path.is_file():
                        # 跳過隱藏文件和系統文件
                        if file_path.name.startswith('.') or file_path.name == '.DS_Store':
                            continue

                        # 計算在 ZIP 中的相對路徑
                        arcname = file_path.relative_to(output_path)
                        zipf.write(file_path, arcname)

            logger.info(f"✅ ZIP 包創建完成: {zip_file_path}")
            logger.info(f"   📊 文件大小: {zip_file_path.stat().st_size / (1024*1024):.2f} MB")

            return str(zip_file_path)

        except Exception as e:
            logger.error(f"❌ 創建 ZIP 包失敗: {e}")
            return ""

    def _generate_html_launcher(self, output_dir: str, site_info: Dict[str, Any]) -> str:
        """生成 HTML 啟動器文件"""
        try:
            output_path = pathlib.Path(output_dir)
            launcher_file = output_path.parent / "啟動報告.html"

            launcher_content = f"""<!DOCTYPE html>
<html lang="zh-tw">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TrendScope 報告啟動器</title>
    <style>
        body {{ font-family: 'Microsoft JhengHei', sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }}
        .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #3a86ff; text-align: center; }}
        .info {{ background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0; }}
        .launch-btn {{ display: block; width: 200px; margin: 20px auto; padding: 15px; background: #3a86ff; color: white; text-align: center; text-decoration: none; border-radius: 5px; font-weight: bold; }}
        .launch-btn:hover {{ background: #2f6bff; }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; margin: 20px 0; }}
        .stat {{ text-align: center; padding: 10px; background: #e3f2fd; border-radius: 5px; }}
        .stat-number {{ font-size: 24px; font-weight: bold; color: #1976d2; }}
        .stat-label {{ font-size: 12px; color: #666; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 TrendScope 技術趨勢分析報告</h1>
        
        <div class="info">
            <h3>📊 報告統計</h3>
            <div class="stats">
                <div class="stat">
                    <div class="stat-number">{site_info.get('statistics', {}).get('html_files', 0)}</div>
                    <div class="stat-label">HTML 頁面</div>
                </div>
                <div class="stat">
                    <div class="stat-number">{site_info.get('statistics', {}).get('total_size_mb', 0)}</div>
                    <div class="stat-label">總大小 (MB)</div>
                </div>
                <div class="stat">
                    <div class="stat-number">{site_info.get('statistics', {}).get('total_files', 0)}</div>
                    <div class="stat-label">總文件數</div>
                </div>
            </div>
        </div>
        
        <div class="info">
            <h3>📝 使用說明</h3>
            <ol>
                <li>點擊下方「開啟報告」按鈕</li>
                <li>報告將在您的預設瀏覽器中開啟</li>
                <li>支援離線瀏覽，無需網路連接</li>
                <li>建議使用現代瀏覽器以獲得最佳體驗</li>
            </ol>
        </div>
        
        <a href="{output_path.name}/index.html" class="launch-btn">🌐 開啟報告</a>
        
        <div class="info">
            <p><strong>生成時間：</strong> {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}</p>
            <p><strong>系統版本：</strong> TrendScope v2.0</p>
        </div>
    </div>
</body>
</html>"""

            with open(launcher_file, 'w', encoding='utf-8') as f:
                f.write(launcher_content)

            logger.info(f"✅ HTML 啟動器創建完成: {launcher_file}")
            return str(launcher_file)

        except Exception as e:
            logger.error(f"❌ 創建 HTML 啟動器失敗: {e}")
            return ""
