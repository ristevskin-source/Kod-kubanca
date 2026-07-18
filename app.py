import streamlit as st
import pandas as pd

# --- KONFIGURACIJA ---
ADMIN_LOZINKA = "1234"
CENE = {
    "Šišanje": "2000 din",
    "Brada": "700 din",
    "Pranje kose": "500 din"
}

# --- FUNKCIJE ---
def ucitaj_termine():
    # Ovde ćemo kasnije dodati čitanje iz Google tabele
    return []

def sacuvaj_termine(termini):
    # Ovde ćemo kasnije dodati čuvanje u Google tabelu
    st.write("Podaci bi ovde bili sačuvani.")

# --- APLIKACIJA ---
st.image("https://raw.githubusercontent.com/ristevskin-source/Kod-kubanca/main/IMG_20260718_151846.jpg", width=300)
st.title("Kod Kubanca")

# --- JAVNI DEO ---
svi_termini_dan = ["09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00"]

with st.form("zakazivanje", clear_on_submit=True):
    usluga = st.selectbox("Usluga", list(CENE.keys()))
    datum = st.date_input("Datum")
    
    termini = ucitaj_termine()
    zauzeti = []
    
    slobodni = [t for t in svi_termini_dan if t not in zauzeti]
    vreme = st.selectbox("Vreme", slobodni if slobodni else ["Nema slobodnih termina"])
    
    ime_prezime = st.text_input("Ime i prezime")
    telefon = st.text_input("Telefon")
    
    if st.form_submit_button("Zakaži"):
        if slobodni and ime_prezime and telefon:
            cena = CENE.get(usluga)
            termini.append({"Ime i prezime": ime_prezime, "Telefon": telefon, "Datum": str(datum), "Vreme": vreme, "Usluga": usluga})
            sacuvaj_termine(termini)
            st.success(f"Uspešno ste zakazali {usluga}! Cena usluge je {cena}.")
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
