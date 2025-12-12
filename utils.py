"""
ユーティリティ関数
ヘルパー関数を提供します。
"""

import os
from pathlib import Path
from typing import List, Dict, Any
import pandas as pd


def ensure_directory_exists(directory_path: str) -> None:
    """
    ディレクトリが存在しない場合は作成します。
    
    Args:
        directory_path: ディレクトリのパス
    """
    Path(directory_path).mkdir(parents=True, exist_ok=True)


def format_confidence(confidence: float) -> str:
    """
    信頼度を整形して返します。
    
    Args:
        confidence: 信頼度（-1〜100）
    
    Returns:
        整形された信頼度文字列
    """
    if confidence == -1:
        return "N/A"
    return f"{confidence:.1f}%"


def create_results_dataframe(ocr_data: Dict[str, List]) -> pd.DataFrame:
    """
    OCR結果から詳細データのDataFrameを作成します。
    
    Args:
        ocr_data: pytesseractから取得したOCRデータ
    
    Returns:
        整形されたDataFrame
    """
    results = []
    
    for i in range(len(ocr_data['text'])):
        word = ocr_data['text'][i].strip()
        if not word:  # 空文字列はスキップ
            continue
            
        results.append({
            '単語': word,
            '信頼度': format_confidence(ocr_data['conf'][i]),
            'X座標': ocr_data['left'][i],
            'Y座標': ocr_data['top'][i],
            '幅': ocr_data['width'][i],
            '高さ': ocr_data['height'][i],
        })
    
    return pd.DataFrame(results)


def calculate_average_confidence(ocr_data: Dict[str, List]) -> float:
    """
    平均信頼度を計算します。
    
    Args:
        ocr_data: pytesseractから取得したOCRデータ
    
    Returns:
        平均信頼度（0〜100）
    """
    confidences = [
        conf for conf, text in zip(ocr_data['conf'], ocr_data['text'])
        if text.strip() and conf != -1
    ]
    
    if not confidences:
        return 0.0
    
    return sum(confidences) / len(confidences)


def save_output(image, text: str, output_dir: str = "outputs") -> Dict[str, str]:
    """
    処理結果を保存します。
    
    Args:
        image: 処理後の画像（PIL Image）
        text: 抽出されたテキスト
        output_dir: 出力ディレクトリ
    
    Returns:
        保存されたファイルのパス情報
    """
    ensure_directory_exists(output_dir)
    
    # タイムスタンプ付きのファイル名を生成
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    image_path = os.path.join(output_dir, f"result_{timestamp}.png")
    text_path = os.path.join(output_dir, f"result_{timestamp}.txt")
    
    # 画像とテキストを保存
    image.save(image_path)
    with open(text_path, 'w', encoding='utf-8') as f:
        f.write(text)
    
    return {
        "image": image_path,
        "text": text_path
    }
