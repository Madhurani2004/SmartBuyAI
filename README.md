# SmartBuy AI — Purchasing Decision Agent

## Overview

SmartBuy AI is a purchasing decision-support application built with Python, Streamlit, and SQLite.

It evaluates a recommended purchase quantity against inventory, expected demand, incoming orders, supplier minimum order quantity, budget, and storage capacity.

Instead of blindly accepting a purchase recommendation, the application calculates the required quantity, checks purchasing constraints, creates a purchase order when the checks pass, and validates the saved order.

## Features

- Calculates required purchase quantity.
- Accounts for current inventory and incoming orders.
- Applies the supplier minimum order quantity.
- Checks available budget and storage capacity.
- Creates purchase orders when the configured checks pass.
- Stores purchase orders in an SQLite database.
- Prevents duplicate creation of the same purchase order ID.
- Validates saved purchase orders.
- Includes an automated database test.

## Technology Stack

- Python
- Streamlit
- SQLite
- Python unittest

## Decision Workflow

1. Investigate inventory, demand, incoming orders, and purchasing constraints.
2. Calculate the required purchase quantity.
3. Check budget and storage capacity.
4. Create and save a purchase order if the checks pass.
5. Retrieve and validate the saved purchase order.

## Example Scenario

The application uses sample data to demonstrate purchasing decisions.

| Input | Example Value |
|---|---:|
| Recommended quantity | 800 units |
| Current inventory | 200 units |
| Expected demand | 400 units |
| Incoming orders | 100 units |
| Supplier minimum order | 50 units |
| Unit price | ₹40 |
| Available budget | ₹30,000 |
| Available storage | 500 units |

With these values, the calculated requirement is:

400 - 200 - 100 = 100 units

Estimated purchase cost:

100 × ₹40 = ₹4,000

The application checks the purchase constraints before creating the order.

## Prerequisites

- Python 3.12 or a compatible Python version
- pip

## Installation

Clone the repository and open the project folder.

Install the required dependency:

    pip install -r requirements.txt

## Run the Application

Install the required dependency:

    pip install -r requirements.txt

Start SmartBuy AI:

    streamlit run app.py

Open the local address shown in your terminal, usually http://localhost:8501.

## Run Automated Tests

Run the database test:

    python -m unittest test_database -v

If the test passes, the terminal should display OK.


Clone the repository and open the project directory.

Install the required dependency:

```bash
pip install -r requirements.txt
