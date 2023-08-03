import csv
import utm
import tkinter as tk
from tkinter import filedialog
import numpy as np

def convert_coordinates():
    csv_file_path = filedialog.askopenfilename(title="Select CSV File", filetypes=[("CSV Files", "*.csv")])
    if not csv_file_path:
        return

    zone_num = int(entry_zone_num.get())
    zone_letter = entry_zone_letter.get().upper()

    converted_data = []
    with open(csv_file_path, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)  # Read the header row
        for row in reader:
            lat = float(row[0])
            lon = float(row[1])
            easting, northing, _, _ = utm.from_latlon(lat, lon, zone_num, zone_letter)
            easting = "{:.3f}".format(easting)  # Keep only thousandths digit
            northing = "{:.3f}".format(northing)  # Keep only thousandths digit
            converted_data.append([easting, northing] + row[2:])  # Append the converted data along with the remaining columns

    # Ask for the save path for the new CSV file
    save_path = filedialog.asksaveasfilename(title="Save Converted CSV File", defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    if save_path:
        with open(save_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Easting", "Northing"] + header[2:])  # Write the header row with updated column names
            writer.writerows(converted_data)  # Write the converted data

def rotate(x, y, x0, y0, angle):
    theta = np.deg2rad(angle)
    xr = (x - x0) * np.cos(theta) - (y - y0) * np.sin(theta) + x0
    yr = (x - x0) * np.sin(theta) + (y - y0) * np.cos(theta) + y0
    return xr, yr

def process_data():
    file_path = filedialog.askopenfilename(title="Select CSV File", filetypes=[("CSV Files", "*.csv")])
    if not file_path:
        return

    # Read the data and header separately
    data = np.genfromtxt(file_path, delimiter=',', skip_header=1, dtype=str)
    header = np.genfromtxt(file_path, delimiter=',', dtype=str, max_rows=1)

    eastings = data[:, 1].astype(float)  # 2nd column as Easting
    northings = data[:, 2].astype(float)  # 3rd column as Northing

    x0 = float(entry_x0.get())
    y0 = float(entry_y0.get())
    angle = float(entry_angle.get())

    rotated_data = np.zeros_like(data, dtype=float)
    rotated_data[:, 1], rotated_data[:, 2] = rotate(eastings, northings, x0, y0, angle)

    # Copy the non-rotated columns
    rotated_data[:, 0] = data[:, 0].astype(float)  # 1st column
    rotated_data[:, 3] = data[:, 3].astype(float)  # 4th column

    # Leave the 5th column empty by using a default fill value (e.g., np.nan)
    rotated_data[:, 4] = np.nan

    # Ask for save path
    save_path = filedialog.asksaveasfilename(title="Save Rotated CSV File", defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    if save_path:
        # Save the rotated data along with the header
        np.savetxt(save_path, rotated_data, delimiter=',', header=','.join(header), comments='', fmt='%.18e,%.18e,%.18e,%.18e,%.18e')

# Create the main window
root = tk.Tk()
root.title("Coordinate Converter and Data Rotator")

# Coordinate Converter widgets
label_zone_num = tk.Label(root, text="Zone Number:")
entry_zone_num = tk.Entry(root)

label_zone_letter = tk.Label(root, text="Zone Letter (N or S):")
entry_zone_letter = tk.Entry(root)

button_convert = tk.Button(root, text="Convert and Save Coordinates", command=convert_coordinates)

# Data Rotator widgets
label_x0 = tk.Label(root, text="X0:")
entry_x0 = tk.Entry(root)

label_y0 = tk.Label(root, text="Y0:")
entry_y0 = tk.Entry(root)

label_angle = tk.Label(root, text="Rotation Angle:")
entry_angle = tk.Entry(root)

button_select_file = tk.Button(root, text="Select CSV File", command=process_data)

# Layout widgets using grid
# Coordinate Converter layout
label_zone_num.grid(row=0, column=0, padx=5, pady=5)
entry_zone_num.grid(row=0, column=1, padx=5, pady=5)

label_zone_letter.grid(row=1, column=0, padx=5, pady=5)
entry_zone_letter.grid(row=1, column=1, padx=5, pady=5)

button_convert.grid(row=2, column=0, columnspan=2, padx=5, pady=10)

# Data Rotator layout
label_x0.grid(row=3, column=0, padx=5, pady=5)
entry_x0.grid(row=3, column=1, padx=5, pady=5)

label_y0.grid(row=4, column=0, padx=5, pady=5)
entry_y0.grid(row=4, column=1, padx=5, pady=5)

label_angle.grid(row=5, column=0, padx=5, pady=5)
entry_angle.grid(row=5, column=1, padx=5, pady=5)

button_select_file.grid(row=6, column=0, columnspan=2, padx=5, pady=10)

# Run the Tkinter event loop
root.mainloop()
