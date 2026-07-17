import streamlit as st
import hashlib
import json
import os
import smtplib
from email.message import EmailMessage

# --- KONFIGURACIJA ---
CONFIG_FILE = "config.json"

def ucitaj_config():
    if not os.path.exists(CONFIG_FILE):
        return {"admin_hash": "NONE"}
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

# --- GLAVNI DEO ---
st.title("Kod Kubanca")
st.image("Screenshot_20260717_011214.jpg", width=300)

st.subheader("Naš cenovnik")
cenovnik = {
    "Šišanje": 1500,
    "Brada": 1000,
    "Šišanje i Brada": 2000,
    "Pranje kose": 400
}

for usluga, cena in cenovnik.items():
    st.write(f"{usluga}: {cena} RSD")

st.divider()

# --- FORMA ---
with st.form("zakazivanje"):
    izabrana_usluga = st.selectbox("Izaberi uslugu", list(cenovnik.keys()))
    datum = st.date_input("Izaberi datum")
    ime = st.text_input("Ime i prezime")
    submit = st.form_submit_button("Zakaži")

    if submit:
        st.success(f"Zahtev za {izabrana_usluga} na dan {datum} je poslat!")
