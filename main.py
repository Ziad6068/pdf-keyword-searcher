import os
import re
import PyPDF2
import config   # 👈 import config file

# =============================
# FUNCTION TO SEARCH CONTEXT
# =============================
def search_keywords_in_pdf(pdf_path, keywords):
    results = []
    try:
        with open(pdf_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + " "
            text = re.sub(r'\s+', ' ', text)  # Normalize spaces

            for keyword in keywords:
                # Regex to get one word before and one after the keyword (case insensitive)
                pattern = r'\b(\w+)\s+(' + re.escape(keyword) + r')\s+(\w+)\b'
                matches = re.findall(pattern, text, flags=re.IGNORECASE)
                for match in matches:
                    context = f"{match[0]} {match[1]} {match[2]}"
                    results.append((keyword, context))
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
    return results

# =============================
# MAIN SCRIPT
# =============================
all_results = []
for filename in os.listdir(config.FOLDER_PATH):
    if filename.lower().endswith(".pdf"):
        file_path = os.path.join(config.FOLDER_PATH, filename)
        print(f"Processing: {filename}")
        matches = search_keywords_in_pdf(file_path, config.KEYWORDS)
        if matches:
            all_results.append(f"--- {filename} ---")
            for keyword, context in matches:
                all_results.append(f"[{keyword}] {context}")
            all_results.append("")  # Blank line between PDFs

# Save results to file
with open(config.OUTPUT_FILE, "w", encoding="utf-8") as out_file:
    out_file.write("\n".join(all_results))

print(f"Search complete. Results saved to {config.OUTPUT_FILE}")
