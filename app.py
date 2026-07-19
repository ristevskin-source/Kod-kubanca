import streamlit as st
import sqlite3

def init_db():
    conn = sqlite3.connect('termini.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS rezervacije 
                 (id INTEGER PRIMARY KEY, usluga TEXT, datum TEXT, vreme TEXT, 
                  ime TEXT, telefon TEXT)''')
    c.execute("SELECT count(*) FROM rezervacije")
    if c.fetchone()[0] == 0:
        dani = ['2026-07-20', '2026-07-21']
        sati = ["09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00"]
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

st.title("Zakazivanje termina")
st.image("IMG_20260718_151846.jpg", width=300)
with st.expander("🔑 Admin pristup"):
    if "admin_ulogovan" not in st.session_state: st.session_state.admin_ulogovan = False
    if not st.session_state.admin_ulogovan:
        lozinka_input = st.text_input("Lozinka:", type="password", key="admin_pass")
        if st.button("Prijavi se", key="login_btn"):
            conn = sqlite3.connect('termini.db')
            c = conn.cursor()
            c.execute("SELECT lozinka FROM konfiguracija")
            if lozinka_input == c.fetchone()[0]:
                st.session_state.admin_ulogovan = True
                st.rerun()
            conn.close()
    else:
        # Dugme za čišćenje baze
        if st.button("🚨 Očisti sve termine", key="reset_db"):
            conn = sqlite3.connect('termini.db')
            c = conn.cursor()
            c.execute("UPDATE rezervacije SET ime=NULL, telefon=NULL, usluga=NULL")
            conn.commit()
            conn.close()
            st.success("Svi termini su sada slobodni!")
            st.rerun()

        st.subheader("Pregled zakazanih")
        conn = sqlite3.connect('termini.db')
        c = conn.cursor()
        c.execute("SELECT * FROM rezervacije WHERE ime IS NOT NULL")
        for t in c.fetchall():
            col1, col2 = st.columns([3, 1])
            col1.write(f"{t[2]} {t[3]} - {t[4]} ({t[5]})")
            if col2.button("Oslobodi", key=f"del_{t[0]}"):
                c.execute("UPDATE rezervacije SET ime=NULL, telefon=NULL, usluga=NULL WHERE id=?", (t[0],))
                conn.commit()
                st.rerun()
        conn.close()

# Forma za klijente
st.subheader("Rezervacija")
conn = sqlite3.connect('termini.db')
c = conn.cursor()
c.execute("SELECT DISTINCT datum FROM rezervacije")
datumi = [r[0] for r in c.fetchall()]
conn.close()

with st.form("klijent_forma"):
    ime = st.text_input("Ime i prezime *")
    tel = st.text_input("Telefon *")
    usluga = st.selectbox("Usluga", ["Šišanje", "Brijanje", "Stilizovanje"])
    datum = st.selectbox("Datum", datumi)
    
    conn = sqlite3.connect('termini.db')
    c = conn.cursor()
    c.execute("SELECT id, vreme FROM rezervacije WHERE datum=? AND ime IS NULL", (datum,))
    slobodni = c.fetchall()
    conn.close()
    
    if slobodni:
        mapa = {t[1]: t[0] for t in slobodni}
        termin = st.selectbox("Slobodan termin", list(mapa.keys()))
        if st.form_submit_button("Zakaži"):
            conn = sqlite3.connect('termini.db')
            c = conn.cursor()
            c.execute("UPDATE rezervacije SET ime=?, telefon=?, usluga=? WHERE id=?", (ime, tel, usluga, mapa[termin]))
            conn.commit()
            conn.close()
            st.success("Zakazano!")
            st.rerun()
    else:
        st.warning("Nema slobodnih termina.")
