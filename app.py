
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

# Ovde postavi putanju do slike ako je u istom folderu
# st.image("ime_slike.jpg", width=300)

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
    st.subheader("Rezervacija termina")
    ime = st.text_input("Ime i prezime")
    termin = st.text_input("Željeni termin")
    if st.form_submit_button("Zakaži"):
        st.success("Zahtev poslat!")
