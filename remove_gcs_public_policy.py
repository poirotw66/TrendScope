#!/usr/bin/env python3
"""
移除 Google Cloud Storage Bucket 的公開訪問政策
"""

import os
import sys
import logging

# 添加項目根目錄到 Python 路徑
sys.path.append(os.path.join(os.path.dirname(__file__)))

from base.gcs.client import get_gcs_client
from google.cloud import storage

# 設置日誌
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def remove_bucket_public_access_policy(bucket_name: str = "neo-trend-hub-documents"):
    """移除 bucket 的公開訪問政策"""
    logger.info(f"🔧 移除 bucket 公開訪問政策: {bucket_name}")
    
    try:
        gcs_client = get_gcs_client()
        if not gcs_client:
            logger.error("❌ 無法初始化 GCS 客戶端")
            return False
        
        bucket = gcs_client.client.bucket(bucket_name)
        
        # 檢查 bucket 是否存在
        if not bucket.exists():
            logger.error(f"❌ Bucket 不存在: {bucket_name}")
            return False
        
        logger.info(f"✅ Bucket 存在: {bucket_name}")
        
        # 獲取當前 IAM 政策
        logger.info("📋 獲取當前 IAM 政策...")
        policy = bucket.get_iam_policy(requested_policy_version=3)
        
        # 顯示當前政策
        logger.info("📋 當前 IAM 政策:")
        public_access_found = False
        for binding in policy.bindings:
            logger.info(f"   角色: {binding['role']}")
            logger.info(f"   成員: {binding['members']}")
            if "allUsers" in binding["members"]:
                public_access_found = True
                logger.warning(f"   ⚠️ 發現公開訪問: {binding['role']}")
            logger.info("")
        
        if not public_access_found:
            logger.info("✅ 未發現公開訪問政策，無需移除")
            return True
        
        # 移除公開訪問政策
        logger.info("🔧 移除公開訪問政策...")
        
        # 創建新的政策，排除包含 allUsers 的綁定
        new_bindings = []
        removed_bindings = []
        
        for binding in policy.bindings:
            if "allUsers" in binding["members"]:
                # 移除 allUsers，保留其他成員
                new_members = binding["members"] - {"allUsers"}
                if new_members:
                    # 如果還有其他成員，保留這個綁定但移除 allUsers
                    new_binding = {
                        "role": binding["role"],
                        "members": new_members
                    }
                    new_bindings.append(new_binding)
                    logger.info(f"   🔧 修改綁定 {binding['role']}: 移除 allUsers，保留其他成員")
                else:
                    # 如果只有 allUsers，完全移除這個綁定
                    logger.info(f"   🗑️ 完全移除綁定 {binding['role']}: 只包含 allUsers")
                
                removed_bindings.append(binding["role"])
            else:
                # 保留不包含 allUsers 的綁定
                new_bindings.append(binding)
        
        if not removed_bindings:
            logger.info("✅ 沒有需要移除的公開訪問政策")
            return True
        
        # 更新政策
        policy.bindings = new_bindings
        bucket.set_iam_policy(policy)
        
        logger.info("✅ 公開訪問政策已移除")
        logger.info(f"   移除的角色: {', '.join(removed_bindings)}")
        
        # 驗證政策更新
        logger.info("🔍 驗證政策更新...")
        updated_policy = bucket.get_iam_policy(requested_policy_version=3)
        
        public_access_still_exists = False
        for binding in updated_policy.bindings:
            if "allUsers" in binding["members"]:
                public_access_still_exists = True
                logger.warning(f"⚠️ 仍存在公開訪問: {binding['role']}")
        
        if not public_access_still_exists:
            logger.info("✅ 公開訪問政策移除驗證成功")
            logger.info("🔒 Bucket 現在設定為私有訪問")
        else:
            logger.error("❌ 公開訪問政策移除驗證失敗")
            return False
        
        return True
        
    except Exception as e:
        logger.error(f"❌ 移除 bucket 公開訪問政策時發生錯誤: {e}")
        return False

def verify_private_access(bucket_name: str = "neo-trend-hub-documents"):
    """驗證私有訪問設定"""
    logger.info(f"🔍 驗證私有訪問設定: {bucket_name}")
    
    try:
        gcs_client = get_gcs_client()
        if not gcs_client:
            logger.error("❌ 無法初始化 GCS 客戶端")
            return False
        
        bucket = gcs_client.client.bucket(bucket_name)
        bucket.reload()
        
        logger.info("📋 Bucket 配置信息:")
        logger.info(f"   名稱: {bucket.name}")
        logger.info(f"   位置: {bucket.location}")
        logger.info(f"   Storage 類別: {bucket.storage_class}")
        
        # 檢查 IAM 政策
        policy = bucket.get_iam_policy(requested_policy_version=3)
        
        logger.info("📋 當前 IAM 政策:")
        public_access_found = False
        
        for binding in policy.bindings:
            logger.info(f"   角色: {binding['role']}")
            logger.info(f"   成員: {list(binding['members'])}")
            if "allUsers" in binding["members"]:
                public_access_found = True
                logger.warning(f"   ⚠️ 發現公開訪問: {binding['role']}")
        
        if not public_access_found:
            logger.info("✅ 確認：無公開訪問政策")
            logger.info("🔒 Bucket 已正確設定為私有訪問")
        else:
            logger.warning("⚠️ 仍存在公開訪問政策")
        
        return not public_access_found
        
    except Exception as e:
        logger.error(f"❌ 驗證私有訪問設定時發生錯誤: {e}")
        return False

def main():
    """主函數"""
    try:
        logger.info("🚀 開始移除 GCS Bucket 公開訪問政策...")
        
        # 檢查環境配置
        credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        bucket_name = os.environ.get("GCS_BUCKET_NAME", "neo-trend-hub-documents")
        
        if not credentials_path:
            logger.error("❌ 未設置 GOOGLE_APPLICATION_CREDENTIALS 環境變量")
            return
        
        logger.info(f"📋 配置信息:")
        logger.info(f"   Bucket: {bucket_name}")
        logger.info(f"   憑證: {credentials_path}")
        
        # 步驟 1: 移除公開訪問政策
        logger.info("\n🔧 步驟 1: 移除公開訪問政策...")
        if not remove_bucket_public_access_policy(bucket_name):
            logger.error("❌ 移除公開訪問政策失敗")
            return
        
        # 步驟 2: 驗證私有訪問設定
        logger.info("\n🔍 步驟 2: 驗證私有訪問設定...")
        if verify_private_access(bucket_name):
            logger.info("\n🎉 Bucket 公開訪問政策移除完成!")
            logger.info("🔒 現在上傳的文件將設定為私有訪問")
            logger.info("💡 重要提醒:")
            logger.info("   1. 文件無法通過公開 URL 訪問")
            logger.info("   2. 需要適當的認證才能下載")
            logger.info("   3. 這提供了更好的安全性")
        else:
            logger.error("\n❌ 私有訪問設定驗證失敗")
        
    except KeyboardInterrupt:
        logger.info("⏹️ 操作被用戶中斷")
    except Exception as e:
        logger.error(f"❌ 操作過程中發生錯誤: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
