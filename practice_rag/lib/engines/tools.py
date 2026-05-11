import os

def keyword_search(keyword: str, file_path: str):
    """
    指定されたファイルからキーワードを含む行を抽出するツール。
    RAGのベクトル検索で見落としがちな『固有名詞』や『型番』を確実に拾います。
    """
    if not os.path.exists(file_path):
        return "ファイルが見つかりません。"
    
    results = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f, 1):
            if keyword in line:
                results.append(f"L{i}: {line.strip()}")
    
    return "\n".join(results) if results else "キーワードは見つかりませんでした。"