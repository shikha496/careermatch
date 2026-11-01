
import io
from pathlib import Path

from docx import Document
from pypdf import PdfReader


class ResumeParser:

    @staticmethod
    def parse(file_bytes: bytes, filename: str):

        extension = Path(filename).suffix.lower()

        if extension == ".pdf":
            return ResumeParser.parse_pdf(file_bytes)

        elif extension == ".docx":
            return ResumeParser.parse_docx(file_bytes)

        elif extension == ".txt":
            return file_bytes.decode(
                "utf-8",
                errors="replace"
            )

        else:
            raise ValueError(
                "Unsupported file format. Use PDF, DOCX or TXT."
            )

    @staticmethod
    def parse_pdf(file_bytes):

        reader = PdfReader(io.BytesIO(file_bytes))

        if reader.is_encrypted:
            raise ValueError("Password-protected PDF is not supported.")

        pages = []

        for page in reader.pages:
            pages.append(page.extract_text() or "")

        text = "\n".join(pages).strip()

        if not text:
            raise ValueError(
                "No extractable text found. "
                "This may be a scanned PDF requiring OCR."
            )

        return text

    @staticmethod
    def parse_docx(file_bytes):

        document = Document(io.BytesIO(file_bytes))

        paragraphs = [
            paragraph.text
            for paragraph in document.paragraphs
            if paragraph.text.strip()
        ]

        for table in document.tables:
            for row in table.rows:
                paragraphs.append(
                    " | ".join(
                        cell.text.strip()
                        for cell in row.cells
                    )
                )

        text = "\n".join(paragraphs).strip()

        if not text:
            raise ValueError("No text found in DOCX.")

        return text
