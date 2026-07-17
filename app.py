import streamlit as st
import json
import os
from datetime import datetime

# --- KONFIGURACIJA ---
FAJL_TERMINA = "termini.json"

# --- FUNKCIJE ---
def ucitaj_termine():
    if os.path.exists(FAJL_TERMINA):
        with open(FAJL_TERMINA, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def sacuvaj_termin(novi_termin):
    termini = ucitaj_termine()
    termini.append(novi_termin)
    with open(FAJL_TERMINA, "w") as f:
        json.dump(termini, f, default=str)

# --- APLIKACIJA ---
st.title("Kod Kubanca")

# Forma za zakazivanje
with st.form("zakazivanje", clear_on_submit=True):
    usluga = st.selectbox("Usluga", ["Šišanje", "Brada"])
    datum = st.date_input("Datum")
    vreme = st.selectbox("Vreme", ["09:00", "10:00", "11:00", "12:00"])
    ime = st.text_input("Ime")
    telefon = st.text_input("Telefon")
    
    if st.form_submit_button("Zakaži"):
        novi = {"Ime": ime, "Datum": str(datum), "Vreme": vreme, "Usluga": usluga}
        sacuvaj_termin(novi)
        st.success("Uspešno zakazano!")

# --- ADMIN PANEL ---
st.divider()
if st.checkbox("Prikaži admin izveštaj"):
    termini = ucitaj_termine()
    st.write("### Svi termini")
    st.table(termini)
    
    # Izračunavanje prometa (primer za 1000 RSD po terminu)
    promet = len(termini) * 1000
    st.metric("Ukupan promet", f"{promet} RSD")
