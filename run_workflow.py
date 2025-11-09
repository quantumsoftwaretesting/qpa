#!/usr/bin/env python3
"""
Simple script to run the QPA: Quantum Patterns Analyser Workflow using Prefect.

This script provides a command-line interface to run the complete workflow
with proper error handling and logging.
"""

import sys

from src.workflows.qpa_flow import qpa_flow


def main():
    """Run the QPA: Quantum Patterns Analyser workflow."""
    print("Starting QPA: Quantum Patterns Analyser Workflow...")
    print("=" * 60)
    
    try:
        # Run the Prefect flow
        result = qpa_flow()
        
        if result["status"] == "success":
            print("\nSUCCESS: Workflow completed successfully!")
            print("\nResults Summary:")
            print(f"  • Patterns: {result['patterns']['patterns_file']}")
            print(f"  • Projects: {result['projects']['projects_file']}")
            print(f"  • Notebooks: {result['notebooks']['notebooks_dir']}")
            print(f"  • Converted: {result['conversion']['converted_dir']}")
            print(f"  • Concepts: {len(result['concepts']['concept_files'])} files")
            print(f"  • Analysis: {result['analysis']['analysis_file']}")
            print(f"  • Reports: {len(result['report']['report_files'])} files")
            print(f"  • Experimental: {result['experimental']['experimental_file']}")
            
            print("\n🎯 Next Steps:")
            print("  1. Review reports in docs/final_pattern_report.md")
            print("  2. Check experimental data in docs/experimental_data.md")
            print("  3. Analyze results in data/report/ directory")
            
            return 0
        else:
            print("ERROR: Workflow failed!")
            return 1
            
    except Exception as e:
        print(f"ERROR: Workflow failed with error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
