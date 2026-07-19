import streamlit as st
import sqlite3

# --- 1. Inicijalizacija baze ---
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

# --- 2. Admin Panel ---
with st.expander("🔑 Admin pristup"):
    if "admin_ulogovan" not in st.session_state: st.session_state.admin_ulogovan = False
    
    if not st.session_state.admin_ulogovan:
        # Dodat jedinstveni key
        lozinka_input = st.text_input("Lozinka:", type="password", key="admin_pass_login")
        if st.button("Prijavi se", key="login_btn"):
            conn = sqlite3.connect('termini.db')
            c = conn.cursor()
            c.execute("SELECT lozinka FROM konfiguracija")
            pw = c.fetchone()[0]
            conn.close()
            if lozinka_input == pw:
                st.session_state.admin_ulogovan = True
                st.rerun()
    else:
        st.subheader("Pregled zakazanih termina")
        conn = sqlite3.connect('termini.db')
        c = conn.cursor()
        c.execute("SELECT * FROM rezervacije")
        for t in c.fetchall():
            info = f"{t[2]} {t[3]} - {t[4] if t[4] else 'SLOBODAN'}"
            col1, col2 = st.columns([3, 1])
            col1.write(info)
            if t[4]:
                # Jedinstven ključ za svako dugme
                if col2.button("Oslobodi", key=f"del_{t[0]}"):
                    c.execute("UPDATE rezervacije SET ime=NULL, telefon=NULL, usluga=NULL WHERE id=?", (t[0],))
                    conn.commit()
                    st.rerun()
        conn.close()

# --- 3. Forma za klijente ---
st.subheader("Rezervacija")
conn = sqlite3.connect('termini.db')
c = conn.cursor()
c.execute("SELECT DISTINCT datum FROM rezervacije")
svi_datumi = [row[0] for row in c.fetchall()]
conn.close()

with st.form("klijent_forma"):
    # Različiti key-evi za polja forme
    ime = st.text_input("Ime i prezime *", key="client_name")
    telefon = st.text_input("Telefon *", key="client_phone")
    usluga = st.selectbox("Usluga *", ["Šišanje", "Brijanje", "Stilizovanje"], key="service_select")
    datum = st.selectbox("Datum *", svi_datumi, key="date_select")
    
    conn = sqlite3.connect('termini.db')
    c = conn.cursor()
    c.execute("SELECT id, vreme FROM rezervacije WHERE datum=? AND ime IS NULL", (datum,))
    slobodni_termini = c.fetchall()
    conn.close()
    
    if slobodni_termini:
        termin_map = {t[1]: t[0] for t in slobodni_termini}
        izabrani_termin = st.selectbox("Slobodan termin *", list(termin_map.keys()), key="time_select")
        
        if st.form_submit_button("Zakaži"):
            if ime and telefon:
                conn = sqlite3.connect('termini.db')
                c = conn.cursor()
                c.execute("UPDATE rezervacije SET ime=?, telefon=?, usluga=? WHERE id=?", 
                          (ime, telefon, usluga, termin_map[izabrani_termin]))
                conn.commit()
                conn.close()
                st.success("Uspešno zakazano!")
                st.rerun()
    else:
        st.warning("Nema slobodnih termina za ovaj dan.")
