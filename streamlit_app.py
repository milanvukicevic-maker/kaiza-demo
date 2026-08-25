"""Demo stranica za "Upravljanje sistemom" -- vodjena, POTPUNO STATICNA prica
(bez zive interakcije/rekalkulacije, korisnikova eksplicitna odluka: klikanje
bi moglo da oteze i izazove kontra-efekat). Prikazuje unapred generisane,
STVARNE grafikone (folder assets/) -- ne dira zivi test projekat."""
import os
import streamlit as st

st.set_page_config(page_title='Upravljanje sistemom -- demo', layout='wide')

# ── Lozinka (2026-08-25, za javno postavljanje na kaiza.rs/Proizvodnja) ─────
# st.secrets je jedini bezbedan nacin -- GitHub repo za Streamlit Cloud mora
# biti PUBLIC (na besplatnom planu), pa lozinka NIKAD ne sme biti u samom
# kodu. Lokalno (bez podesenih secrets) podrazumevana lozinka je 'kaiza-demo'
# -- SAMO za razvoj, PROMENITI/PODESITI pravu lozinku kroz Streamlit Cloud
# dashboard (Settings -> Secrets) pre javnog postavljanja.
def _proveri_lozinku():
    ocekivana = st.secrets.get('lozinka', 'kaiza-demo')

    def uneto():
        st.session_state['lozinka_ok'] = (st.session_state.get('lozinka_unos') == ocekivana)

    if st.session_state.get('lozinka_ok'):
        return True
    st.title('KAIZA -- demo')
    st.text_input('Lozinka', type='password', on_change=uneto, key='lozinka_unos')
    if 'lozinka_ok' in st.session_state and not st.session_state['lozinka_ok']:
        st.error('Pogrešna lozinka.')
    return False


if not _proveri_lozinku():
    st.stop()

# Ugradjen prikaz (st.components.v1.html u iframe-u) je NAPUSTEN -- gust
# graficki prikaz zbijen u uzak, fiksne visine okvir na strani je delovao
# asimetricno/nejasno i navodio na uzaludno pokusano zumiranje (korisnikov
# nalaz). Streamlit static file serving (enableStaticServing) TAKODJE nije
# resenje -- servira .html kao text/plain (bezbednosna mera), browser
# prikazuje sirov izvorni kod umesto da renderuje stranicu. data:text/html
# link JOS JEDNOM nije resenje -- moderni browseri (Chrome/Firefox)
# BLOKIRAJU navigaciju ka data: URL-u kad se otvara u NOVOJ kartici
# (bezbednosna mera protiv phishing-a), bez obzira na sadrzaj. Lokalni
# python -m http.server (127.0.0.1) je RADIO za razvoj na ovom racunaru, ali
# NE MOZE da radi kad se demo postavi na kaiza.rs -- posetiocev "127.0.0.1"
# je NJEGOV racunar, ne server (korisnikov nalaz, 2026-08-25). RESENJE za
# javno postavljanje: st.download_button servira bajtove fajla direktno,
# bez ikakvog servera/porta -- posetilac preuzme samostalan .html i otvori
# ga lokalno (Plotly se ucitava sa javnog CDN-a, ne treba mu nas server).

ASSETS_DIR = os.path.join(os.path.dirname(__file__), 'assets')


def link_otvori(naziv, oznaka):
    with open(os.path.join(ASSETS_DIR, naziv), 'rb') as f:
        st.download_button(oznaka, f.read(), file_name=naziv, mime='text/html')


def dokument(naziv, oznaka, recenica, kolona=None):
    """Jedan dokument = jedna rečenica objašnjenja + dugme za preuzimanje."""
    cilj = kolona if kolona is not None else st
    cilj.markdown(f'<span style="font-size:14px">{recenica}</span>', unsafe_allow_html=True)
    with open(os.path.join(ASSETS_DIR, naziv), 'rb') as f:
        cilj.download_button(oznaka, f.read(), file_name=naziv, mime='text/html')


