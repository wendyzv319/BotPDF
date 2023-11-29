from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
from PDFProcessor import PDFProcessor

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Lista de mensajes en el chat
chat_messages = []

# Crea una instancia global de PDFProcessor
pdf_processor = PDFProcessor()


@app.route('/')
def index():
    return render_template('index1.html', chat_messages=chat_messages)


@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '' or not file.filename.endswith('.pdf'):
            return redirect(request.url)

        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

        result = pdf_processor.load_pdf(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

        print(f'result is: {result}')
        if not result:
            print(f"Error al cargar el PDF")
            return jsonify({'status': 'error', 'message': "error_message"})
        else:
            print("PDF cargado correctamente")
            # Realiza acciones adicionales según sea necesario, como procesar el contenido del PDF
            return jsonify({'status': 'success', 'message': 'Archivo cargado correctamente'})

    except Exception as e:
        error_message = f"Error al cargar el PDF: {str(e)}"
        print(error_message)
        return jsonify({'status': 'error', 'message': error_message})


@app.route('/process', methods=['POST'])
def process_loaded_pdf():
    try:
        # Lógica para procesar el PDF
        print(len(pdf_processor.loaded_content))
        result = pdf_processor.process_loaded_pdf()

        if not result:
            print(f"Error al procesar el PDF")
            return jsonify({'status': 'error', 'message': "error_message", 'code': 1})
        else:
            print("PDF procesado correctamente")
            # Realiza acciones adicionales según sea necesario, como procesar el contenido del PDF
            return jsonify({'status': 'success', 'message': 'Archivo cargado correctamente', 'code': 0})


    except Exception as e:
        error_message = f"Error al procesar el PDF: {str(e)}"
        print(error_message)
        return jsonify({'status': 'error', 'message': error_message, 'code': 1})


@app.route('/get_bot_response', methods=['POST'])
def get_bot_response():
    try:
        print("Bot response")
        user_input = request.form['user_input']
        print(user_input)

        bot_response = pdf_processor.bot_response(user_input)

        return jsonify({'bot_response': bot_response})
    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    app.run(debug=True)
