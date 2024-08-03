import os
import openai
import pandas as pd

# OpenAI API anahtarınızı ayarlayın
openai.api_key = 'sk-proj-CNYSXzG1jQhjCh51rOpaT3BlbkFJuYEafcqTgvl0YVCKAMBa'

def extract_data_and_save_to_csv(text, grafik_turu, output_csv):
    try:
        # ChatGPT API'ye gönderilecek prompt
        prompt = f"""
        Extract the relevant text for the '{grafik_turu}' graph and format it for CSV:

        Format the output as follows:
        1. Fatura Tarihi: <değer>
        2. {grafik_turu.replace('_', ' ').title()}: <değer>

        The values should be consistent and correctly formatted. For example, date in dd-mm-yyyy format and amount in 'xx.xxx,xx' format.
        Ensure that the CSV data is clean and ready for graphing.
        """

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a data extraction assistant."},
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": text}
            ]
        )

        # API'den gelen cevabı işle
        extracted_text = response.choices[0].message['content'].strip()
        print(f"Extracted text from ChatGPT API:\n{extracted_text}")

        # Extracted text'i analiz et ve dictionary formatında sakla
        data_dict = {}
        for line in extracted_text.split('\n'):
            if ': ' in line:
                key, value = line.split(': ', 1)
                data_dict[key.strip()] = value.strip()

        # CSV dosyasına yaz
        df = pd.DataFrame([data_dict])
        df.to_csv(output_csv, index=False, mode='a', header=not os.path.exists(output_csv))
        print(f"Data dictionary to be saved to CSV:\n{data_dict}")

    except Exception as e:
        print(f"Error extracting data or saving to CSV: {e}")

def process_all_text_files(text_folder, grafik_turu):
    try:
        output_csv = f"C:/Users/cosku/Bim_Fatura_Proje/data/processed_data/{grafik_turu}.csv"
        for filename in os.listdir(text_folder):
            if filename.endswith(".txt"):
                file_path = os.path.join(text_folder, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    text = file.read()
                    extract_data_and_save_to_csv(text, grafik_turu, output_csv)
    except Exception as e:
        print(f"Error processing text files: {e}")

if __name__ == "__main__":
    text_folder = "C:/Users/cosku/Bim_Fatura_Proje/data/input_texts"
    grafik_turu = "toplam_tuketim"  # Örneğin "toplam_tuketim" grafiği için verileri işleyin
    process_all_text_files(text_folder, grafik_turu)