def red_dokumenata(*dokumenti):
    """Po 2 dokumenta u redu (kolona levo/desno)."""
    for i in range(0, len(dokumenti), 2):
        par = dokumenti[i:i + 2]
        kolone = st.columns(2)
        for (naziv, oznaka, recenica), kol in zip(par, kolone):
            dokument(naziv, oznaka, recenica, kol)


def dugme_uskoro(oznaka, kolona=None):
    cilj = kolona if kolona is not None else st
    cilj.button(oznaka, disabled=True, help='Dostupno naknadno.')


if 'korak' not in st.session_state:
    st.session_state.korak = 0

KORACI = [
    'Dobrodošlica',
    'Izrada dokumentacije',
    'Normiranje rada',
    'Upravljanje sistemom',
    'a.1) Grubo planiranje — standardna proizvodnja',
    'a.2) Grubo planiranje — nova narudžbina',
    'b) Fino planiranje',
    'c) Pretpodela rada',
    'd) Podela rada na RM',
    'Sledeći korak',
]

st.title('KAIZA')
st.caption('Alat za planiranje i upravljanje proizvodnjom u mikro, malim i srednjim preduzecima')
st.progress(st.session_state.korak / (len(KORACI) - 1))
st.markdown(f'**Korak {st.session_state.korak + 1} od {len(KORACI)} — {KORACI[st.session_state.korak]}**')
st.divider()

korak = st.session_state.korak

# Tekst ide SAMO u levu polovinu strane, levo poravnat (korisnikov zahtev) --
# umesto da se markdown/tabele/dugmad razvlace na punu sirinu "wide" layouta.
# IZUZETAK: korak 1 (mreza dokumenata, 2 po redu) treba visinu bez skrolovanja
# i pun tekst u jednom redu po dugmetu -- polovina strane je preuska za to.
if korak == 1:
    sadrzaj = st.container()
else:
    sadrzaj, _prazno = st.columns([1, 1])
