import streamlit as st
import json
import os

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
st.image("Screenshot_20260717_011214.jpg", width=300)
st.title("Kod Kubanca")

# Forma za zakazivanje
with st.form("zakazivanje", clear_on_submit=True):
    usluga = st.selectbox("Usluga", ["Šišanje", "Brada"])
    datum = st.date_input("Datum")
    vreme = st.selectbox("Vreme", ["09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00"])
    ime = st.text_input("Ime")
    telefon = st.text_input("Telefon")
    
    if st.form_submit_button("Zakaži"):
        if ime and telefon:
            novi = {"Ime": ime, "Datum": str(datum), "Vreme": vreme, "Usluga": usluga}
            sacuvaj_termin(novi)
            st.success("Uspešno zakazano!")
        else:
            st.error("Molim vas, popunite sva polja.")

# --- ADMIN PANEL ---
st.divider()
if st.checkbox("Prikaži admin izveštaj"):
    termini = ucitaj_termine()
    st.write("### Svi termini")
    st.table(termini)
    
    # Izračunavanje prometa (pretpostavljamo cenu od 1000 za šišanje i 500 za bradu)
    ukupno = sum([1000 if t['Usluga'] == "Šišanje" else 500 for t in termini])
    st.metric("Ukupan promet", f"{ukupno} RSD")
