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

# --- 2. Zaglavlje ---
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

# --- 2. Zaglavlje ---
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
        st.subheader("Pregled zakazanih termina")
        conn = sqlite3.connect('termini.db')
        c = conn.cursor()
        c.execute("SELECT * FROM rezervacije")
        zakazani = c.fetchall()
        for t in zakazani:
            info = f"{t[2]} {t[3]} - {t[4] if t[4] else 'SLOBODAN'}"
            col1, col2 = st.columns([3, 1])
            col1.write(info)
            if t[4]:
                if col2.button("Oslobodi", key=f"del_{t[0]}"):
                    c.execute("UPDATE rezervacije SET ime=NULL, telefon=NULL, usluga=NULL WHERE id=?", (t[0],))
                    conn.commit()
                    st.rerun()
        conn.close()

# --- 4. Forma za klijente ---
st.subheader("Rezervacija")
conn = sqlite3.connect('termini.db')
c = conn.cursor()

c.execute("SELECT DISTINCT datum FROM rezervacije")
svi_datumi = [row[0] for row in c.fetchall()]

with st.form("klijent_forma"):
    ime = st.text_input("Ime i prezime *")
    telefon = st.text_input("Telefon *")
    usluga = st.selectbox("Usluga *", ["Šišanje", "Brijanje", "Stilizovanje"])
    datum = st.selectbox("Datum *", svi_datumi)
    
    # DIJAGNOSTIKA: Ovde ispisujemo šta baza vidi za izabrani datum
    c.execute("SELECT id, vreme, ime, telefon FROM rezervacije WHERE datum=?", (datum,))
    podaci = c.fetchall()
    st.write("Debug - Podaci iz baze za izabrani datum:", podaci)
    
    # Filtriramo slobodne (gde su ime i telefon None/prazni)
    slobodni_termini = [t for t in podaci if t[2] is None]
    
    if slobodni_termini:
        termin_map = {t[1]: t[0] for t in slobodni_termini}
        izabrani_termin = st.selectbox("Slobodan termin *", list(termin_map.keys()))
        
        if st.form_submit_button("Zakaži"):
            if ime.strip() and telefon.strip():
                termin_id = termin_map[izabrani_termin]
                c.execute("UPDATE rezervacije SET ime=?, telefon=?, usluga=? WHERE id=?", 
                          (ime, telefon, usluga, termin_id))
                conn.commit()
                st.success("Uspešno zakazano!")
                st.rerun()
            else:
                st.error("Popunite ime i telefon.")
    else:
        st.warning("Nema slobodnih termina za ovaj dan.")
        st.form_submit_button("Zakaži", disabled=True)
        conn.close()

        st.subheader("Pregled zakazanih termina")
        conn = sqlite3.connect('termini.db')
        c = conn.cursor()
        c.execute("SELECT * FROM rezervacije")
        zakazani = c.fetchall()
        for t in zakazani:
            info = f"{t[2]} {t[3]} - {t[4] if t[4] else 'SLOBODAN'}"
            col1, col2 = st.columns([3, 1])
            col1.write(info)
            if t[4]:
                if col2.button("Oslobodi", key=f"del_{t[0]}"):
                    c.execute("UPDATE rezervacije SET ime=NULL, telefon=NULL, usluga=NULL WHERE id=?", (t[0],))
                    conn.commit()
                    st.rerun()
        conn.close()

# --- 4. Forma za klijente ---
st.subheader("Rezervacija")
conn = sqlite3.connect('termini.db')
c = conn.cursor()

c.execute("SELECT DISTINCT datum FROM rezervacije")
svi_datumi = [row[0] for row in c.fetchall()]

with st.form("klijent_forma"):
    ime = st.text_input("Ime i prezime *")
    telefon = st.text_input("Telefon *")
    usluga = st.selectbox("Usluga *", ["Šišanje", "Brijanje", "Stilizovanje"])
    datum = st.selectbox("Datum *", svi_datumi)
    
    # DIJAGNOSTIKA: Ovde ispisujemo šta baza vidi za izabrani datum
    c.execute("SELECT id, vreme, ime, telefon FROM rezervacije WHERE datum=?", (datum,))
    podaci = c.fetchall()
    st.write("Debug - Podaci iz baze za izabrani datum:", podaci)
    
    # Filtriramo slobodne (gde su ime i telefon None/prazni)
    slobodni_termini = [t for t in podaci if t[2] is None]
    
    if slobodni_termini:
        termin_map = {t[1]: t[0] for t in slobodni_termini}
        izabrani_termin = st.selectbox("Slobodan termin *", list(termin_map.keys()))
        
        if st.form_submit_button("Zakaži"):
            if ime.strip() and telefon.strip():
                termin_id = termin_map[izabrani_termin]
                c.execute("UPDATE rezervacije SET ime=?, telefon=?, usluga=? WHERE id=?", 
                          (ime, telefon, usluga, termin_id))
                conn.commit()
                st.success("Uspešno zakazano!")
                st.rerun()
            else:
                st.error("Popunite ime i telefon.")
    else:
        st.warning("Nema slobodnih termina za ovaj dan.")
        st.form_submit_button("Zakaži", disabled=True)
conn.close()
