#!/usr/bin/env python3
import os
import gspread
import requests
import datetime
import pytz
import glob
import io

from PIL import Image

def get_image_type(url):
  try:
    content_type = requests.head(url,allow_redirects=True).headers['Content-Type']
  except:
    return False
  
  if content_type.startswith("image/"):
    return content_type
  else:
    return False

print("===== get posts from gsheet ===")
os.makedirs("_posts", exist_ok=True)



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

old_posts = glob.glob('_posts/*.gs.markdown')
for old_post in old_posts:
  try:
      os.remove(old_post)
  except:
      print("Error while deleting file : ", filePath)

for row in rows:
  if(row['Datum'] == ""):
    continue
  row_date = datetime.date.fromisoformat(row['Datum'])
  today = datetime.datetime.now(pytz.timezone('Europe/Amsterdam')).date()
  if row_date <= today:
    image_url = row['Afbeelding']
    print(f"image_url: {image_url}")
    content_type = get_image_type(image_url)
    print(content_type)
    target_img_file = f"assets/img/day_{row['Dag']}.jpg"
    if content_type:
      print(".")
      image = Image.open(io.BytesIO(requests.get(image_url, stream=True).content)).convert('RGBA')
      print(".")
      image.thumbnail(size=(800,800))
      print(".")

      output_image = Image.new("RGBA", image.size, "WHITE")
      print(".")
      output_image.paste(image, mask=image)
      print(".")
      output_image.convert("RGB").save(target_img_file,format="JPEG",optimize=True)                  #Enregistre l'image dans le buffer
      print(".")
      print(f"Saved {image_url} to {target_img_file}")
    filename = f"{row['Datum']}-{row['Biernaam']}.gs.markdown"
    f = open(f"_posts/{filename}", "w")
    f.write("---\n")
    f.write("layout: post\n")
    f.write(f"title:  'Dag {row['Dag']} - {row['Biernaam']}'\n")
    f.write(f"permalink:  '/day/{row['Dag']}'\n")
    f.write(f"author:  '{row['Toegevoegd door']}'\n")
    f.write(f"description:  '{row['Introductie']}'\n")
    f.write("---\n")
    f.write(f"<p class='intro'><span class='dropcap'>{row['Introductie'][0]}</span>{row['Introductie'][1:]}</p>\n\n")
    f.write(f"{row['Notitie']}\n\n")
    if os.path.isfile(target_img_file):
      f.write(f"<figure><img src='/{target_img_file}' alt=''/> <figcaption>{row['Biernaam']} is een {row['Biertype']} van {row['Alcohol percentage']}%, gebrouwen door {row['Brouwerij']}.</figcaption></figure>\n")
    f.close()
