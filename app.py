import streamlit as st
import sqlite3

def init_db():
    conn = sqlite3.connect('termini.db')
    c = conn.cursor()
    
    # 1. Kreiranje tabela
    c.execute('''CREATE TABLE IF NOT EXISTS rezervacije 
                 (id INTEGER PRIMARY KEY, usluga TEXT, datum TEXT, vreme TEXT, 
                  ime TEXT, telefon TEXT)''')
    
    # Dodavanje kolone cena ako ne postoji
    c.execute("PRAGMA table_info(rezervacije)")
    kolone = [info[1] for info in c.fetchall()]
    if 'cena' not in kolone:
        c.execute("ALTER TABLE rezervacije ADD COLUMN cena INTEGER")
    
    c.execute('''CREATE TABLE IF NOT EXISTS cenovnik (usluga TEXT PRIMARY KEY, cena INTEGER)''')
    cene = [('Šišanje', 2000), ('Brijanje', 700), ('Stilizovanje', 1000)]
    c.executemany("INSERT OR IGNORE INTO cenovnik VALUES (?, ?)", cene)
    
    c.execute('''CREATE TABLE IF NOT EXISTS konfiguracija (lozinka TEXT)''')
    c.execute("SELECT * FROM konfiguracija")
    if not c.fetchone():
        c.execute("INSERT INTO konfiguracija (lozinka) VALUES ('1234')")

    # 2. Automatsko popunjavanje ako je tabela rezervacije prazna
    c.execute("SELECT count(*) FROM rezervacije")
    if c.fetchone()[0] == 0:
        termini = [
            (None, '2026-07-20', '09:00', None, None),
            (None, '2026-07-20', '10:00', None, None),
            (None, '2026-07-20', '11:00', None, None)
        ]
        c.executemany("INSERT INTO rezervacije (usluga, datum, vreme, ime, telefon) VALUES (?, ?, ?, ?, ?)", termini)
        
    conn.commit()
    conn.close()

init_db()

st.title("Zakazivanje termina")

# Logo
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("IMG_20260718_151846.jpg", width=300)

with st.expander("🔑 Admin pristup"):
    if "admin_ulogovan" not in st.session_state: st.session_state.admin_ulogovan = False
    if not st.session_state.admin_ulogovan:
        lozinka_input = st.text_input("Lozinka:", type="password")
        if st.button("Prijavi se"):
            conn = sqlite3.connect('termini.db')
            c = conn.cursor()
            c.execute("SELECT lozinka FROM konfiguracija")
            res = c.fetchone()
            if res and lozinka_input == res[0]:
                st.session_state.admin_ulogovan = True
                st.rerun()
            conn.close()
    else:
        st.subheader("📊 Finansijski izveštaj")
        conn = sqlite3.connect('termini.db')
        c = conn.cursor()
        c.execute("SELECT sum(cena) FROM rezervacije WHERE ime IS NOT NULL")
        total = c.fetchone()[0] or 0
        st.write(f"### Ukupan promet: {total} din")
        
        if st.button("🚨 Očisti sve termine"):
            c.execute("UPDATE rezervacije SET ime=NULL, telefon=NULL, usluga=NULL, cena=NULL")
            conn.commit()
            st.success("Termini očišćeni.")
            st.rerun()
        conn.close()

# Forma za klijente
conn = sqlite3.connect('termini.db')
c = conn.cursor()
c.execute("SELECT DISTINCT datum FROM rezervacije")
datumi = [r[0] for r in c.fetchall()]
c.execute("SELECT usluga, cena FROM cenovnik")
cenovnik_dict = dict(c.fetchall())
conn.close()

if datumi:
    with st.form("klijent_forma"):
        ime = st.text_input("Ime i prezime *")
        tel = st.text_input("Telefon *")
        usluga = st.selectbox("Usluga", list(cenovnik_dict.keys()))
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
                cena = cenovnik_dict[usluga]
                conn = sqlite3.connect('termini.db')
                c = conn.cursor()
                c.execute("UPDATE rezervacije SET ime=?, telefon=?, usluga=?, cena=? WHERE id=?", 
                          (ime, tel, usluga, cena, mapa[termin]))
                conn.commit()
                conn.close()
                st.success(f"Uspešno zakazano: {usluga} ({cena} din).")
                st.rerun()
        else:
            st.warning("Nema slobodnih termina za izabrani datum.")
else:
    st.error("Baza je prazna.")
