import openai
import csv
import os

# OpenAI API anahtarınızı buraya ekleyin
openai.api_key = "sk-proj-CNYSXzG1jQhjCh51rOpaT3BlbkFJuYEafcqTgvl0YVCKAMBa"

# Metin dosyalarını okuma ve işleme fonksiyonu
def extract_text_from_files(text_folder):
    if not os.path.exists(text_folder):
        raise FileNotFoundError(f"The specified path does not exist: {text_folder}")

    extracted_texts = []
    filenames = []

    for filename in os.listdir(text_folder):
        if filename.endswith('.txt'):
            file_path = os.path.join(text_folder, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
                extracted_texts.append(text)
                filenames.append(filename)
    
    return extracted_texts, filenames

# ChatGPT API kullanarak metni işleme fonksiyonu
def process_text_with_chatgpt(text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a data extraction assistant. Extract the following text and format it for CSV:\n\n"
                    "Format the output as follows:\n"
                    "1. Fatura No: <value>\n"
                    "2. Fatura Tarihi: <value>\n"
                    "3. Ödenecek Tutar: <value>\n\n"
                    "Ensure the values are consistent and correctly formatted. For example, date in dd-mm-yyyy format and amount in 'xx.xxx,xx TL' format."
                )
            },
            {
                "role": "user",
                "content": text
            }
        ],
        max_tokens=150
    )
    return response.choices[0].message['content'].strip()

# Veriyi CSV dosyasına kaydetme fonksiyonu
def save_data_to_csv(data, csv_file):
    keys = data[0].keys()
    os.makedirs(os.path.dirname(csv_file), exist_ok=True)  # Dizinleri oluştur
    with open(csv_file, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)

# Ana işlem fonksiyonu
def main():
    text_folder = "C:/Users/cosku/Bim_Fatura_Proje/data/input_texts"
    output_folder = "C:/Users/cosku/Bim_Fatura_Proje/data/processed_data"

    extracted_texts, filenames = extract_text_from_files(text_folder)

    for text, filename in zip(extracted_texts, filenames):
        try:
            processed_text = process_text_with_chatgpt(text)
            
            # İşlenen metni sözlük formatında ayrıştırma
            data_dict = {}
            for line in processed_text.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    data_dict[key.strip()] = value.strip()
            
            # İşlenen veriyi CSV dosyasına kaydetme
            if data_dict:
                output_csv_file = os.path.join(output_folder, filename.replace('.txt', '.csv'))
                save_data_to_csv([data_dict], output_csv_file)
                print(f"Data saved to {output_csv_file}")
            else:
                print(f"No data extracted from {filename}")
        except Exception as e:
            print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    main()
