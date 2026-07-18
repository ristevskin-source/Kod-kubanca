import streamlit as st
import sqlite3
import pandas as pd

# --- BAZA PODATAKA ---
def init_db():
    conn = sqlite3.connect('termini.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS rezervacije 
                 (id INTEGER PRIMARY KEY, usluga TEXT, datum TEXT, vreme TEXT, ime TEXT, telefon TEXT)''')
    conn.commit()
    conn.close()

def upisi_termin(usluga, datum, vreme, ime, telefon):
    conn = sqlite3.connect('termini.db')
    c = conn.cursor()
    c.execute("INSERT INTO rezervacije (usluga, datum, vreme, ime, telefon) VALUES (?,?,?,?,?)",
              (usluga, str(datum), vreme, ime, telefon))
    conn.commit()
    conn.close()

init_db()

# --- APLIKACIJA ---
st.image("IMG_20260718_151846.jpg", width=300)
st.title("Kod Kubanca")

with st.form("zakazivanje", clear_on_submit=True):
    usluga = st.selectbox("Usluga", ["Šišanje", "Brada", "Pranje kose"])
    datum = st.date_input("Datum")
    vreme = st.text_input("Vreme")
    ime_prezime = st.text_input("Ime i prezime")
    telefon = st.text_input("Telefon")
    
    if st.form_submit_button("Zakaži"):
        if ime_prezime and telefon:
            upisi_termin(usluga, datum, vreme, ime_prezime, telefon)
            st.success(f"Uspešno ste zakazali: {usluga} za {datum} u {vreme}. Vidimo se!")
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
