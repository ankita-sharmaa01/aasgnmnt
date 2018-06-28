import csv
import os

from flask import Flask, jsonify, request
app = Flask(__name__)

FILE = os.environ.get("FILE", "test_data_sample.csv")


with open(FILE) as f:
    reader = csv.reader(f)
    terms = [row[0] for row in reader]
    terms=list(set(terms))              #Removed duplicacy of data in first name...

@app.route('/process_search')
def gen_search_json():
    query = request.args.get("q", '')
    results = [{"name" : "This is invalid, just to demo AJAX call is working"}]  
    # must be list of dicts: [{"name": "foo"}, {"name": "bar"}]
	# your logic goes here!
    if ( len(query) >= 3 ):
        list1={}
        list2={}
        list3={}
        for fnames in terms:
            if query in fnames:
                if fnames.startswith(query):
                    list1[fnames]=len(fnames)                  # priority 1, if name starts with search 
                elif fnames.endswith(query):
                    list3[fnames]=len(fnames)                  # priority 3, if name ends with search
                else:
                    list2[fnames]=len(fnames)                  # priority 2, if name has search
        list1 = sorted(list1, key=list1.get)            #in order of name length
        list2 = sorted(list2, key=list2.get)            #in order of name length
        list3 = sorted(list3, key=list3.get)            #in order of name length
        list2.extend(list3) 
        list1.extend(list2)
        if (len(list1) > 0):
            results = []                                # re-initializing results when response is present
            for name in list1:
                dictemp = {"name" : name}
                results.append(dictemp)
    #   print(results)     #for testing
    #else:                  #for testing
    #   print results      #for testing
		
    resp = jsonify(results=results[:10])  # top 10 results
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp
