import streamlit as st
import json
import os

# --- KONFIGURACIJA ---
FAJL_TERMINA = "termini.json"
ADMIN_LOZINKA = "1234" 

# Definišemo usluge i cene
usluge_cene = {
    "Šišanje": 2000,
    "Brada": 1000,
    "Pranje kose": 500
}

# --- FUNKCIJE ---
def ucitaj_termine():
    if os.path.exists(FAJL_TERMINA):
        with open(FAJL_TERMINA, "r") as f:
            try: return json.load(f)
            except: return []
    return []

def sacuvaj_termine(termini):
    with open(FAJL_TERMINA, "w") as f:
        json.dump(termini, f, default=str)

# --- APLIKACIJA ---
st.title("Kod Kubanca")

# Radno vreme
svi_termini_dan = [
    "08:00", "09:00", "10:00", "11:00", "12:00", "13:00", 
    "14:00", "15:00", "16:00", "17:00", "18:00", "19:00"
]

# --- JAVNI DEO ---
with st.form("zakazivanje", clear_on_submit=True):
    opcije = [f"{u} - {c} RSD" for u, c in usluge_cene.items()]
    izbor = st.selectbox("Usluga", opcije)
    usluga_naziv = izbor.split(" - ")[0]
    datum = st.date_input("Datum")
    
    termini = ucitaj_termine()
    zauzeti = []
    blokirani_periodi = []
    
    for t in termini:
        if t['Datum'] == str(datum):
            if t.get('Usluga') == "BLOKIRANO":
                start = svi_termini_dan.index(t['Od'])
                end = svi_termini_dan.index(t['Do'])
                zauzeti.extend(svi_termini_dan[start:end+1])
                blokirani_periodi.append(f"{t['Od']} - {t['Do']}")
            else:
                zauzeti.append(t['Vreme'])
    
    slobodni = [t for t in svi_termini_dan if t not in zauzeti]
    
    vreme = st.selectbox("Vreme", slobodni if slobodni else ["Nema slobodnih termina"])
    ime = st.text_input("Ime")
    telefon = st.text_input("Telefon")
    
    if st.form_submit_button("Zakaži"):
        if slobodni and ime and telefon:
            termini.append({"Ime": ime, "Telefon": telefon, "Datum": str(datum), "Vreme": vreme, "Usluga": usluga_naziv})
            sacuvaj_termine(termini)
            st.success("Zakazano!")
            st.rerun()

    # Prikaz blokiranih perioda za klijente na dnu
    if blokirani_periodi:
        st.divider()
        st.write("Trenutno zauzeti periodi:")
        for period in set(blokirani_periodi):
            st.warning(f"Period: {period}")

# --- ADMIN DEO ---
st.sidebar.title("Admin Pristup")
lozinka = st.sidebar.text_input("Lozinka:", type="password")

if lozinka == ADMIN_LOZINKA:
    st.header("Admin Kontrolna Tabla")
    termini = ucitaj_termine()
    
    if termini:
        # Promet
        aktivni = [t for t in termini if t.get('Usluga') != "BLOKIRANO"]
        ukupno = sum([usluge_cene.get(t['Usluga'], 0) for t in aktivni])
        st.metric("Ukupan promet", f"{ukupno} RSD")
        st.dataframe(termini)

    st.subheader("Blokiraj period")
    with st.form("blokiranje"):
        datum_pauze = st.date_input("Datum pauze")
        col1, col2 = st.columns(2)
        od_vreme = col1.selectbox("Od:", svi_termini_dan)
        do_vreme = col2.selectbox("Do:", svi_termini_dan)
        if st.form_submit_button("Blokiraj"):
            termini.append({"Ime": "PAUZA", "Datum": str(datum_pauze), "Od": od_vreme, "Do": do_vreme, "Usluga": "BLOKIRANO"})
            sacuvaj_termine(termini)
            st.rerun()
