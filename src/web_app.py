import os
from flask import Flask, request, render_template, redirect, url_for
from data_processing import process_all_text_files
from process_and_plot import create_bar_plot

# Initialize Flask app with the correct template folder path
app = Flask(__name__, template_folder="C:/Users/cosku/Bim_Fatura_Proje/src/templates")

# Define the template folder path
template_folder_path = "C:/Users/cosku/Bim_Fatura_Proje/src/templates"
print(f"Template folder path: {template_folder_path}")
print(f"Contents of template folder: {os.listdir(template_folder_path)}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/grafik_olustur', methods=['POST'])
def grafik_olustur():
    grafik_turu = request.form['grafik_turu']
    text_folder = "C:/Users/cosku/Bim_Fatura_Proje/data/input_texts"
    output_csv = f"C:/Users/cosku/Bim_Fatura_Proje/data/processed_data/{grafik_turu}.csv"

    process_all_text_files(text_folder, grafik_turu)
    
    plot_path = os.path.join('C:/Users/cosku/Bim_Fatura_Proje/src/static/images', f'{grafik_turu}.png')
    y_column = f"2. {grafik_turu.replace('_', ' ').title()}"
    print(f"CSV file path: {output_csv}")
    print(f"Plot path: {plot_path}")
    create_bar_plot(output_csv, '1. Fatura Tarihi', y_column, plot_path)
    
    return redirect(url_for('grafik_goster', grafik_turu=grafik_turu))

@app.route('/grafik_goster')
def grafik_goster():
    grafik_turu = request.args.get('grafik_turu')
    plot_path = url_for('static', filename=f'images/{grafik_turu}.png')
    return render_template('graph.html', plot_path=plot_path)

if __name__ == "__main__":
    app.run(debug=True)
