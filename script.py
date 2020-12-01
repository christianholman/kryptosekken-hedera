import os
import sys
import requests
import csv
from datetime import datetime 
from dotenv import load_dotenv, find_dotenv 

load_dotenv(find_dotenv())

DRAGONGLASS_API_KEY = os.environ.get("DRAGONGLASS_API_KEY")

account_id = sys.argv[1]
hedera_accounts = ["0.0.3", "0.0.4", "0.0.98"]
headers = {
    "X-API-KEY": DRAGONGLASS_API_KEY,
}
interval = 1000

def main():
    if not os.path.exists("output"):
        os.makedirs("output")

    file_path = "output/report_%s.csv" % datetime.now().replace(microsecond=0).isoformat()
    with open(file_path, "w+") as csvfile:
        fields = ["Tidspunkt", "Type", "Inn", "Inn-Valuta", "Ut", "Ut-Valuta", "Gebyr", "Gebyr-Valuta", "Marked", "Notat", "Transaksjon-Id"]
        writer = csv.writer(csvfile)
        writer.writerow(fields)

    def get_transfers(from_number):
        r = requests.get("https://api.dragonglass.me/hedera/api/accounts/%s/transactions?from=%s&size=%s" % (account_id, from_number, interval), headers=headers)
        response_body = r.json()

        print(response_body)
        for transaction in response_body["data"]:
            with open(file_path, "a") as csvfile:
                writer = csv.writer(csvfile)

                if transaction["status"] == "SUCCESS":
                    account_id_transfer_sum = 0

                    transaksjon_type = ""
                    tidspunkt = transaction["consensusTime"]
                    gebyr = transaction["transactionFee"] if transaction["payerID"] is account_id else 0
                    gebyr_valuta = "HBAR"
                    inn = 0
                    inn_valuta = "HBAR"
                    ut = 0
                    ut_valuta = "HBAR"

                    for transfer in [transfer for transfer in transaction["transfers"] if transfer["accountID"] == account_id]:
                        account_id_transfer_sum += transfer["amount"]
                    
                    if account_id_transfer_sum > 0:
                        transaksjon_type = "Overføring-Inn"
                        inn = account_id_transfer_sum
                    elif account_id_transfer_sum < 0:
                        transaksjon_type = "Overføring-Ut"
                        ut = abs(account_id_transfer_sum) - gebyr

                    marked = ""
                    notat = transaction["memo"]
                    transaksjon_id = transaction["transactionID"]

                    inn = inn / 100000000
                    ut = ut / 100000000
                    gebyr = gebyr / 100000000

                    write_row(writer, tidspunkt, transaksjon_type, inn, inn_valuta, ut, ut_valuta, gebyr, gebyr_valuta, marked, notat, transaksjon_id)

        if ((from_number + response_body["size"]) < response_body["totalCount"]):
            get_transfers(from_number + interval) 
        else:
            print(file_path + " created!")

    def write_row(writer, tidspunkt, transaksjon_type, inn, inn_valuta, ut, ut_valuta, gebyr, gebyr_valuta, marked, notat, transaksjon_id):
        row = [tidspunkt, transaksjon_type, inn, inn_valuta, ut, ut_valuta, gebyr, gebyr_valuta, marked, notat, transaksjon_id]
        writer.writerow(row)


    get_transfers(0)

main()
