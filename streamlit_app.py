"""Demo stranica za "Upravljanje sistemom" -- vodjena, staticna prica u 5 ekrana po korisnikovom dokumentu
„ŠTA radi.docx“ (2026-10-12): ŠTA radi? · GDE se koristi? · KAKO se koristi? · KADA se koristi? · ZAŠTO KAIZA?
Bez slika u tekstu, osim seme sistema sa povratnom vezom (KADA) -- korisnik 2026-10-12. Prikazi se preuzimaju
kao KLIKABILNI samostalni HTML fajlovi iz kopije pogona u TEST rezimu (simulirani sat), svaki posebno; u Pretpodeli
se operacije mogu pomerati. Normiranje = kartica Normiranje panela sa istim Python kodom alata u pregledacu
(Pyodide), vidi _izvor_novi_demo/napravi_normiranje_html.py. GDE = telefon poslovodje (stranica /tablet) i Podela
rada krojacnice u jednoj stranici, povezani zajednickim stanjem (_izvor_novi_demo/napravi_gde_html.py). Poslednji ekran je poziv „Test u proizvodnji“ sa kontaktom. Prethodne verzije (lokalno): streamlit_app_5_ekrana.py, streamlit_app_12_koraka.py."""
import os
import streamlit as st

st.set_page_config(page_title='Upravljanje sistemom -- demo', layout='wide')

# Tonirana podloga cele stranice (korisnik 2026-10-26): providan sloj iste pastelne plave preko boje teme -- radi u
# svetloj i tamnoj temi; jacina = poslednji broj (0-1). Okvir teksta (0.28) ostaje vidljiv na podlozi.
TON_PODLOGE = 0.15
st.markdown(f"""
<style>
.stApp, [data-testid="stHeader"] {{
    background-image: linear-gradient(rgba(170, 205, 235, {TON_PODLOGE}), rgba(170, 205, 235, {TON_PODLOGE}));
}}
</style>
""", unsafe_allow_html=True)

# Demo je javan, bez lozinke (korisnik 2026-11-03); ranija provera lozinke (st.secrets) je uklonjena.

NOVI_DIR = os.path.join(os.path.dirname(__file__), 'assets', 'novi')

# Pastelna providna podloga centralnog teksta i dugmad Nazad/Napred (korisnik 2026-10-13); providnost je
# birana tako da tekst ostane citljiv i u svetloj i u tamnoj temi Streamlit-a.
st.markdown("""
<style>
.st-key-tekst_osnova {
    background: rgba(170, 205, 235, 0.28);
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
}
.st-key-nazad button, .st-key-napred button {
    background: rgba(170, 205, 235, 0.35);
    border: 1px solid rgba(120, 160, 200, 0.45);
}
.st-key-nazad button:hover, .st-key-napred button:hover {
    background: rgba(170, 205, 235, 0.55);
}
</style>
""", unsafe_allow_html=True)


def slika(ime: str, opis: str | None = None, kolona=None, sirina: int | None = None) -> None:
    """Slika iz assets/novi; bez sirine -- preko cele kolone."""
    cilj = kolona if kolona is not None else st
    put = os.path.join(NOVI_DIR, ime + '.png')
    if sirina:
        cilj.image(put, caption=opis, width=sirina)
        return
    try:
        cilj.image(put, caption=opis, width='stretch')
    except Exception:
        cilj.image(put, caption=opis, use_container_width=True)


def preuzmi(naziv: str, oznaka: str, kolona=None) -> None:
    """Dugme za preuzimanje fajla iz assets/novi (HTML prikaz ili slika)."""
    cilj = kolona if kolona is not None else st
    mime = 'text/html' if naziv.endswith('.html') else 'image/png'
    with open(os.path.join(NOVI_DIR, naziv), 'rb') as f:
        cilj.download_button(oznaka, f.read(), file_name=naziv, mime=mime, key='dl_' + naziv)


def napomena_klik(kolona=None) -> None:
    cilj = kolona if kolona is not None else st
    cilj.caption('Preuzeti fajl se otvara u pregledaču, bez instalacije. Prikaz je klikabilan: dani i smene, '
                 'a u Pretpodeli „Premesti operaciju“ pa prevucite operaciju mišem.')


