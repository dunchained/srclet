# SRCLET

SRCLET računa evapotranspiraciju, vodni bilans tla, učestalost i hidromodul navodnjavanja iz mjesečnih podataka. **Odabir metoda** povezuje mjerenja i rezultate iz istog projekta. Metode koje dolaze uz program mogu se uređivati, kopirati ili zamijeniti kroz isti katalog koji služi za unos vlastitih metoda.

## Pokretanje

- **Linux** — pokreni `./run.sh` iz ovog foldera.
- **Windows** — raspakuj ili kloniraj repo u folder u koji imaš pravo pisanja i dvaput klikni `run.bat`.

Pokretači pripremaju posebno Python okruženje, instaliraju pakete iz `requirements.txt` i otvaraju PyQt6 aplikaciju. Prvo pokretanje zahtijeva internet. Preporučen je 64-bitni Python 3.11 ili noviji. Ako Python nedostaje, Windows pokretač koristi WinGet kada je dostupan. Na Linuxu pokretač prepoznaje APT, DNF i Pacman za dopunu sistemskih biblioteka. Editor formula, proračun i izvoz potom rade lokalno.

## Probaj cijeli tok

1. Otvori **Projekat → Novi projekat**, unesi naziv i izaberi folder. Učitaj [primjer za 12 godina](examples/methods/workflow.csv), provjeri kolone i izaberi **Sačuvaj i otvori**.
2. Na kartici **Odabir metoda** označi **FAO-56 Penman–Monteith** i klikni **Odaberi metodu**. U listi se pojavljuju vodni bilansi koji mogu koristiti izračunatu ET i padavine.
3. Izaberi **McCabe–Markstrom (2007)**. Njegov mjesečni manjak omogućava proračun hidromodula. Za analizu učestalosti možeš izabrati i oticaj, zalihu tla ili drugi niz. **Koeficijenti metode** otvaraju izbor mjeseca, povratnog perioda i raspodjele prije dodavanja metode.
4. Klikni **Izračunaj i sačuvaj**. Kartica **Sačuvani rezultati** prikazuje svaki korak sa formulom, parametrima i korištenim ulaznim nizom. **Izvezi…** nudi XLSX s Excel grafikonom, CSV i tekst s tabulatorima (TSV ili TXT).

Odabir provjerava stvarne vrijednosti u istom mjesecu. Na ekranu se vidi koliko mjeseci ima dovoljno podataka. Vodni bilans sa zalihom iz prethodnog mjeseca zahtijeva neprekinut izabrani period. Za kraći niz učestalosti početni povratni period ograničen je brojem dostupnih godina. Vrijednosti možeš pregledati u **Koeficijenti metode**. Izbor sačuvanog niza omogućava nastavak ranijeg proračuna.

[Primjer za Mlinište](examples/mliniste.csv) sadrži samo avgustovski manjak od 34 mm. Izaberi **Hidromodul navodnjavanja**. Rezultat je **0,12694146 L/s/ha**, odnosno 0,127 iz tabele 22. Godina u primjeru služi za brojanje dana. Pojedinačni [primjeri za svaku metodu](examples/methods/) sadrže sintetičke brojeve za testiranje i raspoloživi su i preko dugmeta **Izvezi primjer podataka** u katalogu.

## Metode i podaci

| Grupa | Katalog |
| --- | --- |
| Evapotranspiracija | FAO-56 Penman–Monteith, Thornthwaite, Turc, Hargreaves–Samani, Trajković i dvije lokalno kalibrirane varijante AHS i ATRAJ. |
| Vodni bilans | Thornthwaite, Palmer (dvije zalihe), Alley, Dingman te McCabe–Markstrom. Koeficijenti i početne zalihe prikazani su uz metodu. |
| Učestalost | California, Hazen, Weibull, Cunnane, Sevruk–Geiger i Adamowski. Svaka pozicija rangiranja može se kombinovati s normalnom, lognormalnom, Weibullovom, gama, Gumbelovom ili eksponencijalnom raspodjelom. |
| Hidromodul | Dnevni proračun s vremenom rada sistema i mjesečni q₂₄ na osnovu manjka i stvarnog broja dana u mjesecu. |
| Pomoćni proračuni i evaluacija | Procjena pritiska pare i zračenja prema jednačinama 43–44. MBE, sd², RMSE, MAE i R² nad uparenim srednjim dnevnim vrijednostima mjeseci. Referentni i procijenjeni mjesečni ET mogu se uvesti kao `FAOPM` i `EstimateET` ili dobiti izborom dviju ET metoda. |

