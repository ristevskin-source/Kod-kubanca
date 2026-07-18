import streamlit as st
import sqlite3
import pandas as pd
from datetime import date

# --- KONFIGURACIJA ---
DOSTUPNI_TERMINI = [f"{sat:02d}:00" for sat in range(9, 21)]
CENE = {"Šišanje": 2000, "Brada": 700, "Pranje kose": 400}

# --- BAZA PODATAKA ---
def init_db():
    conn = sqlite3.connect('termini.db')
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS rezervacije")
    c.execute('''CREATE TABLE rezervacije 
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

init_db()

# --- APLIKACIJA ---
st.title("Kod Kubanca")
st.image("IMG_20260718_151846.jpg", width=300) # Ovde dodajemo sliku
with st.form("zakazivanje", clear_on_submit=True):
    usluga = st.selectbox("Usluga", list(CENE.keys()))
    datum = st.date_input("Datum")
    vreme = st.selectbox("Izaberi vreme", DOSTUPNI_TERMINI)
    ime_prezime = st.text_input("Ime i prezime")
    telefon = st.text_input("Telefon")
    
    if st.form_submit_button("Zakaži"):
        if ime_prezime and telefon:
            upisi_termin(usluga, datum, vreme, ime_prezime, telefon)
            st.success(f"Zakazano: {usluga} za {datum} u {vreme}.")
        else:
            st.error("Molim te, popuni ime i telefon.")

# --- ADMIN DEO ---
st.sidebar.title("Admin")
lozinka = st.sidebar.text_input("Lozinka:", type="password")

if lozinka == "1234":
    conn = sqlite3.connect('termini.db')
    df = pd.read_sql_query("SELECT * FROM rezervacije", conn)
    
    st.subheader("Pregled termina")
    st.table(df)
    
    # Kalkulacija prometa
    st.subheader("Finansijski pregled")
    danas = str(date.today())
    promet_danas = df[df['datum'] == danas]['cena'].sum()
    ukupan_promet = df['cena'].sum()
    
    st.metric("Promet danas", f"{promet_danas} din")
    st.metric("Ukupan promet", f"{ukupan_promet} din")
    
    conn.close()
