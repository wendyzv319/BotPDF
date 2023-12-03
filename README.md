# BotPDF: Assistant for Processing and Analysis of PDFs

The aim of this project is to utilize tools such as LangChain and FAISS to create a chatbot that enables users to upload PDFs and ask questions about the content therein.

## Setup

1. If you don’t have Python (>3.10) installed, [install it from here](https://www.python.org/downloads/).

## Installing / Getting started
    > git clone https://github.com/wendyzv319/BotPDF.git
	From the command prompt access the Boot PDF folder that is located within the repository that you just cloned
    > cd BotPDF/BotPDF
    Run the batch file:
    > install.bat
    Then, run:
    > run.bat
   The application will likely run on http://127.0.0.1:8000/ (port 8000 is configured within the ".env" file).
   
   
## Developing

### Built With
- Flask v2.3
- openai v0.27.8
- openpyxl v3.0.9
- pandas v1.3.4
- Flask-cors v3.0.10
- requests v2.31.0
- python-dotenv v1.0.0
- langchain v0.0.240
- doctran v0.0.9
- pypdf v3.15.4
- faiss-cpu v1.7.4
  
### Prerequisites
- Python 3.10.7
- OPENAI_KEY: [OpenAI key](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)


To work with openai you need to add the variable `OPENAI_API_KEY` to a .env. Check your in the follow link [API key](https://beta.openai.com/account/api-keys) .

## Contact Info

For any questions or information you need about the project, you can send an email to: wendyzv.319@gmail.com
