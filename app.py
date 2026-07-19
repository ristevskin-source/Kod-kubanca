import streamlit as st
import sqlite3

# --- 1. Inicijalizacija ---
def init_db():
    conn = sqlite3.connect('termini.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS rezervacije 
                 (id INTEGER PRIMARY KEY, usluga TEXT, datum TEXT, vreme TEXT, 
                  ime TEXT, telefon TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS konfiguracija (lozinka TEXT)''')
    c.execute("SELECT * FROM konfiguracija")
    if not c.fetchone():
        c.execute("INSERT INTO konfiguracija (lozinka) VALUES ('1234')")
    conn.commit()
    conn.close()

init_db()

if "admin_ulogovan" not in st.session_state: st.session_state.admin_ulogovan = False
if "zakazano" not in st.session_state: st.session_state.zakazano = False

# --- 2. Pomoćne funkcije ---
def get_slobodni_termini(datum):
    svi = ["09:00", "10:00", "11:00", "12:00", "13:00", "14:00"]
    conn = sqlite3.connect('termini.db')
    c = conn.cursor()
    c.execute("SELECT vreme FROM rezervacije WHERE datum = ?", (datum,))
    zauzeti = [row[0] for row in c.fetchall()]
    conn.close()
    return [t for t in svi if t not in zauzeti]

# --- 3. Interfejs ---
st.title("Zakazivanje termina")

# Admin panel (skriveni expander)
with st.expander("🔑 Admin pristup"):
    if not st.session_state.admin_ulogovan:
        lozinka_input = st.text_input("Lozinka:", type="password")
        if st.button("Prijavi se"):
            conn = sqlite3.connect('termini.db')
            c = conn.cursor()
            c.execute("SELECT lozinka FROM konfiguracija")
            if lozinka_input == c.fetchone()[0]:
                st.session_state.admin_ulogovan = True
                st.rerun()
            else:
                st.error("Pogrešna lozinka!")
            conn.close()
    else:
        st.success("Admin ulogovan")
        if st.button("Odjavi se"):
            st.session_state.admin_ulogovan = False
            st.rerun()
        # Izmena lozinke
        nova_lozinka = st.text_input("Nova lozinka:", type="password")
        if st.button("Sačuvaj lozinku"):
            conn = sqlite3.connect('termini.db')
            c = conn.cursor()
            c.execute("UPDATE konfiguracija SET lozinka = ?", (nova_lozinka,))
            conn.commit()
            conn.close()
            st.success("Izmenjeno!")

# Forma za klijente
if not st.session_state.zakazano:
    with st.form("klijent_forma"):
        ime = st.text_input("Ime i prezime")
        telefon = st.text_input("Telefon")
        usluga = st.selectbox("Usluga", ["Šišanje", "Brijanje", "Stilizovanje"])
        datum = st.date_input("Datum")
        dostupni = get_slobodni_termini(str(datum))
        termin = st.selectbox("Slobodan termin", dostupni)
        
        if st.form_submit_button("Zakaži"):
            if dostupni:
                conn = sqlite3.connect('termini.db')
                c = conn.cursor()
                c.execute("INSERT INTO rezervacije (usluga, datum, vreme, ime, telefon) VALUES (?,?,?,?,?)",
                          (usluga, str(datum), termin, ime, telefon))
                conn.commit()
                conn.close()
                st.session_state.zakazano = True
                st.rerun()
            else:
                st.warning("Nema slobodnih termina za ovaj datum.")
else:
    st.success("Uspešno zakazano!")
    if st.button("Novi termin"):
        st.session_state.zakazano = False
        st.rerun()
