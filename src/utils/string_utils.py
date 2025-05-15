import re

def normalize_string(text, remove_chars=r'[\\/":_\'*?\"<>()-|]', keep_extension=False):
    """
    标准化字符串，移除不需要的字符。
    
    Args:
        text (str): 需要标准化的字符串
        remove_chars (str): 正则表达式，指定要移除的字符
        keep_extension (bool): 是否保留文件扩展名
        
    Returns:
        str: 标准化后的字符串
    """
    if not text:
        return ""
        
    text = str(text)
    
    # 如果需要保留扩展名
    extension = ""
    if keep_extension and "." in text:
        parts = text.rsplit(".", 1)
        if len(parts) == 2 and parts[1]:
            text = parts[0]
            extension = "." + parts[1]
    
    # 移除指定字符
    normalized = re.sub(remove_chars, '', text)
    normalized = normalized.strip()
    
    # 添加回扩展名（如果需要）
    if extension:
        normalized += extension
        
    return normalized
