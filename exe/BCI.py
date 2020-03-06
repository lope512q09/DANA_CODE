import pandas as pd
import csv
import tkinter as tk

with open('C:/Users/angela.willis/Desktop/Barcode Check-In/employee_database/employee_database.csv', newline='')\
        as employee_csv:
    reader = csv.DictReader(employee_csv)

    """Data Entry Program"""
    # Open data base using pandas data frame.
    filename = "C:/Users/angela.willis/Desktop/Barcode Check-In/employee_database/employee_database.csv"
    df = pd.read_csv(filename)

    temp_employee_dicts = []
    training = ''

    class App(tk.Frame):
        def __init__(self, master):
            tk.Frame.__init__(self, master, height=42, width=42, bg='#bfbd92')
            self.barcode_prompt = tk.Label(self, text="Scan a barcode:", bg='#bfbd92')
            self.barcode_prompt.pack()
            self.entry = tk.Entry(self)
            self.entry.focus()
            self.entry.pack()
            self.barcode_button = tk.Button(self, text="Enter", command=self.more_employees)
            self.barcode_button.pack()
            self.entry.bind("<Return>", self.on_return_scan)

        def on_return_scan(self, *args):
            global temp_employee_dict
            scan = self.entry.get()
            temp_employee_dict = {'BARCODE': scan, 'NAME': ''}
            temp_employee_dicts.append(temp_employee_dict)
            self.entry.delete(0, 'end')
            self.more_employees()

        def on_return_training(self, *args):
            global training
            training = self.training_entry.get()
            self.training_entry.delete(0, 'end')
            self.assign_training()

        def no_command(self):
            self.entry.destroy()
            self.barcode_button.destroy()
            self.yes_button.destroy()
            self.no_button.destroy()
            self.prompt_label.destroy()
            employee_list_text = "These employees have been added to the training session:"
            self.employees_list = tk.Label(self, text=employee_list_text, bg='#bfbd92')
            self.employees_list.pack()

            # Linking scanned barcode to employee name
            self.names = []
            self.employee_labels = []
            for row in reader:
                for temp_dict in temp_employee_dicts:
                    if row['BARCODE'] == temp_dict['BARCODE']:
                        temp_dict['NAME'] = row['NAME']
                    else:
                        continue
                    name = temp_dict['NAME']
                    self.names.append(name)
                    employee_text = f"{temp_dict['BARCODE']}, {temp_dict['NAME']}"
                    employee_label = tk.Label(self, text=employee_text, bg='#bfbd92')
                    self.employee_labels.append(employee_label)
                    for employee_label in self.employee_labels:
                        employee_label.pack()

            # Write labels to screen and entry box, make entry box work with enter key.
            self.training_prompt = tk.Label(self, text="What type of training is being given?", bg='#bfbd92')
            self.training_prompt.pack()
            self.training_entry = tk.Entry(self)
            self.training_entry.pack()
            self.training_entry.bind("<Return>", self.on_return_training)
            self.training_button = tk.Button(self, text="Enter", command=self.assign_training)
            self.training_button.pack()

        def yes_command(self):
            self.yes_button.destroy()
            self.no_button.destroy()
            self.prompt_label.destroy()
            self.barcode_prompt = tk.Label(self, text="Scan a barcode:", bg='#bfbd92')
            self.barcode_prompt.pack()
            self.entry = tk.Entry(self)
            self.entry.focus()
            self.entry.pack()
            self.barcode_button = tk.Button(self, text="Enter", command=self.more_employees)
            self.barcode_button.pack()
            self.entry.bind("<Return>", self.on_return_scan)

        def more_employees(self):
            global temp_employee_dict
            scan = self.entry.get()
            temp_employee_dict = {'BARCODE': scan, 'NAME': ''}
            if temp_employee_dict not in temp_employee_dicts:
                temp_employee_dicts.append(temp_employee_dict)
            self.barcode_prompt.destroy()
            self.entry.destroy()
            self.barcode_button.destroy()
            prompt = "Do you want to add another employee?"
            self.prompt_label = tk.Label(self, text=prompt, bg='#bfbd92')
            self.prompt_label.pack()
            self.yes_button = tk.Button(self, text="Yes", command=self.yes_command, bg='white')
            self.no_button = tk.Button(self, text="No", command=self.no_command, bg='white')
            self.yes_button.pack()
            self.no_button.pack()

        def assign_training(self):
            """Asks for input of training type and confirms with user.
             Also adds training to each employee in the data frame based on the barcodes scanned earlier."""
            global training
            if training == '':
               training = self.training_entry.get()
            self.training_button.destroy()
            self.employees_list.destroy()
            self.training_prompt.destroy()
            self.training_entry.destroy()
            for employee_label in self.employee_labels:
                employee_label.destroy()
            for temp_dict in temp_employee_dicts:
                for index, row in df.iterrows():
                    if str(df.loc[df.index[index], 'BARCODE']) == temp_dict['BARCODE']:
                        if 'None' not in df.loc[df.index[index], 'TRAINING']:
                            df.loc[df.index[index], 'TRAINING'] += ", " + training
                        elif 'None' in df.loc[df.index[index], 'TRAINING']:
                            df.loc[df.index[index], 'TRAINING'] = df.loc[df.index[index], 'TRAINING'].replace(
                                'None', '')
                            df.loc[df.index[index], 'TRAINING'] += training
            final_text = f"'{training}' has been added for each of these employees:"
            self.final_msg = tk.Label(self, text=final_text, bg='#bfbd92')
            self.final_msg.pack()
            for name in self.names:
                self.name_label = tk.Label(self, text=name, bg='#bfbd92')
                self.name_label.pack()
            self.close_button = tk.Button(self, text="Exit", command=root.destroy)
            self.close_button.pack()



    def main():
        global root
        root = tk.Tk()
        root.geometry('400x300')
        root.iconbitmap('C:/Users/angela.willis/Desktop/Barcode Check-In/exe/BCI_Icon.ico')
        root.title('BCI')
        App(root).pack(expand=True, fill='both')
        root.mainloop()


    if __name__ == "__main__":
        main()

employee_csv.close()

# Printing new data frame.
print(df)

# Exporting new data frame to original CSV file.
df.to_csv(r'C:/Users/angela.willis/Desktop/Barcode Check-In/employee_database/employee_database.csv', index=False)
