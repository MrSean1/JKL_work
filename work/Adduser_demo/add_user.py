import requests

from account_no import demo_acc

mt4_url = '47.52.254.64:8989/addAccount'



response = requests.post(mt4_url, data=demo_acc)
