## 🧠 AI Agent for Data Question Answering

## 📌 Objective

Build an AI-powered agent that:

* 📤 Accepts questions through API endpoints.
* 🧠 Understands the query using a local Large Language Model (LLM).
* 🗃️ Queries the data from SQL tables.
* ✅ Returns accurate, human-readable answers.


## 🚀 Project Overview

This AI system aims to automate Q\&A over structured datasets by integrating a locally hosted LLM, SQL database, and an API service.

---

## 🛠️ Steps to Follow

1. ### 🗂️ Convert Data to SQL

   * Parse and load all datasets into structured SQL tables.
   * Use SQLite, PostgreSQL, or any preferred SQL database.

2. ### 🧠 Choose an LLM (Local)

   * Example options:

     * [LM Studio](https://lmstudio.ai/)
     * [Ollama](https://ollama.com/)
     * [GPT4All](https://github.com/nomic-ai/gpt4all)
   * Download the model for offline usage.

3. ### 🔌 Build the Codebase

   * Connect the following components:

     * The LLM (via API or Python bindings)
     * SQL database (using `sqlite3`)
     * API server ( FastAPI, etc.)

4. ### 🤖 Implement AI Agent Logic

   * Parse incoming question from user.
   * Convert the question to a valid SQL query using the LLM.
   * Execute the query on the SQL database.
   * Format and return the result in a readable way.



## 📦 Tech Stack

* **LLM:** LLaMA
* **Database:** SQLite
* **Backend:** Python + FastAPI 
