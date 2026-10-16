# SmartBuy AI — System Architecture

## 1. Overview

SmartBuy AI is a purchasing decision-support prototype for reviewing
purchase recommendations, checking business constraints, creating
purchase orders, and validating the saved results.

The current implementation uses deterministic business rules and
mock purchasing data. It does not use an external LLM or live supplier API.

## 2. Architecture Diagram

```text
+-----------------------------+
|        Buyer / User         |
+--------------+--------------+
               |
               v
+-----------------------------+
|     Streamlit User Interface|
|  Inventory, Demand, Results |
+--------------+--------------+
               |
               v
+-----------------------------+
|   Purchasing Decision Logic |
|                             |
| - Calculate net requirement |
| - Check budget              |
| - Check storage capacity    |
| - Check supplier minimum    |
| - Recommend an action       |
+--------------+--------------+
               |
               v
+-----------------------------+
|    Buyer Approval Check     |
+--------------+--------------+
               |
               v
+-----------------------------+
|    Purchase Order Service   |
| - Recheck constraints       |
| - Prevent duplicate orders  |
| - Save approved order       |
+--------------+--------------+
               |
               v
+-----------------------------+
|       SQLite Database       |
|       purchase_orders       |
+--------------+--------------+
               |
               v
+-----------------------------+
|   Purchase Order Validation |
| - Verify saved quantity     |
| - Verify total cost         |
| - Check budget and storage  |
| - Verify order status       |
+-----------------------------+
