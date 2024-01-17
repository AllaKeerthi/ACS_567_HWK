import pandas as pd

class Dataset:
    def __init__(self, csv_file_path):
        """
        Initializes the Dataset with data from a CSV file.

        Parameters:
        - csv_file_path (str): Path to the CSV file.
        """
        self.data = pd.read_csv(csv_file_path)
        self.date = self.data['date']
        self.revenue = self.data['revenue']
        self.product = self.data['product']
        self.discounts = self.data['discounts']

    def get_data(self):
        """
        Returns the entire dataset.

        Returns:
        - pd.DataFrame: The entire dataset.
        """
        return self.data
    
class DataManager:
    """
    DataManager class manages operations on a dataset.

    Attributes:
    - _instance (DataManager): Singleton instance of the DataManager.
    - dataset (Dataset): The dataset to be managed.

    Methods:
    - __new__(cls, dataset): Creates a singleton instance of DataManager if not already exists.
    - read_data(): Reads and returns the entire dataset.
    - add_data(new_row_data): Adds new data to the dataset.
    - edit_data(index, column, new_value): Edits existing data in the dataset.
    - delete_data(index): Deletes existing data from the dataset.
    - analyze_data(): Performs data analysis on the dataset.
    - filter_data(choice): Filters data based on the user's choice.
    """

    _instance = None

    def __new__(cls, dataset):
        """
        Creates a singleton instance of DataManager if not already exists.

        Parameters:
        - dataset (Dataset): The dataset to be managed.

        Returns:
        - DataManager: The DataManager instance.
        """
        if cls._instance is None:
            cls._instance = super(DataManager, cls).__new__(cls)
            cls._instance.dataset = dataset
        return cls._instance
    
    def read_data(self):
        """
        Reads and returns the entire dataset.

        Returns:
        - pd.DataFrame: The entire dataset.
        """
        return self.dataset.get_data()

    def add_data(self, new_row_data):
        """
        Adds new data to the dataset.

        Parameters:
        - new_row_data (dict): A dictionary representing the new row data.

        Returns:
        - str: A message indicating the success or failure of the operation.
        """
        new_row_df = pd.DataFrame([new_row_data])

        if new_row_data['date'] in list(self.dataset.data['date'].values):
            return "Duplicate found. Data couldn't be added."
        else:
            self.dataset.data = pd.concat([self.dataset.data, new_row_df], ignore_index=True)
            return "Data added successfully."

    def edit_data(self, index, column, new_value):
        """
        Edits existing data in the dataset.

        Parameters:
        - index (int): Index of the row to edit.
        - column (str): Column to edit.
        - new_value: New value to set.

        Returns:
        - str: A message indicating the success or failure of the operation.
        """
        self.dataset.data.at[index, column] = new_value
        return "Data edited successfully."

    def delete_data(self, index):
        """
        Deletes existing data from the dataset.

        Parameters:
        - index (int): Index of the row to delete.

        Returns:
        - str: A message indicating the success or failure of the operation.
        """
        self.dataset.data = self.dataset.data.drop(index, axis=0).reset_index(drop=True)
        return "Data deleted successfully."

    def analyze_data(self):
        """
        Performs data analysis on the dataset.

        Returns:
        - pd.DataFrame: Analysis results.
        """
        analysis_results = self.dataset.data.describe()
        return analysis_results

    def filter_data(self, choice):
        """
        Filters data based on the user's choice.

        Parameters:
        - choice (int): User's choice for filtering.

        Returns:
        - pd.DataFrame: Filtered data.
        """
        if choice == 1:
            filtered_data = self.dataset.data.query('IT >= 30000')
        elif choice == 2:
            filtered_data = self.dataset.data.query('Marketing < 22000')
        elif choice == 3:
            filtered_data = self.dataset.data.query('Finance.notnull()')
        elif choice == 4:
            filtered_data = self.dataset.data.query('25000 <= Operations <= 30000')
        elif choice == 5:
            filtered_data = self.dataset.data.query('Month in ["January 2023", "March 2023"]')
        else:
            print("Invalid choice. No filtering applied.")
            return None
        
        return filtered_data


class DriverClass:
    """
    DriverClass orchestrates the overall functionality of the data management system.

    Attributes:
    - data_manager (DataManager): The DataManager instance for managing dataset operations.
    - columns (list): List of column names in the dataset.

    Methods:
    - __init__(self, data_manager): Initializes the DriverClass with a DataManager instance.
    - display_menu(): Displays the menu options for user interaction.
    - process_selection(choice): Processes the user's menu choice and calls the corresponding DataManager functions.
    """

    def __init__(self, data_manager):
        """
        Initializes the DriverClass with a DataManager instance.

        Parameters:
        - data_manager (DataManager): The DataManager instance for managing dataset operations.
        """
        self.data_manager = data_manager
        self.columns = data_manager.read_data().columns.tolist()
        self.data = self.data_manager.read_data()

    def display_menu(self):
        """
        Displays the menu options for user interaction.
        """
        print("\nMenu : ")
        print("1. Read Data")
        print("2. Add Data")
        print("3. Edit Data")
        print("4. Delete Data")
        print("5. Analyze Data")
        print("6. Filter Data")
        print("7. Exit")

    def process_selection(self, choice):
        """
        Processes the user's menu choice and calls the corresponding DataManager functions.

        Parameters:
        - choice (int): User's menu choice.
        """
        if choice == 1:
            data = self.data_manager.read_data()
            print(data)

        elif choice == 2:
            print("Fill the following column data:")
            values = {}
            column_names = self.columns
            for c in column_names:
                if self.data[c].dtype != 'object':
                    values[c] = int(input(f"Enter {c} value: "))
                else:
                    values[c] = input(f"Enter {c} value: ")

            result = self.data_manager.add_data(values)
            print(result)
            print(self.data_manager.read_data())

        elif choice == 3:
            index = int(input("Enter index to edit: "))
            column = input("Enter column to edit: ")
            try:
                new_value = int(input("Enter new value: "))
            except:
                new_value = input("Enter new value: ")
            result = self.data_manager.edit_data(index, column, new_value)
            print(result)

        elif choice == 4:
            index = int(input("Enter index to delete: "))
            result = self.data_manager.delete_data(index)
            print(result)

        elif choice == 5:
            analysis_results = self.data_manager.analyze_data()
            print(analysis_results)

        elif choice == 6:
            print("Options:")
            print("1. Filter rows where IT expenses are >= 30000")
            print("2. Filter rows where Marketing expenses are < 22000")
            print("3. Filter rows where Finance expenses are not null")
            print("4. Filter rows where Operations expenses are in range [25000 to 30000]")
            print("5. Filter rows where Month is either 'January 2023' or 'March 2023'")
            choice = int(input("Select 1 - 5: "))

            filtered_data = self.data_manager.filter_data(choice)
            print(filtered_data)

        elif choice == 7:
            exit()

        else:
            print("Invalid choice. Please choose a valid option.")

# Data File Path
csv_file_path = "financial_data.csv"

# Instance of dataset
dataset = Dataset(csv_file_path)

# Instance of DataManager
data_manager = DataManager(dataset)

# Instance of Driver
driver = DriverClass(data_manager)

# Running the driver in an infinite loop
while True:
    driver.display_menu()
    choice = int(input("Enter your choice: "))
    driver.process_selection(choice)

