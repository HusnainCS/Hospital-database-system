# Hospital Database System

A complete Hospital Database System featuring Entity-Relationship (ER) & Data Flow Diagrams (DFD), SQL schema, dummy data generation in Python, and a Streamlit dashboard.

## Features

- Professional DFD & ER diagrams
- SQL schema for hospital management
- Python script for dummy data population
- Interactive Streamlit dashboard

## Project Structure

```
Diagrams/         # DFD & ER diagrams
Schema/           # Hospital Schema (SQL)
Script/           # Dummy data generation script
Dashboard/        # Streamlit dashboard code

```

## Diagrams

### ER Diagram
![ER Diagram](Diagrams/Entity_Relationship_Diagram.drawio)

### DFD
![DFD](Diagrams/Data_Flow_Diagram.drawio)

## Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/HusnainCS/Hospital_Database-System.git
   cd hospital-database-system
   ```

2. **Set up the Docker:**
 First Pull `postgers:latest`.
```bash
   docker build -t your_image_name .
```
Then create a container.
```bash
docker run -d -p 5432:5432 --name hospital_db -e POSTGRES_PASSWORD=your_password postgres
```
3. **Set up Dbeaver:**
   Open DBeaver, click on "New Database Connection", and select **PostgreSQL**.
   Enter host, port (5432), hospital_db, username, and password; then click **Finish** to connect.
   Use the SQL schema in `Schema/Hospital_Schema.sql` to create your database.

4. **Generate Dummy Data:**
   ```bash 
   cd Script
   python dummy_data.py
   ```

5. **Install Dashboard Requirements:**
   ```bash
   cd Dashboard
   pip install -r requirements.txt
   ```

6. **Run the Dashboard:**
   ```bash
   streamlit run Dashboard.py
   ```


## License

[MIT](LICENSE)

## Contact

- Husnain - husnian.cs@gmail.com
