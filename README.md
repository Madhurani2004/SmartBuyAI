# SmartBuy AI — Purchasing Decision Agent

## Overview

SmartBuy AI is a purchasing decision-support application built with Python, Streamlit, and SQLite.

The application reviews a recommended purchase quantity against inventory, expected demand, incoming orders, supplier minimum order quantity, budget, and storage capacity.

It calculates the required quantity, explains the decision, allows buyer approval, creates a purchase order, and validates the saved order.

The current prototype uses sample data and rule-based decision logic. It does not connect to an external LLM or live supplier APIs.

## Features

- Calculates the required purchase quantity.
- Accounts for current inventory and incoming orders.
- Applies the supplier minimum order quantity.
- Checks available budget and storage capacity.
- Requires buyer approval before creating an order.
- Saves purchase orders in SQLite.
- Prevents duplicate purchase order IDs.
- Validates saved order quantities, costs, and constraints.
- Includes automated database tests.

## Technology Stack

- Python
- Streamlit
- SQLite
- Python `unittest`

## How It Works

1. Read the purchasing information.
2. Calculate the net quantity required.
3. Check the budget and storage constraints.
4. Decide whether to accept, modify, reject, or investigate the recommendation.
5. Request buyer approval before creating an order.
6. Save the purchase order in SQLite.
7. Retrieve and validate the saved order.

## Example Scenario

The application uses the following sample data:

| Input | Value |
|---|---:|
| Recommended quantity | 800 units |
| Current inventory | 200 units |
| Expected demand | 400 units |
| Incoming orders | 100 units |
| Supplier minimum order | 50 units |
| Unit price | ₹40 |
| Available budget | ₹30,000 |
| Available storage | 500 units |

**Required quantity**

Expected demand − Current inventory − Incoming orders

400 − 200 − 100 = 100 units

**Estimated cost**

100 × ₹40 = ₹4,000

The application compares the calculated requirement with the original recommendation and checks the configured purchasing constraints.

## Project Structure

```text
SmartBuyAI/
├── app.py
├── database.py
├── test_database.py
├── requirements.txt
├── README.md
├── architecture.md
├── .env.example
└── .gitignore
```

The SQLite database file is created locally when the application runs and should not be committed to the repository.

## Prerequisites

- Python 3.12 or a compatible Python version
- pip

## Installation

Clone the repository and open its directory.

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Run the Application

```bash
python -m streamlit run app.py
```

Open the local address displayed in the terminal, usually `http://localhost:8501`.

## Run Automated Tests

```bash
python -m unittest test_database -v
```

The database tests cover saving and retrieving purchase orders, duplicate order IDs, zero quantities, and negative unit prices.

## Validation Approach

After an order is created, the application retrieves it from SQLite and checks its quantity, total cost, budget, storage capacity, and status.

The validation result indicates whether the saved order satisfies the configured checks.

## Limitations

- Purchasing information is sample data.
- Decisions use deterministic business rules.
- Live supplier APIs and external LLM integration are not implemented.
- Authentication and production deployment are outside the scope of this prototype.
