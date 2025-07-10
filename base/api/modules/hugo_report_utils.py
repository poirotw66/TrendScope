#!/usr/bin/env python3
"""
Hugo 報告生成器輔助工具
包含文件處理、路徑修復、ZIP 打包等功能
"""

import pathlib
import zipfile
import logging
import re
import unicodedata
from typing import List, Dict, Any, Optional
from datetime import datetime
from dataclasses import asdict

logger = logging.getLogger(__name__)

class HugoReportUtils:
    """Hugo 報告生成器輔助工具類"""
    
    def _process_markdown_files(self, md_dir: str, site_dir: pathlib.Path,
                                template_style: str) -> List[str]:
        """處理 Markdown 文件並生成 Hugo 內容 - 支援三階層結構"""
        md_path = pathlib.Path(md_dir)
        content_dir = site_dir / "content"
        html_files = []

        if not md_path.exists():
            logger.warning(f"Markdown 目錄不存在: {md_dir}")
            return html_files

        logger.info(f"🔍 檢查 Markdown 目錄結構: {md_path}")
        
        # 檢查是否為增強版三階層結構
        has_enhanced_structure = self._check_enhanced_structure(md_path)
        
        if has_enhanced_structure:
            logger.info("✅ 檢測到增強版三階層結構，使用專用處理流程")
            html_files = self._process_enhanced_structure(md_path, content_dir, template_style)
        else:
            logger.info("📄 使用標準 Markdown 文件處理流程")
            html_files = self._process_standard_markdown_files(md_path, content_dir, template_style)
        
        return html_files

    def _check_enhanced_structure(self, md_path: pathlib.Path) -> bool:
        """檢查是否為增強版三階層結構"""
        # 檢查關鍵文件和目錄
        trends_analysis = md_path / "trends-analysis.md"
        index_file = md_path / "_index.md"
        trends_dir = md_path / "trends"
        sessions_dir = md_path / "sessions"
        
        has_structure = (
            trends_analysis.exists() or
            index_file.exists() or
            trends_dir.exists() or
            sessions_dir.exists()
        )
        
        logger.info(f"🔍 結構檢查結果:")
        logger.info(f"  📄 trends-analysis.md: {trends_analysis.exists()}")
        logger.info(f"  🏠 _index.md: {index_file.exists()}")
        logger.info(f"  📂 trends/: {trends_dir.exists()}")
        logger.info(f"  📂 sessions/: {sessions_dir.exists()}")
        
        return has_structure

    def _process_enhanced_structure(self, md_path: pathlib.Path, content_dir: pathlib.Path, template_style: str) -> List[str]:
        """處理增強版三階層結構"""
        html_files = []
        
        # 1. 處理首頁文件 (_index.md 或 trends-analysis.md)
        index_file = md_path / "_index.md"
        trends_analysis_file = md_path / "trends-analysis.md"
        
        if index_file.exists():
            logger.info("📄 處理首頁文件: _index.md")
            self._copy_hugo_content_file(index_file, content_dir / "_index.md")
            html_files.append("index.html")
        elif trends_analysis_file.exists():
            logger.info("📄 處理趨勢分析文件作為首頁: trends-analysis.md")
            # 將 trends-analysis.md 轉換為首頁
            self._convert_trends_analysis_to_index(trends_analysis_file, content_dir / "_index.md")
            html_files.append("index.html")
        
        # 2. 處理趨勢分類目錄
        trends_dir = md_path / "trends"
        if trends_dir.exists():
            logger.info(f"📂 處理趨勢分類目錄: {trends_dir}")
            trends_content_dir = content_dir / "trends"
            trends_content_dir.mkdir(parents=True, exist_ok=True)
            
            # 創建趨勢分類索引頁
            self._create_trends_index(trends_content_dir)
            html_files.append("trends/index.html")
            
            # 處理每個趨勢文件
            for trend_file in trends_dir.glob("trend-*.md"):
                logger.info(f"  📄 處理趨勢文件: {trend_file.name}")
                target_file = trends_content_dir / trend_file.name
                self._copy_hugo_content_file(trend_file, target_file)
                html_files.append(f"trends/{trend_file.stem}/index.html")
        
        # 3. 處理會議詳細目錄
        sessions_dir = md_path / "sessions"
        if sessions_dir.exists():
            logger.info(f"📂 處理會議詳細目錄: {sessions_dir}")
            sessions_content_dir = content_dir / "sessions"
            sessions_content_dir.mkdir(parents=True, exist_ok=True)
            
            # 創建會議索引頁
            self._create_sessions_index(sessions_content_dir)
            html_files.append("sessions/index.html")
            
            # 處理每個會議文件
            for session_file in sessions_dir.glob("session-*.md"):
                logger.info(f"  📄 處理會議文件: {session_file.name}")
                target_file = sessions_content_dir / session_file.name
                self._copy_hugo_content_file(session_file, target_file)
                html_files.append(f"sessions/{session_file.stem}/index.html")
        
        # 4. 處理其他 Markdown 文件
        for md_file in md_path.glob("*.md"):
            if md_file.name not in ["_index.md", "trends-analysis.md"]:
                logger.info(f"📄 處理其他文件: {md_file.name}")
                self._process_single_markdown_file(md_file, content_dir, template_style)
                html_files.append(f"{md_file.stem}/index.html")
        
        logger.info(f"✅ 增強版結構處理完成，預期生成 {len(html_files)} 個 HTML 文件")
        return html_files

    def _process_standard_markdown_files(self, md_path: pathlib.Path, content_dir: pathlib.Path, template_style: str) -> List[str]:
        """處理標準 Markdown 文件"""
        html_files = []
        
        # 處理每個 Markdown 文件
        for md_file in md_path.glob("*.md"):
            try:
                html_files.extend(self._process_single_markdown_file(md_file, content_dir, template_style))
            except Exception as e:
                logger.error(f"處理 Markdown 文件失敗 {md_file}: {e}")
        
        return html_files

    def _process_single_markdown_file(self, md_file: pathlib.Path, content_dir: pathlib.Path, template_style: str) -> List[str]:
        """處理單個 Markdown 文件"""
        try:
            # 讀取 Markdown 內容
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # 解析元數據
            metadata = self._extract_metadata_from_content(content, md_file.stem)

            # 創建 Hugo 內容文件
            hugo_content = self._create_hugo_content(content, metadata)

            # 使用 Hugo Page Bundle 結構：每個報告都有自己的目錄
            posts_dir = content_dir / "posts"
            posts_dir.mkdir(parents=True, exist_ok=True)

            # 為 posts 目錄創建 _index.md（如果不存在）
            posts_index = posts_dir / "_index.md"
            if not posts_index.exists():
                with open(posts_index, 'w', encoding='utf-8') as f:
                    f.write("""---
title: 會議報告
description: 所有會議報告的列表
---

# 會議報告

這裡包含所有的會議報告。
""")

            # 生成簡短且安全的文件名
            session_id = md_file.stem

            # 提取 UUID 的前8個字符作為唯一標識
            if '_' in session_id:
                uuid_part = session_id.split('_')[0][:8]
            else:
                uuid_part = session_id[:8]

            # 使用簡短的文件名：report-UUID
            safe_filename = f"report-{uuid_part}"

            # 確保文件名是安全的（只包含字母數字和連字符）
            safe_filename = re.sub(r'[^a-zA-Z0-9-]', '', safe_filename)

            # 創建 Page Bundle 目錄結構：posts/report-xxx/index.md
            bundle_dir = posts_dir / safe_filename
            bundle_dir.mkdir(parents=True, exist_ok=True)

            # 保存為 index.md（Page Bundle 的標準文件名）
            output_file = bundle_dir / "index.md"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(hugo_content)

            # 記錄生成的文件（Hugo Page Bundle 會生成對應的 HTML）
            return [f"posts/{safe_filename}/index.html"]

        except Exception as e:
            logger.error(f"處理 Markdown 文件失敗 {md_file.name}: {e}")
            return []

    def _copy_hugo_content_file(self, source_file: pathlib.Path, target_file: pathlib.Path):
        """複製 Hugo 內容文件"""
        try:
            target_file.parent.mkdir(parents=True, exist_ok=True)
            
            # 讀取源文件內容
            with open(source_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 確保內容有正確的 Hugo front matter
            if not content.startswith('---'):
                # 如果沒有 front matter，添加基本的
                title = source_file.stem.replace('-', ' ').title()
                front_matter = f"""---
title: "{title}"
date: {datetime.now().strftime('%Y-%m-%dT%H:%M:%S+08:00')}
draft: false
---

"""
                content = front_matter + content
            
            # 寫入目標文件
            with open(target_file, 'w', encoding='utf-8') as f:
                f.write(content)
                
            logger.info(f"✅ 複製 Hugo 內容文件: {source_file.name} → {target_file}")
            
        except Exception as e:
            logger.error(f"❌ 複製 Hugo 內容文件失敗 {source_file} → {target_file}: {e}")

    def _convert_trends_analysis_to_index(self, trends_analysis_file: pathlib.Path, index_file: pathlib.Path):
        """將趨勢分析文件轉換為首頁"""
        try:
            with open(trends_analysis_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 修改 front matter 以適合首頁
            if content.startswith('---'):
                # 找到 front matter 的結束位置
                end_pos = content.find('---', 3)
                if end_pos != -1:
                    front_matter = content[3:end_pos].strip()
                    body_content = content[end_pos + 3:].strip()
                    
                    # 創建新的首頁 front matter
                    new_front_matter = f"""---
title: "技術趨勢分析報告"
description: "深度技術趨勢分析與會議洞察"
date: {datetime.now().strftime('%Y-%m-%dT%H:%M:%S+08:00')}
draft: false
type: "homepage"
layout: "index"
---

"""
                    content = new_front_matter + body_content
            
            index_file.parent.mkdir(parents=True, exist_ok=True)
            with open(index_file, 'w', encoding='utf-8') as f:
                f.write(content)
                
            logger.info(f"✅ 轉換趨勢分析為首頁: {trends_analysis_file.name} → {index_file.name}")
            
        except Exception as e:
            logger.error(f"❌ 轉換趨勢分析為首頁失敗: {e}")

    def _create_trends_index(self, trends_content_dir: pathlib.Path):
        """創建趨勢分類索引頁"""
        try:
            index_content = f"""---
title: "技術趨勢分類"
description: "探索各種技術趨勢的詳細分析"
date: {datetime.now().strftime('%Y-%m-%dT%H:%M:%S+08:00')}
draft: false
type: "section"
layout: "list"
---

# 技術趨勢分類

探索當前最重要的技術趨勢，深入了解每個領域的發展動向和關鍵洞察。
"""
            
            index_file = trends_content_dir / "_index.md"
            with open(index_file, 'w', encoding='utf-8') as f:
                f.write(index_content)
                
            logger.info(f"✅ 創建趨勢分類索引頁: {index_file}")
            
        except Exception as e:
            logger.error(f"❌ 創建趨勢分類索引頁失敗: {e}")

    def _create_sessions_index(self, sessions_content_dir: pathlib.Path):
        """創建會議索引頁"""
        try:
            index_content = f"""---
title: "會議詳細報告"
description: "所有會議的詳細分析和洞察"
date: {datetime.now().strftime('%Y-%m-%dT%H:%M:%S+08:00')}
draft: false
type: "section"
layout: "list"
---

# 會議詳細報告

瀏覽所有會議的深度分析報告，獲取技術洞察和實用建議。
"""
            
            index_file = sessions_content_dir / "_index.md"
            with open(index_file, 'w', encoding='utf-8') as f:
                f.write(index_content)
                
            logger.info(f"✅ 創建會議索引頁: {index_file}")
            
        except Exception as e:
            logger.error(f"❌ 創建會議索引頁失敗: {e}")
