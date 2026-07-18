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
    c.execute('''CREATE TABLE IF NOT EXISTS rezervacije 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  usluga TEXT, datum TEXT, vreme TEXT, 
                  ime TEXT, telefon TEXT, cena INTEGER)''')
    conn.commit()
    conn.close()

def upisi_termin(usluga, datum, vreme, ime, telefon, cena=0):
    conn = sqlite3.connect('termini.db')
    c = conn.cursor()
    c.execute("INSERT INTO rezervacije (usluga, datum, vreme, ime, telefon, cena) VALUES (?,?,?,?,?,?)",
              (usluga, str(datum), vreme, ime, telefon, cena))
    conn.commit()
    conn.close()

def dohvati_zauzete(datum):
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
    
    # Filtriranje slobodnih termina
    zauzeti = dohvati_zauzete(datum)
    slobodni = [t for t in SVI_TERMINI if t not in zauzeti]
    
    vreme = st.selectbox("Izaberi vreme", slobodni if slobodni else ["Nema slobodnih termina"])
    ime_prezime = st.text_input("Ime i prezime")
    telefon = st.text_input("Telefon")
    
    if st.form_submit_button("Zakaži"):
        if ime_prezime and telefon and slobodni:
            upisi_termin(usluga, datum, vreme, ime_prezime, telefon, CENE[usluga])
            st.success(f"Uspešno zakazano: {usluga} za {datum} u {vreme}.")
            st.rerun()
        else:
            st.error("Popuni podatke ili izaberi drugi termin.")

# --- ADMIN DEO ---
st.sidebar.title("Admin")
lozinka = st.sidebar.text_input("Lozinka:", type="password")

if lozinka == "1234":
    # 1. BRISANJE I PREGLED
    conn = sqlite3.connect('termini.db')
    df = pd.read_sql_query("SELECT * FROM rezervacije", conn)
    conn.close()
    
    st.subheader("Upravljanje terminima")
    edited_df = st.data_editor(df, num_rows="dynamic")
    
    if st.button("Sačuvaj izmene (Brisanje)"):
        conn = sqlite3.connect('termini.db')
        edited_df.to_sql('rezervacije', conn, if_exists='replace', index=False)
        conn.close()
        st.rerun()

    # 2. DODAVANJE PAUZE
    st.subheader("Dodaj pauzu")
    p_datum = st.date_input("Datum pauze")
    p_vreme = st.selectbox("Vreme pauze", SVI_TERMINI)
    if st.button("Blokiraj termin"):
        upisi_termin("PAUZA", p_datum, p_vreme, "PAUZA", "-", 0)
        st.rerun()
