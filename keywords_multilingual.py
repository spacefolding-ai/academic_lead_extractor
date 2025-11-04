"""
keywords_multilingual.py — Multilingual ICP Keyword Translations
Contains translated technical keywords for non-English speaking countries.
Used by the Academic Lead Extractor to match relevant researchers in their native languages.
"""

# ---------------------------
# MULTI-LANGUAGE ICP SUPPORT
# (for universities in non-English speaking countries)
# ---------------------------

KEYWORDS_BY_LANGUAGE = {
    "German": [
        "leistungselektronik", "energiesysteme", "erneuerbare energie", "nachhaltige energie",
        "mikronetz", "smart grid", "batteriemanagement", "energiespeicher",
        "antriebsstrang", "antriebe", "elektrische antriebe", "fahrzeugelektrifizierung",
        "regelsysteme", "regelungstechnik", "digitale regelung", "systemdynamik",
        "automatisierungstechnik", "bewegungssteuerung",
        "eingebettete systeme", "echtzeitsimulation", "hardware-in-the-loop",
        "elektrotechnik", "mechatronik", "messtechnik", "energietechnik",
        "windenergie", "solarenergie", "photovoltaik", "brennstoffzellen", "wasserstoffsysteme",
        # Additional power electronics & energy terms
        "DC-DC", "AC-DC", "gleichspannungswandler", "wirkleistung", "blindleistung", "virtuelle trägheit", "aktive dämpfung", "schutzrelais",
        "netzdienstleistungen", "asynchrongenerator", "batteriespeicher", "schwungrad", "verschachtelt",
        "bidirektional", "bidirektionales ladegerät", "BLDC", "aufwärtswandler", "BMS", "MPPT",
        "dezentrale erzeugung", "DER", "DSP", "dual active bridge", "DAB", "elektrofahrzeug", "EV", "HEV", "erdschluss", "überspannung",
        "unterspannung", "elektrischer antrieb", "energiemanagement", "oberschwingung", "oberschwingungskompensation", "dspace", "opal-rt", "Speedgoat", "plecs",
        "DIgSILENT", "PowerFactory", "PSCAD", "RTDS", "etap", "neplan", "opendss", "psim", "Simscape Electrical", "rt-lab", "hypersim", "ltspice",
        "fehlerschutz", "IEC 61850", "UPS", "IEEE 1547-2018", "netzanschluss", "IGBT", "MOSFET", "asynchronmaschine",
        "admittanz", "impedanz", "leitwert", "suszeptanz", "reaktanz", "inselerkennung", "anti-islanding", "modularer multilevel-umrichter",
        "MMC", "mehrstufiger wechselrichter", "netzkonformität", "teilverschattung", "plug-in elektro", "lastfluss", "spannungsqualität", "THD", "aktivfilter",
        "Z-source", "PMSM", "synchronmaschine", "kurzschlussanalyse", "SOC ausgleich", "ladezustand", "virtueller synchrongenerator", "vehicle-to-grid",
        "grid-to-vehicle", "spannungswechselrichter", "spannungsregelung", "netzstabilität", "WAMS", "windturbine",
        # Control
        "statik", "robuste regelung", "sliding-mode-regelung", "PLL", "modellprädiktive regelung",
        # HIL variants
        "controller-hardware-in-the-loop", "c-hil", "p-hil", "digitaler zwilling"
    ],
    "Italian": [
        "elettronica di potenza", "sistemi energetici", "energia rinnovabile",
        "microrete", "gestione batterie", "accumulo energia",
        "sistemi di controllo", "controllo automatico", "controllo digitale",
        "sistemi embedded", "simulazione in tempo reale",
        "ingegneria elettrica", "meccatronica", "strumentazione", "sistemi di potenza",
        "energia eolica", "energia solare", "fotovoltaico", "celle a combustibile",
        # Additional power electronics & energy terms
        "DC-DC", "AC-DC", "convertitore dc-dc", "potenza attiva", "potenza reattiva", "inerzia virtuale", "smorzamento attivo", "relè di protezione",
        "servizi ancillari", "generatore asincrono", "accumulo batterie", "volano", "interleaved",
        "bidirezionale", "caricatore bidirezionale", "BLDC", "convertitore boost", "BMS", "MPPT",
        "generazione distribuita", "DER", "DSP", "dual active bridge", "DAB", "veicolo elettrico", "EV", "HEV", "guasto a terra", "sovratensione",
        "sottotensione", "propulsione elettrica", "gestione energia", "armoniche", "compensazione armoniche", "dspace", "opal-rt", "Speedgoat", "plecs",
        "DIgSILENT", "PowerFactory", "PSCAD", "RTDS", "etap", "neplan", "opendss", "psim", "Simscape Electrical", "rt-lab", "hypersim", "ltspice",
        "protezione guasti", "IEC 61850", "UPS", "IEEE 1547-2018", "interconnessione", "IGBT", "MOSFET", "motore asincrono",
        "ammettenza", "impedenza", "conduttanza", "suscettanza", "reattanza", "rilevamento isola", "anti-islanding", "convertitore modulare multilivello",
        "MMC", "inverter multilivello", "conformità rete", "ombreggiamento parziale", "plug-in elettrico", "flusso di potenza", "qualità potenza", "THD", "filtro attivo",
        "Z-source", "PMSM", "motore sincrono", "analisi cortocircuito", "bilanciamento SOC", "stato di carica", "generatore sincrono virtuale", "vehicle-to-grid",
        "grid-to-vehicle", "inverter di tensione", "regolazione tensione", "stabilità sistema", "WAMS", "turbina eolica",
        # Control
        "controllo droop", "controllo robusto", "controllo sliding mode", "PLL", "controllo predittivo",
        # HIL variants
        "controller-hardware-in-the-loop", "c-hil", "p-hil", "gemello digitale"
    ],
    "French": [
        "électronique de puissance", "systèmes énergétiques", "énergie renouvelable",
        "microréseau", "gestion de batterie", "stockage d'énergie",
        "systèmes de contrôle", "contrôle automatique", "contrôle numérique",
        "systèmes embarqués", "simulation temps réel",
        "génie électrique", "mécatronique", "instrumentation",
        "énergie éolienne", "énergie solaire", "photovoltaïque", "piles à combustible",
        # Additional power electronics & energy terms
        "DC-DC", "AC-DC", "convertisseur dc-dc", "puissance active", "puissance réactive", "inertie virtuelle", "amortissement actif", "relais de protection",
        "services auxiliaires", "générateur asynchrone", "stockage batterie", "volant d'inertie", "entrelacé",
        "bidirectionnel", "chargeur bidirectionnel", "BLDC", "convertisseur boost", "BMS", "MPPT",
        "génération distribuée", "DER", "DSP", "dual active bridge", "DAB", "véhicule électrique", "EV", "HEV", "défaut terre", "surtension",
        "sous-tension", "propulsion électrique", "gestion énergie", "harmoniques", "compensation harmoniques", "dspace", "opal-rt", "Speedgoat", "plecs",
        "DIgSILENT", "PowerFactory", "PSCAD", "RTDS", "etap", "neplan", "opendss", "psim", "Simscape Electrical", "rt-lab", "hypersim", "ltspice",
        "protection défaut", "IEC 61850", "UPS", "IEEE 1547-2018", "interconnexion", "IGBT", "MOSFET", "moteur asynchrone",
        "admittance", "impédance", "conductance", "susceptance", "réactance", "détection îlotage", "anti-islanding", "convertisseur modulaire multiniveau",
        "MMC", "onduleur multiniveau", "conformité réseau", "ombrage partiel", "plug-in électrique", "flux de puissance", "qualité puissance", "THD", "filtre actif",
        "Z-source", "PMSM", "moteur synchrone", "analyse court-circuit", "équilibrage SOC", "état de charge", "générateur synchrone virtuel", "vehicle-to-grid",
        "grid-to-vehicle", "onduleur tension", "régulation tension", "stabilité système", "WAMS", "éolienne",
        # Control
        "contrôle droop", "contrôle robuste", "contrôle mode glissant", "PLL", "contrôle prédictif",
        # HIL variants
        "controller-hardware-in-the-loop", "c-hil", "p-hil", "jumeau numérique"
    ],
    "Spanish": [
        "electrónica de potencia", "sistemas energéticos", "energía renovable",
        "microrred", "gestión de baterías", "almacenamiento de energía",
        "sistemas de control", "control automático", "control digital",
        "sistemas embebidos", "simulación en tiempo real",
        "ingeniería eléctrica", "mecatrónica", "instrumentación",
        "energía eólica", "energía solar", "fotovoltaica", "pilas de combustible",
        # Additional power electronics & energy terms
        "DC-DC", "AC-DC", "convertidor dc-dc", "potencia activa", "potencia reactiva", "inercia virtual", "amortiguamiento activo", "relé de protección",
        "servicios auxiliares", "generador asíncrono", "almacenamiento baterías", "volante inercia", "entrelazado",
        "bidireccional", "cargador bidireccional", "BLDC", "convertidor boost", "BMS", "MPPT",
        "generación distribuida", "DER", "DSP", "dual active bridge", "DAB", "vehículo eléctrico", "EV", "HEV", "falla tierra", "sobretensión",
        "subtensión", "propulsión eléctrica", "gestión energía", "armónicos", "compensación armónicos", "dspace", "opal-rt", "Speedgoat", "plecs",
        "DIgSILENT", "PowerFactory", "PSCAD", "RTDS", "etap", "neplan", "opendss", "psim", "Simscape Electrical", "rt-lab", "hypersim", "ltspice",
        "protección fallos", "IEC 61850", "UPS", "IEEE 1547-2018", "interconexión", "IGBT", "MOSFET", "motor asíncrono",
        "admitancia", "impedancia", "conductancia", "susceptancia", "reactancia", "detección isla", "anti-islanding", "convertidor modular multinivel",
        "MMC", "inversor multinivel", "cumplimiento red", "sombreado parcial", "plug-in eléctrico", "flujo potencia", "calidad potencia", "THD", "filtro activo",
        "Z-source", "PMSM", "motor síncrono", "análisis cortocircuito", "balanceo SOC", "estado de carga", "generador síncrono virtual", "vehicle-to-grid",
        "grid-to-vehicle", "inversor tensión", "regulación tensión", "estabilidad sistema", "WAMS", "turbina eólica",
        # Control
        "control droop", "control robusto", "control modo deslizante", "PLL", "control predictivo",
        # HIL variants
        "controller-hardware-in-the-loop", "c-hil", "p-hil", "gemelo digital"
    ],
    "Portuguese": [
        "eletrônica de potência", "sistemas energéticos", "energia renovável",
        "microrede", "gestão de baterias", "armazenamento de energia",
        "sistemas de controle", "controle automático", "controle digital",
        "sistemas embarcados", "simulação em tempo real",
        "engenharia elétrica", "mecatrônica", "instrumentação",
        "energia eólica", "energia solar", "fotovoltaica", "células de combustível",
        # Additional power electronics & energy terms
        "DC-DC", "AC-DC", "conversor dc-dc", "potência ativa", "potência reativa", "inércia virtual", "amortecimento ativo", "relé de proteção",
        "serviços auxiliares", "gerador assíncrono", "armazenamento baterias", "volante inércia", "entrelaçado",
        "bidirecional", "carregador bidirecional", "BLDC", "conversor boost", "BMS", "MPPT",
        "geração distribuída", "DER", "DSP", "dual active bridge", "DAB", "veículo elétrico", "EV", "HEV", "falta terra", "sobretensão",
        "subtensão", "propulsão elétrica", "gestão energia", "harmônicos", "compensação harmônicos", "dspace", "opal-rt", "Speedgoat", "plecs",
        "DIgSILENT", "PowerFactory", "PSCAD", "RTDS", "etap", "neplan", "opendss", "psim", "Simscape Electrical", "rt-lab", "hypersim", "ltspice",
        "proteção falhas", "IEC 61850", "UPS", "IEEE 1547-2018", "interconexão", "IGBT", "MOSFET", "motor assíncrono",
        "admitância", "impedância", "condutância", "susceptância", "reatância", "detecção ilha", "anti-islanding", "conversor modular multinível",
        "MMC", "inversor multinível", "conformidade rede", "sombreamento parcial", "plug-in elétrico", "fluxo potência", "qualidade potência", "THD", "filtro ativo",
        "Z-source", "PMSM", "motor síncrono", "análise curto-circuito", "balanceamento SOC", "estado de carga", "gerador síncrono virtual", "vehicle-to-grid",
        "grid-to-vehicle", "inversor tensão", "regulação tensão", "estabilidade sistema", "WAMS", "turbina eólica",
        # Control
        "controle droop", "controle robusto", "controle modo deslizante", "PLL", "controle preditivo",
        # HIL variants
        "controller-hardware-in-the-loop", "c-hil", "p-hil", "gêmeo digital"
    ],
    "Dutch": [
        "vermogenselektronica", "energiesystemen", "hernieuwbare energie",
        "microgrid", "batterijbeheer", "energieopslag",
        "regelsystemen", "automatische besturing", "digitale regeling",
        "embedded systemen", "realtime simulatie",
        "elektrotechniek", "mechatronica", "instrumentatie",
        "windenergie", "zonne-energie", "fotovoltaïsche", "brandstofcellen",
        # Additional power electronics & energy terms
        "DC-DC", "AC-DC", "dc-dc converter", "actief vermogen", "reactief vermogen", "virtuele inertie", "actieve demping", "beschermingsrelais",
        "ondersteunende diensten", "asynchrone generator", "batterijopslag", "vliegwiel", "interleaved",
        "bidirectioneel", "bidirectionele lader", "BLDC", "boost converter", "BMS", "MPPT",
        "gedistribueerde opwekking", "DER", "DSP", "dual active bridge", "DAB", "elektrisch voertuig", "EV", "HEV", "aardfout", "overspanning",
        "onderspanning", "elektrische voortstuwing", "energiebeheer", "harmonischen", "harmonische compensatie", "dspace", "opal-rt", "Speedgoat", "plecs",
        "DIgSILENT", "PowerFactory", "PSCAD", "RTDS", "etap", "neplan", "opendss", "psim", "Simscape Electrical", "rt-lab", "hypersim", "ltspice",
        "foutbeveiliging", "IEC 61850", "UPS", "IEEE 1547-2018", "interconnectie", "IGBT", "MOSFET", "inductiemotor",
        "admittantie", "impedantie", "conductantie", "susceptantie", "reactantie", "eilanddetectie", "anti-islanding", "modulaire multilevel converter",
        "MMC", "multilevel omvormer", "netconformiteit", "gedeeltelijke schaduw", "plug-in elektrisch", "vermogensstroom", "spanningskwaliteit", "THD", "actief filter",
        "Z-source", "PMSM", "synchrone motor", "kortsluitanalyse", "SOC balancering", "laadtoestand", "virtuele synchrone generator", "vehicle-to-grid",
        "grid-to-vehicle", "spanningsomvormer", "spanningsregeling", "systeemstabiliteit", "WAMS", "windturbine",
        # Control
        "droop regeling", "robuuste regeling", "sliding mode regeling", "PLL", "model predictive control",
        # HIL variants
        "controller-hardware-in-the-loop", "c-hil", "p-hil", "digitale tweeling"
    ],
    "Polish": [
        "elektronika mocy", "systemy energetyczne", "energia odnawialna",
        "mikrosieć", "zarządzanie bateriami", "magazynowanie energii",
        "systemy sterowania", "automatyka", "sterowanie cyfrowe",
        "systemy wbudowane", "symulacja czasu rzeczywistego",
        "elektrotechnika", "mechatronika", "oprzyrządowanie",
        "energia wiatrowa", "energia słoneczna", "fotowoltaika", "ogniwa paliwowe",
        # Additional power electronics & energy terms
        "DC-DC", "AC-DC", "przetwornica dc-dc", "moc czynna", "moc bierna", "wirtualna bezwładność", "tłumienie aktywne", "przekaźnik ochronny",
        "usługi pomocnicze", "generator asynchroniczny", "magazyn baterii", "koło zamachowe", "przeplatany",
        "dwukierunkowy", "ładowarka dwukierunkowa", "BLDC", "przetwornica boost", "BMS", "MPPT",
        "generacja rozproszona", "DER", "DSP", "dual active bridge", "DAB", "pojazd elektryczny", "EV", "HEV", "zwarcie doziemne", "przepięcie",
        "podnapięcie", "napęd elektryczny", "zarządzanie energią", "harmoniczne", "kompensacja harmonicznych", "dspace", "opal-rt", "Speedgoat", "plecs",
        "DIgSILENT", "PowerFactory", "PSCAD", "RTDS", "etap", "neplan", "opendss", "psim", "Simscape Electrical", "rt-lab", "hypersim", "ltspice",
        "ochrona przed uszkodzeniem", "IEC 61850", "UPS", "IEEE 1547-2018", "przyłącze", "IGBT", "MOSFET", "silnik indukcyjny",
        "admitancja", "impedancja", "konduktancja", "susceptancja", "reaktancja", "wykrywanie wyspy", "anti-islanding", "modularny konwerter wielopoziomowy",
        "MMC", "falownik wielopoziomowy", "zgodność z siecią", "częściowe zacienienie", "plug-in elektryczny", "przepływ mocy", "jakość energii", "THD", "filtr aktywny",
        "Z-source", "PMSM", "silnik synchroniczny", "analiza zwarciowa", "bilansowanie SOC", "stan naładowania", "wirtualny generator synchroniczny", "vehicle-to-grid",
        "grid-to-vehicle", "falownik napięciowy", "regulacja napięcia", "stabilność systemu", "WAMS", "turbina wiatrowa",
        # Control
        "sterowanie spadkowe", "sterowanie odporne", "sterowanie ślizgowe", "PLL", "sterowanie predykcyjne",
        # HIL variants
        "controller-hardware-in-the-loop", "c-hil", "p-hil", "cyfrowy bliźniak"
    ],
    "Czech": [
        "výkonová elektronika", "energetické systémy", "obnovitelná energie",
        "mikrosíť", "správa baterií", "ukládání energie",
        "řídicí systémy", "automatické řízení", "digitální řízení",
        "vestavěné systémy", "simulace v reálném čase",
        "elektrotechnika", "mechatronika", "přístrojová technika",
        "větrná energie", "solární energie", "fotovoltaika", "palivové články",
        # Additional power electronics & energy terms
        "DC-DC", "AC-DC", "dc-dc měnič", "činný výkon", "jalový výkon", "virtuální setrvačnost", "aktivní tlumení", "ochranné relé",
        "podpůrné služby", "asynchronní generátor", "bateriové úložiště", "setrvačník", "prokládaný",
        "obousměrný", "obousměrná nabíječka", "BLDC", "boost měnič", "BMS", "MPPT",
        "distribuovaná výroba", "DER", "DSP", "dual active bridge", "DAB", "elektromobil", "EV", "HEV", "zemní porucha", "přepětí",
        "podpětí", "elektrický pohon", "řízení energie", "harmonické", "kompenzace harmonických", "dspace", "opal-rt", "Speedgoat", "plecs",
        "DIgSILENT", "PowerFactory", "PSCAD", "RTDS", "etap", "neplan", "opendss", "psim", "Simscape Electrical", "rt-lab", "hypersim", "ltspice",
        "ochrana proti poruchám", "IEC 61850", "UPS", "IEEE 1547-2018", "propojení", "IGBT", "MOSFET", "asynchronní motor",
        "admitance", "impedance", "konduktance", "susceptance", "reaktance", "detekce ostrovního provozu", "anti-islanding", "modulární víceúrovňový měnič",
        "MMC", "víceúrovňový střídač", "shoda se sítí", "částečné stínění", "plug-in elektrický", "tok výkonu", "kvalita energie", "THD", "aktivní filtr",
        "Z-source", "PMSM", "synchronní motor", "analýza zkratu", "vyvážení SOC", "stav nabití", "virtuální synchronní generátor", "vehicle-to-grid",
        "grid-to-vehicle", "napěťový střídač", "regulace napětí", "stabilita systému", "WAMS", "větrná turbína",
        # Control
        "droop řízení", "robustní řízení", "klouzavý režim řízení", "PLL", "prediktivní řízení",
        # HIL variants
        "controller-hardware-in-the-loop", "c-hil", "p-hil", "digitální dvojče"
    ],
    "Swedish": [
        "kraftelektronik", "energisystem", "förnybar energi",
        "mikronät", "batterihantering", "energilagring",
        "styrsystem", "automatisk styrning", "digital styrning",
        "inbyggda system", "realtidssimulering",
        "elektroteknik", "mekatronik", "instrumentering",
        "vindenergi", "solenergi", "fotovoltaik", "bränsleceller",
        # Additional power electronics & energy terms
        "DC-DC", "AC-DC", "dc-dc omvandlare", "aktiv effekt", "reaktiv effekt", "virtuell tröghet", "aktiv dämpning", "skyddsrelä",
        "stödtjänster", "asynkrongenerator", "batterilagring", "svänghjul", "sammanflätad",
        "dubbelriktad", "dubbelriktad laddare", "BLDC", "boost omvandlare", "BMS", "MPPT",
        "distribuerad produktion", "DER", "DSP", "dual active bridge", "DAB", "elfordon", "EV", "HEV", "jordfel", "överspänning",
        "underspänning", "elektrisk framdrivning", "energihantering", "harmoniska", "harmonisk kompensation", "dspace", "opal-rt", "Speedgoat", "plecs",
        "DIgSILENT", "PowerFactory", "PSCAD", "RTDS", "etap", "neplan", "opendss", "psim", "Simscape Electrical", "rt-lab", "hypersim", "ltspice",
        "felskydd", "IEC 61850", "UPS", "IEEE 1547-2018", "sammankoppling", "IGBT", "MOSFET", "asynkronmotor",
        "admittans", "impedans", "konduktans", "susceptans", "reaktans", "ö-detektion", "anti-islanding", "modulär flernivåomvandlare",
        "MMC", "flernivåväxelriktare", "nätkompatibilitet", "partiell skuggning", "plug-in elektrisk", "effektflöde", "spänningskvalitet", "THD", "aktivt filter",
        "Z-source", "PMSM", "synkronmotor", "kortslutningsanalys", "SOC balansering", "laddningstillstånd", "virtuell synkrongenerator", "vehicle-to-grid",
        "grid-to-vehicle", "spänningsväxelriktare", "spänningsreglering", "systemstabilitet", "WAMS", "vindturbin",
        # Control
        "droop styrning", "robust styrning", "sliding mode styrning", "PLL", "prediktiv styrning",
        # HIL variants
        "controller-hardware-in-the-loop", "c-hil", "p-hil", "digital tvilling"
    ],
    "Norwegian": [
        "kraftelektronikk", "energisystemer", "fornybar energi",
        "mikronett", "batteristyring", "energilagring",
        "kontrollsystemer", "automatisk kontroll", "digital kontroll",
        "innebygde systemer", "sanntidssimulering",
        "elektroteknikk", "mekatronikk", "instrumentering",
        "vindenergi", "solenergi", "fotovoltaisk", "brenselceller",
        # Additional power electronics & energy terms
        "DC-DC", "AC-DC", "dc-dc omformer", "aktiv effekt", "reaktiv effekt", "virtuell treghet", "aktiv demping", "beskyttelsesrelé",
        "tilleggstjenester", "asynkrongenerator", "batterilagring", "svinghjul", "sammenvevd",
        "toveis", "toveis lader", "BLDC", "boost omformer", "BMS", "MPPT",
        "distribuert generering", "DER", "DSP", "dual active bridge", "DAB", "elektrisk kjøretøy", "EV", "HEV", "jordfeil", "overspenning",
        "underspenning", "elektrisk fremdrift", "energistyring", "harmoniske", "harmonisk kompensasjon", "dspace", "opal-rt", "Speedgoat", "plecs",
        "DIgSILENT", "PowerFactory", "PSCAD", "RTDS", "etap", "neplan", "opendss", "psim", "Simscape Electrical", "rt-lab", "hypersim", "ltspice",
        "feilbeskyttelse", "IEC 61850", "UPS", "IEEE 1547-2018", "sammenkobling", "IGBT", "MOSFET", "induksjonsmotor",
        "admittans", "impedans", "konduktans", "susceptans", "reaktans", "øy-deteksjon", "anti-islanding", "modulær flernivå omformer",
        "MMC", "flernivå inverter", "nettoverensstemmelse", "delvis skygge", "plug-in elektrisk", "effektflyt", "spenningskvalitet", "THD", "aktivt filter",
        "Z-source", "PMSM", "synkronmotor", "kortslutningsanalyse", "SOC balansering", "ladetilstand", "virtuell synkrongenerator", "vehicle-to-grid",
        "grid-to-vehicle", "spenningsinverter", "spenningsregulering", "systemstabilitet", "WAMS", "vindturbin",
        # Control
        "droop kontroll", "robust kontroll", "sliding mode kontroll", "PLL", "prediktiv kontroll",
        # HIL variants
        "controller-hardware-in-the-loop", "c-hil", "p-hil", "digital tvilling"
    ],
    "Danish": [
        "effektelektronik", "energisystemer", "vedvarende energi",
        "mikronet", "batteristyring", "energilagring",
        "kontrolsystemer", "automatisk kontrol", "digital kontrol",
        "indlejrede systemer", "realtidssimulering",
        "elektroteknik", "mekatronik", "instrumentering",
        "vindenergi", "solenergi", "fotovoltaisk", "brændselsceller",
        # Additional power electronics & energy terms
        "DC-DC", "AC-DC", "dc-dc konverter", "aktiv effekt", "reaktiv effekt", "virtuel inerти", "aktiv dæmpning", "beskyttelsesrelæ",
        "støttetjenester", "asynkrongenerator", "batterilagring", "svinghjul", "sammenflettet",
        "tovejs", "tovejs oplader", "BLDC", "boost konverter", "BMS", "MPPT",
        "distribueret produktion", "DER", "DSP", "dual active bridge", "DAB", "elektrisk køretøj", "EV", "HEV", "jordfejl", "overspænding",
        "underspænding", "elektrisk fremdrift", "energistyring", "harmoniske", "harmonisk kompensation", "dspace", "opal-rt", "Speedgoat", "plecs",
        "DIgSILENT", "PowerFactory", "PSCAD", "RTDS", "etap", "neplan", "opendss", "psim", "Simscape Electrical", "rt-lab", "hypersim", "ltspice",
        "fejlbeskyttelse", "IEC 61850", "UPS", "IEEE 1547-2018", "sammenkobling", "IGBT", "MOSFET", "induktionsmotor",
        "admittans", "impedans", "konduktans", "susceptans", "reaktans", "ø-detektering", "anti-islanding", "modulær flerniveaukonverter",
        "MMC", "flerniveau inverter", "netoverholdelse", "delvis skygge", "plug-in elektrisk", "effektflow", "spændingskvalitet", "THD", "aktivt filter",
        "Z-source", "PMSM", "synkronmotor", "kortslutningsanalyse", "SOC balancering", "ladetilstand", "virtuel synkrongenerator", "vehicle-to-grid",
        "grid-to-vehicle", "spændingsinverter", "spændingsregulering", "systemstabilitet", "WAMS", "vindmølle",
        # Control
        "droop kontrol", "robust kontrol", "sliding mode kontrol", "PLL", "prædiktiv kontrol",
        # HIL variants
        "controller-hardware-in-the-loop", "c-hil", "p-hil", "digital tvilling"
    ],
    "Finnish": [
        "tehoelektroniikka", "energiajärjestelmät", "uusiutuva energia",
        "mikroverkko", "akkujen hallinta", "energian varastointi",
        "säätöjärjestelmät", "automaattinen säätö", "digitaalinen säätö",
        "sulautetut järjestelmät", "reaaliaikasimulointi",
        "sähkötekniikka", "mekatroniikka", "mittaustekniikka",
        "tuulienergia", "aurinkoenergia", "aurinkosähkö", "polttokennot",
        # Additional power electronics & energy terms
        "DC-DC", "AC-DC", "dc-dc muunnin", "pätöteho", "loisteho", "virtuaalinen hitaus", "aktiivinen vaimennus", "suojarele",
        "liitännäispalvelut", "asynkronigeneraattori", "akkuvarasto", "vauhtipyörä", "lomitettu",
        "kaksisuuntainen", "kaksisuuntainen laturi", "BLDC", "boost muunnin", "BMS", "MPPT",
        "hajautettu tuotanto", "DER", "DSP", "dual active bridge", "DAB", "sähköajoneuvo", "EV", "HEV", "maasulku", "ylijännite",
        "alijännite", "sähköinen voimansiirto", "energianhallinta", "harmoniset", "harmoninen kompensointi", "dspace", "opal-rt", "Speedgoat", "plecs",
        "DIgSILENT", "PowerFactory", "PSCAD", "RTDS", "etap", "neplan", "opendss", "psim", "Simscape Electrical", "rt-lab", "hypersim", "ltspice",
        "vikasuojaus", "IEC 61850", "UPS", "IEEE 1547-2018", "liitäntä", "IGBT", "MOSFET", "oikosulkumoottori",
        "admittanssi", "impedanssi", "konduktanssi", "susceptanssi", "reaktanssi", "saareketunnistus", "anti-islanding", "modulaarinen monitasomuunnin",
        "MMC", "monitasoinvertteri", "verkkovaatimustenmukaisuus", "osittainen varjostus", "plug-in sähkö", "tehonkulku", "jännitteen laatu", "THD", "aktiivinen suodatin",
        "Z-source", "PMSM", "synkronimoottori", "oikosulkuanalyysi", "SOC tasapainotus", "lataus tila", "virtuaalinen synkronigeneraattori", "vehicle-to-grid",
        "grid-to-vehicle", "jänniteinvertteri", "jännitteensäätö", "järjestelmän vakaus", "WAMS", "tuuliturbiini",
        # Control
        "droop säätö", "vankka säätö", "liukuva tila säätö", "PLL", "ennustava säätö",
        # HIL variants
        "controller-hardware-in-the-loop", "c-hil", "p-hil", "digitaalinen kaksonen"
    ],
    "Greek": [
        "ηλεκτρονικά ισχύος", "ενεργειακά συστήματα", "ανανεώσιμη ενέργεια",
        "μικροδίκτυο", "διαχείριση μπαταριών", "αποθήκευση ενέργειας",
        "συστήματα ελέγχου", "αυτόματος έλεγχος",
        "ενσωματωμένα συστήματα", "προσομοίωση πραγματικού χρόνου",
        "ηλεκτρολογία", "μηχατρονική", "οργανολογία",
        "αιολική ενέργεια", "ηλιακή ενέργεια", "φωτοβολταϊκά", "κυψέλες καυσίμου",
        # Additional power electronics & energy terms
        "DC-DC", "AC-DC", "μετατροπέας dc-dc", "ενεργός ισχύς", "άεργος ισχύς", "εικονική αδράνεια", "ενεργή απόσβεση", "ρελέ προστασίας",
        "βοηθητικές υπηρεσίες", "ασύγχρονη γεννήτρια", "αποθήκευση μπαταρίας", "σφόνδυλος", "διαπλεκόμενος",
        "αμφίδρομος", "αμφίδρομος φορτιστής", "BLDC", "μετατροπέας boost", "BMS", "MPPT",
        "κατανεμημένη παραγωγή", "DER", "DSP", "dual active bridge", "DAB", "ηλεκτρικό όχημα", "EV", "HEV", "βραχυκύκλωμα γείωσης", "υπερτάση",
        "υποτάση", "ηλεκτρική πρόωση", "διαχείριση ενέργειας", "αρμονικές", "αντιστάθμιση αρμονικών", "dspace", "opal-rt", "Speedgoat", "plecs",
        "DIgSILENT", "PowerFactory", "PSCAD", "RTDS", "etap", "neplan", "opendss", "psim", "Simscape Electrical", "rt-lab", "hypersim", "ltspice",
        "προστασία σφαλμάτων", "IEC 61850", "UPS", "IEEE 1547-2018", "διασύνδεση", "IGBT", "MOSFET", "επαγωγικός κινητήρας",
        "αγωγιμότητα", "σύνθετη αντίσταση", "αγωγιμότητα", "επιδεκτικότητα", "αντίδραση", "ανίχνευση νησίδας", "anti-islanding", "αρθρωτός πολυεπίπεδος μετατροπέας",
        "MMC", "πολυεπίπεδος μετατροπέας", "συμμόρφωση δικτύου", "μερική σκίαση", "plug-in ηλεκτρικό", "ροή ισχύος", "ποιότητα ισχύος", "THD", "ενεργό φίλτρο",
        "Z-source", "PMSM", "σύγχρονος κινητήρας", "ανάλυση βραχυκυκλώματος", "εξισορρόπηση SOC", "κατάσταση φόρτισης", "εικονική σύγχρονη γεννήτρια", "vehicle-to-grid",
        "grid-to-vehicle", "μετατροπέας τάσης", "ρύθμιση τάσης", "σταθερότητα συστήματος", "WAMS", "ανεμογεννήτρια",
        # Control
        "έλεγχος droop", "εύρωστος έλεγχος", "έλεγχος ολίσθησης", "PLL", "προβλεπτικός έλεγχος",
        # HIL variants
        "controller-hardware-in-the-loop", "c-hil", "p-hil", "ψηφιακός δίδυμος"
    ],
    "Turkish": [
        "güç elektroniği", "enerji sistemleri", "yenilenebilir enerji",
        "mikro şebeke", "batarya yönetimi", "enerji depolama",
        "kontrol sistemleri", "otomatik kontrol", "dijital kontrol",
        "gömülü sistemler", "gerçek zamanlı simülasyon",
        "elektrik mühendisliği", "mekatronik", "enstrümantasyon",
        "rüzgar enerjisi", "güneş enerjisi", "fotovoltaik", "yakıt hücreleri",
        # Additional power electronics & energy terms
        "DC-DC", "AC-DC", "dc-dc dönüştürücü", "aktif güç", "reaktif güç", "sanal atalet", "aktif sönümleme", "koruma rölesi",
        "yardımcı hizmetler", "asenkron jeneratör", "batarya depolama", "volan", "serpiştirme",
        "çift yönlü", "çift yönlü şarj cihazı", "BLDC", "boost dönüştürücü", "BMS", "MPPT",
        "dağıtılmış üretim", "DER", "DSP", "dual active bridge", "DAB", "elektrikli araç", "EV", "HEV", "toprak arızası", "aşırı gerilim",
        "düşük gerilim", "elektrikli tahrik", "enerji yönetimi", "harmonikler", "harmonik telafisi", "dspace", "opal-rt", "Speedgoat", "plecs",
        "DIgSILENT", "PowerFactory", "PSCAD", "RTDS", "etap", "neplan", "opendss", "psim", "Simscape Electrical", "rt-lab", "hypersim", "ltspice",
        "arıza koruması", "IEC 61850", "UPS", "IEEE 1547-2018", "ara bağlantı", "IGBT", "MOSFET", "asenkron motor",
        "admitans", "empedans", "iletkenlik", "süseptans", "reaktans", "ada tespit", "anti-islanding", "modüler çok seviyeli dönüştürücü",
        "MMC", "çok seviyeli evirici", "şebeke uyum", "kısmi gölgeleme", "plug-in elektrik", "güç akışı", "güç kalitesi", "THD", "aktif filtre",
        "Z-source", "PMSM", "senkron motor", "kısa devre analizi", "SOC dengeleme", "şarj durumu", "sanal senkron jeneratör", "vehicle-to-grid",
        "grid-to-vehicle", "gerilim kaynaklı evirici", "gerilim regülasyonu", "sistem kararlılığı", "WAMS", "rüzgar türbini",
        # Control
        "droop kontrol", "gürbüz kontrol", "kayma modu kontrol", "PLL", "öngörülü kontrol",
        # HIL variants
        "controller-hardware-in-the-loop", "c-hil", "p-hil", "dijital ikiz"
    ],
    "Albanian": [
        "elektronika e fuqisë", "sistemet energjetike", "energji e rinovueshme",
        "rrjet mikro", "menaxhimi i baterive", "ruajtja e energjisë",
        "sistemet e kontrollit", "kontroll automatik", "kontroll dixhital",
        "sistemet e integruara", "simulim në kohë reale",
        "inxhinieri elektrike", "mekatronikë", "instrumentacion",
        "energji e erës", "energji diellore", "fotovoltaike", "qelizat e karburantit",
        # Additional power electronics & energy terms
        "DC-DC", "AC-DC", "konvertues dc-dc", "fuqi aktive", "fuqi reaktive", "inerci virtuale", "zhdëmtim aktiv", "rele mbrojtëse",
        "shërbime ndihmëse", "gjenerator asinkron", "ruajtje bateri", "fligji", "ndërthurur",
        "dykahësh", "karikues dykahësh", "BLDC", "konvertues boost", "BMS", "MPPT",
        "gjenerim i shpërndarë", "DER", "DSP", "dual active bridge", "DAB", "mjet elektrik", "EV", "HEV", "defekt toke", "mbitension",
        "nëntension", "përcjellje elektrike", "menaxhim energjie", "harmonikë", "kompensim harmonik", "dspace", "opal-rt", "Speedgoat", "plecs",
        "DIgSILENT", "PowerFactory", "PSCAD", "RTDS", "etap", "neplan", "opendss", "psim", "Simscape Electrical", "rt-lab", "hypersim", "ltspice",
        "mbrojtje defekti", "IEC 61850", "UPS", "IEEE 1547-2018", "ndërlidhje", "IGBT", "MOSFET", "motor asinkron",
        "admitancë", "impedancë", "konduktancë", "susceptancë", "reaktancë", "zbulim ishull", "anti-islanding", "konvertues modular shumënivelit",
        "MMC", "inverter shumënivelit", "pajtueshmëri rrjeti", "hijezim i pjesshëm", "plug-in elektrik", "rrjedhje fuqie", "cilësi fuqie", "THD", "filtër aktiv",
        "Z-source", "PMSM", "motor sinkron", "analizë qarku të shkurtër", "ekuilibrim SOC", "gjendje ngarkese", "gjenerator sinkron virtual", "vehicle-to-grid",
        "grid-to-vehicle", "inverter tensioni", "rregullim tensioni", "stabilitet sistemi", "WAMS", "turbinë ere",
        # Control
        "kontroll droop", "kontroll i fortë", "kontroll sliding mode", "PLL", "kontroll parashikues",
        # HIL variants
        "controller-hardware-in-the-loop", "c-hil", "p-hil", "binjak dixhital"
    ],
    "Armenian": [
        "հզորության էլեկտրոնիկա", "էներգետիկ համակարգեր", "վերականգնվող էներգիա",
        "միկրոցանց", "մարտկոցների կառավարում", "էներգիայի պահպանում",
        "կառավարման համակարգեր", "ավտոմատ կառավարում",
        "ներկառուցված համակարգեր", "իրական ժամանակի մոդելավորում",
        "էլեկտրատեխնիկա", "մեխատրոնիկա",
        "քամու էներգիա", "արևային էներգիա", "ֆոտովոլտային",
        # Universal terms
        "DC-DC", "AC-DC", "BLDC", "BMS", "MPPT", "DER", "DSP", "DAB", "EV", "HEV", "IGBT", "MOSFET",
        "MMC", "THD", "PMSM", "PLL", "dspace", "opal-rt", "Speedgoat", "plecs", "DIgSILENT", "PowerFactory",
        "PSCAD", "RTDS", "etap", "neplan", "opendss", "psim", "Simscape Electrical", "rt-lab", "hypersim",
        "ltspice", "IEC 61850", "UPS", "IEEE 1547-2018", "Z-source", "WAMS", "c-hil", "p-hil",
        "hardware-in-the-loop", "controller-hardware-in-the-loop", "dual active bridge", "vehicle-to-grid",
        "grid-to-vehicle", "anti-islanding", "boost converter"
    ],
    "Belarusian": [
        "сілавая электроніка", "энергетычныя сістэмы", "аднаўляльная энергія",
        "мікрасетка", "кіраванне батарэямі", "захоўванне энергіі",
        "сістэмы кіравання", "аўтаматычнае кіраванне",
        "убудаваныя сістэмы", "мадэляванне ў рэжыме рэальнага часу",
        "электратэхніка", "мехатроніка",
        "ветраная энергія", "сонечная энергія", "фотавальтаіка",
        # Universal terms
        "DC-DC", "AC-DC", "BLDC", "BMS", "MPPT", "DER", "DSP", "DAB", "EV", "HEV", "IGBT", "MOSFET",
        "MMC", "THD", "PMSM", "PLL", "dspace", "opal-rt", "Speedgoat", "plecs", "DIgSILENT", "PowerFactory",
        "PSCAD", "RTDS", "etap", "neplan", "opendss", "psim", "Simscape Electrical", "rt-lab", "hypersim",
        "ltspice", "IEC 61850", "UPS", "IEEE 1547-2018", "Z-source", "WAMS", "c-hil", "p-hil",
        "hardware-in-the-loop", "controller-hardware-in-the-loop", "dual active bridge", "vehicle-to-grid",
        "grid-to-vehicle", "anti-islanding", "boost converter"
    ],
    "Bulgarian": [
        "силова електроника", "енергийни системи", "възобновяема енергия",
        "микромрежа", "управление на батерии", "съхранение на енергия",
        "системи за управление", "автоматично управление", "цифрово управление",
        "вградени системи", "симулация в реално време",
        "електротехника", "мехатроника", "инструментация",
        "вятърна енергия", "слънчева енергия", "фотоволтаици", "горивни клетки",
        # Universal terms
        "DC-DC", "AC-DC", "BLDC", "BMS", "MPPT", "DER", "DSP", "DAB", "EV", "HEV", "IGBT", "MOSFET",
        "MMC", "THD", "PMSM", "PLL", "dspace", "opal-rt", "Speedgoat", "plecs", "DIgSILENT", "PowerFactory",
        "PSCAD", "RTDS", "etap", "neplan", "opendss", "psim", "Simscape Electrical", "rt-lab", "hypersim",
        "ltspice", "IEC 61850", "UPS", "IEEE 1547-2018", "Z-source", "WAMS", "c-hil", "p-hil"
    ],
    "Croatian": [
        "energetska elektronika", "energetski sustavi", "obnovljiva energija",
        "mikromreža", "upravljanje baterijama", "pohrana energije",
        "sustavi upravljanja", "automatsko upravljanje", "digitalno upravljanje",
        "ugrađeni sustavi", "simulacija u stvarnom vremenu",
        "elektrotehnika", "mehatronika", "instrumentacija",
        "energija vjetra", "solarna energija", "fotonaponski", "gorivne ćelije",
        # Universal terms
        "DC-DC", "AC-DC", "BLDC", "BMS", "MPPT", "DER", "DSP", "DAB", "EV", "HEV", "IGBT", "MOSFET",
        "MMC", "THD", "PMSM", "PLL", "dspace", "opal-rt", "Speedgoat", "plecs", "DIgSILENT", "PowerFactory",
        "PSCAD", "RTDS", "etap", "neplan", "opendss", "psim", "Simscape Electrical", "rt-lab", "hypersim",
        "ltspice", "IEC 61850", "UPS", "IEEE 1547-2018", "Z-source", "WAMS", "c-hil", "p-hil"
    ],
    "Estonian": [
        "võimelektroonika", "energiasüsteemid", "taastuv energia",
        "mikrovõrk", "akude haldamine", "energia salvestamine",
        "juhtimissüsteemid", "automaatjuhtimine", "digitaaljuhtimine",
        "süsteemsed süsteemid", "reaalajas simuleerimine",
        "elektrotehnika", "mehatroonika", "instrumentatsioon",
        "tuuleenergia", "päikeseenergia", "fotovoltaika", "kütuseelemendid",
        # Universal terms
        "DC-DC", "AC-DC", "BLDC", "BMS", "MPPT", "DER", "DSP", "DAB", "EV", "HEV", "IGBT", "MOSFET",
        "MMC", "THD", "PMSM", "PLL", "dspace", "opal-rt", "Speedgoat", "plecs", "DIgSILENT", "PowerFactory",
        "PSCAD", "RTDS", "etap", "neplan", "opendss", "psim", "Simscape Electrical", "rt-lab", "hypersim",
        "ltspice", "IEC 61850", "UPS", "IEEE 1547-2018", "Z-source", "WAMS", "c-hil", "p-hil"
    ],
    "Georgian": [
        "სიმძლავრის ელექტრონიკა", "ენერგეტიკული სისტემები", "განახლებადი ენერგია",
        "მიკროქსელი", "ბატარეების მართვა", "ენერგიის შენახვა",
        "კონტროლის სისტემები", "ავტომატური კონტროლი",
        "ჩაშენებული სისტემები", "რეალურ დროში სიმულაცია",
        "ელექტროტექნიკა", "მეხატრონიკა",
        "ქარის ენერგია", "მზის ენერგია", "ფოტოელექტრული",
        # Universal terms
        "DC-DC", "AC-DC", "BLDC", "BMS", "MPPT", "DER", "DSP", "DAB", "EV", "HEV", "IGBT", "MOSFET",
        "MMC", "THD", "PMSM", "PLL", "dspace", "opal-rt", "Speedgoat", "plecs", "DIgSILENT", "PowerFactory",
        "PSCAD", "RTDS", "etap", "neplan", "opendss", "psim", "Simscape Electrical", "rt-lab", "hypersim",
        "ltspice", "IEC 61850", "UPS", "IEEE 1547-2018", "Z-source", "WAMS", "c-hil", "p-hil"
    ],
    "Hungarian": [
        "teljesítményelektronika", "energiarendszerek", "megújuló energia",
        "mikrohálózat", "akkumulátor kezelés", "energiatárolás",
        "vezérlőrendszerek", "automatikus vezérlés", "digitális vezérlés",
        "beágyazott rendszerek", "valós idejű szimuláció",
        "villamosmérnöki", "mechatronika", "műszerezés",
        "szélenergia", "napenergia", "fotovoltaikus", "üzemanyagcellák",
        # Universal terms
        "DC-DC", "AC-DC", "BLDC", "BMS", "MPPT", "DER", "DSP", "DAB", "EV", "HEV", "IGBT", "MOSFET",
        "MMC", "THD", "PMSM", "PLL", "dspace", "opal-rt", "Speedgoat", "plecs", "DIgSILENT", "PowerFactory",
        "PSCAD", "RTDS", "etap", "neplan", "opendss", "psim", "Simscape Electrical", "rt-lab", "hypersim",
        "ltspice", "IEC 61850", "UPS", "IEEE 1547-2018", "Z-source", "WAMS", "c-hil", "p-hil"
    ],
    "Icelandic": [
        "aflrafeindatækni", "orkukerfi", "endurnýjanleg orka",
        "örnet", "rafhlöðustjórnun", "orkugeymsla",
        "stýrikerfi", "sjálfvirk stýring", "stafræn stýring",
        "innbyggð kerfi", "rauntíma hermir",
        "rafmagnsverkfræði", "véltækni", "mælitækni",
        "vindorka", "sólarorka", "ljósrafafl", "eldsneytiselda",
        # Universal terms
        "DC-DC", "AC-DC", "BLDC", "BMS", "MPPT", "DER", "DSP", "DAB", "EV", "HEV", "IGBT", "MOSFET",
        "MMC", "THD", "PMSM", "PLL", "dspace", "opal-rt", "Speedgoat", "plecs", "DIgSILENT", "PowerFactory",
        "PSCAD", "RTDS", "etap", "neplan", "opendss", "psim", "Simscape Electrical", "rt-lab", "hypersim",
        "ltspice", "IEC 61850", "UPS", "IEEE 1547-2018", "Z-source", "WAMS", "c-hil", "p-hil"
    ],
    "Latvian": [
        "jaudas elektronika", "enerģijas sistēmas", "atjaunojamā enerģija",
        "mikrotīkls", "akumulatoru pārvaldība", "enerģijas uzglabāšana",
        "vadības sistēmas", "automātiskā vadība", "digitālā vadība",
        "iegultās sistēmas", "reāllaika simulācija",
        "elektrotehnika", "mehatronika", "instrumentācija",
        "vēja enerģija", "saules enerģija", "fotovoltaiskais", "degvielas šūnas",
        # Universal terms
        "DC-DC", "AC-DC", "BLDC", "BMS", "MPPT", "DER", "DSP", "DAB", "EV", "HEV", "IGBT", "MOSFET",
        "MMC", "THD", "PMSM", "PLL", "dspace", "opal-rt", "Speedgoat", "plecs", "DIgSILENT", "PowerFactory",
        "PSCAD", "RTDS", "etap", "neplan", "opendss", "psim", "Simscape Electrical", "rt-lab", "hypersim",
        "ltspice", "IEC 61850", "UPS", "IEEE 1547-2018", "Z-source", "WAMS", "c-hil", "p-hil"
    ],
    "Lithuanian": [
        "galios elektronika", "energijos sistemos", "atsinaujinanti energija",
        "mikrotinklas", "baterijų valdymas", "energijos saugojimas",
        "valdymo sistemos", "automatinis valdymas", "skaitmeninis valdymas",
        "įterptinės sistemos", "realaus laiko modeliavimas",
        "elektrotechnika", "mechatronika", "prietaisai",
        "vėjo energija", "saulės energija", "fotovoltinis", "kuro elementai",
        # Universal terms
        "DC-DC", "AC-DC", "BLDC", "BMS", "MPPT", "DER", "DSP", "DAB", "EV", "HEV", "IGBT", "MOSFET",
        "MMC", "THD", "PMSM", "PLL", "dspace", "opal-rt", "Speedgoat", "plecs", "DIgSILENT", "PowerFactory",
        "PSCAD", "RTDS", "etap", "neplan", "opendss", "psim", "Simscape Electrical", "rt-lab", "hypersim",
        "ltspice", "IEC 61850", "UPS", "IEEE 1547-2018", "Z-source", "WAMS", "c-hil", "p-hil"
    ],
    "Romanian": [
        "electronică de putere", "sisteme energetice", "energie regenerabilă",
        "microreţea", "gestionarea bateriilor", "stocare energie",
        "sisteme de control", "control automat", "control digital",
        "sisteme embedded", "simulare în timp real",
        "inginerie electrică", "mecatronică", "instrumentaţie",
        "energie eoliană", "energie solară", "fotovoltaică", "celule combustibil",
        # Universal terms
        "DC-DC", "AC-DC", "BLDC", "BMS", "MPPT", "DER", "DSP", "DAB", "EV", "HEV", "IGBT", "MOSFET",
        "MMC", "THD", "PMSM", "PLL", "dspace", "opal-rt", "Speedgoat", "plecs", "DIgSILENT", "PowerFactory",
        "PSCAD", "RTDS", "etap", "neplan", "opendss", "psim", "Simscape Electrical", "rt-lab", "hypersim",
        "ltspice", "IEC 61850", "UPS", "IEEE 1547-2018", "Z-source", "WAMS", "c-hil", "p-hil"
    ],
    "Serbian": [
        "elektronika snage", "energetski sistemi", "obnovljiva energija",
        "mikromreža", "upravljanje baterijama", "skladištenje energije",
        "kontrolni sistemi", "automatska kontrola", "digitalna kontrola",
        "ugrađeni sistemi", "simulacija u realnom vremenu",
        "elektrotehnika", "mehatronika", "instrumentacija",
        "energija vetra", "solarna energija", "fotonaponska", "gorivne ćelije",
        # Universal terms
        "DC-DC", "AC-DC", "BLDC", "BMS", "MPPT", "DER", "DSP", "DAB", "EV", "HEV", "IGBT", "MOSFET",
        "MMC", "THD", "PMSM", "PLL", "dspace", "opal-rt", "Speedgoat", "plecs", "DIgSILENT", "PowerFactory",
        "PSCAD", "RTDS", "etap", "neplan", "opendss", "psim", "Simscape Electrical", "rt-lab", "hypersim",
        "ltspice", "IEC 61850", "UPS", "IEEE 1547-2018", "Z-source", "WAMS", "c-hil", "p-hil"
    ],
    "Slovak": [
        "výkonová elektronika", "energetické systémy", "obnoviteľná energia",
        "mikrosieť", "správa batérií", "skladovanie energie",
        "riadiace systémy", "automatické riadenie", "digitálne riadenie",
        "vstavaný systémy", "simulácia v reálnom čase",
        "elektrotechnika", "mechatronika", "prístrojová technika",
        "veterná energia", "solárna energia", "fotovoltaika", "palivové články",
        # Universal terms
        "DC-DC", "AC-DC", "BLDC", "BMS", "MPPT", "DER", "DSP", "DAB", "EV", "HEV", "IGBT", "MOSFET",
        "MMC", "THD", "PMSM", "PLL", "dspace", "opal-rt", "Speedgoat", "plecs", "DIgSILENT", "PowerFactory",
        "PSCAD", "RTDS", "etap", "neplan", "opendss", "psim", "Simscape Electrical", "rt-lab", "hypersim",
        "ltspice", "IEC 61850", "UPS", "IEEE 1547-2018", "Z-source", "WAMS", "c-hil", "p-hil"
    ],
    "Slovenian": [
        "močnostna elektronika", "energetski sistemi", "obnovljiva energija",
        "mikromrežo", "upravljanje baterij", "shranjevanje energije",
        "krmilni sistemi", "avtomatsko krmiljenje", "digitalno krmiljenje",
        "vdelani sistemi", "simulacija v realnem času",
        "elektrotehniko", "mehatronika", "instrumentacija",
        "energija vetra", "sončna energija", "fotovoltaika", "gorivne celice",
        # Universal terms
        "DC-DC", "AC-DC", "BLDC", "BMS", "MPPT", "DER", "DSP", "DAB", "EV", "HEV", "IGBT", "MOSFET",
        "MMC", "THD", "PMSM", "PLL", "dspace", "opal-rt", "Speedgoat", "plecs", "DIgSILENT", "PowerFactory",
        "PSCAD", "RTDS", "etap", "neplan", "opendss", "psim", "Simscape Electrical", "rt-lab", "hypersim",
        "ltspice", "IEC 61850", "UPS", "IEEE 1547-2018", "Z-source", "WAMS", "c-hil", "p-hil"
    ],
    "Ukrainian": [
        "силова електроніка", "енергетичні системи", "відновлювана енергія",
        "мікромережа", "управління батареями", "зберігання енергії",
        "системи керування", "автоматичне керування", "цифрове керування",
        "вбудовані системи", "моделювання в реальному часі",
        "електротехніка", "мехатроніка", "приладобудування",
        "вітрова енергія", "сонячна енергія", "фотовольтаїка", "паливні елементи",
        # Universal terms
        "DC-DC", "AC-DC", "BLDC", "BMS", "MPPT", "DER", "DSP", "DAB", "EV", "HEV", "IGBT", "MOSFET",
        "MMC", "THD", "PMSM", "PLL", "dspace", "opal-rt", "Speedgoat", "plecs", "DIgSILENT", "PowerFactory",
        "PSCAD", "RTDS", "etap", "neplan", "opendss", "psim", "Simscape Electrical", "rt-lab", "hypersim",
        "ltspice", "IEC 61850", "UPS", "IEEE 1547-2018", "Z-source", "WAMS", "c-hil", "p-hil"
    ],
    "Macedonian": [
        "моќна електроника", "енергетски системи", "обновлива енергија",
        "микромрежа", "управување со батерии", "складирање на енергија",
        "контролни системи", "автоматска контрола", "дигитална контрола",
        "вградени системи", "симулација во реално време",
        "електротехника", "мехатроника", "инструментација",
        "енергија од ветер", "соларна енергија", "фотоволтаика", "горивни ќелии",
        # Universal terms
        "DC-DC", "AC-DC", "BLDC", "BMS", "MPPT", "DER", "DSP", "DAB", "EV", "HEV", "IGBT", "MOSFET",
        "MMC", "THD", "PMSM", "PLL", "dspace", "opal-rt", "Speedgoat", "plecs", "DIgSILENT", "PowerFactory",
        "PSCAD", "RTDS", "etap", "neplan", "opendss", "psim", "Simscape Electrical", "rt-lab", "hypersim",
        "ltspice", "IEC 61850", "UPS", "IEEE 1547-2018", "Z-source", "WAMS", "c-hil", "p-hil"
    ],
    "English": [
        # Same as KEYWORDS_INCLUDE - for UK/Ireland/Malta
        "power electronics", "energy systems", "renewable energy", "sustainable power",
        "battery management", "bms", "energy storage", "power conversion",
        "microgrid", "smart grid", "powertrain", "drives", "electric drives",
        "hydrogen systems", "fuel cell", "photovoltaics", "solar energy", "wind energy",
        "DC-DC", "AC-DC", "DC‑DC converter", "active power", "reactive power", "virtual inertia", "active damping", "protection relay",
        "Ancillary services", "Asynchronous generator", "battery energy storage", "flywheel", "interleaved",
        "Bidirectional", "bidirectional charger", "BLDC", "Boost converter", "BMS", "battery management system", "MPPT",
        "distributed generation", "DER", "DSP", "dual active bridge", "DAB", "electric vehicle", "EV", "HEV", "ground fault", "overvoltage",
        "undervoltage", "electric propulsion", "energy management", "harmonic", "harmonic compensation", "dspace", "opal-rt", "Speedgoat", "plecs",
        "DIgSILENT", "PowerFactory", "PSCAD", "RTDS", "etap", "neplan", "opendss", "psim", "Simscape Electrical", "rt-lab", "hypersim", "ltspice",
        "fault protection", "IEC 61850", "UPS", "IEEE 1547-2018", "interconnection", "IGBT", "MOSFET", "induction motor",
        "admittance", "impedance", "conductance", "susceptance", "reactance", "islanding detection", "anti-islanding", "modular multilevel converter",
        "MMC", "multilevel inverter", "grid compliance", "partial shading", "Plug‑in electric", "power flow", "power quality", "THD", "active filter",
        "Z‑source", "PMSM", "synchronous motor", "Short‑circuit analysis", "SOC balancing", "state‑of‑charge", "virtual synchronous generator", "Vehicle‑to‑grid",
        "grid‑to‑vehicle", "Voltage‑source inverter", "voltage regulation", "power system stability", "WAMS", "wind turbine",
        "control systems", "automatic control", "digital control",
        "droop", "robust control", "sliding mode control", "PLL", "model predictive control",
        "embedded systems", "real-time simulation", "hardware-in-the-loop", "Controller‑hardware‑in‑the‑loop", "hil", "c-hil", "p-hil",
        "cyber-physical systems", "digital twin",
        "electrical engineering", "mechatronics", "instrumentation", "converter design",
        "power systems", "grid integration", "high voltage", "hvdc"
    ]
}

