import pandas as pd
import matplotlib.pyplot as plt
import os

def create_plot(data, x_column, y_column, plot_path):
    data[x_column] = pd.to_datetime(data[x_column], format='%d-%m-%Y', errors='coerce')
    data[y_column] = data[y_column].str.replace('.', '').str.replace(',', '.').str.replace(' TL', '').astype(float)
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

def main():
    data_folder = "C:/Users/cosku/Bim_Fatura_Proje/data/processed_data"
    all_data = pd.DataFrame()

    for filename in os.listdir(data_folder):
        if filename.endswith('.csv'):
            file_path = os.path.join(data_folder, filename)
            df = pd.read_csv(file_path)
            all_data = pd.concat([all_data, df], ignore_index=True)

    plot_path = os.path.join('C:/Users/cosku/Bim_Fatura_Proje/src/static/images', 'plot.png')
    create_plot(all_data, '2. Fatura Tarihi', '3. Ödenecek Tutar', plot_path)

if __name__ == "__main__":
    main()