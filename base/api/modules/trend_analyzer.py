#!/usr/bin/env python3
"""
趨勢分析模組
實現 plan.md 中描述的 LLM 趨勢分析和自動標記功能
"""
import logging
import json
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import google.generativeai as genai
import os
from dotenv import load_dotenv

# 加載環境變量
load_dotenv()

logger = logging.getLogger(__name__)

@dataclass
class TrendInfo:
    """趨勢信息數據類"""
    name: str
    description: str
    keywords: List[str]
    importance_score: float
    session_count: int = 0
    
@dataclass
class SessionTrendMapping:
    """會議趨勢映射數據類"""
    session_id: str
    title: str
    trends: List[str]
    confidence_scores: Dict[str, float]
    reasoning: str

class TrendAnalyzer:
    """趨勢分析器 - 實現 plan.md 中的第一和第二階段功能"""
    
    def __init__(self):
        """初始化趨勢分析器"""
        # 配置 Gemini API
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY 環境變量未設置")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        
    def analyze_trends(self, sessions: List[Dict[str, Any]]) -> List[TrendInfo]:
        """
        第一階段：使用 LLM 進行趨勢分析
        
        Args:
            sessions: 會議數據列表
            
        Returns:
            List[TrendInfo]: 五大趨勢信息
        """
        logger.info(f"開始分析 {len(sessions)} 個會議的技術趨勢...")
        
        # 準備分析數據
        analysis_data = self._prepare_analysis_data(sessions)
        
        # 構建趨勢分析提示詞
        prompt = self._build_trend_analysis_prompt(analysis_data)
        
        try:
            # 調用 LLM 進行趨勢分析
            response = self.model.generate_content(prompt)
            
            if not response or not response.text:
                raise Exception("LLM 趨勢分析返回空結果")
            
            # 解析 LLM 返回的趨勢分析結果
            trends = self._parse_trend_analysis_response(response.text)
            
            logger.info(f"成功識別 {len(trends)} 個技術趨勢")
            return trends
            
        except Exception as e:
            logger.error(f"趨勢分析失敗: {e}")
            # 返回默認趨勢作為備用方案
            return self._get_default_trends()
    
    def classify_sessions(self, sessions: List[Dict[str, Any]], 
                         trends: List[TrendInfo]) -> List[SessionTrendMapping]:
        """
        第二階段：基於 LLM 的自動標記系統
        
        Args:
            sessions: 會議數據列表
            trends: 趨勢信息列表
            
        Returns:
            List[SessionTrendMapping]: 會議趨勢映射結果
        """
        logger.info(f"開始為 {len(sessions)} 個會議進行趨勢標記...")
        
        mappings = []
        trend_names = [trend.name for trend in trends]
        
        for session in sessions:
            try:
                # 為單個會議進行趨勢分類
                mapping = self._classify_single_session(session, trends)
                mappings.append(mapping)
                
                logger.debug(f"會議 '{session.get('name', 'Unknown')}' 標記完成")
                
            except Exception as e:
                logger.error(f"會議 {session.get('id', 'unknown')} 趨勢標記失敗: {e}")
                # 創建默認映射
                mappings.append(SessionTrendMapping(
                    session_id=session.get('conference_id', session.get('id', 'unknown')),
                    title=session.get('name', 'Unknown'),
                    trends=[],
                    confidence_scores={},
                    reasoning="標記過程中發生錯誤"
                ))
        
        logger.info(f"完成 {len(mappings)} 個會議的趨勢標記")
        return mappings
    
    def _prepare_analysis_data(self, sessions: List[Dict[str, Any]]) -> str:
        """準備用於趨勢分析的數據"""
        analysis_items = []
        
        for session in sessions[:50]:  # 限制分析數量以避免 token 超限
            title = session.get('name', 'Unknown')
            seminar = session.get('seminar', 'Unknown')
            content = session.get('ppt_context', '')[:500]  # 限制內容長度
            
            analysis_items.append(f"研討會: {seminar}\n標題: {title}\n內容摘要: {content}\n")
        
        return "\n---\n".join(analysis_items)
    
    def _build_trend_analysis_prompt(self, analysis_data: str) -> str:
        """構建趨勢分析提示詞"""
        return f"""
請分析以下研討會資料，識別出五個最重要的技術發展趨勢。

分析要求：
1. 深度語意理解：理解技術內容的深層含義和發展脈絡
2. 趨勢識別：從研討會主題和摘要中識別技術發展趨勢
3. 關聯分析：分析不同技術領域間的交集和演進關係
4. 結構化輸出：產生包含趨勢名稱、描述、關鍵詞、重要性評分的結構化報告

研討會資料：
{analysis_data}

請以 JSON 格式返回分析結果，格式如下：
{{
  "trends": [
    {{
      "name": "趨勢名稱",
      "description": "詳細描述（100-200字）",
      "keywords": ["關鍵詞1", "關鍵詞2", "關鍵詞3"],
      "importance_score": 0.95
    }}
  ]
}}

要求：
- 必須識別出恰好5個趨勢
- 重要性評分範圍：0.0-1.0
- 描述要具體且有深度
- 關鍵詞要準確反映趨勢特徵
- 使用繁體中文
"""
    
    def _parse_trend_analysis_response(self, response_text: str) -> List[TrendInfo]:
        """解析 LLM 趨勢分析響應"""
        try:
            # 嘗試提取 JSON 部分
            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if not json_match:
                raise ValueError("無法在響應中找到 JSON 格式")
            
            json_text = json_match.group(0)
            data = json.loads(json_text)
            
            trends = []
            for trend_data in data.get('trends', []):
                trend = TrendInfo(
                    name=trend_data.get('name', ''),
                    description=trend_data.get('description', ''),
                    keywords=trend_data.get('keywords', []),
                    importance_score=float(trend_data.get('importance_score', 0.0))
                )
                trends.append(trend)
            
            return trends[:5]  # 確保只返回5個趨勢
            
        except Exception as e:
            logger.error(f"解析趨勢分析響應失敗: {e}")
            return self._get_default_trends()
    
    def _classify_single_session(self, session: Dict[str, Any], 
                                trends: List[TrendInfo]) -> SessionTrendMapping:
        """為單個會議進行趨勢分類"""
        title = session.get('name', 'Unknown')
        content = session.get('ppt_context', '')[:1000]  # 限制內容長度
        
        # 構建分類提示詞
        trend_descriptions = "\n".join([
            f"{i+1}. {trend.name}: {trend.description[:100]}..."
            for i, trend in enumerate(trends)
        ])
        
        prompt = f"""
請分析以下會議內容，判斷它與哪些技術趨勢相關。

會議信息：
標題：{title}
內容：{content}

可選趨勢：
{trend_descriptions}

請以 JSON 格式返回分析結果：
{{
  "related_trends": ["趨勢名稱1", "趨勢名稱2"],
  "confidence_scores": {{
    "趨勢名稱1": 0.85,
    "趨勢名稱2": 0.72
  }},
  "reasoning": "分析推理說明"
}}

要求：
- 可以選擇0-3個相關趨勢
- 置信度範圍：0.0-1.0
- 只有置信度 >= 0.6 的趨勢才應該被選中
- 使用繁體中文
"""
        
        try:
            response = self.model.generate_content(prompt)
            
            if not response or not response.text:
                raise Exception("LLM 分類返回空結果")
            
            # 解析分類結果
            import re
            json_match = re.search(r'\{.*\}', response.text, re.DOTALL)
            if not json_match:
                raise ValueError("無法在響應中找到 JSON 格式")
            
            data = json.loads(json_match.group(0))
            
            return SessionTrendMapping(
                session_id=session.get('conference_id', session.get('id', 'unknown')),
                title=title,
                trends=data.get('related_trends', []),
                confidence_scores=data.get('confidence_scores', {}),
                reasoning=data.get('reasoning', '')
            )
            
        except Exception as e:
            logger.error(f"會議分類失敗: {e}")
            return SessionTrendMapping(
                session_id=session.get('conference_id', session.get('id', 'unknown')),
                title=title,
                trends=[],
                confidence_scores={},
                reasoning=f"分類過程中發生錯誤: {str(e)}"
            )
    
    def _get_default_trends(self) -> List[TrendInfo]:
        """獲取默認趨勢（備用方案）"""
        return [
            TrendInfo(
                name="AI 晶片與硬體加速",
                description="專用 AI 晶片、GPU 加速、邊緣計算硬體等技術的發展趨勢，包括神經網路處理器(NPU)、張量處理單元(TPU)、以及針對 AI 工作負載優化的專用晶片架構。",
                keywords=["AI晶片", "GPU", "TPU", "NPU", "邊緣計算", "硬體加速", "神經網路處理器"],
                importance_score=0.9
            ),
            TrendInfo(
                name="多模態 AI 技術",
                description="結合文字、圖像、語音、視頻等多種模態的 AI 技術發展，實現跨模態理解、生成和推理能力，推動 AI 系統向更接近人類認知的方向發展。",
                keywords=["多模態", "視覺語言模型", "語音識別", "圖像生成", "跨模態學習", "CLIP", "DALL-E"],
                importance_score=0.85
            ),
            TrendInfo(
                name="大型語言模型與生成式 AI",
                description="大型語言模型在各領域的應用與優化技術，包括模型壓縮、微調技術、提示工程、以及生成式 AI 在內容創作、程式開發等領域的應用。",
                keywords=["LLM", "ChatGPT", "GPT", "BERT", "生成式AI", "提示工程", "模型微調", "RAG"],
                importance_score=0.88
            ),
            TrendInfo(
                name="雲原生與分散式系統",
                description="雲原生技術、微服務架構、容器化部署、服務網格等分散式系統技術的發展，以及 DevOps、GitOps 等現代軟體開發和部署實踐。",
                keywords=["雲原生", "微服務", "容器化", "Kubernetes", "Docker", "服務網格", "DevOps", "GitOps"],
                importance_score=0.82
            ),
            TrendInfo(
                name="資料科學與 MLOps",
                description="資料科學方法論、機器學習模型生命週期管理、MLOps 實踐、資料工程、以及 AI/ML 系統的可觀測性和治理等技術的演進。",
                keywords=["資料科學", "機器學習", "MLOps", "資料工程", "模型部署", "特徵工程", "資料治理"],
                importance_score=0.80
            )
        ]

    def get_trend_evolution_analysis(self, sessions: List[Dict[str, Any]],
                                   time_window_months: int = 12) -> Dict[str, Any]:
        """
        分析技術趨勢的演進情況

        Args:
            sessions: 會議數據列表
            time_window_months: 分析時間窗口（月）

        Returns:
            Dict: 趨勢演進分析結果
        """
        logger.info("開始分析技術趨勢演進...")

        try:
            # 按時間分組會議
            time_groups = self._group_sessions_by_time(sessions, time_window_months)

            # 為每個時間段分析趨勢
            evolution_data = {}
            for time_period, period_sessions in time_groups.items():
                if len(period_sessions) >= 3:  # 至少需要3個會議才進行分析
                    trends = self.analyze_trends(period_sessions)
                    evolution_data[time_period] = {
                        'trends': trends,
                        'session_count': len(period_sessions),
                        'period': time_period
                    }

            # 分析趨勢變化
            trend_changes = self._analyze_trend_changes(evolution_data)

            return {
                'evolution_data': evolution_data,
                'trend_changes': trend_changes,
                'analysis_summary': self._generate_evolution_summary(trend_changes)
            }

        except Exception as e:
            logger.error(f"趨勢演進分析失敗: {e}")
            return {
                'evolution_data': {},
                'trend_changes': {},
                'analysis_summary': "趨勢演進分析暫時無法完成"
            }

    def _group_sessions_by_time(self, sessions: List[Dict[str, Any]],
                               window_months: int) -> Dict[str, List[Dict]]:
        """按時間窗口分組會議"""
        from datetime import datetime, timedelta
        import calendar

        time_groups = {}
        current_date = datetime.now()

        # 創建時間窗口
        for i in range(window_months):
            period_start = current_date - timedelta(days=30 * (i + 1))
            period_end = current_date - timedelta(days=30 * i)
            period_key = f"{period_start.strftime('%Y-%m')}"
            time_groups[period_key] = []

        # 將會議分配到對應時間窗口（簡化處理，實際應從會議數據中提取時間）
        sessions_per_period = len(sessions) // max(1, len(time_groups))

        for i, (period_key, _) in enumerate(time_groups.items()):
            start_idx = i * sessions_per_period
            end_idx = start_idx + sessions_per_period
            if i == len(time_groups) - 1:  # 最後一個時間段包含剩餘所有會議
                end_idx = len(sessions)
            time_groups[period_key] = sessions[start_idx:end_idx]

        return time_groups

    def _analyze_trend_changes(self, evolution_data: Dict) -> Dict[str, Any]:
        """分析趨勢變化"""
        trend_changes = {
            'emerging_trends': [],
            'declining_trends': [],
            'stable_trends': [],
            'trend_momentum': {}
        }

        # 收集所有時間段的趨勢
        all_trends = {}
        for period, data in evolution_data.items():
            for trend in data['trends']:
                if trend.name not in all_trends:
                    all_trends[trend.name] = []
                all_trends[trend.name].append({
                    'period': period,
                    'importance_score': trend.importance_score,
                    'session_count': trend.session_count
                })

        # 分析每個趨勢的變化
        for trend_name, trend_history in all_trends.items():
            if len(trend_history) >= 2:
                # 計算趨勢動量
                scores = [t['importance_score'] for t in trend_history]
                momentum = (scores[-1] - scores[0]) / len(scores)

                trend_changes['trend_momentum'][trend_name] = momentum

                # 分類趨勢
                if momentum > 0.1:
                    trend_changes['emerging_trends'].append(trend_name)
                elif momentum < -0.1:
                    trend_changes['declining_trends'].append(trend_name)
                else:
                    trend_changes['stable_trends'].append(trend_name)

        return trend_changes

    def _generate_evolution_summary(self, trend_changes: Dict) -> str:
        """生成趨勢演進摘要"""
        summary_parts = []

        if trend_changes['emerging_trends']:
            emerging = ', '.join(trend_changes['emerging_trends'])
            summary_parts.append(f"新興趨勢: {emerging}")

        if trend_changes['declining_trends']:
            declining = ', '.join(trend_changes['declining_trends'])
            summary_parts.append(f"衰退趨勢: {declining}")

        if trend_changes['stable_trends']:
            stable = ', '.join(trend_changes['stable_trends'])
            summary_parts.append(f"穩定趨勢: {stable}")

        return "; ".join(summary_parts) if summary_parts else "趨勢分析數據不足"

    def analyze_trend_correlations(self, sessions: List[Dict[str, Any]],
                                 session_mappings: List[SessionTrendMapping]) -> Dict[str, Any]:
        """
        分析趨勢間的關聯性和共現模式

        Args:
            sessions: 會議數據列表
            session_mappings: 會議趨勢映射列表

        Returns:
            Dict: 趨勢關聯性分析結果
        """
        logger.info("開始分析趨勢間關聯性...")

        try:
            # 構建趨勢共現矩陣
            co_occurrence_matrix = self._build_cooccurrence_matrix(session_mappings)

            # 計算趨勢相似度
            trend_similarities = self._calculate_trend_similarities(sessions, session_mappings)

            # 識別趨勢集群
            trend_clusters = self._identify_trend_clusters(co_occurrence_matrix, trend_similarities)

            # 生成趨勢關聯性洞察
            correlation_insights = self._generate_correlation_insights(
                co_occurrence_matrix, trend_similarities, trend_clusters
            )

            return {
                'co_occurrence_matrix': co_occurrence_matrix,
                'trend_similarities': trend_similarities,
                'trend_clusters': trend_clusters,
                'correlation_insights': correlation_insights,
                'analysis_metadata': {
                    'total_sessions': len(sessions),
                    'mapped_sessions': len([m for m in session_mappings if m.trends]),
                    'analysis_timestamp': datetime.now().isoformat()
                }
            }

        except Exception as e:
            logger.error(f"趨勢關聯性分析失敗: {e}")
            return {
                'co_occurrence_matrix': {},
                'trend_similarities': {},
                'trend_clusters': [],
                'correlation_insights': [],
                'error': str(e)
            }

    def _build_cooccurrence_matrix(self, session_mappings: List[SessionTrendMapping]) -> Dict[str, Dict[str, int]]:
        """構建趨勢共現矩陣"""
        co_occurrence = {}

        # 收集所有趨勢
        all_trends = set()
        for mapping in session_mappings:
            all_trends.update(mapping.trends)

        # 初始化矩陣
        for trend1 in all_trends:
            co_occurrence[trend1] = {}
            for trend2 in all_trends:
                co_occurrence[trend1][trend2] = 0

        # 計算共現次數
        for mapping in session_mappings:
            trends = mapping.trends
            for i, trend1 in enumerate(trends):
                for j, trend2 in enumerate(trends):
                    if i != j:  # 不計算自己與自己的共現
                        co_occurrence[trend1][trend2] += 1

        return co_occurrence

    def _calculate_trend_similarities(self, sessions: List[Dict[str, Any]],
                                    session_mappings: List[SessionTrendMapping]) -> Dict[str, Dict[str, float]]:
        """計算趨勢間的語意相似度"""
        similarities = {}

        # 為每個趨勢收集相關會議的內容
        trend_contents = {}
        mapping_dict = {m.session_id: m for m in session_mappings}

        for session in sessions:
            session_id = session.get('conference_id', session.get('id'))
            mapping = mapping_dict.get(session_id)

            if mapping and mapping.trends:
                content = session.get('ppt_context', '')[:500]  # 限制長度
                for trend in mapping.trends:
                    if trend not in trend_contents:
                        trend_contents[trend] = []
                    trend_contents[trend].append(content)

        # 計算趨勢間的相似度（簡化版本，使用關鍵詞重疊）
        trend_names = list(trend_contents.keys())
        for i, trend1 in enumerate(trend_names):
            similarities[trend1] = {}
            for j, trend2 in enumerate(trend_names):
                if i == j:
                    similarities[trend1][trend2] = 1.0
                else:
                    # 簡化的相似度計算（基於內容重疊）
                    content1 = ' '.join(trend_contents[trend1])
                    content2 = ' '.join(trend_contents[trend2])
                    similarity = self._calculate_text_similarity(content1, content2)
                    similarities[trend1][trend2] = similarity

        return similarities

    def _calculate_text_similarity(self, text1: str, text2: str) -> float:
        """計算文本相似度（簡化版本）"""
        # 使用簡單的詞彙重疊計算相似度
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())

        if not words1 or not words2:
            return 0.0

        intersection = words1.intersection(words2)
        union = words1.union(words2)

        return len(intersection) / len(union) if union else 0.0

    def _identify_trend_clusters(self, co_occurrence_matrix: Dict,
                               similarities: Dict) -> List[Dict[str, Any]]:
        """識別趨勢集群"""
        clusters = []

        # 簡化的集群識別：基於高共現和高相似度
        processed_trends = set()

        for trend1, co_occurrences in co_occurrence_matrix.items():
            if trend1 in processed_trends:
                continue

            cluster = {
                'primary_trend': trend1,
                'related_trends': [],
                'cluster_strength': 0.0,
                'description': ''
            }

            # 找到與當前趨勢高度相關的其他趨勢
            for trend2, co_count in co_occurrences.items():
                if (trend2 != trend1 and
                    trend2 not in processed_trends and
                    co_count > 0 and
                    similarities.get(trend1, {}).get(trend2, 0) > 0.3):

                    cluster['related_trends'].append({
                        'trend': trend2,
                        'co_occurrence': co_count,
                        'similarity': similarities[trend1][trend2]
                    })

            if cluster['related_trends']:
                # 計算集群強度
                total_strength = sum(
                    r['co_occurrence'] * r['similarity']
                    for r in cluster['related_trends']
                )
                cluster['cluster_strength'] = total_strength / len(cluster['related_trends'])

                # 生成集群描述
                related_names = [r['trend'] for r in cluster['related_trends']]
                cluster['description'] = f"{trend1} 與 {', '.join(related_names[:2])} 等趨勢密切相關"

                clusters.append(cluster)
                processed_trends.add(trend1)
                processed_trends.update(related_names)

        # 按集群強度排序
        clusters.sort(key=lambda x: x['cluster_strength'], reverse=True)
        return clusters

    def _generate_correlation_insights(self, co_occurrence_matrix: Dict,
                                     similarities: Dict,
                                     clusters: List[Dict]) -> List[str]:
        """生成趨勢關聯性洞察"""
        insights = []

        # 最強關聯性洞察
        if clusters:
            strongest_cluster = clusters[0]
            insights.append(
                f"最強技術關聯：{strongest_cluster['primary_trend']} "
                f"與相關技術形成緊密的技術生態圈"
            )

        # 共現頻率洞察
        max_co_occurrence = 0
        max_pair = None
        for trend1, co_occurrences in co_occurrence_matrix.items():
            for trend2, count in co_occurrences.items():
                if count > max_co_occurrence and trend1 != trend2:
                    max_co_occurrence = count
                    max_pair = (trend1, trend2)

        if max_pair and max_co_occurrence > 1:
            insights.append(
                f"技術融合熱點：{max_pair[0]} 與 {max_pair[1]} "
                f"在 {max_co_occurrence} 場會議中同時出現"
            )

        # 相似度洞察
        max_similarity = 0.0
        max_sim_pair = None
        for trend1, sims in similarities.items():
            for trend2, sim in sims.items():
                if sim > max_similarity and trend1 != trend2:
                    max_similarity = sim
                    max_sim_pair = (trend1, trend2)

        if max_sim_pair and max_similarity > 0.5:
            insights.append(
                f"技術相似性：{max_sim_pair[0]} 與 {max_sim_pair[1]} "
                f"在技術內容上高度相似（相似度：{max_similarity:.2f}）"
            )

        return insights
