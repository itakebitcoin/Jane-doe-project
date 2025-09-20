#!/usr/bin/env python3
"""
Jane Doe Search System
A tool for searching Jane Doe databases to help reunite families with missing loved ones.
"""

import sys
import os
import argparse

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.cli import CLIInterface


def main():
    """Main entry point for the Jane Doe Search System"""
    parser = argparse.ArgumentParser(
        description="Jane Doe Search System - Help reunite families with missing loved ones",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py              # Start interactive CLI
  python main.py --cli        # Start interactive CLI

This tool searches publicly available Jane Doe databases using physical
characteristics and location filters to help identify unidentified persons.

IMPORTANT: Use this tool ethically and responsibly. Always work with law
enforcement for verification of any potential matches.
        """
    )
    
    parser.add_argument(
        '--cli', 
        action='store_true', 
        help='Start the command-line interface (default)'
    )
    
    parser.add_argument(
        '--gui', 
        action='store_true', 
        help='Start the graphical user interface (not yet implemented)'
    )
    
    parser.add_argument(
        '--version', 
        action='version', 
        version='Jane Doe Search System v1.0.0'
    )
    
    args = parser.parse_args()
    
    # Default to CLI if no interface specified
    if not args.gui:
        print("Starting Jane Doe Search System CLI...")
        try:
            cli = CLIInterface()
            cli.run()
        except KeyboardInterrupt:
            print("\nGoodbye!")
            sys.exit(0)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
    else:
        print("GUI interface is not yet implemented.")
        print("Please use the CLI interface by running: python main.py")
        sys.exit(1)


if __name__ == "__main__":
    main()