#!/usr/bin/env python3
"""
增強的報告生成器
實現 plan.md 中描述的三階層網站結構和完整的 Markdown 文件生成
"""
import logging
import pathlib
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
from dataclasses import asdict
import yaml
from .trend_analyzer import TrendInfo, SessionTrendMapping, TrendAnalyzer

logger = logging.getLogger(__name__)

class EnhancedReportGenerator:
    """增強的報告生成器 - 實現 plan.md 中的第三階段功能"""
    
    def __init__(self):
        """初始化增強報告生成器"""
        self.trend_analyzer = TrendAnalyzer()
    
    def generate_comprehensive_reports(self, sessions: List[Dict[str, Any]],
                                     output_dir: pathlib.Path,
                                     analysis_mode: str = "comprehensive",
                                     output_template: str = "professional",
                                     enable_trend_analysis: bool = True,
                                     enable_recommendations: bool = False) -> Dict[str, Any]:
        """
        生成完整的三階層報告結構

        Args:
            sessions: 會議數據列表
            output_dir: 輸出目錄
            analysis_mode: 分析模式
            output_template: 輸出模板
            enable_trend_analysis: 是否啟用 LLM 趨勢分析
            enable_recommendations: 是否啟用智慧推薦引擎

        Returns:
            Dict: 生成結果信息
        """
        logger.info(f"開始生成完整的三階層報告結構，共 {len(sessions)} 個會議")
        
        try:
            # 根據配置決定是否執行趨勢分析
            if enable_trend_analysis:
                # 第一階段：趨勢分析
                logger.info("執行 LLM 趨勢分析...")
                trends = self.trend_analyzer.analyze_trends(sessions)

                # 第二階段：會議分類
                logger.info("執行會議趨勢分類...")
                session_mappings = self.trend_analyzer.classify_sessions(sessions, trends)

                # 更新趨勢的會議數量統計
                self._update_trend_session_counts(trends, session_mappings)

                # 2.5 階段：趨勢關聯性分析
                logger.info("執行趨勢關聯性分析...")
                correlation_analysis = self.trend_analyzer.analyze_trend_correlations(sessions, session_mappings)
            else:
                # 使用基礎的趨勢分析（不使用 LLM）
                logger.info("使用基礎趨勢分析（跳過 LLM 分析）...")
                trends, session_mappings, correlation_analysis = self._generate_basic_trends(sessions)

            # 第三階段：生成 Markdown 文件
            logger.info("生成 Markdown 文件...")
            
            # 1. 生成趨勢分析報告文件 (trends-analysis.md)
            trends_analysis_file = self._generate_trends_analysis_file(
                trends, session_mappings, correlation_analysis, output_dir
            )
            
            # 2. 生成趨勢分類頁面文件 (trend-*.md)
            trend_files = self._generate_trend_category_files(
                trends, session_mappings, sessions, output_dir
            )
            
            # 3. 生成研討會詳細頁面文件 (session-*.md)
            session_files = self._generate_session_detail_files(
                sessions, session_mappings, output_dir, analysis_mode, output_template
            )
            
            # 4. 生成 Hugo 首頁文件 (_index.md)
            index_file = self._generate_hugo_index_file(trends, output_dir)

            # 5. 生成推薦信息（如果啟用）
            recommendations = []
            if enable_recommendations:
                logger.info("生成智慧推薦...")
                recommendations = self._generate_recommendations(sessions, trends, session_mappings)

            result = {
                'trends_analysis_file': trends_analysis_file,
                'trend_files': trend_files,
                'session_files': session_files,
                'index_file': index_file,
                'trends': [asdict(trend) for trend in trends],
                'session_mappings': [asdict(mapping) for mapping in session_mappings],
                'recommendations': recommendations,
                'total_files': 1 + len(trend_files) + len(session_files) + 1,
                'statistics': {
                    'total_sessions': len(sessions),
                    'total_trends': len(trends),
                    'mapped_sessions': len([m for m in session_mappings if m.trends]),
                    'total_recommendations': len(recommendations)
                },
                'features_enabled': {
                    'trend_analysis': enable_trend_analysis,
                    'recommendations': enable_recommendations
                }
            }
            
            logger.info(f"完成三階層報告生成，共生成 {result['total_files']} 個文件")
            return result
            
        except Exception as e:
            logger.error(f"生成完整報告失敗: {e}")
            raise
    
    def _update_trend_session_counts(self, trends: List[TrendInfo], 
                                   session_mappings: List[SessionTrendMapping]):
        """更新趨勢的會議數量統計"""
        trend_counts = {}
        
        for mapping in session_mappings:
            for trend_name in mapping.trends:
                trend_counts[trend_name] = trend_counts.get(trend_name, 0) + 1
        
        for trend in trends:
            trend.session_count = trend_counts.get(trend.name, 0)
    
    def _generate_trends_analysis_file(self, trends: List[TrendInfo],
                                     session_mappings: List[SessionTrendMapping],
                                     correlation_analysis: Dict[str, Any],
                                     output_dir: pathlib.Path) -> str:
        """生成趨勢分析報告文件 (trends-analysis.md)"""
        
        # 統計信息
        total_sessions = len(session_mappings)
        mapped_sessions = len([m for m in session_mappings if m.trends])
        
        # 構建 Front Matter
        front_matter = {
            'title': '技術趨勢分析報告',
            'date': datetime.now().strftime('%Y-%m-%d'),
            'type': 'trends-analysis',
            'layout': 'trends-analysis',
            'description': '基於 AI 分析的技術發展趨勢報告',
            'total_sessions': total_sessions,
            'mapped_sessions': mapped_sessions,
            'analysis_date': datetime.now().isoformat()
        }
        
        # 構建內容
        content = f"""
## 趨勢總覽

本報告基於 {total_sessions} 場研討會的深度分析，識別出以下五大技術發展趨勢：

### 統計資料
- **總會議數量**: {total_sessions}
- **成功分類會議**: {mapped_sessions}
- **分類成功率**: {mapped_sessions/total_sessions*100:.1f}%
- **分析時間**: {datetime.now().strftime('%Y年%m月%d日')}

## 五大技術趨勢

"""
        
        # 按重要性排序趨勢
        sorted_trends = sorted(trends, key=lambda x: x.importance_score, reverse=True)
        
        for i, trend in enumerate(sorted_trends, 1):
            content += f"""
### {i}. {trend.name}

**重要性評分**: {trend.importance_score:.2f} / 1.00  
**相關會議數量**: {trend.session_count} 場

{trend.description}

**關鍵技術詞彙**:
{', '.join([f'`{keyword}`' for keyword in trend.keywords])}

---
"""
        
        # 趨勢關聯性分析
        content += """
## 趨勢間關聯性分析

基於會議內容的深度分析，我們識別出以下技術趨勢間的關聯模式：

"""

        # 添加關聯性洞察
        correlation_insights = correlation_analysis.get('correlation_insights', [])
        if correlation_insights:
            content += "### 關鍵洞察\n\n"
            for insight in correlation_insights:
                content += f"- {insight}\n"
            content += "\n"

        # 添加趨勢集群信息
        trend_clusters = correlation_analysis.get('trend_clusters', [])
        if trend_clusters:
            content += "### 技術生態圈\n\n"
            for i, cluster in enumerate(trend_clusters[:3], 1):  # 只顯示前3個最強的集群
                content += f"**{i}. {cluster['primary_trend']} 生態圈**\n\n"
                content += f"{cluster['description']}\n\n"

                if cluster['related_trends']:
                    content += "相關技術：\n"
                    for related in cluster['related_trends'][:3]:  # 只顯示前3個相關趨勢
                        content += f"- {related['trend']} (關聯強度: {related['similarity']:.2f})\n"
                    content += "\n"

        # 添加技術融合分析
        co_occurrence_matrix = correlation_analysis.get('co_occurrence_matrix', {})
        if co_occurrence_matrix:
            content += "### 技術融合熱點\n\n"
            content += "以下技術趨勢經常在同一場會議中被討論，顯示出強烈的技術融合趨勢：\n\n"

            # 找出最高共現的趨勢對
            max_pairs = []
            for trend1, co_occurrences in co_occurrence_matrix.items():
                for trend2, count in co_occurrences.items():
                    if trend1 != trend2 and count > 0:
                        max_pairs.append((trend1, trend2, count))

            # 排序並顯示前5個
            max_pairs.sort(key=lambda x: x[2], reverse=True)
            for trend1, trend2, count in max_pairs[:5]:
                content += f"- **{trend1}** ↔ **{trend2}** (共現 {count} 次)\n"
            content += "\n"
        
        # 生成完整的 Markdown 文件
        yaml_front_matter = yaml.dump(front_matter, default_flow_style=False, allow_unicode=True)
        full_content = f"""---
{yaml_front_matter.strip()}
---
{content}
"""
        
        # 保存文件
        file_path = output_dir / "trends-analysis.md"
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(full_content)
        
        logger.info(f"已生成趨勢分析報告: {file_path}")
        return str(file_path)
    
    def _generate_trend_category_files(self, trends: List[TrendInfo],
                                     session_mappings: List[SessionTrendMapping],
                                     sessions: List[Dict[str, Any]],
                                     output_dir: pathlib.Path) -> List[str]:
        """生成趨勢分類頁面文件 (trend-*.md)"""
        
        trend_files = []
        
        # 創建 trends 子目錄
        trends_dir = output_dir / "trends"
        trends_dir.mkdir(exist_ok=True)
        
        # 為每個趨勢生成專屬頁面
        for trend in trends:
            # 生成安全的文件名
            safe_name = self._slugify(trend.name)
            file_path = trends_dir / f"trend-{safe_name}.md"
            
            # 找到屬於此趨勢的會議
            related_sessions = []
            for mapping in session_mappings:
                if trend.name in mapping.trends:
                    # 找到對應的會議詳細信息
                    session_detail = next(
                        (s for s in sessions if s.get('conference_id') == mapping.session_id or 
                         s.get('id') == mapping.session_id), None
                    )
                    if session_detail:
                        confidence = mapping.confidence_scores.get(trend.name, 0.0)
                        related_sessions.append({
                            'mapping': mapping,
                            'session': session_detail,
                            'confidence': confidence
                        })
            
            # 按置信度排序
            related_sessions.sort(key=lambda x: x['confidence'], reverse=True)
            
            # 構建 Front Matter
            front_matter = {
                'title': trend.name,
                'date': datetime.now().strftime('%Y-%m-%d'),
                'type': 'trend',
                'layout': 'trend-single',
                'description': trend.description[:100] + '...',
                'importance_score': trend.importance_score,
                'session_count': len(related_sessions),
                'keywords': trend.keywords,
                'trend_slug': safe_name
            }
            
            # 構建內容
            content = f"""
## 趨勢描述

{trend.description}

### 重要性評估
- **評分**: {trend.importance_score:.2f} / 1.00
- **相關會議**: {len(related_sessions)} 場
- **技術成熟度**: {'高' if trend.importance_score > 0.8 else '中' if trend.importance_score > 0.6 else '新興'}

### 關鍵技術
{', '.join([f'`{keyword}`' for keyword in trend.keywords])}

## 相關研討會

"""
            
            if related_sessions:
                for item in related_sessions:
                    session = item['session']
                    confidence = item['confidence']
                    session_title = session.get('name', 'Unknown')
                    seminar = session.get('seminar', 'Unknown')
                    session_id = session.get('conference_id', session.get('id', 'unknown'))
                    
                    # 生成會議文件的鏈接
                    session_date = datetime.now().strftime('%Y%m%d')  # 簡化處理
                    session_slug = self._slugify(session_title)[:20]
                    session_link = f"/sessions/session-{session_date}-{session_slug}/"
                    
                    content += f"""
### [{session_title}]({session_link})

- **研討會**: {seminar}
- **相關度**: {confidence:.2f}
- **會議ID**: `{session_id}`

---
"""
            else:
                content += "\n目前沒有會議被分類到此趨勢。\n"
            
            # 生成完整的 Markdown 文件
            yaml_front_matter = yaml.dump(front_matter, default_flow_style=False, allow_unicode=True)
            full_content = f"""---
{yaml_front_matter.strip()}
---
{content}
"""
            
            # 保存文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(full_content)
            
            trend_files.append(str(file_path))
            logger.info(f"已生成趨勢分類頁面: {file_path}")
        
        return trend_files
    
    def _generate_session_detail_files(self, sessions: List[Dict[str, Any]],
                                      session_mappings: List[SessionTrendMapping],
                                      output_dir: pathlib.Path,
                                      analysis_mode: str,
                                      output_template: str) -> List[str]:
        """生成研討會詳細頁面文件 (session-*.md)"""

        session_files = []

        # 創建 sessions 子目錄
        sessions_dir = output_dir / "sessions"
        sessions_dir.mkdir(exist_ok=True)

        # 創建映射字典以便快速查找
        mapping_dict = {mapping.session_id: mapping for mapping in session_mappings}

        for session in sessions:
            session_id = session.get('conference_id', session.get('id', 'unknown'))
            title = session.get('name', 'Unknown Title')
            seminar = session.get('seminar', 'Unknown Seminar')
            url = session.get('url', '')
            ppt_context = session.get('ppt_context', '')

            # 獲取趨勢映射信息
            mapping = mapping_dict.get(session_id)
            trends = mapping.trends if mapping else []

            # 生成文件名 (按照 plan.md 的命名規則)
            session_date = datetime.now().strftime('%Y%m%d')  # 簡化處理，實際應從數據中提取
            title_slug = self._slugify(title)[:20]  # 限制長度
            filename = f"session-{session_date}-{title_slug}.md"
            file_path = sessions_dir / filename

            # 構建 Front Matter (按照 plan.md 的要求)
            front_matter = {
                'title': title,
                'date': datetime.now().strftime('%Y-%m-%d'),
                'type': 'session',
                'layout': 'session-single',
                'seminar': seminar,
                'category': '主題演講',  # 默認類型
                'trends': trends,
                'session_id': session_id,
                'url_source': url,
                'analysis_mode': analysis_mode,
                'template_style': output_template
            }

            if mapping:
                front_matter['trend_confidence'] = mapping.confidence_scores
                front_matter['classification_reasoning'] = mapping.reasoning

            # 使用現有的 generate_session_report 生成內容
            from ..routes.batch_reports import generate_session_report

            try:
                report_result = generate_session_report(session, analysis_mode, output_template)

                if report_result['status'] == 'completed':
                    # 提取報告內容，移除原有的 Front Matter 和標題
                    report_content = report_result['content']

                    # 移除原有的標題和會議資訊部分，因為這些會在 Front Matter 中處理
                    import re
                    content_without_header = re.sub(
                        r'^#.*?\n.*?---\n', '', report_content, flags=re.DOTALL
                    ).strip()

                    # 如果有趨勢分類信息，添加到內容中
                    if trends:
                        trend_section = "\n## 🏷️ 技術趨勢分類\n\n"
                        for trend in trends:
                            confidence = mapping.confidence_scores.get(trend, 0.0) if mapping else 0.0
                            trend_slug = self._slugify(trend)
                            trend_link = f"/trends/trend-{trend_slug}/"
                            trend_section += f"- [{trend}]({trend_link}) (相關度: {confidence:.2f})\n"

                        content_without_header = trend_section + "\n" + content_without_header

                    # 生成完整的 Markdown 文件
                    yaml_front_matter = yaml.dump(front_matter, default_flow_style=False, allow_unicode=True)
                    full_content = f"""---
{yaml_front_matter.strip()}
---

{content_without_header}
"""

                    # 保存文件
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(full_content)

                    session_files.append(str(file_path))
                    logger.info(f"已生成會議詳細頁面: {file_path}")

                else:
                    logger.error(f"生成會議報告失敗: {session_id}")

            except Exception as e:
                logger.error(f"處理會議 {session_id} 時發生錯誤: {e}")

        return session_files

    def _generate_hugo_index_file(self, trends: List[TrendInfo],
                                output_dir: pathlib.Path) -> str:
        """生成 Hugo 首頁文件 (_index.md)"""

        # 構建 Front Matter
        front_matter = {
            'title': 'NeoTrendHub 技術趨勢分析',
            'date': datetime.now().strftime('%Y-%m-%d'),
            'type': 'homepage',
            'layout': 'index',
            'description': 'AI 驅動的技術趨勢分析與會議報告平台',
            'total_trends': len(trends),
            'analysis_date': datetime.now().isoformat()
        }

        # 構建內容
        content = f"""
# 歡迎來到 NeoTrendHub

基於人工智慧的技術趨勢分析平台，為您提供最新的技術發展洞察。

## 🔍 五大技術趨勢

我們通過深度分析各大技術研討會，識別出以下五個重要的技術發展趨勢：

"""

        # 按重要性排序趨勢
        sorted_trends = sorted(trends, key=lambda x: x.importance_score, reverse=True)

        for i, trend in enumerate(sorted_trends, 1):
            trend_slug = self._slugify(trend.name)
            trend_link = f"/trends/trend-{trend_slug}/"

            content += f"""
### {i}. [{trend.name}]({trend_link})

{trend.description[:150]}...

- **重要性**: {trend.importance_score:.2f}/1.00
- **相關會議**: {trend.session_count} 場
- **關鍵詞**: {', '.join(trend.keywords[:3])}

[了解更多 →]({trend_link})

---
"""

        content += """
## 📊 平台特色

- **🤖 AI 驅動分析**: 使用先進的大型語言模型進行深度趨勢分析
- **📈 實時更新**: 持續追蹤最新的技術發展動態
- **🔗 智慧分類**: 自動將會議內容分類到相關技術趨勢
- **📱 響應式設計**: 支援各種設備的最佳瀏覽體驗

## 🚀 開始探索

- [瀏覽所有趨勢](/trends/) - 查看完整的技術趨勢分析
- [會議報告](/sessions/) - 瀏覽所有研討會報告
- [關於我們](/about/) - 了解平台技術架構

---

*本平台由 NeoTrendHub 團隊開發，致力於為技術從業者提供最有價值的趨勢洞察。*
"""

        # 生成完整的 Markdown 文件
        yaml_front_matter = yaml.dump(front_matter, default_flow_style=False, allow_unicode=True)
        full_content = f"""---
{yaml_front_matter.strip()}
---
{content}
"""

        # 保存文件
        file_path = output_dir / "_index.md"
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(full_content)

        logger.info(f"已生成 Hugo 首頁文件: {file_path}")
        return str(file_path)

    def _slugify(self, text: str) -> str:
        """將文本轉換為 URL 友好的 slug"""
        import re

        # 移除特殊字符，保留中文、英文、數字
        text = re.sub(r'[^\w\s-]', '', text)
        # 替換空格為連字符
        text = re.sub(r'[-\s]+', '-', text)
        # 轉換為小寫
        text = text.lower().strip('-')

        return text or "unknown"

    def _generate_basic_trends(self, sessions: List[Dict[str, Any]]) -> Tuple[List, List, Dict]:
        """生成基礎趨勢分析（不使用 LLM）"""
        from ..modules.trend_analyzer import TrendInfo, SessionTrendMapping

        # 創建基礎趨勢
        basic_trends = [
            TrendInfo(
                name="技術創新與發展",
                description="涵蓋各種技術創新和發展趨勢",
                keywords=["技術", "創新", "發展"],
                importance_score=0.8,
                session_count=len(sessions)
            )
        ]

        # 創建基礎會議映射
        basic_mappings = []
        for session in sessions:
            session_id = session.get('conference_id', session.get('id', ''))
            session_title = session.get('name', 'Unknown')

            mapping = SessionTrendMapping(
                session_id=session_id,
                title=session_title,
                trends=["技術創新與發展"],
                confidence_scores={"技術創新與發展": 0.7},
                reasoning="基礎分類（未使用 LLM 分析）"
            )
            basic_mappings.append(mapping)

        # 創建基礎關聯性分析
        basic_correlation = {
            'correlation_insights': ["基礎模式：所有會議歸類為技術創新與發展趨勢"],
            'trend_clusters': [],
            'analysis_metadata': {
                'total_sessions': len(sessions),
                'mapped_sessions': len(sessions),
                'analysis_mode': 'basic'
            }
        }

        return basic_trends, basic_mappings, basic_correlation

    def _generate_recommendations(self, sessions: List[Dict[str, Any]],
                                trends: List, session_mappings: List) -> List[Dict[str, Any]]:
        """生成智慧推薦"""
        try:
            from ..modules.trend_recommendation_engine import TrendRecommendationEngine, UserProfile

            # 創建一個通用的用戶檔案
            user_profile = UserProfile(
                user_id="batch_report_user",
                interests=["技術創新", "AI", "機器學習", "雲計算"],
                preferred_trends=[trend.name for trend in trends[:3]],  # 取前三個趨勢
                interaction_history=[],
                expertise_level="intermediate"
            )

            # 轉換數據格式
            trends_data = [
                {
                    "name": trend.name,
                    "description": trend.description,
                    "keywords": trend.keywords,
                    "importance_score": trend.importance_score
                }
                for trend in trends
            ]

            session_mappings_data = [
                {
                    "session_id": mapping.session_id,
                    "title": mapping.title,
                    "trends": mapping.trends,
                    "confidence_scores": mapping.confidence_scores
                }
                for mapping in session_mappings
            ]

            # 生成推薦
            recommendation_engine = TrendRecommendationEngine()
            recommendations = recommendation_engine.generate_personalized_recommendations(
                user_profile=user_profile,
                trends=trends_data,
                sessions=sessions,
                session_mappings=session_mappings_data,
                max_recommendations=10
            )

            # 轉換為字典格式
            return [
                {
                    "item_id": rec.item_id,
                    "item_type": rec.item_type,
                    "title": rec.title,
                    "description": rec.description,
                    "relevance_score": rec.relevance_score,
                    "reasoning": rec.reasoning,
                    "metadata": rec.metadata
                }
                for rec in recommendations
            ]

        except Exception as e:
            logger.warning(f"生成推薦失敗: {e}")
            return []
