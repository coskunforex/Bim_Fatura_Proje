from flask import Flask, render_template, request, redirect, url_for, send_file, flash
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

# Tkinter kullanımını devre dışı bırak
matplotlib.use('Agg')

app = Flask(__name__)
app.secret_key = 'supersecretkey'

def load_and_combine_csv_files(data_folder):
    all_files = [os.path.join(data_folder, f) for f in os.listdir(data_folder) if f.endswith('.csv')]
    combined_data = pd.concat((pd.read_csv(f) for f in all_files), ignore_index=True)
    return combined_data, all_files

def create_plot(data, x_column, y_column, plot_path):
    try:
        data[x_column] = pd.to_datetime(data[x_column], format='%d-%m-%Y', errors='coerce')
    except Exception as e:
        print(f"Error converting {x_column} to datetime: {e}")
        return
    
    try:
        data[y_column] = data[y_column].str.replace('.', '').str.replace(',', '.').str.replace(' TL', '').astype(float)
    except Exception as e:
        print(f"Error converting {y_column} to float: {e}")
        return

    data = data.dropna(subset=[x_column, y_column])
    data.sort_values(x_column, inplace=True)

    plt.figure(figsize=(10, 6))
    plt.plot(data[x_column], data[y_column], marker='o')
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.title(f'{y_column} vs. {x_column}')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    os.makedirs(os.path.dirname(plot_path), exist_ok=True)
    plt.savefig(plot_path)
    plt.close()
    print(f"Plot saved to {plot_path}")
    print(f"Files in directory: {os.listdir(os.path.dirname(plot_path))}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.csv'):
            file.save(os.path.join('C:/Users/cosku/Bim_Fatura_Proje/data/processed_data', file.filename))
            flash('File uploaded successfully')
            return redirect(url_for('index'))
        else:
            flash('Invalid file format')
    return render_template('index.html')

@app.route('/graph', methods=['GET', 'POST'])
def graph():
    data_folder = "C:/Users/cosku/Bim_Fatura_Proje/data/processed_data"
    combined_data, _ = load_and_combine_csv_files(data_folder)

    if combined_data.empty:
        flash('No data available for plotting')
        return redirect(url_for('index'))

    x_column = '2. Fatura Tarihi'
    y_column = '3. Ödenecek Tutar'

    if request.method == 'POST':
        x_column = request.form['x_column']
        y_column = request.form['y_column']

    plot_path = os.path.join('C:/Users/cosku/Bim_Fatura_Proje/src/static/images', 'plot.png')
    create_plot(combined_data, x_column, y_column, plot_path)

    return render_template('graph.html', plot_path=url_for('static', filename='images/plot.png'), tables=[combined_data.to_html(classes='data')], titles=combined_data.columns.values)

@app.route('/select_columns')
def select_columns():
    return render_template('select_columns.html')

@app.route('/download_report')
def download_report():
    data_folder = "C:/Users/cosku/Bim_Fatura_Proje/data/processed_data"
    combined_data, _ = load_and_combine_csv_files(data_folder)

    if not combined_data.empty:
        report_file = os.path.join(data_folder, 'combined_report.csv')
        combined_data.to_csv(report_file, index=False)
        return send_file(report_file, as_attachment=True)
    else:
        flash('No data available to download.')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
