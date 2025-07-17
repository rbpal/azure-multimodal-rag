#!/usr/bin/env python3
"""
PDF to Markdown Converter

This script converts PDF files to Markdown format using PyMuPDF (fitz).
It preserves text formatting, extracts images, and handles tables.

Requirements:
    pip install PyMuPDF markdown python-markdown

Usage:
    python 01-01-utility-convert-pdf-to-markdown.py input.pdf output.md
    python 01-01-utility-convert-pdf-to-markdown.py input.pdf  # outputs to input.md
    python 01-01-utility-convert-pdf-to-markdown.py --batch  # converts all PDFs in the default folder
"""

import fitz  # PyMuPDF
import os
import sys
import re
from pathlib import Path

# Store original working directory first
ORIGINAL_CWD = Path.cwd()

# Auto-detect project root (look for common project markers)
def find_project_root():
    # Start from current working directory (where script was called from)
    current_dir = ORIGINAL_CWD
    
    # Look for project root indicators
    while current_dir != current_dir.parent:
        if any((current_dir / marker).exists() for marker in 
               ['data', 'requirements.txt', '.git', 'pyproject.toml', 'setup.py']):
            return current_dir
        current_dir = current_dir.parent
    
    # If not found, use current working directory
    return ORIGINAL_CWD

# Get project root
PROJECT_ROOT = find_project_root()

# Configuration - relative paths from project root
PDF_FOLDER = PROJECT_ROOT / "data/raw/pdfs/"
MARKDOWN_FOLDER = PROJECT_ROOT / "data/raw/markdown/"

def extract_text_with_formatting(page):
    """Extract text with basic formatting preservation"""
    blocks = page.get_text("dict")
    markdown_content = []
    
    for block in blocks["blocks"]:
        if block.get("type") == 0:  # Text block
            block_text = []
            
            for line in block["lines"]:
                line_text = []
                
                for span in line["spans"]:
                    text = span["text"]
                    font_size = span["size"]
                    font_flags = span["flags"]
                    
                    # Handle different text formatting
                    if font_flags & 2**4:  # Bold
                        text = f"**{text}**"
                    if font_flags & 2**1:  # Italic
                        text = f"*{text}*"
                    
                    # Handle headings based on font size
                    if font_size > 16:
                        text = f"# {text}"
                    elif font_size > 14:
                        text = f"## {text}"
                    elif font_size > 12:
                        text = f"### {text}"
                    
                    line_text.append(text)
                
                if line_text:
                    block_text.append("".join(line_text))
            
            if block_text:
                markdown_content.append("\n".join(block_text))
    
    return "\n\n".join(markdown_content)

def extract_images(page, page_num, output_dir):
    """Extract images from the page"""
    image_list = page.get_images()
    images_md = []
    
    for img_index, img in enumerate(image_list):
        try:
            xref = img[0]
            pix = fitz.Pixmap(page.parent, xref)
            
            if pix.n - pix.alpha < 4:  # Skip if not RGB/GRAY
                img_filename = f"image_page{page_num}_{img_index}.png"
                img_path = os.path.join(output_dir, img_filename)
                pix.save(img_path)
                images_md.append(f"![Image](images/{img_filename})")
            
            pix = None
        except Exception as e:
            print(f"Error extracting image {img_index} from page {page_num}: {e}")
    
    return images_md

def extract_tables(page):
    """Extract tables and convert to markdown format"""
    tables = page.find_tables()
    tables_md = []
    
    for table in tables:
        try:
            table_data = table.extract()
            if not table_data:
                continue
            
            # Convert to markdown table
            md_table = []
            
            # Header row
            if table_data:
                header = table_data[0]
                md_table.append("| " + " | ".join(str(cell) if cell else "" for cell in header) + " |")
                md_table.append("| " + " | ".join("---" for _ in header) + " |")
                
                # Data rows
                for row in table_data[1:]:
                    md_table.append("| " + " | ".join(str(cell) if cell else "" for cell in row) + " |")
            
            tables_md.append("\n".join(md_table))
        except Exception as e:
            print(f"Error extracting table: {e}")
    
    return tables_md

def clean_markdown(text):
    """Clean up the markdown text"""
    # Remove excessive whitespace
    text = re.sub(r'\n\s*\n\s*\n', '\n\n', text)
    
    # Fix heading formatting
    text = re.sub(r'^(#{1,6})\s*(.+)', r'\1 \2', text, flags=re.MULTILINE)
    
    # Remove trailing whitespace
    text = '\n'.join(line.rstrip() for line in text.split('\n'))
    
    return text.strip()

