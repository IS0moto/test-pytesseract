"""
設定ファイル
OCRエンジンの言語、PSMモード、その他の設定を定義します。
"""

# 利用可能な言語
LANGUAGES = {
    "日本語": "jpn",
    "英語": "eng",
    "英語+日本語": "eng+jpn",
}

# PSMモード（Page Segmentation Mode）
PSM_MODES = {
    "3: 完全自動ページセグメンテーション（デフォルト）": "3",
    "6: 単一の均一なテキストブロック": "6",
    "7: 単一のテキスト行": "7",
    "8: 単一の単語": "8",
    "11: 可能な限り多くのテキストを検出": "11",
}

# デフォルト設定
DEFAULT_LANGUAGE = "eng"  # English is typically pre-installed
DEFAULT_PSM_MODE = "3"
DEFAULT_OEM_MODE = "3"  # OCR Engine Mode (3 = Default, based on what is available)

# バウンディングボックスの色設定（BGR形式）
BBOX_COLOR_HIGH_CONF = (0, 255, 0)  # 緑色 - 高信頼度（80%以上）
BBOX_COLOR_MEDIUM_CONF = (0, 165, 255)  # オレンジ色 - 中信頼度（50-80%）
BBOX_COLOR_LOW_CONF = (0, 0, 255)  # 赤色 - 低信頼度（50%未満）

# バウンディングボックスの線の太さ
BBOX_THICKNESS = 2

# 信頼度のしきい値
CONFIDENCE_THRESHOLD_HIGH = 80
CONFIDENCE_THRESHOLD_MEDIUM = 50
