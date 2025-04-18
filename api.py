from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from chat import chatbot
from quora import qv
from newgser import hn

app = Flask(__name__)

# Load CSVs once
csv_file_path1 = 'quora_search_results.csv'
csv_file_path2 = 'search_results.csv'

df1 = pd.read_csv(csv_file_path1)
df2 = pd.read_csv(csv_file_path2)

# Function to compute sentiment distribution
def compute_sentiments(df):
    pos = df['sentiment'].value_counts().get('Positive', 0)
    net = df['sentiment'].value_counts().get('Neutral', 0)
    neg = df['sentiment'].value_counts().get('Negative', 0)
    total = pos + net + neg
    return pos, net, neg, total


@app.route('/', methods=["GET", "POST"])
def home():
    return render_template("simple_frontend.jsx")


@app.route('/back', methods=["GET", "POST"])
def back():
    varr = ""
    if request.method == "POST":
        varr = request.form.get("varr")
        return redirect(url_for('home', query=varr))

    varr = request.args.get("query", "")

    # Calculate sentiments
    pos1, net1, neg1, res2 = compute_sentiments(df2)
    pos2, net2, neg2, res1 = compute_sentiments(df1)

    pos_total = pos1 + pos2
    neg_total = neg1 + neg2
    net_total = net1 + net2
    grand_total = pos_total + neg_total + net_total

    posp = int((pos_total / grand_total) * 100) if grand_total else 0
    negp = int((neg_total / grand_total) * 100) if grand_total else 0
    netp = int((net_total / grand_total) * 100) if grand_total else 0

    print("                            opwefj  " +varr)
    # Process query if available
    if varr:
        qv(varr)
        hn(varr)
        aires = chatbot(varr)
        print(aires)
    else:
        aires = ""



    return render_template("simple_frontend.html" ,  posp, netp , aires)





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
