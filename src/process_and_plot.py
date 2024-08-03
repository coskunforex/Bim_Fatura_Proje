import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

# Tkinter arka uç hatalarından kaçınmak için matplotlib arka ucunu ayarlayın
import matplotlib
matplotlib.use('Agg')

def create_bar_plot(csv_file, x_column, y_column, plot_path, bar_width=0.9):
    try:
        # Load data from CSV file into a DataFrame
        data = pd.read_csv(csv_file)
        
        # Debugging line to check the DataFrame content
        print("Data loaded from CSV file:\n", data)

        # Ensure the column names are stripped of extra spaces
        data.columns = data.columns.str.strip()

        # Convert date column to datetime
        data[x_column] = pd.to_datetime(data[x_column], format='%d-%m-%Y', errors='coerce')
        # Convert currency column to float
        data[y_column] = data[y_column].str.replace('.', '').str.replace(',', '.').str.replace(' TL', '').astype(float)
        # Drop rows with NaN values in the specified columns
        data = data.dropna(subset=[x_column, y_column])
        # Sort data by the date column
        data.sort_values(x_column, inplace=True)

        # Debugging: Verilerin doğru işlendiğinden emin olmak için yazdır
        print("Processed data for plotting:\n", data)

        # Create x values for the bar plot
        x_values = np.arange(len(data))
        # Set figure size
        plt.figure(figsize=(10, 5))  # Adjusted figure size
        # Create bar plot with specified bar width
        plt.bar(x_values, data[y_column], color='skyblue', width=bar_width)
        # Set labels and title
        plt.xlabel(x_column)
        plt.ylabel(y_column)
        plt.title(f'{y_column} vs. {x_column}')
        # Add grid lines
        plt.grid(True, linestyle='--', alpha=0.7)
        # Set x-axis ticks and labels
        plt.xticks(ticks=x_values, labels=data[x_column].dt.strftime('%d-%m-%Y'), rotation=45)
        # Adjust layout to fit everything
        plt.tight_layout()

        # Ensure the directory exists
        os.makedirs(os.path.dirname(plot_path), exist_ok=True)
        # Save the plot to the specified path
        plt.savefig(plot_path)
        # Close the plot to free memory
        plt.close()
        print(f"Grafik kaydedildi: {plot_path}")

    except Exception as e:
        print(f"Error creating bar plot: {e}")

# Örnek kullanım
csv_file_path = "C:/Users/cosku/Bim_Fatura_Proje/data/processed_data/toplam_tuketim.csv"
plot_file_path = "C:/Users/cosku/Bim_Fatura_Proje/src/static/images/toplam_tuketim.png"
create_bar_plot(csv_file_path, 'Fatura Tarihi', 'Toplam Tuketim', plot_file_path)
