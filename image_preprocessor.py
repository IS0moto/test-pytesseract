"""
画像前処理モジュール
OCR精度を向上させるための画像前処理機能を提供します。
"""

from PIL import Image, ImageEnhance, ImageFilter
import cv2
import numpy as np
from typing import Tuple


def pil_to_cv2(pil_image: Image.Image) -> np.ndarray:
    """
    PIL ImageをOpenCV形式に変換します。
    
    Args:
        pil_image: PIL Image
    
    Returns:
        OpenCV形式の画像（numpy array）
    """
    # RGBに変換してからnumpy配列に変換
    rgb_image = pil_image.convert('RGB')
    open_cv_image = np.array(rgb_image)
    # RGBからBGRに変換（OpenCVはBGRを使用）
    open_cv_image = open_cv_image[:, :, ::-1].copy()
    return open_cv_image


def cv2_to_pil(cv2_image: np.ndarray) -> Image.Image:
    """
    OpenCV形式をPIL Imageに変換します。
    
    Args:
        cv2_image: OpenCV形式の画像
    
    Returns:
        PIL Image
    """
    # BGRからRGBに変換
    rgb_image = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)
    return Image.fromarray(rgb_image)


def convert_to_grayscale(image: Image.Image) -> Image.Image:
    """
    画像をグレースケールに変換します。
    
    Args:
        image: 入力画像
    
    Returns:
        グレースケール画像
    """
    return image.convert('L')


def enhance_contrast(image: Image.Image, factor: float = 2.0) -> Image.Image:
    """
    画像のコントラストを調整します。
    
    Args:
        image: 入力画像
        factor: コントラスト係数（1.0 = 元の画像, >1.0 = コントラスト増加）
    
    Returns:
        コントラスト調整後の画像
    """
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(factor)


def enhance_sharpness(image: Image.Image, factor: float = 2.0) -> Image.Image:
    """
    画像のシャープネスを調整します。
    
    Args:
        image: 入力画像
        factor: シャープネス係数（1.0 = 元の画像, >1.0 = シャープネス増加）
    
    Returns:
        シャープネス調整後の画像
    """
    enhancer = ImageEnhance.Sharpness(image)
    return enhancer.enhance(factor)


def denoise_image(image: Image.Image) -> Image.Image:
    """
    画像のノイズを除去します。
    
    Args:
        image: 入力画像
    
    Returns:
        ノイズ除去後の画像
    """
    # OpenCV形式に変換
    cv2_image = pil_to_cv2(image)
    
    # Non-local Means Denoisingを適用
    denoised = cv2.fastNlMeansDenoisingColored(cv2_image, None, 10, 10, 7, 21)
    
    # PIL形式に戻す
    return cv2_to_pil(denoised)


def preprocess_image(
    image: Image.Image,
    apply_grayscale: bool = False,
    apply_contrast: bool = False,
    apply_sharpness: bool = False,
    apply_denoise: bool = False,
    contrast_factor: float = 2.0,
    sharpness_factor: float = 2.0
) -> Image.Image:
    """
    画像に前処理を適用します。
    
    Args:
        image: 入力画像
        apply_grayscale: グレースケール変換を適用するか
        apply_contrast: コントラスト調整を適用するか
        apply_sharpness: シャープネス調整を適用するか
        apply_denoise: ノイズ除去を適用するか
        contrast_factor: コントラスト係数
        sharpness_factor: シャープネス係数
    
    Returns:
        前処理後の画像
    """
    processed_image = image.copy()
    
    # ノイズ除去（最初に適用）
    if apply_denoise:
        processed_image = denoise_image(processed_image)
    
    # コントラスト調整
    if apply_contrast:
        processed_image = enhance_contrast(processed_image, contrast_factor)
    
    # シャープネス調整
    if apply_sharpness:
        processed_image = enhance_sharpness(processed_image, sharpness_factor)
    
    # グレースケール変換（最後に適用）
    if apply_grayscale:
        processed_image = convert_to_grayscale(processed_image)
    
    return processed_image
