import re
import numpy as np
import cv2 as cv
import pdfplumber
import pytesseract
from pdf2image import convert_from_path
from Levenshtein import distance as levenshtein_distance

class PDFProcessor:
    """
    A class to encapsulate the entire PDF text extraction pipeline,
    aligning with the object-oriented design from Chapter III.
    """
    def __init__(self, file_path):
        self.file_path = file_path
        self.pdf_type = self._get_pdf_type()

    def _get_pdf_type(self):
        """Detects if a PDF is text-based or image-based."""
        try:
            with pdfplumber.open(self.file_path) as pdf:
                first_page_text = pdf.pages[0].extract_text()
                return "text" if first_page_text and first_page_text.strip() else "image"
        except Exception:
            return "image"

    def _preprocess_image_for_ocr(self, image):
        """Applies preprocessing to an image to improve OCR accuracy."""
        img_cv = np.array(image)
        gray = cv.cvtColor(img_cv, cv.COLOR_BGR2GRAY)
        binary = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                       cv.THRESH_BINARY, 11, 2)
        return binary

    def extract_text(self):
        """Extracts text based on the detected PDF type."""
        if self.pdf_type == 'text':
            return self._extract_from_text_pdf()
        else:
            return self._extract_from_image_pdf()

    def _extract_from_text_pdf(self):
        """Extracts text from a text-based PDF."""
        full_text = ""
        with pdfplumber.open(self.file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    full_text += page_text + "\n\n"
        return full_text

    def _extract_from_image_pdf(self):
        """Extracts text from a scanned PDF using OCR."""
        try:
            # Verify Tesseract is accessible
            # tesseract_version = pytesseract.get_tesseract_version()

            # if not tesseract_version:
            #     return ("OCR Error: Tesseract is not installed or not found in PATH. "
            #             "Please install Tesseract (https://github.com/UB-Mannheim/tesseract/wiki) "
            #             "and ensure it is added to your system PATH.")
            
            # Attempt to convert PDF to images using pdf2image (requires Poppler)
            try:
                images = convert_from_path(self.file_path, dpi=300)
            except Exception as e:
                raise RuntimeError(
                    "OCR dependencies missing. Ensure Tesseract and Poppler are installed."
                )
            full_text = ""
            for image in images:
                preprocessed_image = self._preprocess_image_for_ocr(image)
                text = pytesseract.image_to_string(preprocessed_image, lang='eng')
                full_text += text + "\n\n"
            return full_text
        except Exception as e:
            if "poppler" in str(e).lower():
                return ("OCR Error: Poppler is not installed or not found in PATH. "
                        "Please install Poppler (e.g., https://github.com/oschwartz10612/poppler-windows for Windows) "
                        "and ensure it is added to your system PATH. Original error: " + str(e))
            return f"OCR Error: {str(e)}. Ensure Tesseract and Poppler are installed and in PATH."

    @staticmethod
    def post_process_text(text):
        """Cleans raw extracted text."""
        text = re.sub(r'[\n\t]+', '\n', text)
        text = re.sub(r' +', ' ', text)
        text = re.sub(r'\n\s*(\d+|Page \d+)\s*\n', '\n', text, flags=re.IGNORECASE)
        text = text.replace('ﬁ', 'fi').replace('ﬂ', 'fl')
        return text.strip()

    @staticmethod
    def evaluate_accuracy(ground_truth_text, extracted_text):
        """
        Calculates CER and other metrics. This function represents the 'Evaluator'
        module from the design.
        """
        if not ground_truth_text:
            return {"error": "Ground truth text is empty."}
        
        # Character Error Rate (CER)
        cer = levenshtein_distance(ground_truth_text, extracted_text) / len(ground_truth_text)
        
        # Simple word-level precision/recall for F1-score
        gt_words = set(ground_truth_text.split())
        ext_words = set(extracted_text.split())
        
        true_positives = len(gt_words.intersection(ext_words))
        precision = true_positives / len(ext_words) if ext_words else 0
        recall = true_positives / len(gt_words) if gt_words else 0
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) else 0

        return {
            "Character Error Rate (CER)": f"{cer:.2%}",
            "Precision": f"{precision:.2%}",
            "Recall": f"{recall:.2%}",
            "F1-Score": f"{f1_score:.2%}"
        }