def kontakt() -> None:
    st.markdown('    **Dr Milan R. VUKIĆEVIĆ, dipl. inž.**')
    st.markdown('    **060/329-1451**')
    st.markdown('    **milan.vukicevic@kaiza.rs**')


if 'korak' not in st.session_state:
    st.session_state.korak = 0

KORACI = ['ŠTA radi?', 'GDE se koristi?', 'KAKO se koristi?', 'KADA se koristi?', 'ZAŠTO KAIZA?', 'Test u proizvodnji']

st.title('KAIZA')
st.caption('Sistem za podršku odlučivanju u upravljanju proizvodnjom u mikro, malim i srednjim preduzećima')
korak = st.session_state.korak
st.progress(korak / (len(KORACI) - 1))
st.markdown(f'**{korak + 1} od {len(KORACI)} — {KORACI[korak]}**')
st.divider()

# Tekst ide SAMO u levu polovinu strane, levo poravnat (korisnikov zahtev); ispod teksta dugmad za preuzimanje.
tekst_kolona, _prazno = st.columns([1, 1])
tekst = tekst_kolona.container(key='tekst_osnova')

if korak == 0:
    with tekst:
        st.header('ŠTA radi?')
        st.markdown("""
KAIZA, na ovom nivou razvoja, rešava problem razmeštanja procesa u vremenu, odnosno određivanja početka i završetka 
posla pri različitim konceptima proizvodnje. Podržava push i pull koncept proizvodnje kod izrade osnovnog i dopunskog 
plana, kao i njihovu kombinaciju u istom planu. Vodi računa o tehnologiji, konsolidaciji pripremno-završnog vremena 
kod grupne tehnologije, optimizaciji unutrašnjeg transporta, kao i o organizaciji višemašinskog rada. Da bi većinu ovih
ciljeva realizovao, KAIZA ima ugrađenu funkciju pomeranja operacija u vremenu u okviru radnog mesta. Takođe,
uključena je i funkcija propagacije operacija zbog tehnoloških veza ili zato što operacije slede iza pomerenih operacija.
""")
    preuzmi('pretpodela_rada.html', '↗ Pretpodela rada (subota 10.10. S1)')
    napomena_klik()

elif korak == 1:
    with tekst:
        st.header('GDE se koristi?')
        st.markdown("""
KAIZA u preduzeću povezuje mesto izvršenja procesa, pogon, i mesto donošenja odluka, kancelariju. Protok
informacija je direktan, bez posrednika i šuma na vezama. Nalozi za rad idu od menadžera prema
poslovođi/radniku u pogonu, a on pomoću tableta/telefona šalje informaciju o napretku procesa rada ili
poremećajima u procesu. Da bi u nekom narednom periodu moglo da se pređe na predikciju poremećaja, predviđeno je
evidentiranje konteksta poremećaja. Znači, ne samo trajanja, nego i uzroka i posledica poremećaja i preduzetih
mera. To omogućava praćenje kretanja pokazatelja Ukupne efikasnosti opreme — OEE (Overall Equipment
Effectiveness).
""")
    preuzmi('pogon_i_kancelarija.html', '↗ Telefon poslovođe i Podela rada na radna mesta')
    st.caption('Otvara se u pregledaču, bez instalacije: levo telefon poslovođe, desno Podela rada menadžera, '
               'povezani kao u pogonu — T1 na Podeli se odmah vidi na telefonu, a T2–T5 i poremećaji sa telefona '
               'na Podeli.')

elif korak == 2:
    with tekst:
        st.header('KAKO se koristi?')
        st.markdown("""
KAIZA je vizuelna interpretacija razmeštaja procesa u vremenu u jednom pogonu. Za razliku od drugih aplikacija
koje su zasnovane na dokumentima, KAIZA kombinuje dominantan vizuelni prikaz i neophodnu dokumentaciju. Prvo,
daje Grubi plan koji omogućava, pri ugovaranju posla, brzu proveru raspoloživih kapaciteta za realizaciju u
roku. Fini plan, koji detaljno definiše razmeštaj svih operacija plana, osnovnog i dopunskog, u planskom
periodu. Pretpodelu rada po radnim danama i smenama sa opcijom pomeranja operacija i praćenja propagacije zbog
nastalih pomeranja operacija. Grubi plan, Fini plan i Pretpodela rada su statički prikaz procesa. Podela rada na
radna mesta, i sa njom povezan tablet poslovođe/radnika, čine dinamički prikaz procesa. Oni registruju početak i
završetak svih događaja i poremećaja i na osnovu toga stvarni početak i kraj rada na operacijama i proizvodu.
""")
    k1, k2, k3, k4, _ = st.columns([1, 1, 1, 1.4, 1.6])
    preuzmi('grubi_plan.html', '↗ Grubi plan', k1)
    preuzmi('fini_plan.html', '↗ Fini plan', k2)
    preuzmi('pretpodela_rada.html', '↗ Pretpodela rada', k3)
    preuzmi('podela_rada_rm.html', '↗ Podela rada na radna mesta', k4)
    napomena_klik()

