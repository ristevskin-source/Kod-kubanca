
import streamlit as st
import pandas as pd

# --- KONFIGURACIJA ---
ADMIN_LOZINKA = "1234"
# Ovo je link ka tvom CSV formatu
URL_CSV = "https://docs.google.com/spreadsheets/d/1_hWwzOOhupyrv1t2FWRh-7gHpIh7JQpyVDVqLUut6bE/export?format=csv"

# --- FUNKCIJE ---
def ucitaj_termine():
    # Direktno čitanje iz CSV formata
    df = pd.read_csv(URL_CSV)
    return df

# --- APLIKACIJA ---
st.image("IMG_20260718_151846.jpg", width=300)
st.title("Kod Kubanca")

# --- JAVNI DEO ---
with st.form("zakazivanje", clear_on_submit=True):
    usluga = st.selectbox("Usluga", ["Šišanje", "Brada", "Pranje kose"])
    datum = st.date_input("Datum")
    vreme = st.text_input("Vreme (npr. 10:00)")
    ime_prezime = st.text_input("Ime i prezime")
    telefon = st.text_input("Telefon")
    
    if st.form_submit_button("Zakaži"):
        st.write("Sistem je spreman.")

# --- ADMIN DEO ---
st.sidebar.title("Admin")
lozinka = st.sidebar.text_input("Lozinka:", type="password")

if lozinka == ADMIN_LOZINKA:
    st.subheader("Pregled zakazanih termina")
    try:
        termini = ucitaj_termine()
        st.table(termini)
    except Exception as e:
        st.write("Greška pri učitavanju: ", e)
