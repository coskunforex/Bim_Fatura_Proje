import fitz  # PyMuPDF
import os

def extract_text_from_pdf(pdf_path):
    document = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text += page.get_text()
    return text

def save_text_to_file(text, output_path):
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(text)

if __name__ == "__main__":
    input_pdf_dir = "C:/Users/cosku/Bim_Fatura_Proje/data/input_pdfs"
    output_text_dir = "C:/Users/cosku/Bim_Fatura_Proje/data/input_texts"

    if not os.path.exists(output_text_dir):
        os.makedirs(output_text_dir)

    for pdf_filename in os.listdir(input_pdf_dir):
        if pdf_filename.endswith(".pdf"):
            pdf_path = os.path.join(input_pdf_dir, pdf_filename)
            text = extract_text_from_pdf(pdf_path)
            output_text_path = os.path.join(output_text_dir, pdf_filename.replace(".pdf", ".txt"))
            save_text_to_file(text, output_text_path)
            print(f"Processed {pdf_filename}")