def convert_pdf_to_markdown(pdf_path, output_path=None):
    """Convert PDF to Markdown"""
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    
    if output_path is None:
        # Preserve folder structure from PDF folder to markdown folder
        pdf_path_obj = Path(pdf_path)
        
        # Get relative path from PDF_FOLDER
        try:
            relative_path = pdf_path_obj.relative_to(PDF_FOLDER)
            # Create same structure in markdown folder
            output_path = MARKDOWN_FOLDER / relative_path.with_suffix('.md')
        except ValueError:
            # If PDF is not in PDF_FOLDER, just use filename
            pdf_name = pdf_path_obj.stem
            output_path = MARKDOWN_FOLDER / f"{pdf_name}.md"
    
    # Ensure output directory exists
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Create images directory in the same subfolder
    images_dir = output_dir / "images"
    images_dir.mkdir(exist_ok=True)
    
    # Open PDF
    doc = fitz.open(pdf_path)
    markdown_content = []
    
    print(f"Converting {pdf_path} to {output_path}")
    print(f"Total pages: {len(doc)}")
    
    for page_num in range(len(doc)):
        print(f"Processing page {page_num + 1}/{len(doc)}")
        page = doc[page_num]
        
        # Add page separator
        if page_num > 0:
            markdown_content.append(f"\n---\n*Page {page_num + 1}*\n")
        
        # Extract text with formatting
        text_content = extract_text_with_formatting(page)
        if text_content.strip():
            markdown_content.append(text_content)
        
        # Extract tables
        tables = extract_tables(page)
        for table in tables:
            markdown_content.append(table)
        
        # Extract images
        images = extract_images(page, page_num + 1, images_dir)
        for img in images:
            markdown_content.append(img)
    
    doc.close()
    
    # Combine all content
    final_content = "\n\n".join(markdown_content)
    final_content = clean_markdown(final_content)
    
    # Write to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(final_content)
    
    print(f"Conversion complete! Output saved to: {output_path}")
    return output_path

def batch_convert_pdfs():
    """Convert all PDFs in the configured folder while preserving folder structure"""
    if not PDF_FOLDER.exists():
        print(f"PDF folder does not exist: {PDF_FOLDER}")
        return
    
    # Find all PDF files recursively
    pdf_files = list(PDF_FOLDER.rglob("*.pdf"))
    
    if not pdf_files:
        print(f"No PDF files found in: {PDF_FOLDER}")
        return
    
    print(f"Found {len(pdf_files)} PDF files to convert")
    
    # Ensure markdown folder exists
    MARKDOWN_FOLDER.mkdir(parents=True, exist_ok=True)
    
    successful_conversions = 0
    failed_conversions = 0
    
    for pdf_file in pdf_files:
        try:
            print(f"\n{'='*50}")
            print(f"Converting: {pdf_file.relative_to(PDF_FOLDER)}")
            
            # Preserve folder structure
            relative_path = pdf_file.relative_to(PDF_FOLDER)
            output_file = MARKDOWN_FOLDER / relative_path.with_suffix('.md')
            
            convert_pdf_to_markdown(str(pdf_file), str(output_file))
            
            successful_conversions += 1
            print(f"✓ Successfully converted to: {output_file.relative_to(MARKDOWN_FOLDER)}")
            
        except Exception as e:
            failed_conversions += 1
            print(f"✗ Failed to convert {pdf_file.relative_to(PDF_FOLDER)}: {e}")
    
    print(f"\n{'='*50}")
    print(f"Batch conversion complete!")
    print(f"Successful: {successful_conversions}")
    print(f"Failed: {failed_conversions}")
    print(f"Total: {len(pdf_files)}")
    
    # Show folder structure created
    print(f"\nFolder structure created in {MARKDOWN_FOLDER}:")
    for subfolder in sorted([f for f in MARKDOWN_FOLDER.iterdir() if f.is_dir()]):
        print(f"  📁 {subfolder.name}/")
        md_files = list(subfolder.glob("*.md"))
        for md_file in sorted(md_files):
            print(f"    📄 {md_file.name}")
        if (subfolder / "images").exists():
            img_count = len(list((subfolder / "images").glob("*.png")))
            if img_count > 0:
                print(f"    🖼️  images/ ({img_count} images)")

def main():
    try:
        if len(sys.argv) == 2 and sys.argv[1] == "--batch":
            batch_convert_pdfs()
            return
        
        if len(sys.argv) < 2:
            print("Usage:")
            print("  python pdf_to_markdown.py <input.pdf> [output.md]")
            print("  python pdf_to_markdown.py --batch")
            print(f"\nOriginal directory: {ORIGINAL_CWD}")
            print(f"Project root detected: {PROJECT_ROOT}")
            print(f"Configured folders:")
            print(f"  PDF folder: {PDF_FOLDER}")
            print(f"  Markdown folder: {MARKDOWN_FOLDER}")
            sys.exit(1)
        
        input_pdf = sys.argv[1]
        output_md = sys.argv[2] if len(sys.argv) > 2 else None
        
        convert_pdf_to_markdown(input_pdf, output_md)
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    finally:
        # Restore original working directory
        os.chdir(ORIGINAL_CWD)

if __name__ == "__main__":
    main()