from flask import Flask, render_template, request, jsonify
import pandas as pd
import os

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/datalab"

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/upload", methods=["POST","GET"])
def upload():
    if request.method == "POST":
        file = request.files['fileinput']
        if file.filename != '':
            filepath =os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)
            input_data = pd.read_excel(file, sheet_name=None)
            df_datastatus = input_data.get('Data_Status')
            df_datateknik = input_data.get('Data_Teknik')
            df_dataasset = input_data.get('Data_Asset')
            df_dataconsume = input_data.get('Data_Consume')
            df_dataassesment = input_data.get('Data_Assesment')
           
            data_status, data_teknik, data_asset, data_consume , data_assesment = [], [] , [], [] , []
            for i in range(len(df_datastatus.index)):
                data = { 'status' : df_datastatus['Status'][i],
                        'detil' : df_datastatus['Detil'][i]
                        }
                data_status.append(data)
            print(data_status)
            for i in range(len(df_datateknik.index)):
                data = {'name' : df_datateknik['Data_Teknik'][i],
                        'detil' : df_datateknik['Detil'][i],
                        'status' : df_datateknik['Status'][i]
                        } 
                data_teknik.append(data)
            print(data_teknik)
            for i in range(len(df_dataasset.index)):
                data = {'name' : df_dataasset['Data_asset'][i],
                        'detil' : df_dataasset['Detil'][i],
                        'status' : int(df_dataasset['Status'][i])
                        } 
                data_asset.append(data)
            print(data_asset)
            for i in range(len(df_dataconsume.index)):
                data = { 'chemical' : df_dataconsume['Chemical'][i],
                        'pcs' : int(df_dataconsume['PCS'][i])
                        }
                data_consume.append(data)
            print(data_consume)
            for i in range(len(df_dataassesment.index)):
                data =  {
                        "name": df_dataassesment['Testing_Parameter'][i],
                        "result":df_dataassesment['Result'][i],
                        "unit": df_dataassesment['Unit'][i],
                        "methods": df_dataassesment['Methods'][i],
                        "recomendation": df_dataassesment['Recomendation'][i]
                    }
                data_assesment.append(data)
            print(data_assesment)
        output = {
                        "data_status": data_status,
                        "data_teknik" : data_teknik,
                        "data_asset" : data_asset,
                        "data_consume" : data_consume,
                        "data_assesment" : data_assesment
                    }

    return jsonify(output)
        

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
    