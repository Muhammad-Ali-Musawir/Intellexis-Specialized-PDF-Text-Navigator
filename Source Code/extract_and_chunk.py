import fitz  # PyMuPDF
import os
import json
from collections import Counter, defaultdict

def is_bold_italic(span):
    flags = span.get("flags", 0)
    return {
        "is_bold": bool(flags & 2),
        "is_italic": bool(flags & 1),
        "is_underlined": bool(flags & 4)
    }

def extract_font_spans(pdf_path):
    doc = fitz.open(pdf_path)
    font_spans = []

    print("🔍 Extracting text spans and font properties...")

    for page_num in range(len(doc)):
        page = doc[page_num]
        blocks = page.get_text("dict")["blocks"]

        for block in blocks:
            if block["type"] != 0:
                continue

            for line in block["lines"]:
                for span in line["spans"]:
                    text = span["text"].strip()
                    if text:
                        style_info = is_bold_italic(span)
                        font_spans.append({
                            "text": text,
                            "font": span["font"],
                            "size": round(span["size"], 1),
                            "is_bold": style_info["is_bold"],
                            "is_italic": style_info["is_italic"],
                            "is_underlined": style_info["is_underlined"],
                            "bbox": span["bbox"],
                            "color": span["color"],
                            "page": page_num + 1
                        })

    print(f"✅ Found {len(font_spans)} spans.\n")
    return font_spans

def analyze_most_common_font(spans):
    font_counter = Counter()
    text_distribution = defaultdict(set)

    for span in spans:
        font_key = (
            span["font"],
            span["size"],
            span["is_bold"],
            span["is_italic"],
            span["is_underlined"]
        )
        cleaned_text = span["text"].strip()

        if len(cleaned_text.split()) >= 3:
            font_counter[font_key] += 1
            text_distribution[font_key].add(cleaned_text)

    filtered_fonts = {
        key: count for key, count in font_counter.items()
        if len(text_distribution[key]) >= 3
    }

    if not filtered_fonts:
        raise ValueError("❌ No reliable body font could be detected.")

    print("📊 Filtered Fonts (Used in >= 3 full-text spans):")
    for (font, size, is_bold, is_italic, is_underlined), count in sorted(filtered_fonts.items(), key=lambda x: x[1], reverse=True)[:5]:
        style = []
        if is_bold: style.append("Bold")
        if is_italic: style.append("Italic")
        if is_underlined: style.append("Underline")
        style_str = " ".join(style) or "Regular"
        print(f"  • Font: {font}, Size: {size}, Style: {style_str} — Used {count} times")

    most_common = max(filtered_fonts, key=filtered_fonts.get)
    print(f"\n✅ Most common narrative body font: {most_common}\n")
    return most_common  # (font, size, is_bold, is_italic, is_underlined)

def chunk_spans(spans, body_font_key):
    print("✂️  Chunking spans into structured sections...")

    def is_body_font(span):
        return (
            span["font"] == body_font_key[0]
            and span["size"] == body_font_key[1]
            and span["is_bold"] == body_font_key[2]
            and span["is_italic"] == body_font_key[3]
            and span["is_underlined"] == body_font_key[4]
        )

    chunks = []
    current_chunk = {
        "type": "text",
        "section": None,
        "content": "",
        "font": None,
        "size": None,
        "page_start": None,
        "page_end": None
    }

    for span in spans:
        text = span["text"]
        font = span["font"]
        size = span["size"]
        page = span["page"]

        if not text.strip():
            continue

        if is_body_font(span):
            if current_chunk["section"] is None:
                current_chunk["section"] = "Untitled Section"
                current_chunk["font"] = font
                current_chunk["size"] = size
                current_chunk["page_start"] = page

            current_chunk["content"] += (" " if current_chunk["content"] else "") + text
            current_chunk["page_end"] = page
        else:
            if current_chunk["content"]:
                chunks.append(current_chunk)
                current_chunk = {
                    "type": "text",
                    "section": None,
                    "content": "",
                    "font": None,
                    "size": None,
                    "page_start": None,
                    "page_end": None
                }

            heading_chunk = {
                "type": "heading",
                "section": text,
                "content": "",
                "font": font,
                "size": size,
                "page_start": page,
                "page_end": page
            }
            chunks.append(heading_chunk)

    if current_chunk["content"]:
        chunks.append(current_chunk)

    # Merge heading → next paragraph under 1 section
    final_chunks = []
    last_heading = None
    for chunk in chunks:
        if chunk["type"] == "heading":
            last_heading = chunk["section"]
        else:
            chunk["section"] = last_heading or "Untitled Section"
            final_chunks.append(chunk)

    return final_chunks

def main():
    pdf_path = "Source Code/Assets/document.pdf"
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"❌ PDF not found at: {pdf_path}")

    # Step 1: Extract spans
    spans = extract_font_spans(pdf_path)

    # Step 2: Save raw spans
    with open("Source Code/Assets/raw_extraction.json", "w", encoding="utf-8") as f:
        json.dump(spans, f, indent=2, ensure_ascii=False)
    print("💾 Saved to Assets/raw_extraction.json")

    # Step 3: Detect body font
    body_font = analyze_most_common_font(spans)

    # Step 4: Chunk the document using detected font
    chunks = chunk_spans(spans, body_font)

    # Step 5: Save chunks
    with open("Source Code/Assets/chunks.json", "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)
    print(f"✅ Chunking complete. Total chunks: {len(chunks)}")

if __name__ == "__main__":
    main()

