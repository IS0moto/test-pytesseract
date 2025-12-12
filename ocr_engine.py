"""
OCRエンジンモジュール
pytesseractを使用したOCR処理とバウンディングボックスの描画機能を提供します。
"""

import pytesseract
from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np
from typing import Dict, List, Tuple, Any

from config import (
    DEFAULT_PSM_MODE,
    DEFAULT_OEM_MODE,
    BBOX_COLOR_HIGH_CONF,
    BBOX_COLOR_MEDIUM_CONF,
    BBOX_COLOR_LOW_CONF,
    BBOX_THICKNESS,
    CONFIDENCE_THRESHOLD_HIGH,
    CONFIDENCE_THRESHOLD_MEDIUM,
)


def perform_ocr(
    image: Image.Image,
    lang: str = 'eng',
    psm_mode: str = DEFAULT_PSM_MODE
) -> str:
    """
    画像からテキストを抽出します。
    
    Args:
        image: 入力画像
        lang: 言語コード（例: 'eng', 'jpn', 'eng+jpn'）
        psm_mode: Page Segmentation Mode
    
    Returns:
        抽出されたテキスト
    """
    custom_config = f'--oem {DEFAULT_OEM_MODE} --psm {psm_mode}'
    text = pytesseract.image_to_string(image, lang=lang, config=custom_config)
    return text.strip()


def get_ocr_data(
    image: Image.Image,
    lang: str = 'eng',
    psm_mode: str = DEFAULT_PSM_MODE
) -> Dict[str, List]:
    """
    画像からOCRの詳細データを取得します。
    
    Args:
        image: 入力画像
        lang: 言語コード
        psm_mode: Page Segmentation Mode
    
    Returns:
        OCRデータ（単語、座標、信頼度など）
    """
    custom_config = f'--oem {DEFAULT_OEM_MODE} --psm {psm_mode}'
    data = pytesseract.image_to_data(
        image,
        lang=lang,
        config=custom_config,
        output_type=pytesseract.Output.DICT
    )
    return data


def get_bbox_color(confidence: float) -> Tuple[int, int, int]:
    """
    信頼度に基づいてバウンディングボックスの色を決定します。
    
    Args:
        confidence: 信頼度（0〜100）
    
    Returns:
        BGR形式の色タプル
    """
    if confidence >= CONFIDENCE_THRESHOLD_HIGH:
        return BBOX_COLOR_HIGH_CONF
    elif confidence >= CONFIDENCE_THRESHOLD_MEDIUM:
        return BBOX_COLOR_MEDIUM_CONF
    else:
        return BBOX_COLOR_LOW_CONF


def draw_bounding_boxes(
    image: Image.Image,
    ocr_data: Dict[str, List],
    show_confidence: bool = True
) -> Image.Image:
    """
    画像にバウンディングボックスを描画します。
    
    Args:
        image: 入力画像
        ocr_data: OCRデータ
        show_confidence: 信頼度を表示するか
    
    Returns:
        バウンディングボックスが描画された画像
    """
    # PIL ImageをOpenCV形式に変換
    cv2_image = np.array(image.convert('RGB'))
    cv2_image = cv2_image[:, :, ::-1].copy()  # RGBからBGRに変換
    
    n_boxes = len(ocr_data['text'])
    
    for i in range(n_boxes):
        # 空のテキストや信頼度が-1のものはスキップ
        if not ocr_data['text'][i].strip() or int(ocr_data['conf'][i]) == -1:
            continue
        
        # バウンディングボックスの座標を取得
        x = ocr_data['left'][i]
        y = ocr_data['top'][i]
        w = ocr_data['width'][i]
        h = ocr_data['height'][i]
        conf = float(ocr_data['conf'][i])
        
        # 信頼度に基づいて色を決定
        color = get_bbox_color(conf)
        
        # 矩形を描画
        cv2.rectangle(
            cv2_image,
            (x, y),
            (x + w, y + h),
            color,
            BBOX_THICKNESS
        )
        
        # 信頼度を表示
        if show_confidence:
            label = f"{conf:.0f}%"
            # ラベルの背景を描画
            label_size, _ = cv2.getTextSize(
                label,
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                1
            )
            cv2.rectangle(
                cv2_image,
                (x, y - label_size[1] - 4),
                (x + label_size[0], y),
                color,
                -1  # 塗りつぶし
            )
            # ラベルのテキストを描画
            cv2.putText(
                cv2_image,
                label,
                (x, y - 2),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),  # 白色
                1
            )
    
    # OpenCV形式からPIL Imageに変換
    rgb_image = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)
    result_image = Image.fromarray(rgb_image)
    
    return result_image


def process_image_with_ocr(
    image: Image.Image,
    lang: str = 'eng',
    psm_mode: str = DEFAULT_PSM_MODE,
    show_confidence: bool = True
) -> Tuple[Image.Image, str, Dict[str, List], float]:
    """
    画像に対してOCR処理を実行し、バウンディングボックス付きの画像を生成します。
    
    Args:
        image: 入力画像
        lang: 言語コード
        psm_mode: Page Segmentation Mode
        show_confidence: 信頼度を表示するか
    
    Returns:
        (バウンディングボックス付き画像, 抽出テキスト, OCRデータ, 平均信頼度)
    """
    # OCRデータを取得
    ocr_data = get_ocr_data(image, lang, psm_mode)
    
    # テキストを抽出
    text = perform_ocr(image, lang, psm_mode)
    
    # バウンディングボックスを描画
    bbox_image = draw_bounding_boxes(image, ocr_data, show_confidence)
    
    # 平均信頼度を計算
    confidences = [
        float(conf) for conf, txt in zip(ocr_data['conf'], ocr_data['text'])
        if txt.strip() and int(conf) != -1
    ]
    avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0
    
    return bbox_image, text, ocr_data, avg_confidence
