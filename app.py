import requests
import time

from flask import Flask, render_template

app = Flask(__name__)

def verify_domain_txt_record(dnskey: str, domain: str):
    url = f'https://dns.google/resolve?name={domain}&type=TXT'

    try:
        res = requests.get(url)
        if res.status_code == 200:
            dns_records = res.json().get('Answer', [])
            for record in dns_records:
                if dnskey in record.get('data', ''):
                    return True
    except Exception:
        print('verify domain failed. domain: %s, dnskey: %s',
                             domain, dnskey)

        # no txt record in the domain
        return False
    return "Verify Domain"

@app.route("/")
def hello_world():
    test_dns_key = "zJNxSTTI5KvgruKUlMuVsyBHGfYI6NpqaA04hdtE4U8v8r5TQ6O3jZOH+A31v3kn4qctZ/o9FnFNqKvRVY0rOA=="
    test_domaiin = "rohrdorfer.eu"
    start_time = time.time()
    has_txt_record = verify_domain_txt_record(test_dns_key, test_domaiin)
    end_time = time.time()
    verified_time = end_time - start_time
    print(f"Verified time: {verified_time} seconds")
    
    if has_txt_record:
        print("TXT Record Exist")
    else:
        print("Not exist")

    return render_template("index.html", title="Hello")
