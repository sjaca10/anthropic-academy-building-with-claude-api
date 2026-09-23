import os
from pathlib import Path

import pytest
from markitdown import MarkItDownException

from tools.document import binary_document_to_markdown, document_path_to_markdown


class TestBinaryDocumentToMarkdown:
    # Define fixture paths
    FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")
    DOCX_FIXTURE = os.path.join(FIXTURES_DIR, "mcp_docs.docx")
    PDF_FIXTURE = os.path.join(FIXTURES_DIR, "mcp_docs.pdf")

    def test_fixture_files_exist(self):
        """Verify test fixtures exist."""
        assert os.path.exists(self.DOCX_FIXTURE), (
            f"DOCX fixture not found at {self.DOCX_FIXTURE}"
        )
        assert os.path.exists(self.PDF_FIXTURE), (
            f"PDF fixture not found at {self.PDF_FIXTURE}"
        )

    def test_binary_document_to_markdown_with_docx(self):
        """Test converting a DOCX document to markdown."""
        # Read binary content from the fixture
        with open(self.DOCX_FIXTURE, "rb") as f:
            docx_data = f.read()

        # Call function
        result = binary_document_to_markdown(docx_data, "docx")

        # Basic assertions to check the conversion was successful
        assert isinstance(result, str)
        assert len(result) > 0
        # Check for typical markdown formatting - this will depend on your actual test file
        assert "#" in result or "-" in result or "*" in result

    def test_binary_document_to_markdown_with_pdf(self):
        """Test converting a PDF document to markdown."""
        # Read binary content from the fixture
        with open(self.PDF_FIXTURE, "rb") as f:
            pdf_data = f.read()

        # Call function
        result = binary_document_to_markdown(pdf_data, "pdf")

        # Basic assertions to check the conversion was successful
        assert isinstance(result, str)
        assert len(result) > 0
        # Check for typical markdown formatting - this will depend on your actual test file
        assert "#" in result or "-" in result or "*" in result


class TestDocumentPathToMarkdown:
    # Define fixture paths
    FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")
    DOCX_FIXTURE = os.path.join(FIXTURES_DIR, "mcp_docs.docx")
    PDF_FIXTURE = os.path.join(FIXTURES_DIR, "mcp_docs.pdf")
    EMPTY_PDF_FIXTURE = os.path.join(FIXTURES_DIR, "empty.pdf")
    CORRUPTED_PDF_FIXTURE = os.path.join(FIXTURES_DIR, "corrupted.pdf")
    UNSUPPORTED_FIXTURE = os.path.join(FIXTURES_DIR, "unsupported.txt")

    def test_fixture_files_exist(self):
        """Verify test fixtures exist."""
        assert os.path.exists(self.DOCX_FIXTURE), (
            f"DOCX fixture not found at {self.DOCX_FIXTURE}"
        )
        assert os.path.exists(self.PDF_FIXTURE), (
            f"PDF fixture not found at {self.PDF_FIXTURE}"
        )
        assert os.path.exists(self.EMPTY_PDF_FIXTURE), (
            f"Empty PDF fixture not found at {self.EMPTY_PDF_FIXTURE}"
        )
        assert os.path.exists(self.CORRUPTED_PDF_FIXTURE), (
            f"Corrupted PDF fixture not found at {self.CORRUPTED_PDF_FIXTURE}"
        )
        assert os.path.exists(self.UNSUPPORTED_FIXTURE), (
            f"Unsupported-extension fixture not found at {self.UNSUPPORTED_FIXTURE}"
        )

    def test_document_path_to_markdown_with_docx(self):
        """Test converting a DOCX document to markdown given its file path."""
        result = document_path_to_markdown(self.DOCX_FIXTURE)

        # Basic assertions to check the conversion was successful
        assert isinstance(result, str)
        assert len(result) > 0
        # Check for typical markdown formatting - this will depend on your actual test file
        assert "#" in result or "-" in result or "*" in result

    def test_document_path_to_markdown_with_pdf(self):
        """Test converting a PDF document to markdown given its file path."""
        result = document_path_to_markdown(self.PDF_FIXTURE)

        # Basic assertions to check the conversion was successful
        assert isinstance(result, str)
        assert len(result) > 0
        # Check for typical markdown formatting - this will depend on your actual test file
        assert "#" in result or "-" in result or "*" in result

    def test_document_path_to_markdown_content_matches_binary_version(self):
        """Path-based conversion should return identical markdown to the binary-based conversion for the same file."""
        with open(self.PDF_FIXTURE, "rb") as f:
            pdf_data = f.read()

        path_result = document_path_to_markdown(self.PDF_FIXTURE)
        binary_result = binary_document_to_markdown(pdf_data, "pdf")

        assert path_result == binary_result

    def test_document_path_to_markdown_accepts_str_and_path_object(self):
        """Test that the tool accepts both a str path and a pathlib.Path object, with identical results."""
        str_result = document_path_to_markdown(self.DOCX_FIXTURE)
        path_result = document_path_to_markdown(Path(self.DOCX_FIXTURE))

        assert str_result == path_result

    def test_document_path_to_markdown_with_relative_path(self):
        """Test that a path given relative to the current working directory is resolved correctly."""
        relative_path = os.path.relpath(self.PDF_FIXTURE, os.getcwd())

        result = document_path_to_markdown(relative_path)

        assert isinstance(result, str)
        assert len(result) > 0
        assert "#" in result or "-" in result or "*" in result

    def test_document_path_to_markdown_file_not_found(self):
        """Test that a nonexistent path raises FileNotFoundError."""
        missing_path = os.path.join(self.FIXTURES_DIR, "does_not_exist.pdf")

        with pytest.raises(FileNotFoundError):
            document_path_to_markdown(missing_path)

    def test_document_path_to_markdown_unsupported_extension(self):
        """Test that a file with an unsupported extension raises a clear error."""
        with pytest.raises(ValueError):
            document_path_to_markdown(self.UNSUPPORTED_FIXTURE)

    def test_document_path_to_markdown_path_is_directory(self):
        """Test that passing a directory path raises IsADirectoryError."""
        with pytest.raises(IsADirectoryError):
            document_path_to_markdown(self.FIXTURES_DIR)

    def test_document_path_to_markdown_empty_file(self):
        """Test that an empty (zero-byte) file with a valid extension raises a conversion error."""
        with pytest.raises(MarkItDownException):
            document_path_to_markdown(self.EMPTY_PDF_FIXTURE)

    def test_document_path_to_markdown_corrupted_file(self):
        """Test that a file with a valid extension but invalid/garbage content raises a conversion error."""
        with pytest.raises(MarkItDownException):
            document_path_to_markdown(self.CORRUPTED_PDF_FIXTURE)

    def test_document_path_to_markdown_infers_type_from_extension(self):
        """Test that the tool correctly infers DOCX vs PDF handling purely from the file's extension."""
        with open(self.DOCX_FIXTURE, "rb") as f:
            docx_data = f.read()
        with open(self.PDF_FIXTURE, "rb") as f:
            pdf_data = f.read()

        docx_result = document_path_to_markdown(self.DOCX_FIXTURE)
        pdf_result = document_path_to_markdown(self.PDF_FIXTURE)

        assert docx_result == binary_document_to_markdown(docx_data, "docx")
        assert pdf_result == binary_document_to_markdown(pdf_data, "pdf")
        # Sanity check that the two fixtures actually produce different content
        assert docx_result != pdf_result