**Naučne konvencije.** Za Thornthwaite su posebno označene dvije verzije. Jedna prenosi jednačine 24–26 kako su odštampane u doktoratu. Druga koristi omjer 10T/I, trajanje dana i dužinu mjeseca kao biblioteka navedena u poglavlju 5.1.5. MBE i sd² prate znakove kako su napisani u jednačinama 38–39. Za HS i TRAJ koeficijente možeš mijenjati. Za AHS i ATRAJ uvezeni lokalni koeficijent ima prednost nad vrijednošću za odgovarajući naziv stanice iz [tabele 16](parameters/station_coefficients.csv). Procjene učestalosti koriste prilagodbu kvantila na empirijske pozicije i posebno tretiraju udio nula kod nenegativnih nizova. Za provjeru pristajanja čuvaju se rangovi i RMSE. [Disertacija](docs/Doktorska_disertacija_Čadro_Sabrija.pdf) · [PyETo, Thornthwaite](https://pyeto.readthedocs.io/en/latest/_modules/pyeto/thornthwaite.html) · [FAO-56](https://www.fao.org/4/x0490e/x0490e08.htm) · [Dingman, okvir 7-3](https://civil.colorado.edu/~balajir/CVEN5333/Lectures/Dingman-Chap7-PET.pdf) · [USGS, McCabe–Markstrom](https://pubs.usgs.gov/of/2007/1088/).

## Uređivanje

- **Podaci** — uvezi TXT, TSV, CSV ili XLSX, ili izaberi **Ručni unos podataka**. Godina i mjesec označavaju period. Prazno polje i -999 predstavljaju nedostajuću vrijednost. U otvorenom projektu **Uredi podatke projekta** služi za redove, kolone i dopunu koordinata stanice. Izvorni uvezeni radni list čuva se u projektu.
- **Metode** — u katalogu zadaj grupu, naziv, oznaku, jedinicu i izlaznu veličinu. Za novu ET metodu koristi `ET0` kao zajednički izlaz ako daje mjesečnu ET u mm. Za vodni bilans koristi `Deficit` ako je glavni izlaz mjesečni manjak. Vlastita oznaka metode takođe ostaje dostupna drugim formulama. Vizuelni editor ima razlomke, korijene, stepene, zagrade i izraze s uslovima. Složeniji račun može imati više koraka i početne vrijednosti veličina koje se prenose u naredni mjesec. Uključivanje **Ponudi kao rezultat** čini međurezultat dostupnim sljedećoj metodi.
- **Parametri** — osnovne veličine za uvoz i koeficijenti imaju svoje editore pod **Prilagodi → Parametri**. U katalogu metode možeš preuzeti imenovani koeficijent i prilagoditi njegovu vrijednost toj metodi.
- **Postavke** — bosanski, engleski i francuski, veličina teksta, menija, unosa i ikona primjenjuju se pri odabiru. Nazivi i opisi koje korisnik sam upiše čuvaju se u izvornom obliku.

## Uputstvo u aplikaciji

**Pomoć → Uputstvo (F1)** otvara devet poglavlja s lokalnim snimcima ekrana. Poglavlja se otvaraju klikom, snimci se mogu uvećati, a promjena jezika zadržava otvorena poglavlja. Uputstvo se može otvoriti i direktno u pregledniku: [bosanski](srclet/manual/ba/index.html), [English](srclet/manual/en/index.html), [français](srclet/manual/fr/index.html).

U [video_url.txt](video_url.txt) upiši jednu HTTP ili HTTPS adresu. Link se osvježava i dok je uputstvo otvoreno. Prazna datoteka skriva videolink. Za obnovu snimaka ekrana koristi `.venv/bin/python tools/manual_screenshots.py`. Pravilo održavanja svih jezičkih verzija nalazi se u [AGENTS.md](AGENTS.md).

## Testovi

Nakon prvog pokretanja, na Linuxu koristi `.venv/bin/python -m unittest discover -s tests -v`, a na Windowsu `.venv-win\Scripts\python.exe -m unittest discover -s tests -v`. Testovi obuhvataju katalog i primjere, povezivanje metoda kroz stvarni prozor, formulu za Mlinište, FAO-56 primjer za Bangkok, čuvanje i ponovno otvaranje te čitanje Excel grafikona iz izvezene radne knjige.
