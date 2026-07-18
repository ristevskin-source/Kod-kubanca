import streamlit as st
import sqlite3
import pandas as pd

# --- KONFIGURACIJA ---
DOSTUPNI_TERMINI = [f"{sat:02d}:00" for sat in range(9, 21)]
CENE = {"Šišanje": 2000, "Brada": 700, "Pranje kose": 400}

# --- BAZA PODATAKA ---


def upisi_termin(usluga, datum, vreme, ime, telefon):
    conn = sqlite3.connect('termini.db')
    c = conn.cursor()
    cena = CENE.get(usluga, 0)
    c.execute("INSERT INTO rezervacije (usluga, datum, vreme, ime, telefon, cena) VALUES (?,?,?,?,?,?)",
              (usluga, str(datum), vreme, ime, telefon, cena))
    conn.commit()
    conn.close()

init_db()

# --- APLIKACIJA ---
st.image("IMG_20260718_151846.jpg", width=300)
st.title("Kod Kubanca")

with st.form("zakazivanje", clear_on_submit=True):
    usluga = st.selectbox("Usluga", list(CENE.keys()))
    datum = st.date_input("Datum")
    vreme = st.selectbox("Izaberi vreme", DOSTUPNI_TERMINI)
    ime_prezime = st.text_input("Ime i prezime")
    telefon = st.text_input("Telefon")
    
    if st.form_submit_button("Zakaži"):
        if ime_prezime and telefon:
            upisi_termin(usluga, datum, vreme, ime_prezime, telefon)
            st.success(f"Uspešno ste zakazali: {usluga} ({CENE[usluga]} din) za {datum} u {vreme}.")
        else:
            st.error("Molim te, popuni ime i telefon.")

# --- ADMIN DEO ---
st.sidebar.title("Admin")
lozinka = st.sidebar.text_input("Lozinka:", type="password")

if lozinka == "1234":
    st.subheader("Pregled zakazanih termina")
    conn = sqlite3.connect('termini.db')
    df = pd.read_sql_query("SELECT * FROM rezervacije", conn)
    st.table(df)
    conn.close()
