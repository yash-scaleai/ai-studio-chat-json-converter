#!/usr/bin/env python3
"""
Converts AI Studio chat JSON format to target Vercel app format.

Input format: Branch of Simulated Racism Discussion.json (AI Studio format)
Output format: conversation-2025-08-01T19-35-26-051Z.json (Vercel app format)
"""

import json
import sys
from pathlib import Path


def convert_json_format(input_file: str, output_file: str) -> None:
    """
    Convert AI Studio JSON format to Vercel app format.
    
    Args:
        input_file: Path to input JSON file (AI Studio format)
        output_file: Path to output JSON file (Vercel app format)
    """
    # Read input JSON
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Initialize output structure
    output = {
        "messages": []
    }
    
    # Extract messages from chunkedPrompt.chunks
    if "chunkedPrompt" in data and "chunks" in data["chunkedPrompt"]:
        chunks = data["chunkedPrompt"]["chunks"]
        
        for chunk in chunks:
            # Skip thought chunks (internal model thinking)
            if chunk.get("isThought", False):
                continue
            
            # Map role: 'model' -> 'assistant'
            role = "assistant" if chunk.get("role") == "model" else chunk.get("role", "user")
            
            # Extract text content
            text_content = ""
            
            # Check if chunk has parts array
            if "parts" in chunk:
                # Concatenate all text parts
                for part in chunk["parts"]:
                    if isinstance(part, dict) and "text" in part:
                        # Skip thought parts
                        if not part.get("thought", False):
                            text_content += part["text"]
                    elif isinstance(part, str):
                        text_content += part
            elif "text" in chunk:
                # Direct text field
                text_content = chunk["text"]
            
            # Create message in target format
            if text_content.strip():  # Only add non-empty messages
                message = {
                    "role": role,
                    "content": [
                        {
                            "type": "text",
                            "text": text_content
                        }
                    ]
                }
                output["messages"].append(message)
    
    # Write output JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"Conversion complete: {input_file} -> {output_file}")
    print(f"Total messages converted: {len(output['messages'])}")


def main():
    """Main function to handle command line arguments."""
    if len(sys.argv) != 3:
        print("Usage: python convert_json_format.py <input_file> <output_file>")
        print("Example: python convert_json_format.py 'Branch of Simulated Racism Discussion.json' output.json")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    # Check if input file exists
    if not Path(input_file).exists():
        print(f"Error: Input file '{input_file}' not found.")
        sys.exit(1)
    
    try:
        convert_json_format(input_file, output_file)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in input file: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error during conversion: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()