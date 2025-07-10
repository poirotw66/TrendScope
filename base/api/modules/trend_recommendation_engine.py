#!/usr/bin/env python3
"""
趨勢推薦引擎
基於用戶興趣和趨勢分析提供個性化推薦
"""
import logging
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import json

logger = logging.getLogger(__name__)

@dataclass
class UserProfile:
    """用戶興趣檔案"""
    user_id: str
    interests: List[str]  # 興趣關鍵詞
    preferred_trends: List[str]  # 偏好的趨勢
    interaction_history: List[Dict[str, Any]]  # 互動歷史
    expertise_level: str  # 專業程度: beginner, intermediate, expert
    
@dataclass
class RecommendationItem:
    """推薦項目"""
    item_id: str
    item_type: str  # session, trend, topic
    title: str
    description: str
    relevance_score: float
    reasoning: str
    metadata: Dict[str, Any]

class TrendRecommendationEngine:
    """趨勢推薦引擎"""
    
    def __init__(self):
        """初始化推薦引擎"""
        self.user_profiles = {}  # 用戶檔案緩存
        
    def generate_personalized_recommendations(self, 
                                            user_profile: UserProfile,
                                            trends: List[Dict[str, Any]],
                                            sessions: List[Dict[str, Any]],
                                            session_mappings: List[Dict[str, Any]],
                                            max_recommendations: int = 10) -> List[RecommendationItem]:
        """
        生成個性化推薦
        
        Args:
            user_profile: 用戶興趣檔案
            trends: 趨勢列表
            sessions: 會議列表
            session_mappings: 會議趨勢映射
            max_recommendations: 最大推薦數量
            
        Returns:
            List[RecommendationItem]: 推薦項目列表
        """
        logger.info(f"為用戶 {user_profile.user_id} 生成個性化推薦...")
        
        try:
            recommendations = []
            
            # 1. 基於興趣的趨勢推薦
            trend_recommendations = self._recommend_trends_by_interest(
                user_profile, trends
            )
            recommendations.extend(trend_recommendations)
            
            # 2. 基於趨勢的會議推薦
            session_recommendations = self._recommend_sessions_by_trends(
                user_profile, sessions, session_mappings
            )
            recommendations.extend(session_recommendations)
            
            # 3. 基於相似用戶的推薦（協同過濾）
            collaborative_recommendations = self._recommend_by_collaborative_filtering(
                user_profile, sessions, session_mappings
            )
            recommendations.extend(collaborative_recommendations)
            
            # 4. 基於內容相似性的推薦
            content_recommendations = self._recommend_by_content_similarity(
                user_profile, sessions
            )
            recommendations.extend(content_recommendations)
            
            # 5. 排序和去重
            final_recommendations = self._rank_and_deduplicate_recommendations(
                recommendations, max_recommendations
            )
            
            logger.info(f"為用戶 {user_profile.user_id} 生成了 {len(final_recommendations)} 個推薦")
            return final_recommendations
            
        except Exception as e:
            logger.error(f"生成個性化推薦失敗: {e}")
            return []
    
    def _recommend_trends_by_interest(self, user_profile: UserProfile, 
                                    trends: List[Dict[str, Any]]) -> List[RecommendationItem]:
        """基於用戶興趣推薦趨勢"""
        recommendations = []
        
        for trend in trends:
            trend_name = trend.get('name', '')
            trend_keywords = trend.get('keywords', [])
            trend_description = trend.get('description', '')
            importance_score = trend.get('importance_score', 0.0)
            
            # 計算興趣匹配度
            interest_match_score = self._calculate_interest_match(
                user_profile.interests, trend_keywords + [trend_name]
            )
            
            # 計算最終相關性分數
            relevance_score = (interest_match_score * 0.7 + importance_score * 0.3)
            
            if relevance_score > 0.3:  # 閾值過濾
                recommendations.append(RecommendationItem(
                    item_id=f"trend_{trend_name}",
                    item_type="trend",
                    title=trend_name,
                    description=trend_description[:200] + "...",
                    relevance_score=relevance_score,
                    reasoning=f"基於您對 {', '.join(user_profile.interests[:3])} 的興趣",
                    metadata={
                        'trend_data': trend,
                        'match_keywords': self._find_matching_keywords(
                            user_profile.interests, trend_keywords
                        )
                    }
                ))
        
        return recommendations
    
    def _recommend_sessions_by_trends(self, user_profile: UserProfile,
                                    sessions: List[Dict[str, Any]],
                                    session_mappings: List[Dict[str, Any]]) -> List[RecommendationItem]:
        """基於用戶偏好趨勢推薦會議"""
        recommendations = []
        
        # 創建映射字典
        mapping_dict = {
            mapping.get('session_id', ''): mapping 
            for mapping in session_mappings
        }
        
        for session in sessions:
            session_id = session.get('conference_id', session.get('id', ''))
            session_title = session.get('name', 'Unknown')
            session_content = session.get('ppt_context', '')
            
            mapping = mapping_dict.get(session_id)
            if not mapping:
                continue
                
            session_trends = mapping.get('trends', [])
            confidence_scores = mapping.get('confidence_scores', {})
            
            # 計算趨勢匹配度
            trend_match_score = self._calculate_trend_match(
                user_profile.preferred_trends, session_trends, confidence_scores
            )
            
            # 計算內容匹配度
            content_match_score = self._calculate_interest_match(
                user_profile.interests, session_content.split()[:100]
            )
            
            # 計算最終相關性分數
            relevance_score = (trend_match_score * 0.6 + content_match_score * 0.4)
            
            if relevance_score > 0.4:  # 閾值過濾
                recommendations.append(RecommendationItem(
                    item_id=f"session_{session_id}",
                    item_type="session",
                    title=session_title,
                    description=session_content[:200] + "...",
                    relevance_score=relevance_score,
                    reasoning=f"匹配您關注的趨勢: {', '.join(session_trends[:2])}",
                    metadata={
                        'session_data': session,
                        'trends': session_trends,
                        'confidence_scores': confidence_scores
                    }
                ))
        
        return recommendations
    
    def _recommend_by_collaborative_filtering(self, user_profile: UserProfile,
                                            sessions: List[Dict[str, Any]],
                                            session_mappings: List[Dict[str, Any]]) -> List[RecommendationItem]:
        """基於協同過濾的推薦（簡化版本）"""
        recommendations = []
        
        # 簡化的協同過濾：基於相似興趣的用戶行為
        # 在實際應用中，這裡會查詢數據庫中的用戶行為數據
        
        # 模擬相似用戶的偏好
        similar_user_preferences = self._find_similar_user_preferences(user_profile)
        
        for session in sessions[:5]:  # 限制數量以避免過多推薦
            session_id = session.get('conference_id', session.get('id', ''))
            session_title = session.get('name', 'Unknown')
            
            # 檢查是否被相似用戶喜歡
            if session_id in similar_user_preferences:
                recommendations.append(RecommendationItem(
                    item_id=f"collab_session_{session_id}",
                    item_type="session",
                    title=session_title,
                    description="基於相似用戶偏好推薦",
                    relevance_score=0.6,
                    reasoning="與您興趣相似的用戶也關注此內容",
                    metadata={
                        'session_data': session,
                        'recommendation_type': 'collaborative'
                    }
                ))
        
        return recommendations
    
    def _recommend_by_content_similarity(self, user_profile: UserProfile,
                                       sessions: List[Dict[str, Any]]) -> List[RecommendationItem]:
        """基於內容相似性的推薦"""
        recommendations = []
        
        # 基於用戶歷史互動內容進行相似性推薦
        user_content_profile = self._build_user_content_profile(user_profile)
        
        for session in sessions[:10]:  # 限制數量
            session_content = session.get('ppt_context', '')
            session_title = session.get('name', 'Unknown')
            session_id = session.get('conference_id', session.get('id', ''))
            
            # 計算內容相似度
            similarity_score = self._calculate_content_similarity(
                user_content_profile, session_content
            )
            
            if similarity_score > 0.3:
                recommendations.append(RecommendationItem(
                    item_id=f"content_session_{session_id}",
                    item_type="session",
                    title=session_title,
                    description=session_content[:200] + "...",
                    relevance_score=similarity_score,
                    reasoning="內容與您的興趣高度相關",
                    metadata={
                        'session_data': session,
                        'similarity_score': similarity_score,
                        'recommendation_type': 'content_based'
                    }
                ))
        
        return recommendations
    
    def _calculate_interest_match(self, user_interests: List[str], 
                                content_words: List[str]) -> float:
        """計算興趣匹配度"""
        if not user_interests or not content_words:
            return 0.0
        
        # 轉換為小寫進行比較
        user_interests_lower = [interest.lower() for interest in user_interests]
        content_words_lower = [word.lower() for word in content_words]
        
        # 計算交集
        matches = set(user_interests_lower).intersection(set(content_words_lower))
        
        # 計算匹配度
        match_score = len(matches) / len(user_interests_lower)
        return min(match_score, 1.0)
    
    def _calculate_trend_match(self, user_trends: List[str], 
                             session_trends: List[str],
                             confidence_scores: Dict[str, float]) -> float:
        """計算趨勢匹配度"""
        if not user_trends or not session_trends:
            return 0.0
        
        total_score = 0.0
        match_count = 0
        
        for user_trend in user_trends:
            if user_trend in session_trends:
                confidence = confidence_scores.get(user_trend, 0.5)
                total_score += confidence
                match_count += 1
        
        return total_score / len(user_trends) if user_trends else 0.0
    
    def _find_matching_keywords(self, user_interests: List[str], 
                              trend_keywords: List[str]) -> List[str]:
        """找到匹配的關鍵詞"""
        user_interests_lower = [interest.lower() for interest in user_interests]
        trend_keywords_lower = [keyword.lower() for keyword in trend_keywords]
        
        matches = set(user_interests_lower).intersection(set(trend_keywords_lower))
        return list(matches)
    
    def _find_similar_user_preferences(self, user_profile: UserProfile) -> List[str]:
        """找到相似用戶的偏好（模擬）"""
        # 在實際應用中，這裡會查詢數據庫
        # 現在返回模擬數據
        return ["session_001", "session_002", "session_003"]
    
    def _build_user_content_profile(self, user_profile: UserProfile) -> str:
        """構建用戶內容檔案"""
        # 基於用戶興趣和互動歷史構建內容檔案
        content_profile = " ".join(user_profile.interests)
        
        # 添加歷史互動內容
        for interaction in user_profile.interaction_history:
            if interaction.get('type') == 'view' and 'content' in interaction:
                content_profile += " " + interaction['content'][:100]
        
        return content_profile
    
    def _calculate_content_similarity(self, user_content: str, session_content: str) -> float:
        """計算內容相似度"""
        if not user_content or not session_content:
            return 0.0
        
        # 簡化的相似度計算
        user_words = set(user_content.lower().split())
        session_words = set(session_content.lower().split())
        
        if not user_words or not session_words:
            return 0.0
        
        intersection = user_words.intersection(session_words)
        union = user_words.union(session_words)
        
        return len(intersection) / len(union) if union else 0.0
    
    def _rank_and_deduplicate_recommendations(self, recommendations: List[RecommendationItem],
                                            max_count: int) -> List[RecommendationItem]:
        """排序和去重推薦結果"""
        # 去重（基於 item_id）
        seen_items = set()
        unique_recommendations = []
        
        for rec in recommendations:
            if rec.item_id not in seen_items:
                unique_recommendations.append(rec)
                seen_items.add(rec.item_id)
        
        # 按相關性分數排序
        unique_recommendations.sort(key=lambda x: x.relevance_score, reverse=True)
        
        # 限制數量
        return unique_recommendations[:max_count]
