import streamlit as st
import json
import os

# --- KONFIGURACIJA ---
FAJL_TERMINA = os.path.join(os.getcwd(), "termini.json")
ADMIN_LOZINKA = "1234"

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
st.image("Screenshot_20260717_011214.jpg", width=300)
st.title("Kod Kubanca")

# --- JAVNI DEO ---
svi_termini_dan = ["09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00"]
with st.form("zakazivanje", clear_on_submit=True):
    usluga = st.selectbox("Usluga", ["Šišanje", "Brada"])
    datum = st.date_input("Datum")
    
    termini = ucitaj_termine()
    zauzeti = []
    
    for t in termini:
        if t['Datum'] == str(datum):
            if t.get('Usluga') == "BLOKIRANO" and 'Od' in t and 'Do' in t:
                start = svi_termini_dan.index(t['Od'])
                end = svi_termini_dan.index(t['Do'])
                zauzeti.extend(svi_termini_dan[start:end+1])
            elif 'Vreme' in t:
                zauzeti.append(t['Vreme'])
    
    slobodni = [t for t in svi_termini_dan if t not in zauzeti]
    vreme = st.selectbox("Vreme", slobodni if slobodni else ["Nema slobodnih termina"])
    
    ime_prezime = st.text_input("Ime i prezime")
    telefon = st.text_input("Telefon")
    
    if st.form_submit_button("Zakaži"):
        if slobodni and ime_prezime and telefon:
            termini.append({"Ime i prezime": ime_prezime, "Telefon": telefon, "Datum": str(datum), "Vreme": vreme, "Usluga": usluga})
            sacuvaj_termine(termini)
            st.success("Uspešno zakazano!")
            st.rerun()
        else:
            st.error("Molimo vas, popunite sva polja.")

# --- ADMIN DEO ---
st.sidebar.title("Admin")
lozinka = st.sidebar.text_input("Lozinka:", type="password")

if lozinka == ADMIN_LOZINKA:
    if st.sidebar.button("Obriši sve termine"):
        sacuvaj_termine([])
        st.sidebar.success("Obrisano!")
        
    st.subheader("Blokiraj period")
    with st.form("blokiranje"):
        datum_pauze = st.date_input("Datum pauze")
        od_vreme = st.selectbox("Od:", svi_termini_dan)
        do_vreme = st.selectbox("Do:", svi_termini_dan)
        if st.form_submit_button("Potvrdi"):
            termini = ucitaj_termine()
            termini.append({"Ime": "PAUZA", "Datum": str(datum_pauze), "Od": od_vreme, "Do": do_vreme, "Usluga": "BLOKIRANO"})
            sacuvaj_termine(termini)
            st.rerun()
