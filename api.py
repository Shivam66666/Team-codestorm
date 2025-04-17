from flask import Flask, jsonify , render_template , request
import threading
from chat import chatbot
from quora import qv
from newgser import hn

app = Flask(__name__)

import pandas as pd

# Path to your CSV file
csv_file_path1 = 'quora_search_results.csv'

# Read the CSV file
df1 = pd.read_csv(csv_file_path1)

# Path to your CSV file
csv_file_path2 = 'search_results.csv'

# Read the CSV file
df2 = pd.read_csv(csv_file_path2)


# Display the contents
# print(df["score"])



pos1 = 0
neg1 = 0
net1 = 0
pos2 = 0
net2 = 0
neg2 = 0
res1 = 0
res2 = 0
varr = "python"




@app.route('/', methods = ["GET" , "POST"])
def home():
    global varr
    if request.method == "POST":
        varr = request.form.get("varr")
        return varr
    # print(varr)





    global pos1 
    global neg1 
    global net1 
    global pos2 
    global net2 
    global neg2 
    global res1 
    global res2 



    for sc in df1["sentiment"]:
        if sc== "Positive":
            pos2 = pos2+1
        if sc== "Neutral":
            net2 = net2+1
        if sc== "Negative":
            neg2 = neg2+1
        res1 = res1+1

    for sc in df2["sentiment"]:
        if sc== "Positive":
            pos1 = pos1+1
        if sc== "Neutral":
            net1 = net1+1
        if sc== "Negative":
            neg1 = neg1+1
        res2 = res2+1
    
    pos=pos1+pos2
    neg=neg1+neg2
    net=net1+net2
    total=pos+neg+net
    posp=(int)((pos/total)*100    )
    negp=(int)((neg/total)*100    )
    netp=(int)((net/total)*100    )

    # print(posp)









    qv(varr)
    hn(varr)
    aires =  chatbot(varr)



    return render_template("simple_frontend.html",pos = posp,neg= negp ,net = netp,res1=res1,res2=res2 , aires = aires)











if __name__ == '__main__':  # Corrected line
    app.run(host='0.0.0.0', port=5000, debug=True)
    
