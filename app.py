import streamlit as st
import sqlite3

# --- Inicijalizacija ---
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

# --- Prikaz Logo-a ---
st.image("IMG_20260718_151846.jpg", width=300)

st.title("Zakazivanje termina")

# --- Admin Panel (Kontrolni centar) ---
with st.expander("🔑 Admin pristup"):
    if "admin_ulogovan" not in st.session_state: st.session_state.admin_ulogovan = False
    
    if not st.session_state.admin_ulogovan:
        lozinka_input = st.text_input("Lozinka:", type="password")
        if st.button("Prijavi se"):
            conn = sqlite3.connect('termini.db')
            c = conn.cursor()
            c.execute("SELECT lozinka FROM konfiguracija")
            if lozinka_input == c.fetchone()[0]:
                st.session_state.admin_ulogovan = True
                st.rerun()
            conn.close()
    else:
        st.subheader("Upravljanje terminima")
        conn = sqlite3.connect('termini.db')
        c = conn.cursor()
        c.execute("SELECT * FROM rezervacije")
        termini = c.fetchall()
        
        for t in termini:
            col1, col2 = st.columns([3, 1])
            info = f"{t[2]} | {t[3]} - {t[4] if t[4] else 'SLOBODNO'}"
            col1.write(info)
            if col2.button("Oslobodi", key=f"del_{t[0]}"):
                c.execute("UPDATE rezervacije SET ime=NULL, telefon=NULL, usluga=NULL WHERE id=?", (t[0],))
                conn.commit()
                st.rerun()
        conn.close()

# --- Forma za klijente ---
# (Nastavi ovde sa logikom forme za zakazivanje koju smo ranije definisali)
