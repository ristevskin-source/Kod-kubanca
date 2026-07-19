import streamlit as st
import sqlite3
from datetime import datetime, timedelta

# ---------- KONFIGURACIJA ----------
RADNO_VREME = [(9,0), (20,0)]  # od 09:00 do 17:00
INTERVAL_MIN = 60              # na svakih sat vremena
BROJ_DANA = 7                  # prikazujemo 7 dana

# ---------- INICIJALIZACIJA BAZE ----------
def init_db():
    conn = sqlite3.connect('termini.db')
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS rezervacije 
                 (id INTEGER PRIMARY KEY, usluga TEXT, datum TEXT, vreme TEXT, 
                  ime TEXT, telefon TEXT, cena INTEGER)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS cenovnik (usluga TEXT PRIMARY KEY, cena INTEGER)''')
    default_cene = [('Šišanje', 2000), ('Brijanje', 700), ('Stilizovanje', 1000)]
    c.executemany("INSERT OR IGNORE INTO cenovnik VALUES (?, ?)", default_cene)
    
    c.execute('''CREATE TABLE IF NOT EXISTS konfiguracija (lozinka TEXT)''')
    c.execute("SELECT * FROM konfiguracija")
    if not c.fetchone():
        c.execute("INSERT INTO konfiguracija (lozinka) VALUES ('1234')")
    
    conn.commit()
    conn.close()

init_db()

# ---------- POMOĆNE FUNKCIJE ----------
def generisi_datume():
    """Vraća listu od 7 datuma (YYYY-MM-DD) sa pomeranjem u 20h"""
    now = datetime.now()
    # Ako je 20h ili kasnije, današnji dan preskačemo
    if now.hour >= 20:
        start = now + timedelta(days=1)
    else:
        start = now
    
    start = start.replace(hour=0, minute=0, second=0, microsecond=0)
    datumi = []
    for i in range(BROJ_DANA):
        dan = start + timedelta(days=i)
        datumi.append(dan.strftime("%Y-%m-%d"))
    return datumi

def generisi_termine_za_dan(datum_str):
    """Kreira termine za dati dan (od RADNO_VREME do kraja) ako ne postoje"""
    conn = sqlite3.connect('termini.db')
    c = conn.cursor()
    
    # Proveri da li već postoje termini za taj dan
    c.execute("SELECT count(*) FROM rezervacije WHERE datum=?", (datum_str,))
    if c.fetchone()[0] > 0:
        conn.close()
        return  # već postoje
    
    # Generiši termine
    sat_start, min_start = RADNO_VREME[0]
    sat_kraj, min_kraj = RADNO_VREME[1]
    trenutno = datetime.strptime(datum_str, "%Y-%m-%d").replace(hour=sat_start, minute=min_start)
    kraj = datetime.strptime(datum_str, "%Y-%m-%d").replace(hour=sat_kraj, minute=min_kraj)
    
    termini = []
    while trenutno < kraj:
        vreme = trenutno.strftime("%H:%M")
        termini.append((None, datum_str, vreme, None, None, None))  # usluga, datum, vreme, ime, telefon, cena
        trenutno += timedelta(minutes=INTERVAL_MIN)
    
    if termini:
        c.executemany("INSERT INTO rezervacije (usluga, datum, vreme, ime, telefon, cena) VALUES (?, ?, ?, ?, ?, ?)", termini)
        conn.commit()
    conn.close()

def osvezi_termine():
    """Generiši termine za sve datume u kliznom prozoru"""
    datumi = generisi_datume()
    for d in datumi:
        generisi_termine_za_dan(d)

osvezi_termine()  # Pokreni pri svakom učitavanju

# ---------- UI ----------
st.title("💈 Zakazivanje termina")

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("IMG_20260718_151846.jpg", width=300)

# Admin panel
with st.expander("🔑 Admin pristup"):
    if "admin_ulogovan" not in st.session_state:
        st.session_state.admin_ulogovan = False
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

# ---------- FORMA ZA KLIJENTE ----------
conn = sqlite3.connect('termini.db')
c = conn.cursor()

# Dinamički datumi (7 dana)
datumi = generisi_datume()

# Cenovnik
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
                st.success(f"✅ Uspešno zakazano: {usluga} ({cena} din).")
                st.rerun()
        else:
            st.warning("⏳ Nema slobodnih termina za izabrani datum.")
else:
    st.error("❌ Baza je prazna.")
