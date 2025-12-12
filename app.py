"""
Gradio OCRアプリケーション
画像からテキストを抽出し、バウンディングボックス付きで結果を表示するWebインターフェース
"""

import gradio as gr
from PIL import Image
import pandas as pd
import pytesseract

from config import LANGUAGES, PSM_MODES
from image_preprocessor import preprocess_image
from ocr_engine import process_image_with_ocr
from utils import create_results_dataframe, format_confidence


def ocr_interface(
    image: Image.Image,
    language: str,
    psm_mode: str,
    apply_grayscale: bool,
    apply_contrast: bool,
    apply_sharpness: bool,
    apply_denoise: bool
) -> tuple:
    """
    OCR処理のメイン関数（Gradioインターフェース用）
    
    Args:
        image: 入力画像
        language: 選択された言語（日本語表記）
        psm_mode: 選択されたPSMモード（説明付き）
        apply_grayscale: グレースケール変換を適用するか
        apply_contrast: コントラスト調整を適用するか
        apply_sharpness: シャープネス調整を適用するか
        apply_denoise: ノイズ除去を適用するか
    
    Returns:
        (バウンディングボックス付き画像, 抽出テキスト, 信頼度情報, 詳細データテーブル)
    """
    if image is None:
        return None, "画像をアップロードしてください。", "", None
    
    try:
        # 言語コードとPSMモードを取得
        lang_code = LANGUAGES[language]
        psm_code = PSM_MODES[psm_mode]
        
        # 言語データの確認
        available_langs = pytesseract.get_languages()
        required_langs = lang_code.split('+')
        missing_langs = [lang for lang in required_langs if lang not in available_langs]
        
        if missing_langs:
            error_msg = f"""
**❌ エラー: 言語データが見つかりません**

選択した言語（{language}）のデータがインストールされていません。

**不足している言語データ:** {', '.join(missing_langs)}

**インストール方法:**
```bash
# Ubuntu/Debianの場合
sudo apt-get update
sudo apt-get install tesseract-ocr-{missing_langs[0]}
```

**利用可能な言語:** {', '.join(available_langs)}

英語（eng）であれば通常デフォルトでインストールされています。
"""
            return None, error_msg, "", None
        
        # 画像の前処理
        processed_image = preprocess_image(
            image,
            apply_grayscale=apply_grayscale,
            apply_contrast=apply_contrast,
            apply_sharpness=apply_sharpness,
            apply_denoise=apply_denoise
        )
        
        # OCR処理を実行
        bbox_image, extracted_text, ocr_data, avg_confidence = process_image_with_ocr(
            processed_image,
            lang=lang_code,
            psm_mode=psm_code,
            show_confidence=True
        )
        
        # テキストが抽出されなかった場合
        if not extracted_text:
            extracted_text = "（テキストが検出されませんでした）"
        
        # 信頼度情報を整形
        confidence_info = f"**平均信頼度:** {format_confidence(avg_confidence)}"
        
        # 詳細データのDataFrameを作成
        details_df = create_results_dataframe(ocr_data)
        
        return bbox_image, extracted_text, confidence_info, details_df
        
    except Exception as e:
        error_msg = f"エラーが発生しました: {str(e)}"
        return None, error_msg, "", None


def create_gradio_interface():
    """
    Gradioインターフェースを作成します。
    """
    with gr.Blocks(
        title="OCR System with Bounding Boxes"
    ) as demo:
        gr.Markdown(
            """
            # 📸 OCRシステム（バウンディングボックス表示）
            
            画像をアップロードして、テキストを抽出します。
            抽出された単語は信頼度に応じて色分けされたバウンディングボックスで表示されます。
            
            **信頼度の色分け:**
            - 🟢 **緑色**: 高信頼度 (80%以上)
            - 🟠 **オレンジ色**: 中信頼度 (50-80%)
            - 🔴 **赤色**: 低信頼度 (50%未満)
            """
        )
        
        with gr.Row():
            # 左側: 入力セクション
            with gr.Column(scale=1):
                gr.Markdown("### 📥 入力")
                
                image_input = gr.Image(
                    type="pil",
                    label="画像をアップロード",
                    height=300
                )
                
                language_dropdown = gr.Dropdown(
                    choices=list(LANGUAGES.keys()),
                    value="英語",
                    label="言語選択",
                    info="OCRで使用する言語を選択してください"
                )
                
                psm_dropdown = gr.Dropdown(
                    choices=list(PSM_MODES.keys()),
                    value="3: 完全自動ページセグメンテーション（デフォルト）",
                    label="PSMモード",
                    info="ページセグメンテーションモードを選択してください"
                )
                
                gr.Markdown("### ⚙️ 画像前処理オプション")
                
                grayscale_checkbox = gr.Checkbox(
                    label="グレースケール変換",
                    value=False,
                    info="画像を白黒に変換します"
                )
                
                contrast_checkbox = gr.Checkbox(
                    label="コントラスト強調",
                    value=False,
                    info="画像のコントラストを上げます"
                )
                
                sharpness_checkbox = gr.Checkbox(
                    label="シャープネス強調",
                    value=False,
                    info="画像をシャープにします"
                )
                
                denoise_checkbox = gr.Checkbox(
                    label="ノイズ除去",
                    value=False,
                    info="画像のノイズを除去します（処理に時間がかかります）"
                )
                
                process_btn = gr.Button(
                    "🚀 OCR処理を実行",
                    variant="primary",
                    size="lg"
                )
            
            # 右側: 出力セクション
            with gr.Column(scale=1):
                gr.Markdown("### 📤 出力")
                
                bbox_image_output = gr.Image(
                    label="バウンディングボックス付き画像",
                    height=300
                )
                
                confidence_output = gr.Markdown(
                    label="信頼度情報"
                )
                
                text_output = gr.Textbox(
                    label="抽出されたテキスト",
                    lines=8,
                    max_lines=15
                )
        
        # 詳細データテーブル（下部に配置）
        gr.Markdown("### 📊 詳細データ")
        details_output = gr.Dataframe(
            label="単語レベルの詳細情報",
            row_count=5,
            wrap=True
        )
        
        # 使用例
        gr.Markdown(
            """
            ---
            ### 💡 使い方
            
            1. 上部の「画像をアップロード」エリアに画像をドラッグ&ドロップするか、クリックしてファイルを選択
            2. 必要に応じて言語とPSMモードを選択
            3. 画像前処理オプションを選択（オプショナル）
            4. 「OCR処理を実行」ボタンをクリック
            5. 結果を確認！
            
            **ヒント:** OCR精度が低い場合は、画像前処理オプションを試してみてください。
            """
        )
        
        # イベントハンドラ
        process_btn.click(
            fn=ocr_interface,
            inputs=[
                image_input,
                language_dropdown,
                psm_dropdown,
                grayscale_checkbox,
                contrast_checkbox,
                sharpness_checkbox,
                denoise_checkbox
            ],
            outputs=[
                bbox_image_output,
                text_output,
                confidence_output,
                details_output
            ]
        )
        
        # サンプル画像の例（オプション）
        gr.Markdown(
            """
            ---
            **作成者:** Pytesseract + Gradio OCR System  
            **バージョン:** 1.0.0  
            **最終更新:** 2025-12-12
            """
        )
    
    return demo


if __name__ == "__main__":
    demo = create_gradio_interface()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True,
        inbrowser=True
    )
