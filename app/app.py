from flask import Flask, request, render_template, session, send_from_directory
import os
from sieve_data import sieve_data
from finess_modulus import finess_modulus
from graph import graph
from alter_graph import alter_graph
from download import download_pdf
from aashto import aashto
from uscs import uscs
from my_server import my_server


app = Flask(__name__)
app.secret_key = 'My_Nigga'

def upload_file_path():
            file = request.files['file']
            current_directory = os.path.dirname(__file__).replace("\\","/")
            file_path = os.path.join(current_directory, file.filename).replace("\\","/")
            file.save(file_path)

            return file_path
    

@app.route('/')
def home_page():
      return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    try:
        file_path = upload_file_path()
        session['file_path'] = file_path

        sieves_passing = sieve_data(file_path)
        

        return render_template('index.html', message="File saved successfully!", file_path=file_path,
                                    passing_sieve_5mm = sieves_passing[0], passing_sieve_2mm = sieves_passing[1], 
                                    passing_sieve_425micro_m = sieves_passing[2], passing_sieve_75micro_m = sieves_passing[3])
    
    except (PermissionError, UnicodeDecodeError, ValueError):
            return render_template('index.html', message="Invalid File! File may be corrupt") 

@app.route('/generate', methods=['GET', 'POST'])
def generate():
    if request.method == 'POST':
        file_path = session.get('file_path')

        liquid_limit_1 = request.form.get('liquidLimit')
        liquid_limit = int(float(liquid_limit_1))
        plastic_limit_1 = request.form.get('plasticLimit')
        plastic_limit = int(float(plastic_limit_1))

        if plastic_limit > 0:
            PI = float(liquid_limit_1) - float(plastic_limit_1)
        else:
            PI = 0.0
                
        #Check the A-Line plot for USCS Classification
        graph_check = (PI+14.6)/liquid_limit
                
        _5mm = float(request.form.get('5mm'))
        _2mm = float(request.form.get('2mm'))
        _425micro_m = float(request.form.get('425micro_m'))
        _75micro_m = float(request.form.get('75micro_m'))

        aashto_class = aashto(_2mm, _425micro_m, _75micro_m, liquid_limit, plastic_limit, PI)

        if (file_path):
            D60, D30, D10, CU, CC = graph(file_path)
        else:
            D60, D30, D10, CU, CC = alter_graph(_5mm, _2mm, _425micro_m, _75micro_m)

        D60 = round(D60, 3)
        D30 = round(D30, 3)
        D10 = round(D10, 3)
        CU = round(CU, 3)
        CC = round(CC, 3)

        finess_mod = finess_modulus(file_path)

        uscs_class = uscs(PI, liquid_limit, CC, CU, _5mm, _75micro_m, graph_check)    

        pdf_file = download_pdf(plastic_limit_1, liquid_limit_1, finess_mod, D60, D30, D10, CU, CC, aashto_class, uscs_class)
        session['pdf_file'] = pdf_file

      

        my_server(_5mm, _2mm, _425micro_m, _75micro_m, finess_mod, CC, CU, liquid_limit_1,
                    plastic_limit_1, PI, graph_check, aashto_class, uscs_class)

        return render_template('generate.html', message="File saved successfully!", file_path=file_path,
                                    liquid_limit=liquid_limit, plastic_limit=plastic_limit, cu0 = D60,
                                    cu3 = CU, cu4 = CC, cu1 = D30, cu2 = D10,
                                    _5mm=_5mm, _2mm=_2mm, _425micro_m=_425micro_m, _75micro_m=_75micro_m,
                                    uscs_class=uscs_class, aashto_class=aashto_class, finess_mod=finess_mod, pdf_file=pdf_file)
    else:
          render_template('generate.html')



@app.route('/download/soil_report.pdf', methods=['GET'])
def download_file():
    filename = 'soil_report.pdf'
    return send_from_directory(os.path.join(app.root_path, 'static'), filename, as_attachment=True)

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')