# ---------------------------
# COUNTRY → LANGUAGE MAPPING
# ---------------------------

COUNTRY_LANGUAGE = {
    "Albania": "Albanian",
    "Armenia": "Armenian",
    "Austria": "German",
    "Belarus": "Belarusian",
    "Belgium": "French",  # Also Dutch, but French more common for universities
    "Bosnia and Herzegovina": "Serbian",  # Also Croatian, Bosnian
    "Bulgaria": "Bulgarian",
    "Croatia": "Croatian",
    "Cyprus": "Greek",
    "Czech Republic": "Czech",
    "Czechia": "Czech",
    "Denmark": "Danish",
    "Estonia": "Estonian",
    "Finland": "Finnish",
    "Georgia": "Georgian",
    "Germany": "German",
    "Greece": "Greek",
    "Hungary": "Hungarian",
    "Iceland": "Icelandic",
    "Ireland": "English",
    "Italy": "Italian",
    "Kosovo": "Serbian",  # Also Albanian
    "Latvia": "Latvian",
    "Lithuania": "Lithuanian",
    "Luxembourg": "French",  # Also German, Luxembourgish
    "Malta": "English",
    "Moldova": "Romanian",
    "Montenegro": "Serbian",
    "Netherlands": "Dutch",
    "North Macedonia": "Macedonian",
    "Norway": "Norwegian",
    "Poland": "Polish",
    "Portugal": "Portuguese",
    "Romania": "Romanian",
    "Serbia": "Serbian",
    "Slovakia": "Slovak",
    "Slovenia": "Slovenian",
    "Spain": "Spanish",
    "Sweden": "Swedish",
    "Switzerland": "German",  # Also French, Italian
    "Turkey": "Turkish",
    "Tuerkiye": "Turkish",
    "Ukraine": "Ukrainian",
    "United Kingdom": "English"
}

