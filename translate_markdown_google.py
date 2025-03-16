import os
import sys
from google.cloud import translate_v2 as translate

def translate_text(text, target_language="en"):
    """Translate text using Google Cloud Translation API."""
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return result["translatedText"]

def translate_markdown(input_file, output_file):
    """Reads a Markdown file, translates it, and saves the translated version."""
    if not os.path.exists(input_file):
        print(f"❌ Error: File '{input_file}' not found.\n")
        print_help()
        sys.exit(1)

    with open(input_file, "r", encoding="utf-8") as f:
        content = f.readlines()  # Read line by line

    translated_lines = []
    inside_code_block = False  # Track whether we're inside a code block

    for idx, line in enumerate(content):
        stripped_line = line.strip()

        # Detect start/end of code blocks (``` or ~~~)
        if stripped_line.startswith("```") or stripped_line.startswith("~~~"):
            inside_code_block = not inside_code_block
            translated_lines.append(line)  # Keep original ` ``` `
            continue  # Skip translating the line itself

        # Preserve empty lines and existing markdown structure
        if stripped_line == "":
            translated_lines.append(line)
            continue

        # **Translate everything inside code blocks**
        if inside_code_block:
            print(f"🔄 Translating code block line {idx+1}/{len(content)}...")
            translated_line = translate_text(line)
            translated_lines.append(translated_line + "\n")
        else:
            print(f"🔄 Translating line {idx+1}/{len(content)}...")
            translated_lines.append(translate_text(line) + "\n")

    # Save the translated content
    with open(output_file, "w", encoding="utf-8") as f:
        f.writelines(translated_lines)

    print(f"\n✅ Translation complete! Saved to: {output_file}")

def print_help():
    """Print usage instructions."""
    print("Usage:")
    print("  python translate_markdown_google.py <input_file.md> [output_file.md]")
    print("\nExample:")
    print("  python translate_markdown_google.py train_README-ja.md train_README-en.md")
    print("\nIf no output file is specified, the default will be '<input_file>-translated.md'.")

# Check for command-line arguments
if len(sys.argv) < 2:
    print("❌ Error: No input file provided.\n")
    print_help()
    sys.exit(1)

# Get filenames from arguments
input_filename = sys.argv[1]
output_filename = sys.argv[2] if len(sys.argv) > 2 else input_filename.replace(".md", "-translated.md")

# Run the translation
translate_markdown(input_filename, output_filename)

