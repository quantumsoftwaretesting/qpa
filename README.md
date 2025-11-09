# QPA: Quantum Patterns Analyser

This project analyzes source code from quantum computing libraries to identify recurring software patterns. It uses `just` as a command runner to execute the pipeline from data collection to analysis and reporting.

The workflow queries the GitHub API to find quantum software projects, clones them, preprocesses their code (including Jupyter Notebooks), and runs analysis scripts to extract and classify programming concepts.

## Research Contributions

This project provides two datasets as key contributions:

### 1. Quantum Patterns Knowledge Base

**File:** [`data/knowledge_base/knowledge_base.csv`](data/knowledge_base/knowledge_base.csv)

A knowledge base consolidating quantum computing concepts from three major frameworks (Qiskit, PennyLane, and Classiq). This dataset contains:

- **Framework concepts**: Extracted programming concepts (functions, classes, methods) from Qiskit, PennyLane, and Classiq
- **Pattern classifications**: Manual classification of concepts mapped to quantum software patterns from the PlanQK Pattern Atlas
- **Unified format**: Single consolidated dataset combining all three framework-specific datasets for easy analysis and comparison

This knowledge base serves as a reference dataset for understanding how quantum computing concepts are implemented across different frameworks and how they relate to established software patterns.

### 2. Quantum Concept Pattern Matches

**File:** [`data/quantum_concept_matches_with_patterns.csv`](data/quantum_concept_matches_with_patterns.csv)

A dataset documenting the semantic analysis results matching quantum computing concepts found in target projects to patterns in the knowledge base. This dataset contains:

- **Concept matches**: Identified quantum computing concepts from analyzed projects
- **Pattern mappings**: Matches between discovered concepts and patterns from the PlanQK Pattern Atlas
- **Match metadata**: Information about match types (name-based, semantic, etc.), confidence scores, and source frameworks
- **Project context**: Which projects contain which patterns and how patterns are adopted across the quantum software ecosystem

This dataset provides insights into how quantum software patterns are actually used in practice across different quantum computing projects.

**Note:** Both datasets are generated through the workflow described below. To reproduce these datasets, follow the replication workflow starting from Step 0.

## Workflow Overview

The project follows an 8-step workflow organized into three stages:

**Stage 1: Data Acquisition (Steps 1-2)**
- Step 1: Download Patterns → Pattern Definitions ([`quantum_patterns.json`](data/quantum_patterns.json))
- Step 2: Discover Projects → Project List ([`filtered_repo_list.txt`](data/filtered_repo_list.txt))

**Stage 2: Project and Concept Processing (Steps 3-6)**
- Step 3: Extract Concepts → Framework concept files
- Step 4: Manual Classification → Classified Concepts
- Step 5: Extract Notebooks → Notebook files
- Step 6: Convert Notebooks → Python Files

**Stage 3: Analysis and Reporting (Steps 7-8)**
- Step 7: Run Analysis → Pattern Matches
- Step 8: Generate Report → Markdown Report, CSV Tables, Experimental Data

Visual workflow diagrams are available in the `docs/` directory:
- [`diagram1.mermaid`](docs/diagram1.mermaid) - Data Acquisition Stage
- [`diagram2.mermaid`](docs/diagram2.mermaid) - Project and Concept Processing Stage
- [`diagram3.mermaid`](docs/diagram3.mermaid) - Analysis and Reporting Stage

## Project Setup & Installation

### Prerequisites

