# Pytesseract Test Project

Pytesseractライブラリを使用したOCR（光学文字認識）のテストプロジェクトです。uvを使用して依存関係を管理しています。

## 📋 概要

このプロジェクトは、PythonからTesseract OCRエンジンを使用するための包括的なテスト環境を提供します。基本的なテキスト抽出から詳細なデータ分析まで、pytesseractの主要機能をデモンストレーションします。

## ✨ 機能

- ✅ 画像ファイルからのテキスト抽出
- ✅ カスタム設定によるOCR精度の調整
- ✅ 単語レベルの信頼度スコア取得
- ✅ プログラムによる画像生成とOCR処理
- ✅ バージョン情報と利用可能な言語の確認

## 🔧 必要なもの

### システム要件
- Python 3.x
- Tesseract OCR エンジン
- uv（Pythonパッケージマネージャー）

### システムパッケージのインストール

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
```

**macOS:**
```bash
brew install tesseract
```

**Windows:**
[Tesseract at UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki)からインストーラーをダウンロード

## 🚀 セットアップ

1. **リポジトリのクローン:**
   ```bash
   git clone https://github.com/IS0moto/test-pytesseract.git
   ```

2. **依存関係のインストール:**
   ```bash
   uv sync
   ```

   または、uvがまだインストールされていない場合：
   ```bash
   # uvのインストール
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # プロジェクトの依存関係をインストール
   uv sync
   ```

## 📖 使い方

### テストプログラムの実行

```bash
# uvを使用して実行
uv run hello.py

# または仮想環境を有効化してから実行
source .venv/bin/activate
python hello.py
```

### プログラムでの使用例

```python
import pytesseract
from PIL import Image

# 基本的な使い方
image = Image.open('your_image.png')
text = pytesseract.image_to_string(image, lang='eng')
print(text)

# カスタム設定での使用
custom_config = r'--oem 3 --psm 6'
text = pytesseract.image_to_string(image, config=custom_config)

# 詳細データの取得
data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
for i, word in enumerate(data['text']):
    if word.strip():
        confidence = data['conf'][i]
        print(f"単語: {word}, 信頼度: {confidence}%")
```

## 📁 プロジェクト構成

```
test-pytesseract/
├── README.md              # このファイル
├── hello.py               # メインテストプログラム
├── pyproject.toml         # プロジェクト設定と依存関係
├── uv.lock               # 依存関係のロックファイル
├── test_image.png        # テスト用サンプル画像
├── generated_test.png    # 自動生成されたテスト画像
└── .venv/                # 仮想環境（自動生成）
```

## 🧪 テスト結果

`hello.py`を実行すると、以下の5つのテストが実行されます：

| テスト名 | 説明 | 結果 |
|---------|------|------|
| Version Info | Tesseractのバージョン確認 | ✓ PASS |
| Basic OCR | 基本的なテキスト抽出 | ✓ PASS |
| OCR with Config | カスタム設定での抽出 | ✓ PASS |
| Detailed Data | 詳細データと信頼度取得 | ✓ PASS |
| Create & Read | 画像生成とOCR処理 | ✓ PASS |

**テスト成功率: 5/5 (100%)**

## 🌐 追加の言語サポート

日本語など他の言語を使用する場合は、追加の言語データをインストールします：

```bash
# 日本語
sudo apt-get install tesseract-ocr-jpn

# 中国語（簡体字）
sudo apt-get install tesseract-ocr-chi-sim

# 韓国語
sudo apt-get install tesseract-ocr-kor
```

使用例：
```python
# 日本語OCR
text = pytesseract.image_to_string(image, lang='jpn')

# 複数言語の組み合わせ
text = pytesseract.image_to_string(image, lang='eng+jpn')
```

## 📚 依存関係

- **pytesseract** (0.3.13) - Tesseract OCRのPythonラッパー
- **Pillow** (12.0.0) - Python画像処理ライブラリ
- **packaging** (25.0) - pytesseractの依存関係

## 💡 ヒント

### OCR精度を向上させるには

1. **画像の前処理:**
   ```python
   from PIL import ImageEnhance
   
   # コントラストを上げる
   enhancer = ImageEnhance.Contrast(image)
   image = enhancer.enhance(2)
   
   # グレースケール変換
   image = image.convert('L')
   ```

2. **適切なPSMモードの選択:**
   - PSM 3: 完全自動ページセグメンテーション（デフォルト）
   - PSM 6: 単一の均一なテキストブロック
   - PSM 7: 単一のテキスト行
   - PSM 8: 単一の単語

3. **画質の改善:**
   - 高解像度の画像を使用（DPI 300以上推奨）
   - 明瞭なフォントと適切なコントラスト
   - ノイズの除去

## 🔗 関連リンク

- [Pytesseract GitHub](https://github.com/madmaze/pytesseract)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [uv Documentation](https://docs.astral.sh/uv/)

## 📄 ライセンス

このプロジェクトはテスト・学習目的で作成されています。

## 🤝 貢献

バグ報告や改善提案は歓迎します！

---

**作成日:** 2025-12-11  
**Tesseractバージョン:** 5.3.4  
**Pythonバージョン:** 3.x
