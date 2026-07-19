import streamlit as st
import sqlite3

# --- 1. Inicijalizacija baze ---
def init_db():
    conn = sqlite3.connect('termini.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS rezervacije 
                 (id INTEGER PRIMARY KEY, usluga TEXT, datum TEXT, vreme TEXT, 
                  ime TEXT, telefon TEXT, cena INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS konfiguracija (lozinka TEXT)''')
    c.execute("SELECT * FROM konfiguracija")
    if not c.fetchone():
        c.execute("INSERT INTO konfiguracija (lozinka) VALUES ('1234')")
    conn.commit()
    conn.close()

init_db()

# --- 2. Inicijalizacija stanja ---
if "admin_ulogovan" not in st.session_state:
    st.session_state.admin_ulogovan = False
if "zakazano" not in st.session_state:
    st.session_state.zakazano = False

# --- 3. Funkcije ---
def proveri_lozinku(unesena):
    conn = sqlite3.connect('termini.db')
    c = conn.cursor()
    c.execute("SELECT lozinka FROM konfiguracija")
    prava = c.fetchone()[0]
    conn.close()
    return unesena == prava

# --- 4. Interfejs ---
st.title("Zakazivanje termina")

# Admin panel logika
if not st.session_state.admin_ulogovan:
    with st.expander("🔑 Admin Prijava"):
        lozinka_input = st.text_input("Unesi lozinku:", type="password")
        if st.button("Prijavi se"):
            if proveri_lozinku(lozinka_input):
                st.session_state.admin_ulogovan = True
                st.rerun()
            else:
                st.error("Pogrešna lozinka!")
else:
    st.success("Admin ulogovan")
    if st.button("Odjavi se"):
        st.session_state.admin_ulogovan = False
        st.rerun()
    
    with st.expander("⚙️ Sigurnosne postavke"):
        stara = st.text_input("Stara lozinka", type="password")
        nova = st.text_input("Nova lozinka", type="password")
        if st.button("Sačuvaj novu lozinku"):
            if proveri_lozinku(stara):
                conn = sqlite3.connect('termini.db')
                c = conn.cursor()
                c.execute("UPDATE konfiguracija SET lozinka = ?", (nova,))
                conn.commit()
                conn.close()
                st.success("Lozinka promenjena!")
            else:
                st.error("Stara lozinka nije tačna!")

# Forma za klijente
if not st.session_state.zakazano:
    with st.form("zakazivanje", clear_on_submit=False):
        ime = st.text_input("Ime i prezime")
        telefon = st.text_input("Telefon")
        submit = st.form_submit_button("Zakaži")
        
        if submit:
            # Ovde dodaj svoju logiku za upis u bazu
            st.session_state.zakazano = True
            st.rerun()
else:
    st.success("Uspešno zakazano! Hvala na poverenju.")
    if st.button("Zakaži novi termin"):
        st.session_state.zakazano = False
        st.rerun()
