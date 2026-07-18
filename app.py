import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# --- KONFIGURACIJA ---
ADMIN_LOZINKA = "1234"
URL_TABELE = "https://docs.google.com/spreadsheets/d/1_hWwzOOhupyrv1t2FWRh-7gHpIh7JQpyVDVqLUut6bE/edit?usp=drivesdk"

CENE = {
    "Šišanje": "2000 din",
    "Brada": "700 din",
    "Pranje kose": "500 din"
}

# --- FUNKCIJE ---
def ucitaj_termine():. 
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(spreadsheet=URL_TABELE, usecols=[0, 1, 2])
    return df

# --- APLIKACIJA ---
st.image("https://raw.githubusercontent.com/ristevskin-source/Kod-kubanca/main/IMG_20260718_151846.jpg", width=300)
st.title("Kod Kubanca")

# --- JAVNI DEO ---
with st.form("zakazivanje", clear_on_submit=True):
    usluga = st.selectbox("Usluga", list(CENE.keys()))
    datum = st.date_input("Datum")
    vreme = st.text_input("Vreme (npr. 10:00)")
    ime_prezime = st.text_input("Ime i prezime")
    telefon = st.text_input("Telefon")
    
    if st.form_submit_button("Zakaži"):
        st.write("Sistem je spreman. Molimo vas proverite Admin panel.")

# --- ADMIN DEO ---
st.sidebar.title("Admin")
lozinka = st.sidebar.text_input("Lozinka:", type="password")

if lozinka == ADMIN_LOZINKA:
    st.subheader("Pregled zakazanih termina")
    try:
        termini = ucitaj_termine()
        st.table(termini)
    except:
        st.write("Još uvek nema podataka u tabeli ili veza nije uspostavljena.")
