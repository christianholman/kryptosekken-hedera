import os
import sys
import requests
import csv
from datetime import datetime
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

DRAGONGLASS_API_KEY = os.environ.get("DRAGONGLASS_API_KEY")

account_id = sys.argv[1]
headers = {
    "X-API-KEY": DRAGONGLASS_API_KEY,
}
interval = 1000

fields = ["Tidspunkt", "Type", "Inn", "Inn-Valuta", "Ut", "Ut-Valuta", "Gebyr", "Gebyr-Valuta", "Marked", "Notat"]
file_name = "report_%s.csv" % datetime.now().replace(microsecond=0).isoformat()

if not os.path.exists("output"):
    os.makedirs("output")

with open("output/" + file_name, "w+") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(fields)

def get_transfers(from_number):
    r = requests.get("https://api.dragonglass.me/hedera/api/accounts/%s/transfers?from=%s&size=%s" % (account_id, from_number, interval), headers=headers)
    response_body = r.json()

    for transfer in response_body["data"]:
        with open(file_name, "a") as csvfile:
            writer = csv.writer(csvfile)

            transfer_amount_hbar = transfer["amount"] / 100000000

            tidspunkt = transfer["consensusTime"]
            transaksjon_type = "Overføring-Inn" if transfer["amount"] > 0 else "Overføring-Ut"
            inn = transfer_amount_hbar if transfer["amount"] > 0 else "0"
            inn_valuta = "HBAR"
            ut = abs(transfer_amount_hbar) if transfer["amount"] < 0 else "0"
            ut_valuta = "HBAR"
            gebyr = "0"
            gebyr_valuta = "0"
            marked = ""
            notat = transfer["memo"]

            row = [tidspunkt, transaksjon_type, inn, inn_valuta, ut, ut_valuta, gebyr, gebyr_valuta, marked, notat]

            writer.writerow(row)

    if ((from_number + response_body["size"]) < response_body["totalCount"]):
        get_transfers(from_number + interval) 
    else:
        print(file_name + " created!")

get_transfers(0)

