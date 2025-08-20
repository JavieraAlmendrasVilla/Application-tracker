````markdown
# 📊 Job Description Extractor  

This app extracts structured job posting information (position, company, skills, etc.) from unstructured job descriptions.  
It uses **LangChain + Ollama (local LLM)** and saves results automatically into a CSV file.  

## 🚀 Features  
- Extracts key information from job descriptions:  
  - **Position / Job Title**  
  - **Company**  
  - **Company Summary**  
  - **Job Description Summary** (about the position only)  
  - **Technical Skills**  
  - **Soft Skills**  
  - **Education**  
- Missing fields are filled with blanks (`""`) → ensures consistent CSV rows.  
- Interactive **Gradio interface** for easy copy-paste input.  
- Saves structured results to `applications.csv`.  

---

## ⚙️ Installation  

1. **Clone the repo**  
   ```bash
   git clone https://github.com/your-username/job-description-extractor.git
   cd job-description-extractor
````

2. **Set up a virtual environment (recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate    # macOS/Linux
   venv\Scripts\activate       # Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Install Ollama and the model**

   * [Download Ollama](https://ollama.ai) and install it.
   * Pull the model:

     ```bash
     ollama pull llama3.2:1b
     ```

---

## ▶️ Run the App

```bash
python app.py
```

* Gradio will start a local server at:
  👉 `http://127.0.0.1:7860`

Paste any job description into the textbox and the app will:

1. Extract structured information.
2. Append it as a row in `applications.csv`.

---

## 📂 Output

Example row in **applications.csv**:

| Position     | Company | Company Summary              | Job Description Summary            | Technical Skills      | Soft Skills                  | Education         |
| ------------ | ------- | ---------------------------- | ---------------------------------- | --------------------- | ---------------------------- | ----------------- |
| Data Analyst | Best Start-up  | We are the best Start-up in the world | As data analyst you will be analyzing data | SQL, PowerBI, Tableau | Communication, Teamwork | Bachelor / Master |

---

## 🛠 Tech Stack

* [LangChain](https://www.langchain.com/)
* [Ollama](https://ollama.ai) (local LLM)
* [Gradio](https://www.gradio.app/)
* Python 3.9+

---

```

Do you want me to also create a **requirements.txt** for you so users can install everything in one go?
```
