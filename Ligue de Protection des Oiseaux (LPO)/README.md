## **Bird Counting Data Management for the League for the Protection of Birds (LPO)**

### **Overview**  
This project involves designing and implementing a database to manage bird counting records for the League for the Protection of Birds (LPO). The goal is to streamline data management, perform relevant statistical analysis, and present the results in a visual and interactive manner.  

### **Project Steps**  
1. **Database Modeling**  
   - **ERD (Entity-Relationship Diagram):** Defining the entities, relationships, and constraints to represent bird counts, observers, species, sites, etc.  
   - **LDM (Logical Data Model):** Translating the ERD into relational tables suited for PostgreSQL.  

2. **Database Setup (PostgreSQL)**  
   - Creation of tables and defining constraints (primary keys, foreign keys, etc.).  
   - Inserting data to simulate actual bird count records.  
   - Developing SQL queries to query, analyze, and manage the data.  

3. **Statistical Analysis (Excel)**  
   - Extracting relevant data from PostgreSQL.  
   - Performing descriptive statistics: number of individuals per species, geographic distribution of observations, population trends over time, etc.  
   - Creating charts to visualize the results.  

4. **Interactive Report (Power BI)**  
   - Importing consolidated data from PostgreSQL.  
   - Designing an interactive dashboard to display:  
     - Trends in bird populations.  
     - Geographical areas with the richest biodiversity.  
     - Annual or seasonal comparisons.  
   - Highlighting key indicators to facilitate decision-making.  

### **Technologies Used**  
- **Database:** PostgreSQL, pgAdmin4  
- **Query Language:** SQL  
- **Statistical Tools:** Microsoft Excel  
- **Visualization:** Power BI  

### **Installation and Execution**  
1. **Setup the database:**  
   - Install PostgreSQL and run the provided SQL scripts to create and populate the database.  

2. **Export data for analysis:**  
   - Use SQL queries to extract the necessary data and import it into Excel for statistical analysis.  

3. **Load data into Power BI:**  
   - Connect Power BI to PostgreSQL to generate the interactive dashboard.  
