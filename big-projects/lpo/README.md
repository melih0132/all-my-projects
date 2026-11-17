# LPO Bird Counting

Database and BI pipeline for League for the Protection of Birds count data.

## Overview

Model observers, species, sites, and counts in PostgreSQL, then analyze with Excel and Power BI dashboards for trends and biodiversity.

## Features

- ERD / LDM modeling
- PostgreSQL schema, seeds, and SQL queries
- Excel descriptive stats
- Power BI interactive dashboard

## Stack

- PostgreSQL, SQL, pgAdmin4
- Excel
- Power BI
- Visual Paradigm / PowerAMC

## Layout

```
lpo/
├── 1_Modelisation/
├── 2_Insert_Query/
├── 3_View_Stat/
└── 4_PowerBI/
```

## Run

1. Create the PostgreSQL database from the SQL scripts
2. Export query results for Excel analysis
3. Open the Power BI report against the database or extracts
