import streamlit as st
import sqlite3
import pandas as pd
from datetime import date

# --- KONFIGURACIJA ---
SVI_TERMINI = [f"{sat:02d}:00" for sat in range(9, 21)]
CENE = {"Šišanje": 2000, "Brada": 700, "Pranje kose": 400}

# --- BAZA PODATAKA ---
def init_db():
    conn = sqlite3.connect('termini.db')
    c = conn.cursor()
    # CREATE TABLE IF NOT EXISTS čuva postojeće podatke
    c.execute('''CREATE TABLE IF NOT EXISTS rezervacije 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  usluga TEXT, datum TEXT, vreme TEXT, 
                  ime TEXT, telefon TEXT, cena INTEGER)''')
    conn.commit()
    conn.close()

def upisi_termin(usluga, datum, vreme, ime, telefon):
    conn = sqlite3.connect('termini.db')
    c = conn.cursor()
    cena = CENE.get(usluga, 0)
    c.execute("INSERT INTO rezervacije (usluga, datum, vreme, ime, telefon, cena) VALUES (?,?,?,?,?,?)",
              (usluga, str(datum), vreme, ime, telefon, cena))
    conn.commit()
    conn.close()

def dohvati_sve_termine():
    conn = sqlite3.connect('termini.db')
    df = pd.read_sql_query("SELECT * FROM rezervacije", conn)
    conn.close()
    return df

init_db()

# --- APLIKACIJA ---
st.title("Kod Kubanca")
st.image("IMG_20260718_151846.jpg", width=300)

with st.form("zakazivanje", clear_on_submit=True):
    usluga = st.selectbox("Usluga", list(CENE.keys()))
    datum = st.date_input("Datum")
    vreme = st.selectbox("Izaberi vreme", SVI_TERMINI)
    ime_prezime = st.text_input("Ime i prezime")
    telefon = st.text_input("Telefon")
    
    if st.form_submit_button("Zakaži"):
        if ime_prezime and telefon:
            upisi_termin(usluga, datum, vreme, ime_prezime, telefon)
            # POTVRDA KLIJENTU
            st.success(f"Uspešno zakazano: {usluga} za {datum} u {vreme}. Hvala!")
        else:
            st.error("Molim te, popuni ime i telefon.")

# --- ADMIN DEO ---
st.sidebar.title("Admin")
lozinka = st.sidebar.text_input("Lozinka:", type="password")

if lozinka == "1234":
    df = dohvati_sve_termine()
    st.subheader("Pregled svih zakazanih termina")
    st.table(df)
    
    # ZBIRNI PROMET
    st.subheader("Finansijski pregled")
    danas = str(date.today())
    promet_danas = df[df['datum'] == danas]['cena'].sum()
    ukupan_promet = df['cena'].sum()
    
    st.metric("Promet danas", f"{promet_danas} din")
    st.metric("Ukupan promet", f"{ukupan_promet} din")
