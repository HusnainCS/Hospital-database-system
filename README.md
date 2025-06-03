# Hospital Database System

A complete Hospital Database System featuring Entity-Relationship (ER) & Data Flow Diagrams (DFD), SQL schema, dummy data generation in Python, and a Streamlit dashboard.

## Features

- Professional DFD & ER diagrams
- SQL schema for hospital management
- Python script for dummy data population
- Interactive Streamlit dashboard

## Project Structure

```
Diagrams/         # DFD & ER diagram images
Schema/           # Database schema (SQL)
Script/           # Dummy data generation script
Dashboard/        # Streamlit dashboard code
docs/             # Additional documentation
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

2. **Set up the database:**
   - Use the SQL schema in `schema/schema.sql` to create your database.

3. **Generate Dummy Data:**
   ```bash
   cd script
   python dummy_data.py
   ```

4. **Install Dashboard Requirements:**
   ```bash
   cd dashboard
   pip install -r requirements.txt
   ```

5. **Run the Dashboard:**
   ```bash
   streamlit run Dashboard.py
   ```


## License

[MIT](LICENSE)

## Contact

- Husnain - husnian.cs@gmail.com