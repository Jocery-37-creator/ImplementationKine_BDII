# 💳 KINE: Transactional Database System Inspired by Nequi

**Databases II – Final Project**  
**Universidad Distrital Francisco José de Caldas**  
**Semester 2025-I**

- Jose Jesus Cespedes Rivera 20211020118
- Sofia Lozano Martinez 20211020088

## 📌 Overview

**Kine** is a transactional system inspired by digital banking platforms such as **Nequi**. It replicates a real-world financial service environment where operations like transfers, payments, and balance checks must be processed with high availability, consistency, and regulatory compliance. The system was designed to simulate OLTP workloads with an emphasis on ACID integrity, distributed architecture, and real-time performance.


## ⚙️ Technologies Used

| Layer                | Technology          | Purpose                          |
|---------------------|---------------------|----------------------------------|
| Relational Database | PostgreSQL          | Core transactional engine (OLTP) |
| NoSQL Database      | MongoDB             | Document-based support storage   |
| Scripting           | Python + Faker      | Data generation and automation   |

---

## 🎯 Key Features

- **Distributed Architecture:** Designed to support massive concurrency and data separation (hot vs cold storage).
- **Hybrid Storage:** PostgreSQL for structured data, MongoDB for unstructured, historical, or supporting content.
- **Regulatory Compliance:** Includes archival logic for maintaining transaction data over time.
- **BI Ready:** Query sets for reporting, analytics, and management dashboards.
- **Performance Oriented:** Proven capacity to process hundreds of transactions per second in OLTP simulations.

---

## 📊 Business and Technical Components

- **📦 Business Model Canvas:** Captures the value proposition, customer segments, and revenue logic.
- **🧑‍💼 User Stories:** Detailed stories with acceptance criteria for each core function.
- **📜 Requirements:** Covers functional and non-functional demands aligned with Nequi’s context.
- **🏛️ Architecture Diagram:** Illustrates data flow, component distribution, and database roles.
- **🧠 Business Intelligence:** Demonstrates managerial insight through SQL aggregation and temporal queries.