- **Python 3.12+**
- **Just**: Command runner. Installation instructions: [here](https://github.com/casey/just#installation)
- **Git**: For cloning repositories
- **GitHub Personal Access Token (PAT)**: Required to avoid API rate limits. Create a token and save it in a [`.env`](.env) file in the project root:

```text
# in .env file
GITHUB_TOKEN="ghp_YourTokenHere"
```

## Replication Workflow: Step-by-Step Guide

This guide describes the sequence of commands to set up the project and replicate the study's results.

### Step 0: Initial Project Setup

This command prepares the project. It will:
1. Discover and clone quantum software repositories from GitHub
2. Create a virtual environment (`.venv`)
3. Install Python dependencies from [`pyproject.toml`](pyproject.toml)
4. Install cloned `qiskit` and `pennylane` repositories in editable mode

```bash
just install
```

Note: This command re-runs the setup each time to ensure a clean state. The initial run requires time and disk space.

### Step 1: Download Quantum Pattern Definitions

Fetches quantum software patterns from the PlanQK Pattern Atlas for use as a classification baseline.

```bash
just download_pattern_list
```

Output: [`data/quantum_patterns.json`](data/quantum_patterns.json) (59 quantum patterns)

### Step 2: Discover Target Projects from GitHub

Searches GitHub for quantum computing projects and filters them.

```bash
just search-repos
```

This runs [`src/data_acquisition/discover_projects.py`](src/data_acquisition/discover_projects.py) to find and filter quantum projects.

Output: [`data/filtered_repo_list.txt`](data/filtered_repo_list.txt)

### Step 3: Extract Core Concepts from Frameworks

Parses source code from Qiskit, PennyLane, and Classiq to identify core concepts (functions and classes).

```bash
just identify-concepts
```

This command generates the following files in the `data/` directory:
- [`data/classiq_quantum_concepts.csv`](data/classiq_quantum_concepts.csv)
- [`data/pennylane_quantum_concepts.csv`](data/pennylane_quantum_concepts.csv)
- [`data/qiskit_quantum_concepts.csv`](data/qiskit_quantum_concepts.csv)

### Step 4: Manual Concept Classification

This is the only manual step in the workflow. Classify the concepts extracted in Step 3. Two options:

*   **To replicate existing results:** Pre-classified files are provided in the `data/knowledge_base/` directory:
    *   [`data/knowledge_base/enriched_classiq_quantum_patterns.csv`](data/knowledge_base/enriched_classiq_quantum_patterns.csv)
    *   [`data/knowledge_base/enriched_pennylane_quantum_patterns.csv`](data/knowledge_base/enriched_pennylane_quantum_patterns.csv)
    *   [`data/knowledge_base/enriched_qiskit_quantum_patterns.csv`](data/knowledge_base/enriched_qiskit_quantum_patterns.csv)
    *   [`data/knowledge_base/knowledge_base.csv`](data/knowledge_base/knowledge_base.csv) - Consolidated knowledge base

*   **To perform your own classification:**
    1.  Open the `_quantum_concepts.csv` files generated in Step 3
    2.  Add classification data to the rows
    3.  Save the modified files with the `enriched_` prefix in the `data/knowledge_base/` directory (e.g., [`data/knowledge_base/enriched_qiskit_quantum_patterns.csv`](data/knowledge_base/enriched_qiskit_quantum_patterns.csv))

Output: Classified Concepts (enriched CSV files)

**Note:** After Step 4, the consolidated knowledge base [`data/knowledge_base/knowledge_base.csv`](data/knowledge_base/knowledge_base.csv) is available. This is one of the key research contributions (see [Key Research Contributions](#key-research-contributions)).

### Step 5: Extract Notebooks

Finds all Jupyter Notebooks (`.ipynb`) within the cloned projects.

```bash
just preprocess-notebooks
```

This extracts notebooks from discovered projects.

### Step 6: Convert Notebooks

Converts Jupyter Notebooks to Python scripts (`.ipynb.py`) for analysis and creates an archive of the original notebooks.

```bash
just convert-archived-notebooks
```

Output: Python Files (converted `.py` files)

### Step 7: Run Analysis

Runs the semantic analysis workflow using the `enriched_*.csv` files and preprocessed source code to search for quantum computing concepts across target projects.

```bash
just run_main
```

Note: Ignore these warnings in the output (they are warnings, not errors):

```bash
<unknown>:238: SyntaxWarning: invalid escape sequence '\d'
<unknown>:485: SyntaxWarning: invalid escape sequence '\D'
```

Output: Pattern Matches ([`data/quantum_concept_matches_with_patterns.csv`](data/quantum_concept_matches_with_patterns.csv))

**Note:** This file is one of the key research contributions (see [Key Research Contributions](#key-research-contributions)). It contains the semantic analysis results matching quantum concepts from target projects to patterns in the knowledge base.

### Step 8: Generate Report

Generates the final report summarizing the analysis findings.

```bash
just report
```

This creates:
- [`data/final_pattern_report.txt`](data/final_pattern_report.txt) - Text summary report
- [`docs/final_pattern_report.md`](docs/final_pattern_report.md) - Markdown report
- [`data/report/`](data/report/) - CSV tables for analysis

### Step 8.1: Generate Experimental Data Report

After completing all previous steps, generate the experimental data report. This command requires all data files from Steps 1-7 to exist.

```bash
just experimental-data
```

This creates [`docs/experimental_data.md`](docs/experimental_data.md) with datasets formatted for academic use, including row numbers and data.

**Note:** This command will fail if the required data files have not been generated by the previous workflow steps. Ensure you have completed Steps 1-7 before running this command.

## Experimental Data

After completing the workflow steps (Steps 0-8), you can generate a report containing all experimental datasets. The experimental data report includes:

**Framework Concept Extractions:**
- Classiq Quantum Patterns ([`data/classiq_quantum_concepts.csv`](data/classiq_quantum_concepts.csv))
- PennyLane Quantum Patterns ([`data/pennylane_quantum_concepts.csv`](data/pennylane_quantum_concepts.csv))
- Qiskit Quantum Patterns ([`data/qiskit_quantum_concepts.csv`](data/qiskit_quantum_concepts.csv))
- Consolidated Knowledge Base ([`data/knowledge_base/knowledge_base.csv`](data/knowledge_base/knowledge_base.csv))

**Pattern Analysis Results:**
- Top 10 Most Frequently Matched Quantum Concepts ([`data/report/top_matched_concepts.csv`](data/report/top_matched_concepts.csv))
- Match Type Analysis ([`data/report/match_type_counts.csv`](data/report/match_type_counts.csv))
- Framework Analysis ([`data/report/matches_by_framework.csv`](data/report/matches_by_framework.csv))
- Pattern Frequency Analysis ([`data/report/patterns_by_match_count.csv`](data/report/patterns_by_match_count.csv))

**Pattern Atlas Data:**
- Quantum patterns from PlanQK Pattern Atlas ([`data/quantum_patterns.json`](data/quantum_patterns.json))
- Pattern metadata including names, aliases, intents, and descriptions

**Prerequisites:** All workflow steps (Steps 0-8) must be completed before generating the experimental data report. The report generation requires the following files to exist:
- Framework concept files from Step 3
- Enriched pattern files from Step 4
- Pattern definitions from Step 1
- Analysis results from Step 7

## Workflow Orchestration

The project includes Prefect for workflow orchestration, providing dependency management, error handling, and monitoring.

### Quick Start with Orchestration

```bash
# Run the workflow with orchestration
just workflow

# Monitor progress
just workflow-ui
# Open http://localhost:4200 in your browser
```

### Orchestration Features

| **Manual Execution** | **Prefect Orchestration** |
|---------------------|---------------------------|
| Manual dependency tracking | Automatic dependency resolution |
| No retry logic | Built-in retry with exponential backoff |
| No progress monitoring | Progress dashboard |
| Manual error handling | Failure recovery |
| Sequential execution only | Parallel execution where possible |
| No execution history | Execution logs and history |

## Generated Files & Outputs

### Key Research Datasets

**Primary Contributions:**
- [`data/knowledge_base/knowledge_base.csv`](data/knowledge_base/knowledge_base.csv) - **Consolidated Quantum Patterns Knowledge Base** (see [Key Research Contributions](#key-research-contributions))
- [`data/quantum_concept_matches_with_patterns.csv`](data/quantum_concept_matches_with_patterns.csv) - **Quantum Concept Pattern Matches** (see [Key Research Contributions](#key-research-contributions))

### Main Analysis Outputs

**Reports:**
- [`docs/final_pattern_report.md`](docs/final_pattern_report.md) - Main analysis report (Markdown)
- [`data/final_pattern_report.txt`](data/final_pattern_report.txt) - Main analysis report (Text)
- [`docs/experimental_data.md`](docs/experimental_data.md) - Experimental datasets

**CSV Data Tables:**
- [`data/classiq_quantum_concepts.csv`](data/classiq_quantum_concepts.csv) - Classiq framework concepts
- [`data/pennylane_quantum_concepts.csv`](data/pennylane_quantum_concepts.csv) - PennyLane framework concepts
- [`data/qiskit_quantum_concepts.csv`](data/qiskit_quantum_concepts.csv) - Qiskit framework concepts
- [`data/knowledge_base/knowledge_base.csv`](data/knowledge_base/knowledge_base.csv) - Consolidated knowledge base
- [`data/quantum_patterns.json`](data/quantum_patterns.json) - Pattern Atlas data

**Analysis Results:**
- [`data/report/top_matched_concepts.csv`](data/report/top_matched_concepts.csv) - Most frequently matched concepts
- [`data/report/match_type_counts.csv`](data/report/match_type_counts.csv) - Match type distribution
- [`data/report/matches_by_framework.csv`](data/report/matches_by_framework.csv) - Framework analysis
- [`data/report/patterns_by_match_count.csv`](data/report/patterns_by_match_count.csv) - Pattern frequency
- [`data/report/source_pattern_analysis.csv`](data/report/source_pattern_analysis.csv) - Source pattern analysis
- [`data/report/adoption_pattern_analysis.csv`](data/report/adoption_pattern_analysis.csv) - Pattern adoption analysis

### Intermediate Files

**Preprocessed Code:**
- [`notebooks/`](notebooks/) - Converted Jupyter notebooks (`.ipynb.py`)
- [`converted_notebooks/`](converted_notebooks/) - Archive of original notebooks
- [`target_github_projects/`](target_github_projects/) - Cloned quantum software repositories

**Configuration:**
- `.venv/` - Python virtual environment
- [`uv.lock`](uv.lock) - Dependency lock file
- [`.env`](.env) - Environment variables (GitHub token)

## Command Reference

Run `just` to see an interactive list of available commands.

### Main Workflow Commands

*   `install`: Sets up the project, including cloning, environment creation, and dependency installation
*   `identify-concepts`: Runs concept extraction for Qiskit, PennyLane, and Classiq
*   `run_main`: Executes the semantic analysis workflow
*   `report`: Generates the summary report
*   `workflow`: Runs the workflow using Prefect orchestration

### Workflow Orchestration

*   `workflow`: Run the analysis pipeline with dependency management and monitoring
*   `workflow-ui`: Start Prefect UI server for workflow monitoring
*   `workflow-deploy`: Deploy workflow to Prefect Cloud (requires account)
*   `workflow-step <step>`: Run individual workflow steps for debugging

### Individual Data & Preprocessing Steps

*   `download_pattern_list`: Fetches pattern definitions from the PlanQK Pattern Atlas ([`src/data_acquisition/download_patterns.py`](src/data_acquisition/download_patterns.py))
*   `search-repos`: Runs GitHub search to find quantum projects ([`src/data_acquisition/discover_projects.py`](src/data_acquisition/discover_projects.py))
*   `discover-and-clone`: Runs only the GitHub search and cloning steps
*   `preprocess-notebooks`: Converts `.ipynb` files to `.py` and creates an archive ([`src/preprocessing/extract_notebooks.py`](src/preprocessing/extract_notebooks.py))
*   `convert-archived-notebooks`: Converts notebooks from the archive folder ([`src/preprocessing/convert_notebooks.py`](src/preprocessing/convert_notebooks.py))
*   `consolidate-knowledge-base`: Consolidates framework-specific data into a unified knowledge base ([`src/preprocessing/knowledge_base_consolidator.py`](src/preprocessing/knowledge_base_consolidator.py))

### Reporting Commands

*   `experimental-data`: Generates experimental datasets report ([`src/reporting/report_generator.py`](src/reporting/report_generator.py))
*   `base-concept-report`: Generates framework concept extraction summary ([`src/reporting/report_generator.py`](src/reporting/report_generator.py))
*   `pattern-report`: Generates PlanQK Pattern Atlas report ([`src/reporting/report_generator.py`](src/reporting/report_generator.py))
*   `extended-patterns`: Analyzes extended pattern coverage across frameworks ([`src/reporting/pattern_analyzer.py`](src/reporting/pattern_analyzer.py))
*   `pdf`: Generates PDF files from Markdown documents ([`src/reporting/pdf_generator.py`](src/reporting/pdf_generator.py))
*   `all-reports`: Generates all reports at once ([`src/reporting/report_generator.py`](src/reporting/report_generator.py))

### Utility Commands

*   `clean`: Removes generated artifacts: virtual environment, cloned code, and the `data`, `notebooks`, and `converted_notebooks` directories
*   `upgrade`: Updates the [`uv.lock`](uv.lock) file based on [`pyproject.toml`](pyproject.toml). Run this after changing dependencies
*   `setup`: One-time command to install the `uv` package manager

### Testing & Development Commands

*   `test`: Run all tests with coverage
*   `test-coverage`: Run tests with coverage report
*   `test-file <file>`: Run tests for a specific file
*   `format`: Format all Python files with Black
*   `lint`: Run linting with Ruff
*   `format-lint-test`: Run formatting, linting, and testing in sequence

## Testing & Quality Assurance

### Test Coverage
- Unit Tests: Individual component testing
- Integration Tests: End-to-end workflow testing
- Coverage Reports: Code coverage analysis
- Automated Testing: GitHub Actions CI/CD pipeline

### Code Quality
- Black: Code formatting
- Ruff: Python linting and fixing
- Type Hints: Type annotation support
- Documentation: Docstrings and README

### Development Workflow
```bash
# Run tests
just test

# Format and lint code
just format-lint-test

# Generate experimental data (requires completed workflow)
just experimental-data
```

## Documentation

- **Main README**: This file - project overview and setup
- **Experimental Data**: [`docs/experimental_data.md`](docs/experimental_data.md) - Experimental datasets
- **Workflow Diagrams**: [`docs/workflow_diagrams.md`](docs/workflow_diagrams.md) - Visual workflow documentation
- **Coverage Report**: [`docs/COVERAGE.md`](docs/COVERAGE.md) - Testing documentation
- **Formatting Guide**: [`docs/FORMATTING.md`](docs/FORMATTING.md) - Code style guidelines
- **Refactoring Summary**: [`docs/refactoring_summary.md`](docs/refactoring_summary.md) - Architecture documentation

## Project Architecture

### Workflow Dependencies

| **Step** | **Phase** | **File** | **Dependencies** | **Description** |
|----------|-----------|----------|-------------------|-----------------|
| 1 | Data Acquisition | [`download_patterns.py`](src/data_acquisition/download_patterns.py) | None | Download quantum patterns from PlanQK Atlas |
| 2 | Data Acquisition | [`discover_projects.py`](src/data_acquisition/discover_projects.py) | None | Search GitHub for quantum projects |
| 3 | Extraction | [`extract_concepts.py`](src/extraction/extract_concepts.py) | Step 2 | Extract quantum concepts from frameworks |
| 4 | Manual | Classification | Step 1, Step 3 | Manual classification of concepts |
| 5 | Preprocessing | [`extract_notebooks.py`](src/preprocessing/extract_notebooks.py) | Step 2 | Extract notebooks from discovered projects |
| 6 | Preprocessing | [`convert_notebooks.py`](src/preprocessing/convert_notebooks.py) | Step 5 | Convert `.ipynb` to `.py` files |
| 7 | Analysis | [`run_analysis.py`](src/analysis/run_analysis.py) | Step 1, Step 4, Step 6 | Run semantic analysis |
| 8 | Analysis | [`generate_report.py`](src/analysis/generate_report.py) | Step 7 | Generate analysis report |

### Core Components

**Data Processing:**
- [`src/data_acquisition/`](src/data_acquisition/) - External data collection (patterns, projects)
- [`src/preprocessing/`](src/preprocessing/) - Data preparation and notebook conversion
- [`src/extraction/`](src/extraction/) - Quantum concept extraction workflows
- [`src/analysis/`](src/analysis/) - Analysis and reporting workflows

**Utilities:**
- [`src/reporting/`](src/reporting/) - Report generation and data export
- [`src/conf/`](src/conf/) - Configuration management
- [`src/core_concepts/`](src/core_concepts/) - Framework-specific concept extraction

**Testing:**
- [`tests/`](tests/) - Test suite
- [`pytest.ini`](pytest.ini) - Test configuration
- `.coveragerc` - Coverage settings

### File Structure

```
qpa/
├── src/                          # Source code
│   ├── data_acquisition/         # Steps 1-2: External data collection
│   │   ├── download_patterns.py  # Download quantum patterns
│   │   └── discover_projects.py  # GitHub search for projects
│   ├── preprocessing/            # Steps 5-6: Data preparation
│   │   ├── extract_notebooks.py  # Extract notebooks from projects
│   │   ├── convert_notebooks.py  # Convert .ipynb to .py files
│   │   └── knowledge_base_consolidator.py  # Consolidate framework data
│   ├── extraction/              # Step 3: Concept extraction
│   │   └── extract_concepts.py  # Extract quantum concepts
│   ├── analysis/                # Steps 7-8: Analysis and reporting
│   │   ├── run_analysis.py      # Main analysis workflow
│   │   └── generate_report.py   # Generate final report
│   ├── reporting/               # Report generation utilities
│   │   ├── report_generator.py         # Report generation system
│   │   ├── pattern_analyzer.py         # Pattern analysis and statistics
│   │   └── pdf_generator.py            # PDF generation from Markdown
│   ├── core_concepts/           # Framework-specific extraction
│   ├── workflows/               # Workflow orchestration
│   └── conf/                    # Configuration management
├── tests/                       # Test suite
├── docs/                       # Documentation
├── data/                       # Generated data
├── notebooks/                  # Converted notebooks
├── converted_notebooks/        # Notebook archive
├── target_github_projects/     # Cloned repositories
├── justfile                    # Command automation
├── pyproject.toml             # Project configuration
└── README.md                   # This file
```

## Contributing

This project follows practices for scientific software:

1. **Reproducible Research**: All data and code are version controlled
2. **Testing**: Test coverage with automated CI/CD
3. **Code Quality**: Automated formatting and linting
4. **Documentation**: Documentation for all components
5. **Modular Architecture**: Separation of concerns

For development, use the provided commands:
```bash
just format-lint-test  # Format, lint, and test
just test-coverage     # Run with coverage
just experimental-data # Generate data report
```
