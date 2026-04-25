#!/usr/bin/env python3
"""
Example: Load ULAD config from .улад file
"""

import sys
import os

# Add parent directory to path to import parser
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ulad_parser import UladParser
import json


def main():
    # Path to config file
    config_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        'пример.улад'
    )

    # Create parser and load file
    parser = UladParser()

    try:
        config = parser.load_file(config_path)

        print("=== ULAD CONFIGURATION LOADED ===\n")
        print(json.dumps(config, indent=2, ensure_ascii=False))

        # Access specific values
        print("\n=== ACCESSING VALUES ===")
        print(f"Database host: {config['СОЕДИНЕНИЕ']['ХОЗЯИН']}")
        print(f"Database port: {config['СОЕДИНЕНИЕ']['ПРОХОД']}")
        print(f"Debug mode: {config['СЛУЖБА']['ОТЛАДКА']}")

    except FileNotFoundError:
        print(f"Error: Config file not found at {config_path}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    main()