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
svi_termini_dan = ["09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00"]
with st.form("zakazivanje", clear_on_submit=True):
    usluga = st.selectbox("Usluga", ["Šišanje", "Brada"])
    datum = st.date_input("Datum")
    
    termini = ucitaj_termine()
    zauzeti = []
    
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
svi_termini_dan = ["09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00"]
with st.form("zakazivanje", clear_on_submit=True):
    usluga = st.selectbox("Usluga", ["Šišanje", "Brada"])
    datum = st.date_input("Datum")
    
    termini = ucitaj_termine()
    zauzeti = []
    for t in termini:
        if t['Datum'] == str(datum):
            if t.get('Usluga') == "BLOKIRANO":
                # Ako je pauza period, dodaj sve sate iz opsega u zauzete
                start = svi_termini_dan.index(t['Od'])
                end = svi_termini_dan.index(t['Do'])
                zauzeti.extend(svi_termini_dan[start:end+1])
            else:
                zauzeti.append(t['Vreme'])
    
    slobodni = [t for t in svi_termini_dan if t not in zauzeti]
    
    st.info("Prikaz slobodnih termina za ovaj dan")
    vreme = st.selectbox("Vreme", slobodni if slobodni else ["Nema slobodnih termina"])
    
    ime = st.text_input("Ime")
    telefon = st.text_input("Telefon")
    
    if st.form_submit_button("Zakaži"):
        if slobodni and ime and telefon:
            termini.append({"Ime": ime, "Telefon": telefon, "Datum": str(datum), "Vreme": vreme, "Usluga": usluga})
            sacuvaj_termine(termini)
            st.success(f"Uspešno ste zakazali {usluga} za {datum} u {vreme}. Hvala!")
            st.balloons()
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
    if termini:
        meseci = sorted(list(set([t['Datum'][:7] for t in termini])))
        izabrani_mesec = st.selectbox("Izaberi mesec:", meseci)
        filtrirani = [t for t in termini if t['Datum'].startswith(izabrani_mesec)]
        st.dataframe(filtrirani, use_container_width=True)

    st.subheader("Blokiraj period (Pauza)")
    with st.form("blokiranje_perioda", clear_on_submit=True):
        datum_pauze = st.date_input("Datum pauze")
        col1, col2 = st.columns(2)
        od_vreme = col1.selectbox("Od:", svi_termini_dan)
        do_vreme = col2.selectbox("Do:", svi_termini_dan)
        
        if st.form_submit_button("Potvrdi blokiranje"):
            if od_vreme <= do_vreme:
                termini = ucitaj_termine()
                termini.append({"Ime": "PAUZA", "Telefon": "-", "Datum": str(datum_pauze), "Od": od_vreme, "Do": do_vreme, "Usluga": "BLOKIRANO"})
                sacuvaj_termine(termini)
                st.success("Period blokiran!")
                st.rerun()
            else:
                st.error("Pogrešan opseg!")
elif lozinka != "":
    st.sidebar.error("Pogrešna lozinka!")
      
            else:
                zauzeti.append(t['Vreme'])
    
    slobodni = [t for t in svi_termini_dan if t not in zauzeti]
    
    st.info("Prikaz slobodnih termina za ovaj dan")
    vreme = st.selectbox("Vreme", slobodni if slobodni else ["Nema slobodnih termina"])
    
    ime = st.text_input("Ime")
    telefon = st.text_input("Telefon")
    
    if st.form_submit_button("Zakaži"):
        if slobodni and ime and telefon:
            termini.append({"Ime": ime, "Telefon": telefon, "Datum": str(datum), "Vreme": vreme, "Usluga": usluga})
            sacuvaj_termine(termini)
            st.success(f"Uspešno ste zakazali {usluga} za {datum} u {vreme}. Hvala!")
            st.balloons()
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
    if termini:
        meseci = sorted(list(set([t['Datum'][:7] for t in termini])))
        izabrani_mesec = st.selectbox("Izaberi mesec:", meseci)
        filtrirani = [t for t in termini if t['Datum'].startswith(izabrani_mesec)]
        st.dataframe(filtrirani, use_container_width=True)

    st.subheader("Blokiraj period (Pauza)")
    with st.form("blokiranje_perioda", clear_on_submit=True):
        datum_pauze = st.date_input("Datum pauze")
        col1, col2 = st.columns(2)
        od_vreme = col1.selectbox("Od:", svi_termini_dan)
        do_vreme = col2.selectbox("Do:", svi_termini_dan)
        
        if st.form_submit_button("Potvrdi blokiranje"):
            if od_vreme <= do_vreme:
                termini = ucitaj_termine()
                termini.append({"Ime": "PAUZA", "Telefon": "-", "Datum": str(datum_pauze), "Od": od_vreme, "Do": do_vreme, "Usluga": "BLOKIRANO"})
                sacuvaj_termine(termini)
                st.success("Period blokiran!")
                st.rerun()
            else:
                st.error("Pogrešan opseg!")
elif lozinka != "":
    st.sidebar.error("Pogrešna lozinka!")