with sadrzaj:
    if korak == 0:
        st.header('Dobrodošli')
        st.markdown("""
Ovo je kratak, vođen pregled onoga što KAIZA radi — na jednom hipotetičkom
primeru kako bi zadovoljio različite tehnologije. Ništa ovde nije potrebno
da podešavate — samo pratite priču.
""")
        st.info('Namenjeno vlasnicima i menadžerima koji razmatraju uvođenje upravljanja proizvodnjom u '
                'svakodnevni rad, kako bi kroz sinergetski efekat unapredili poslovanje.')

        st.subheader('Alat ima 4 grane')
        st.markdown("""
1) Izrada dokumentacije
2) Normiranje rada
3) Upravljanje sistemom
4) Kreiraj odeljenje
""")

    elif korak == 1:
        st.header('1) Izrada dokumentacije')
        st.markdown('Sve počinje od dokumenata koje je potrebno pripremiti:')
        red_dokumenata(
            ('pregled_narudzbina.html', '↗ Pregled narudžbina (Period 1)',
             'Šta je ugovoreno — proizvod, količina i koje odeljenje obrađuje koji detalj.'),
            ('tehnoloski_postupci.html', '↗ Tehnološki postupci (Hoklica/HOK.d1.KRO)',
             'Kako se izrađuje — operacije i vremena za jedan detalj, koje tehnolog ručno unosi.'),
            ('tehnoloska_sastavnica.html', '↗ Tehnološka sastavnica (Hoklica)',
             'Redosled spajanja detalja u proizvod, sumarni podaci detalja po odeljenjima — direktno hrani Grubi plan, ne unosi se ručno.'),
            ('atributi_sistema.html', '↗ Atributi sistema',
             'Trajne, sistemske postavke (push/pull) koje važe za sva odeljenja.'),
        )

        st.markdown("""
Iz gotovog plana, alat zatim SAM generiše dokumentaciju koja prati
proizvodnju na terenu — bez dodatnog ručnog rada menadžera ili tehnologa.
Menadžeru se tako štede sati ručnog popunjavanja — dokumenti se generišu
automatski, direktno iz već izrađenog plana (primer za Hoklica/HOK.d1.KRO):
""")
        red_dokumenata(
            ('terminska_karta.html', '↗ Terminska karta',
             'Planirani i stvarni početak/kraj svake operacije, za praćenje na terenu.'),
            ('propratna_karta.html', '↗ Propratna karta',
             'Prati proizvod kroz operacije, sa planiranom i dobijenom količinom.'),
            ('pogonski_radni_nalog.html', '↗ Pogonski radni nalog',
             'Radni nalog za pogon — operacije, vremena i planirana količina.'),
            ('kanban.html', '↗ Kanban ',
             'Signalna kartica za početak jedne operacije, za signalizaciju između odeljenja.'),
        )

        st.markdown("""
Radnik na svakom radnom mestu ima svoju Radnu kartu — njom prijavljuje stvarni
tok rada i eventualne poremećaje. Terminska karta iznad upravo iz nje povlači
STVARNA vremena (planirano se upoređuje sa onim što je radnik zaista prijavio):
""")
        st.markdown('Radnikov pregled zakazanih operacija na jednom radnom mestu, sa prijavom toka rada.')
        link_otvori('radna_karta.html', '↗ Radna karta (RM1)')
        st.caption('U ovom prikazu dugmad za unos su neaktivna — u pravom alatu radnik njima prijavljuje stvarni tok rada.')

        st.markdown("""
Sirovi podaci iz proizvodnje o frekvenciji i trajanju poremećaja/prekida
prema kategoriji služe za izračunavanje ukupne efektivnosti opreme - OEE
(Overall Equipment Effectiveness):
""")
        dokument('oee.html', '↗ OEE — praćenje poremećaja',
                 'Stvarna baza poremećaja razvrstana po OEE komponenti (dostupnost/performanse/kvalitet).')

    elif korak == 2:
        st.header('2) Normiranje rada')
        st.markdown("""
Upravljanje sistemom podrazumeva razmeštanje procesa u prostoru i vremenu.
KAIZA rešava problem razmeštanja u vremenu. Da bi ispunio taj cilj,
neophodna mu je vremenska dimenzija procesa. Potrebni su mu normativi rada.
Dolaženje do tih podatka je složen i dugotrajan proces koji se zbog toga
najčešće i preskače. Da bi se premostio taj jaz, za te potrebe razvijena je
metoda koja kombinuje standardne zahvate i MTM-2 metodu.
""")

        st.subheader('Primer: Dimenzionisanje debljine (rendisaljka debljača)')
        st.markdown("""
Ista operacija, ista mašina — ali dva različita načina organizacije rada
daju bitno različitu normu (**37 min** sa 2 radnika, **117 min** sa 1
radnikom, 3,2× razlika) — i poređenje sa bržim "razredi" metodom, koji u
ovom slučaju daje identičan konačan rezultat uprkos odstupanju pojedinačnih
zahvata 10–28%.
""")
        link_otvori('normiranje_primer.html', '↗ Otvori kompletan proračun')

    elif korak == 3:
        st.header('3) Upravljanje sistemom')
        st.markdown("""
Podrazumeva različite nivoe tačnosti kod sastavljanja planova, od veoma
grubih na nivou odeljenja do veoma finih na nivou izvršenja operacija na
radnom mestu. Obuhvata:

a) Grubo planiranje &nbsp;·&nbsp; b) Fino planiranje &nbsp;·&nbsp;
c) Pretpodelu rada &nbsp;·&nbsp; d) Podelu rada na RM
""")

    elif korak == 4:
        st.header('a.1) Grubo planiranje — standardna proizvodnja')
        st.markdown("""
Na bazi potrebnog i raspoloživog kapaciteta definiše se iskorišćenost
kapaciteta i ravnomernost njegovog korišćenja po odeljenjima.

Svaka boja predstavlja jedan proizvod, a svaki blok jedan njegov deo (detalj)
— širina bloka pokazuje koliki je potreban kapacitet za izradu detalja u
odnosu na raspoloživi kapacitet odeljenja.

Otvorite Grubi plan za tri standardna proizvoda (Hoklica, Sto, Stolica),
proizvedena za poznatog kupca, po narudžbini (pull koncept), kroz sva 4
odeljenja proizvodnje.
""")
        link_otvori('grubi_pocetni.html', '↗ Otvori standardni Grubi plan')

    elif korak == 5:
        st.header('a.2) Grubo planiranje — nova narudžbina')
        st.markdown("""
Dodavanje novih proizvoda tokom planskog perioda je uobičajena stvar. U
isti plan su dodata dva nova proizvoda (Klupa, Vitrina). Za svaki od njih
menadžer eksplicitno bira push ili pull, nezavisno od standardne
proizvodnje — KAIZA odmah pokazuje posledicu tog izbora na preostali
kapacitet, bez narušavanja stanja prethodnog plana.
""")
        link_otvori('grubi_dopuna.html', '↗ Otvori dopunski Grubi plan')

    elif korak == 6:
        st.header('b) Fino planiranje')
        st.markdown("""
Radi se za svako odeljenje posebno i daje razmeštanje operacija u vremenu
po radnim mestima poštujući tehnološki postupak izrade detalja.

Svaki red je jedno radno mesto. Blokovi predstavljaju proizvodno vreme
pojedinačne operacije, dajući na taj način termin početka i završetka
svake operacije.

KAIZA omogućava i **objedinjen pregled svih odeljenja** na istoj vremenskoj
osi, što je neophodno kod usklađivanja rada između odeljenja.
""")
        link_otvori('fini_plan.html', '↗ Otvori Fini plan')

    elif korak == 7:
        st.header('c) Pretpodela rada')
        st.markdown("""
Prikazuje na dnevnom nivou plan izvršenja operacija. Sa organizacionog
aspekta ovom planu je dodeljena jedna funkcionalnost koja ga čini izuzetno
fleksibilnim po pitanju izvršenja procesa. Radi se o mogućnosti promene
položaja operacije u vremenu, odnosno redosledu rada tehnoloških operacija
po radnim mestima. To dovodi do propagacije operacija koje slede i/ili su
tehnološki povezane. Na taj način menadžer može da vidi očekivane promene u
vremenu realizacije pojedinih poslova.

Pogledajte stvaran prikaz za jedno odeljenje (krojačnica).
""")
        link_otvori('pretpodela_rada.html', '↗ Otvori Pretpodelu rada')

    elif korak == 8:
        st.header('d) Podela rada na RM')
        st.markdown("""
Ovo je operativni sloj u upravljanju sistemom, koji funkcioniše na principu
povratne veze. To je mesto koje je povezano sa radnim mestima u odeljenju,
odakle dobija informacije o poremećajima, njihovom tipu i trajanju. Na
osnovu uzroka menadžer definiše set mera za njihovo rešavanje.
""")
        link_otvori('podela_rada_rm.html', '↗ Otvori Podelu rada na RM')

    elif korak == 9:
        st.header('Sledeći korak')
        st.markdown("""
Ovo je bio samo kratak pregled — u stvarnoj upotrebi, KAIZA pokriva daleko
širi aspekt rada, od grube provere kapaciteta, preko detaljnog rasporeda,
do praćenja izvršenja i evidentiranja stvarnih vremena rada.

**Faza testiranja traje 6+ meseci** — cilj je da
zajedno proverimo in-house alat u realnim uslovima Vašeg pogona.
Nije Vam potrebna nikakva dodatna oprema, niti integracija sa postojećim sistemima. KAIZA je samostalni alat koji se koristi  
na običnom laptopu ili desktop računaru.

**Zainteresovani ste?** Javite se za kratak razgovor — objasniću Vam
metodologiju rada i kako izgleda uvođenje u Vaš pogon.
""")
        st.markdown('    **Dr Milan R. VUKIĆEVIĆ, dipl. inž.**')
        st.markdown('    **060/329-1451**')
        st.markdown('    **milan.vukicevic@kaiza.rs**')

st.divider()
kol1, kol2, kol3 = st.columns([1, 3, 1])
with kol1:
    if st.session_state.korak > 0:
        if st.button('← Nazad'):
            st.session_state.korak -= 1
            st.rerun()
with kol3:
    if st.session_state.korak < len(KORACI) - 1:
        if st.button('Dalje →'):
            st.session_state.korak += 1
            st.rerun()
