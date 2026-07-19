import streamlit as st
import sqlite3

# --- 1. Inicijalizacija ---
def init_db():
    conn = sqlite3.connect('termini.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS rezervacije 
                 (id INTEGER PRIMARY KEY, usluga TEXT, datum TEXT, vreme TEXT, 
                  ime TEXT, telefon TEXT)''')
    # Ubaci termine ako tabela nema ništa
    c.execute("SELECT count(*) FROM rezervacije")
    if c.fetchone()[0] == 0:
        dani = ['2026-07-20', '2026-07-21']
        sati = ["09:00", "10:00", "11:00", "12:00"]
        for d in dani:
            for s in sati:
                c.execute("INSERT INTO rezervacije (datum, vreme) VALUES (?, ?)", (d, s))
    
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

# --- 3. Admin Panel ---
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
        # Izmena lozinke
        nova_lozinka = st.text_input("Nova lozinka:", type="password")
        if st.button("Promeni lozinku"):
            conn = sqlite3.connect('termini.db')
            c = conn.cursor()
            c.execute("UPDATE konfiguracija SET lozinka=?", (nova_lozinka,))
            conn.commit()
            conn.close()
            st.success("Lozinka promenjena!")
        
        st.subheader("Svi termini")
        conn = sqlite3.connect('termini.db')
        c = conn.cursor()
        c.execute("SELECT * FROM rezervacije")
        for t in c.fetchall():
            info = f"{t[2]} {t[3]} | {t[4] if t[4] else 'SLOBODNO'} | {t[5] if t[5] else ''}"
            col1, col2 = st.columns([3, 1])
            col1.write(info)
            if t[4]: # Ako je zauzeto, prikaži dugme
                if col2.button("Oslobodi", key=f"del_{t[0]}"):
                    c.execute("UPDATE rezervacije SET ime=NULL, telefon=NULL, usluga=NULL WHERE id=?", (t[0],))
                    conn.commit()
                    st.rerun()
        conn.close()

# --- 4. Forma za klijente ---
conn = sqlite3.connect('termini.db')
c = conn.cursor()
c.execute("SELECT DISTINCT datum FROM rezervacije WHERE ime IS NULL")
dostupni_datumi = [row[0] for row in c.fetchall()]

if dostupni_datumi:
    with st.form("klijent_forma"):
        ime = st.text_input("Ime i prezime")
        telefon = st.text_input("Telefon")
        usluga = st.selectbox("Usluga", ["Šišanje", "Brijanje", "Stilizovanje"])
        datum = st.selectbox("Datum", dostupni_datumi)
        
        c.execute("SELECT id, vreme FROM rezervacije WHERE datum=? AND ime IS NULL", (datum,))
        termini = c.fetchall()
        termin = st.selectbox("Termin", [t[1] for t in termini])
        
        if st.form_submit_button("Zakaži"):
            termin_id = [t[0] for t in termini if t[1] == termin][0]
            c.execute("UPDATE rezervacije SET ime=?, telefon=?, usluga=? WHERE id=?", (ime, telefon, usluga, termin_id))
            conn.commit()
            st.success(f"Uspešno ste zakazali {usluga} za {datum} u {termin}. Vidimo se!")
    conn.close()
else:
    st.warning("Trenutno nema slobodnih termina.")
    conn.close()
