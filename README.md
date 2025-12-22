# Proverbia Semantic Engine

## Overview
This project is a Semantic Web–based application that represents proverbs as a structured knowledge graph using RDF and OWL, and enables semantic querying through SPARQL. A Streamlit-based frontend allows users to interactively explore proverbs based on themes, sub-themes, regions, and sources.

The project demonstrates ontology-based knowledge representation and semantic data access using standard Semantic Web technologies.

---

## Key Technologies
- Python  
- RDF (Resource Description Framework)  
- OWL (Web Ontology Language)  
- SPARQL  
- rdflib  
- Streamlit  

---

## Project Architecture

CSV Dataset  
↓  
Python (Pandas + rdflib)  
↓  
OWL-based RDF Knowledge Graph (.ttl)  
↓  
SPARQL Queries  
↓  
Streamlit Web Application  

---

## Dataset Description
The dataset contains proverbs along with the following attributes:
- Proverb Text  
- Meaning  
- Theme  
- Sub-Theme  
- Region  
- Source  

The dataset is stored in CSV format and is automatically transformed into an RDF knowledge graph.

---

## Ontology Design (OWL)

### Classes
The ontology defines the following OWL classes:
- Proverb  
- Theme  
- SubTheme  
- Region  
- Source  

### Object Properties
- hasTheme (Proverb → Theme)  
- hasSubTheme (Proverb → SubTheme)  
- hasRegion (Proverb → Region)  
- hasSource (Proverb → Source)  

### Datatype Properties
- hasText (Proverb → string)  
- hasMeaning (Proverb → string)  

OWL is used to formally define the semantics and structure of the data, while RDF is used to store instance-level information.

---

## RDF Generation Process
1. The CSV dataset is loaded using Pandas.
2. OWL classes and properties are explicitly defined using rdflib.
3. Each proverb is converted into an RDF resource.
4. Relationships between proverbs and their attributes are added as RDF triples.
5. The complete knowledge graph is serialized into a Turtle (`.ttl`) file.

This approach ensures semantic consistency and extensibility.

---

## SPARQL Querying
SPARQL is used to query the RDF knowledge graph. Typical queries include:
- Retrieving proverbs by theme or sub-theme
- Filtering proverbs by region
- Selecting proverbs from a specific source
- Combining multiple semantic filters

These queries operate directly on the OWL-based RDF graph.

---

## Streamlit Application
The Streamlit application provides an interactive user interface that:
- Loads the RDF/OWL Turtle file
- Uses SPARQL queries in the backend
- Allows users to explore proverbs using dropdown-based filters
- Displays proverb text and meanings dynamically

No changes to the Streamlit application are required when OWL is added, as it interacts with the data through SPARQL.

---

## How to Run the Project

### Install Dependencies
```bash
pip install pandas rdflib streamlit
```

### Run Streamlit App
```bash
streamlit run app.py
