import streamlit as st
import sqlite3

# --- 1. Inicijalizacija ---
def init_db():
    conn = sqlite3.connect('termini.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS rezervacije 
                 (id INTEGER PRIMARY KEY, usluga TEXT, datum TEXT, vreme TEXT, 
                  ime TEXT, telefon TEXT)''')
    # Popunjavanje termina ako su prazni (osnova)
    c.execute("SELECT count(*) FROM rezervacije")
    if c.fetchone()[0] == 0:
        for sat in ["09:00", "10:00", "11:00", "12:00"]:
            c.execute("INSERT INTO rezervacije (datum, vreme) VALUES (?, ?)", ('2026-07-20', sat))
    c.execute('''CREATE TABLE IF NOT EXISTS konfiguracija (lozinka TEXT)''')
    c.execute("SELECT * FROM konfiguracija")
    if not c.fetchone():
        c.execute("INSERT INTO konfiguracija (lozinka) VALUES ('1234')")
    conn.commit()
    conn.close()

init_db()

# --- 2. Prikaz ---
st.image("IMG_20260718_151846.jpg", width=300)
st.title("Zakazivanje termina")

# --- Admin Panel (Sakriven) ---
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
        for t in c.fetchall():
            col1, col2 = st.columns([3, 1])
            col1.write(f"{t[3]} - {t[4] if t[4] else 'SLOBODNO'}")
            if t[4]: 
                if col2.button("Oslobodi", key=f"del_{t[0]}"):
                    c.execute("UPDATE rezervacije SET ime=NULL, telefon=NULL, usluga=NULL WHERE id=?", (t[0],))
                    conn.commit()
                    st.rerun()
        conn.close()

# --- 3. Forma za klijente ---
conn = sqlite3.connect('termini.db')
c = conn.cursor()
c.execute("SELECT id, vreme FROM rezervacije WHERE ime IS NULL")
slobodni = c.fetchall()
conn.close()

if slobodni:
    with st.form("klijent_forma"):
        ime = st.text_input("Ime i prezime")
        telefon = st.text_input("Telefon")
        usluga = st.selectbox("Usluga", ["Šišanje", "Brijanje"])
        izabrani_termin = st.selectbox("Slobodan termin", [t[1] for t in slobodni])
        
        if st.form_submit_button("Zakaži"):
            if ime and telefon:
                termin_id = [t[0] for t in slobodni if t[1] == izabrani_termin][0]
                conn = sqlite3.connect('termini.db')
                c = conn.cursor()
                c.execute("UPDATE rezervacije SET ime=?, telefon=?, usluga=? WHERE id=?", 
                          (ime, telefon, usluga, termin_id))
                conn.commit()
                conn.close()
                st.success("Uspešno zakazano!")
                st.rerun()
            else:
                st.error("Popunite sva polja!")
else:
    st.warning("Nema slobodnih termina.")
