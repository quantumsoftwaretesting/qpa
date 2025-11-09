# Reporting module for QPA: Quantum Patterns Analyser

"""
This module contains all reporting functionality for the QPA: Quantum Patterns Analyser project.

The reporting module provides:
- Unified report generation system
- Pattern analysis utilities
- PDF generation capabilities
- Comprehensive data export

Key Classes:
- ReportGenerator: Unified system for all report types
- PatternAnalyzer: Pattern coverage and statistics analysis
- PDFGenerator: Markdown to PDF conversion utilities
"""

from .report_generator import (
    ReportGenerator,
    generate_experimental_data_report,
    generate_base_concept_report,
    generate_pattern_report,
    generate_extended_pattern_analysis,
    generate_all_reports,
    main as generate_reports_main,
)

from .pattern_analyzer import (
    PatternAnalyzer,
    analyze_pattern_coverage,
    get_pattern_statistics,
    export_pattern_analysis,
    main as analyze_patterns_main,
)

# PDF Generator imports are lazy-loaded to avoid WeasyPrint dependency issues
# when only using report generation functionality
def _lazy_pdf_import():
    """Lazy import for PDF generator to avoid WeasyPrint dependency issues."""
    try:
        from .pdf_generator import (
            PDFGenerator,
            generate_pdfs,
            main as generate_pdfs_main,
        )
        return PDFGenerator, generate_pdfs, generate_pdfs_main
    except (ImportError, OSError) as e:
        raise ImportError(
            "PDF generation requires WeasyPrint and system libraries. "
            "Install system dependencies: https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#installation"
        ) from e

__all__ = [
    # Report Generator
    "ReportGenerator",
    "generate_experimental_data_report",
    "generate_base_concept_report", 
    "generate_pattern_report",
    "generate_extended_pattern_analysis",
    "generate_all_reports",
    "generate_reports_main",
    
    # Pattern Analyzer
    "PatternAnalyzer",
    "analyze_pattern_coverage",
    "get_pattern_statistics",
    "export_pattern_analysis",
    "analyze_patterns_main",
    
    # PDF Generator (lazy-loaded)
    "PDFGenerator",
    "generate_pdfs",
    "generate_pdfs_main",
]

# Lazy-load PDF generator attributes
def __getattr__(name):
    if name in ("PDFGenerator", "generate_pdfs", "generate_pdfs_main"):
        PDFGenerator, generate_pdfs, generate_pdfs_main = _lazy_pdf_import()
        if name == "PDFGenerator":
            return PDFGenerator
        elif name == "generate_pdfs":
            return generate_pdfs
        elif name == "generate_pdfs_main":
            return generate_pdfs_main
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")