elif korak == 3:
    with tekst:
        st.header('KADA se koristi?')
        st.markdown("""
KAIZA je neophodan kada dinamičnost sistema postane ograničavajući faktor daljeg razvoja preduzeća. Ne postoje
istraživanja tačke preloma, ali neka iskustva ljudi u proizvodnji kažu da se to kreće 10+ zaposlenih i da zavisi
od vrste proizvodnje. Za sisteme sa visokom dinamičnošću procesa od presudne važnosti je to da KAIZA radi u
realnom vremenu. Tako on menadžeru omogućava da na bazi izlaznih signala proizvodnje, donosi odgovarajuće odluke
kojima se obezbeđuje željeno stanje sistema.
""")
    slika('kada_povratna_veza', 'Sistem sa povratnom vezom')

elif korak == 4:
    with tekst:
        st.header('ZAŠTO KAIZA?')
        st.markdown("""
Zato što složen posao planiranja i upravljanja sistemom čini vizuelnim i lako razumljivim. Zato što
kombinujući metode organizacije i upravljanja sistemima sa matematičkim metodama, obezbeđuje visoku tačnost
dobijenih izlaznih informacija i odluka u skladu sa njima u meri koliko su tačni ulazni podaci. Najranjiviji deo
upravljanja sistemom je vreme izrade tehnološke operacije. Danas, kada je prekidna proizvodnja preovladavajući
sistem proizvodnje, dominantan je stav da je to nepotreban podatak. Logika kaže da to znači da ni upravljanje
sistemom nije potrebno i da vreme kao resurs nema vrednost u kalkulacijama. Ali, realnost pokazuje drugačiju
situaciju. Nemar prema tom resursu rezultirao je, prema istraživanjima, sa 15%-20% korišćenja kapaciteta i
enormno visokim troškovima proizvodnje. KAIZA taj problem rešava kombinacijom standardnih zahvata i MTM-2
metode. Moguć je izbor između dve opcije. Simulaciona metoda, brža i manje tačna i izvorna, sa pojedinačnim
definisanjem kriterijuma kod svakog pokreta. Sporija, ali i tačnija.
""")
    preuzmi('normiranje.html', '↗ Normiranje')
    st.caption('Isti ekran i isti proračun kao u sistemu: izvorni postupak (MTM-2), simulacija i dokument normiranih '
               'operacija. Pri otvaranju je potrebna internet veza; prvo učitavanje traje 10–30 sekundi. Upisi '
               'ostaju dok je stranica otvorena.')

else:
    with tekst:
        st.header('Test u proizvodnji')
        st.markdown("""
Tražimo **5 pogona** za test u proizvodnji, **do 45 dana**. Potrebni su
računar i telefon (ili tablet) poslovođe — bez dodatne opreme i bez povezivanja
sa postojećim sistemima. Zajedno proveravamo sistem u stvarnim uslovima Vašeg
pogona.

**Zainteresovani ste?** Javite se za kratak razgovor — objasniću Vam
metodologiju rada i kako izgleda uvođenje u Vaš pogon.
""")
        kontakt()

st.divider()
kol1, kol2, kol3 = st.columns([1, 3, 1])
with kol1:
    if st.session_state.korak > 0:
        if st.button('← Nazad', key='nazad'):
            st.session_state.korak -= 1
            st.rerun()
with kol3:
    if st.session_state.korak < len(KORACI) - 1:
        if st.button('Napred →', key='napred'):
            st.session_state.korak += 1
            st.rerun()
