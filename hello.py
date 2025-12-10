"""
Pytesseract Test Program

This program demonstrates basic usage of pytesseract for OCR (Optical Character Recognition).
It includes multiple test cases to show different features of pytesseract.
"""

import pytesseract
from PIL import Image, ImageDraw, ImageFont
import sys


def test_basic_ocr():
    """Test basic OCR functionality with a test image."""
    print("=" * 60)
    print("Test 1: Basic OCR from Image File")
    print("=" * 60)
    
    try:
        # Load the test image
        image = Image.open('test_image.png')
        
        # Perform OCR
        text = pytesseract.image_to_string(image, lang='eng')
        
        print(f"Extracted text:\n{text}")
        print("✓ Test passed\n")
        return True
    except Exception as e:
        print(f"✗ Test failed: {e}\n")
        return False


def test_ocr_with_config():
    """Test OCR with custom configuration."""
    print("=" * 60)
    print("Test 2: OCR with Custom Configuration")
    print("=" * 60)
    
    try:
        image = Image.open('test_image.png')
        
        # Use custom config for better accuracy
        custom_config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(image, config=custom_config)
        
        print(f"Extracted text with custom config:\n{text}")
        print("✓ Test passed\n")
        return True
    except Exception as e:
        print(f"✗ Test failed: {e}\n")
        return False


def test_get_data():
    """Test getting detailed OCR data."""
    print("=" * 60)
    print("Test 3: Get Detailed OCR Data")
    print("=" * 60)
    
    try:
        image = Image.open('test_image.png')
        
        # Get detailed data
        data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
        
        print("Detected words and their confidence levels:")
        for i, word in enumerate(data['text']):
            if word.strip():  # Only show non-empty words
                conf = data['conf'][i]
                print(f"  - '{word}' (confidence: {conf}%)")
        
        print("✓ Test passed\n")
        return True
    except Exception as e:
        print(f"✗ Test failed: {e}\n")
        return False


def test_create_and_read_image():
    """Create a simple image with text and read it."""
    print("=" * 60)
    print("Test 4: Create Image and Perform OCR")
    print("=" * 60)
    
    try:
        # Create a simple image with text
        img = Image.new('RGB', (400, 100), color='white')
        draw = ImageDraw.Draw(img)
        
        # Draw text on image
        text = "Pytesseract Test 123!"
        draw.text((20, 30), text, fill='black')
        
        # Save the created image
        img.save('generated_test.png')
        print("Created test image: generated_test.png")
        
        # Perform OCR on the created image
        extracted_text = pytesseract.image_to_string(img)
        
        print(f"Original text: {text}")
        print(f"Extracted text: {extracted_text.strip()}")
        print("✓ Test passed\n")
        return True
    except Exception as e:
        print(f"✗ Test failed: {e}\n")
        return False


def test_version_info():
    """Display pytesseract and Tesseract version information."""
    print("=" * 60)
    print("Version Information")
    print("=" * 60)
    
    try:
        # Get Tesseract version
        version = pytesseract.get_tesseract_version()
        print(f"Tesseract version: {version}")
        
        # Get available languages
        languages = pytesseract.get_languages()
        print(f"Available languages: {', '.join(languages)}")
        print("✓ Version check passed\n")
        return True
    except Exception as e:
        print(f"✗ Version check failed: {e}")
        print("\nNote: Make sure Tesseract OCR is installed on your system.")
        print("Install on Ubuntu/Debian: sudo apt-get install tesseract-ocr")
        print("Install on macOS: brew install tesseract")
        print("Install on Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki\n")
        return False


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("PYTESSERACT TEST SUITE")
    print("=" * 60 + "\n")
    
    results = []
    
    # Check if Tesseract is installed
    results.append(("Version Info", test_version_info()))
    
    # Run tests only if Tesseract is available
    if results[0][1]:
        results.append(("Basic OCR", test_basic_ocr()))
        results.append(("OCR with Config", test_ocr_with_config()))
        results.append(("Detailed Data", test_get_data()))
        results.append(("Create & Read", test_create_and_read_image()))
    
    # Summary
    print("=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{test_name}: {status}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"\nTotal: {passed}/{total} tests passed")
    print("=" * 60 + "\n")
    
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
