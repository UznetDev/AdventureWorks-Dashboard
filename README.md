# AdventureWorks Sales Dashboard Application

In this program, dashboards and prediction models have been created using **Streamlit** on the AdventureWorks 2019 dataset. The app uses a machine learning model (Linear Regression) trained on sales data to make predictions. It is built using **Streamlit** for the frontend interface and **scikit-learn** for machine learning model development.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Model Details](#model-details)
- [Contributors](#contributors)

## Project Overview

The Sales Dashboard app allows users to input various sales-related data fields such as `SalesOrderID`, `OrderQty`, `LineTotal`, `StandardCost`, and more. The application uses a pre-trained Linear Regression model to predict the total due for the given input data. This app can be used by businesses to estimate future order dues based on historical data. With the smart dashboard, you can view the current sales situation.

## Features

- Input fields for all relevant sales order information, including order quantity, line total, costs, and dates.
- Predict the **TotalDue** using a pre-trained machine learning model.
- Automatically fills the date fields with the current date.
- Displays an error message if any required fields are missing.
- Easy-to-use web interface powered by **Streamlit**.
- A dashboard and prediction model based on the AdventureWorks 2019 dataset, completely free to use.

## Technologies Used

- **Python**: Main programming language.
- **Streamlit**: Web framework for building the user interface.
- **scikit-learn**: For training and using the machine learning model.
- **joblib**: For saving and loading the trained model.
- **MySQL**: Database for storing sales data.
- **GitHub**: Version control and project management.

## Installation

To run this application locally, follow these steps:

### Prerequisites

- Python 3.7 or higher
- Streamlit
- scikit-learn
- joblib
- MySQL (optional if you're using a local MySQL database)

### Steps

1. **Clone the repository to your local machine:**

   ```bash
   git clone https://github.com/UznetDev/AdventureWorks-Dashboard.git
   ```

2. **Navigate to the project directory:**

   ```bash
   cd AdventureWorks-Dashboard
   ```

3. **Create and activate a virtual environment (recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Linux: 
   venv\Scripts\activate # Oon windows
   ```

4. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   
5. **Create a .env file:**
   - On Windows:
     ```sh
     wsl nano .env
     ```
   - On macOS and Linux:
     ```sh
     nano .env
     ```

6. **Write in the .env file:**
  ```
HOST= <host default localhost>
MYSQL_USER= <your MySQL user>
MYSQL_PASSWORD= <your MySQL password>
MYSQL_DATABASE= <your MySQL database>
```

7. **Create a run.py file:**
   - On Windows:
     ```sh
     wsl nano run.py
     ```
   - On macOS and Linux:
     ```sh
     nano run.py
     ```


6. **Write in the run.py file:**
      ```python
     import sys
     from streamlit.web import cli as stcli
        
     if __name__ == "__main__":
        script_path = " <PATH DIRECTORY> /AdventureWorks-Dashboard/🏠_Home.py"
        sys.argv = ["streamlit", "run", script_path, "--server.port", "1212"]
        stcli.main()
    ```

7. **Include database:**

   ```bash
   mysql -u [your MySQL user] -p [your MySQL database] < atabase.sql
   ```

8. **Run the Streamlit application:**

   ```bash
   streamlit run app.py
   ```

The app should now be running on `http://localhost:8501/`.



## Project Structure

```plaintext
AdventureWorks-Dashboard/
├── README.md                            # Project documentation
├── loader.py                            # Python script to load and prepare data
├── requirements.txt                     # Project dependencies
├── LICENSE                              # License file
│
├── data/                                # Folder for storing raw data
│   └── config.py                        # A collection of necessary variables
│
├── db/                                  # SQL queries and database operations
│   └── mysql_db.py                      # Class for working with MySQL database
│
├── function/                            # Python functions for data manipulation
│   └── function.py                      # Core bot functionalities
│
├── pages/                               # Power BI dashboard pages
│   └── 🏂_Prediction.py.pbix            # 🏂_Prediction page script
│
├── model.pkl                            # Pretrained machine learning model (if applicable)
└── 🏠_Home.py                           # Main script for 🏠_Home page

```

## Usage

Once the app is running, you can enter the following fields:

- **SalesOrderID**: The unique identifier of the sales order.
- **OrderQty**: The quantity of products ordered.
- **LineTotal**: The total line cost for the order.
- **StandardCost**: The standard cost of the product.
- **ListPrice**: The list price of the product.
- **CustomerID**: The unique identifier of the customer.
- **AccountNumber**: The account number associated with the customer.
- **OrderDate**, **DueDate**, **ShipDate**: These fields will be auto-filled with the current date but can be modified if necessary.

After filling in the required fields, press the **Predict TotalDue** button. The predicted `TotalDue` will be displayed on the screen.

## Model Details

The model used in this application is a **Linear Regression** model trained on historical sales data. The model was trained using the following features:

- **OrderQty**: Number of units ordered.
- **LineTotal**: The total value of the order line.
- **StandardCost**: The cost to produce the product.
- **ListPrice**: The sales price of the product.
- **CustomerID**: Customer identifier.
- **AccountNumber**: Customer's account number.

The prediction is made based on the relationship between these features and the total amount due for previous sales.

## Contributing

We welcome contributions! Please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a pull request.
## Reporting Issues

If you find any issues with the bot or have suggestions, please open an issue in this repository.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## <i>Contact</i>

If you have any questions or suggestions, please contact:
- Email: uznetdev@example.com
- GitHub Issues: [Issues section](https://github.com/UznetDev/AdventureWorks-Dashboard/issues)
- GitHub Profile: [UznetDev](https://github.com/UznetDev/)
- Telegram: [UZNet_Dev](https://t.me/UZNet_Dev)
- Linkedin: [Abdurahmon Niyozaliev](https://www.linkedin.com/in/abdurakhmon-niyozaliyev-%F0%9F%87%B5%F0%9F%87%B8-66545222a/)


### <i>Thank you for your interest in the project!</i>