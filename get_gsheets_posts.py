#!/usr/bin/env python3
import os
import gspread

print("===== get posts from gsheet ===")
print(os.environ["GSPREAD_TYPE"])


gspread_creds = {
  "type": os.environ["GSPREAD_TYPE"],
  "project_id": os.environ["GSPREAD_PROJECT_ID"],
  "private_key_id": os.environ["GSPREAD_PRIVATE_KEY_ID"],
  "private_key": os.environ["GSPREAD_PRIVATE_KEY"],
  "client_email": os.environ["GSPREAD_CLIENT_EMAIL"],
  "client_id": os.environ["GSPREAD_CLIENT_ID"],
  "auth_uri": os.environ["GSPREAD_AUTH_URI"],
  "token_uri": os.environ["GSPREAD_TOKEN_URI"],
  "auth_provider_x509_cert_url": os.environ["GSPREAD_AUTH_PROVIDER_X509_CERT_URL"],
  "client_x509_cert_url": os.environ["GSPREAD_CLIENT_X509_CERT_URL"]
}


gc = gspread.service_account_from_dict(gspread_creds)

sh = gc.open("BeerCalendar")

ws = sh.worksheet("Beers")

rows = ws.get_all_records()

for row in rows:
  filename = f"{row['Datum']}-{row['Biernaam']}.markdown"
  f = open(f"_posts/{filename}", "w")
  f.write("---")
  f.write("layout: post")
  f.write(f"title:  '{row['Biernaam']}'")
  f.write('''---

# Welcome test

**Hello world**, this is my first Jekyll blog post.

I hope you like it!
''')
  f.close()
