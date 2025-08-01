# AI Studio Chat JSON Converter

This Python script converts AI Studio chat JSON format to a simpler format for viewing in Vercel apps.

## Usage

```bash
python3 convert_json_format.py <input_file> <output_file>
```

## Example

```bash
python3 convert_json_format.py "Branch of Simulated Racism Discussion.json" converted_output.json
```

## Format Details

### Input Format (AI Studio)
- Contains metadata like `runSettings`, `systemInstruction`
- Messages are in `chunkedPrompt.chunks` array
- Each chunk has `parts` array with text fragments
- Includes internal "thought" chunks
- Role is "model" for assistant messages

### Output Format (Vercel App)
- Simple structure with just `messages` array
- Each message has:
  - `role`: "user" or "assistant"
  - `content`: array with objects containing `type` and `text`
- No metadata or internal thoughts

## Features

- Automatically skips internal thought chunks
- Maps "model" role to "assistant" role
- Concatenates multi-part text into single messages
- Preserves user messages as-is
- Handles Unicode characters properly