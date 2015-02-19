import json
import csv


data = """[{
    "account": "3147409", 
    "comments": "Customer made an enquiry into response times in tickets, re-kicking basically times on everything.", 
    "requests": [
        "Tomcat", 
        "Apache2.4", 
        "Mysql5.5", 
        "sshuser", 
        "ftpuser"
    ], 
    "ticket": "141114-03201", 
    "issues": [
        "rekicked"
    ], 
    "subject": ""
}]
"""

def writeCSV(jsonObject):
   csv_file = csv.writer(open("./erran.csv", "wb+"))
   for item in jsonObject:
     csv_file.writerow([item["account"],
                       item["ticket"],
                       item["subject"],
                       item["requests"],
                       item["issues"],
                       item["comments"]])
   #csv_file.close()

#f = open('test.json') 
#data = json.load(f) 
#f.close()

obj = json.loads(data)
writeCSV(obj)