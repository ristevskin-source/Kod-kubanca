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

def upisi_termin(usluga, datum, vreme, ime, telefon, cena):
    conn = sqlite3.connect('termini.db')
    c = conn.cursor()
    # Ovde eksplicitno upisujemo vrednosti koje dobijamo iz forme
    c.execute("INSERT INTO rezervacije (usluga, datum, vreme, ime, telefon, cena) VALUES (?,?,?,?,?,?)",
              (usluga, str(datum), vreme, ime, telefon, cena))
    conn.commit()
    conn.close()

init_db()

# --- APLIKACIJA ---
st.title("Kod Kubanca")

with st.form("forma_zakazivanje", clear_on_submit=True):
    usluga = st.selectbox("Usluga", list(CENE.keys()))
    datum = st.date_input("Datum")
    
    # Filtriranje termina
    conn = sqlite3.connect('termini.db')
    zauzeti_df = pd.read_sql_query("SELECT vreme FROM rezervacije WHERE datum = ?", conn, params=(str(datum),))
    conn.close()
    zauzeti = zauzeti_df['vreme'].tolist()
    slobodni = [t for t in SVI_TERMINI if t not in zauzeti]
    
    vreme = st.selectbox("Izaberi vreme", slobodni if slobodni else ["Nema termina"])
    
    # Korišćenje ključeva (keys) osigurava da Streamlit pravilno povezuje polja
    ime_klijenta = st.text_input("Ime i prezime", key="ime_input")
    telefon_klijenta = st.text_input("Telefon", key="tel_input")
    
    submit = st.form_submit_button("Zakaži")

    if submit:
        if ime_klijenta and telefon_klijenta and slobodni:
            upisi_termin(usluga, datum, vreme, ime_klijenta, telefon_klijenta, CENE[usluga])
            st.success(f"Uspešno zakazano: {usluga}, {datum} u {vreme}. Hvala, {ime_klijenta}!")
            st.rerun() 
        else:
            st.error("Molim te, popuni sva polja ispravno.")

# --- ADMIN DEO ---
st.sidebar.title("Admin")
lozinka = st.sidebar.text_input("Lozinka:", type="password")

if lozinka == "1234":
    conn = sqlite3.connect('termini.db')
    df = pd.read_sql_query("SELECT * FROM rezervacije", conn)
    conn.close()
    
    st.subheader("Pregled i brisanje")
    edited_df = st.data_editor(df, num_rows="dynamic")
    
    if st.button("Sačuvaj promene"):
        conn = sqlite3.connect('termini.db')
        edited_df.to_sql('rezervacije', conn, if_exists='replace', index=False)
        conn.close()
        st.success("Tabela ažurirana!")
        st.rerun()
