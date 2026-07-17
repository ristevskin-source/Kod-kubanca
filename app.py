import streamlit as st
import json
import os

# --- KONFIGURACIJA ---
FAJL_TERMINA = "termini.json"
ADMIN_LOZINKA = "1234" 

# --- FUNKCIJE ---
def ucitaj_termine():
    if os.path.exists(FAJL_TERMINA):
        with open(FAJL_TERMINA, "r") as f:
            try: return json.load(f)
            except: return []
    return []

def sacuvaj_termine(termini):
    with open(FAJL_TERMINA, "w") as f:
        json.dump(termini, f, default=str)

# --- APLIKACIJA ---
st.image("Screenshot_20260717_011214.jpg", width=300)
st.title("Kod Kubanca")

# --- JAVNI DEO ---
with st.form("zakazivanje", clear_on_submit=True):
    usluga = st.selectbox("Usluga", ["Šišanje", "Brada"])
    datum = st.date_input("Datum")
    
    # Logika za prikaz samo slobodnih termina
    svi_termini_dan = ["09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00"]
    termini = ucitaj_termine()
    zauzeti = [t['Vreme'] for t in termini if t['Datum'] == str(datum)]
    slobodni = [t for t in svi_termini_dan if t not in zauzeti]
    
    st.info("Prikaz slobodnih termina za ovaj dan")
    vreme = st.selectbox("Vreme", slobodni if slobodni else ["Nema slobodnih termina"])
    
    ime = st.text_input("Ime")
    telefon = st.text_input("Telefon")
    
    if st.form_submit_button("Zakaži"):
        if slobodni and ime and telefon:
            termini.append({"Ime": ime, "Telefon": telefon, "Datum": str(datum), "Vreme": vreme, "Usluga": usluga})
            sacuvaj_termine(termini)
            st.success("Uspešno zakazano!")
            st.rerun() 
        elif not slobodni:
            st.error("Nažalost, nema slobodnih termina za izabrani dan.")
        else:
            st.error("Molim vas, popunite sva polja.")

# --- ADMIN DEO ---
st.sidebar.title("Admin Pristup")
lozinka = st.sidebar.text_input("Unesite lozinku:", type="password")

if lozinka == ADMIN_LOZINKA:
    st.sidebar.success("Dobrodošao, gazda!")
    st.divider()
    st.header("Admin Kontrolna Tabla")
    
    termini = ucitaj_termine()
    if not termini:
        st.info("Nema zakazanih termina.")
    else:
        meseci = sorted(list(set([t['Datum'][:7] for t in termini])))
        izabrani_mesec = st.selectbox("Izaberi mesec:", meseci)
        filtrirani = [t for t in termini if t['Datum'].startswith(izabrani_mesec)]
        
        st.write(f"### Detaljni termini za {izabrani_mesec}")
        st.dataframe(filtrirani, use_container_width=True)
        
        ukupno = sum([1000 if t['Usluga'] == "Šišanje" else 500 for t in filtrirani if t['Usluga'] != "BLOKIRANO"])
        st.metric("Promet", f"{ukupno} RSD")

        st.subheader("Blokiraj termin (Pauza)")
        with st.form("blokiranje", clear_on_submit=True):
            datum_pauze = st.date_input("Datum pauze")
            vreme_pauze = st.selectbox("Vreme pauze", ["09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00"])
            
            if st.form_submit_button("Potvrdi blokiranje"):
                termini = ucitaj_termine()
                termini.append({"Ime": "PAUZA", "Telefon": "-", "Datum": str(datum_pauze), "Vreme": vreme_pauze, "Usluga": "BLOKIRANO"})
                sacuvaj_termine(termini)
                st.rerun()
elif lozinka != "":
    st.sidebar.error("Pogrešna lozinka!")
