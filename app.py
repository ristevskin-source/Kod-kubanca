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
    # OVO VIŠE NE BRIŠEMO DA BI SE ČUVALI PODACI
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

def dohvati_zauzete_termine(datum):
    conn = sqlite3.connect('termini.db')
    query = "SELECT vreme FROM rezervacije WHERE datum = ?"
    df = pd.read_sql_query(query, conn, params=(str(datum),))
    conn.close()
    return df['vreme'].tolist()

init_db()

# --- APLIKACIJA ---
st.title("Kod Kubanca")
st.image("IMG_20260718_151846.jpg", width=300)

with st.form("zakazivanje", clear_on_submit=True):
    usluga = st.selectbox("Usluga", list(CENE.keys()))
    datum = st.date_input("Datum")
    
    # Filtriranje termina
    zauzeti = dohvati_zauzete_termine(datum)
    slobodni = [t for t in SVI_TERMINI if t not in zauzeti]
    
    vreme = st.selectbox("Izaberi vreme", slobodni if slobodni else ["Nema slobodnih termina"])
    ime_prezime = st.text_input("Ime i prezime")
    telefon = st.text_input("Telefon")
    
    if st.form_submit_button("Zakaži"):
        if ime_prezime and telefon and vreme != "Nema slobodnih termina":
            upisi_termin(usluga, datum, vreme, ime_prezime, telefon)
            st.success(f"Zakazano: {usluga} za {datum} u {vreme}.")
            st.rerun() # Osvežava stranicu da se odmah vidi promena
        else:
            st.error("Proveri podatke ili izaberi drugi termin.")

# --- ADMIN DEO ---
st.sidebar.title("Admin")
lozinka = st.sidebar.text_input("Lozinka:", type="password")

if lozinka == "1234":
    conn = sqlite3.connect('termini.db')
    df = pd.read_sql_query("SELECT * FROM rezervacije", conn)
    st.subheader("Pregled svih termina")
    st.table(df)
    
    st.subheader("Finansijski pregled")
    danas = str(date.today())
    promet_danas = df[df['datum'] == danas]['cena'].sum()
    st.metric("Promet danas", f"{promet_danas} din")
    conn.close()
