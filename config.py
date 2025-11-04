"""
config.py — Configuration file for Academic Lead Extractor v2
Contains ICP keywords, language mappings, exclusion rules, and script parameters.
"""

# ---------------------------
# SCRIPT CONFIGURATION
# ---------------------------

HEADERS = {"User-Agent": "AcademicLeadExtractorBot/2.0 (contact: your-email@domain.com)"}
SEM_LIMIT = 10  # concurrent HTTP requests per faculty page
UNI_PARALLEL = 5  # number of universities to process in parallel
MAX_FACULTY_LINKS = 50  # max number of 'people/staff' pages to crawl per university (increased for deep exploration)
MAX_DEPARTMENT_LINKS = 15  # max department/institute pages to explore (reduced to manageable size)
AUTOSAVE_INTERVAL = 10  # save extracted data every N universities
TIMEOUT = 15  # request timeout (seconds)
EXPLORE_SUBDOMAINS = True  # Follow department/institute subdomains

# Browser automation settings
USE_BROWSER = False  # Disable browser for stability - aiohttp is much faster and stable
BROWSER_TIMEOUT = 30000  # Playwright timeout in milliseconds (30 seconds)
WAIT_FOR_NETWORK_IDLE = False  # Disabled for better performance - just wait for DOM load

# ---------------------------
# ICP KEYWORD MATCHING
# ---------------------------

# ✅ Primary technical keywords (English) — match against page text, titles, and roles
KEYWORDS_INCLUDE = [
    # Power & Energy Systems
    "power electronics", "energy systems", "renewable energy", "sustainable power",
    "battery management", "bms", "energy storage", "power conversion",
    "microgrid", "smart grid", "powertrain", "drives", "electric drives",
    "hydrogen systems", "fuel cells", "photovoltaics", "solar energy", "wind energy",

    # Control & Automation
    "control systems", "automatic control", "digital control",
    "model predictive control", "motion control", "robust control",

    # Embedded / Real-Time / Simulation
    "embedded systems", "real-time simulation", "hardware-in-the-loop", "hil",
    "cyber-physical systems", "digital twin", "time sensitive networking",

    # Electrical Engineering / Mechatronics
    "electrical engineering", "mechatronics", "instrumentation", "converter design",
    "power systems", "grid integration", "high voltage", "hvdc",
]

# 🚫 Non-ICP keywords — to optionally exclude generic/non-technical roles
KEYWORDS_EXCLUDE = [
    "admissions", "alumni", "library", "marketing", "accounting",
    "finance", "human resources", "corporate relations", "student services",
    "recruitment", "outreach", "administration", "communications",
]

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
        "windenergie", "solarenergie", "photovoltaik", "brennstoffzellen", "wasserstoffsysteme"
    ],
    "Italian": [
        "elettronica di potenza", "sistemi energetici", "energia rinnovabile",
        "microrete", "gestione batterie", "accumulo energia",
        "sistemi di controllo", "controllo automatico", "controllo digitale",
        "sistemi embedded", "simulazione in tempo reale",
        "ingegneria elettrica", "meccatronica", "strumentazione", "sistemi di potenza",
        "energia eolica", "energia solare", "fotovoltaico", "celle a combustibile"
    ],
    "French": [
        "électronique de puissance", "systèmes énergétiques", "énergie renouvelable",
        "microréseau", "gestion de batterie", "stockage d'énergie",
        "systèmes de contrôle", "contrôle automatique", "contrôle numérique",
        "systèmes embarqués", "simulation temps réel",
        "génie électrique", "mécatronique", "instrumentation",
        "énergie éolienne", "énergie solaire", "photovoltaïque", "piles à combustible"
    ],
    "Spanish": [
        "electrónica de potencia", "sistemas energéticos", "energía renovable",
        "microrred", "gestión de baterías", "almacenamiento de energía",
        "sistemas de control", "control automático", "control digital",
        "sistemas embebidos", "simulación en tiempo real",
        "ingeniería eléctrica", "mecatrónica", "instrumentación",
        "energía eólica", "energía solar", "fotovoltaica", "pilas de combustible"
    ],
    "Portuguese": [
        "eletrônica de potência", "sistemas energéticos", "energia renovável",
        "microrede", "gestão de baterias", "armazenamento de energia",
        "sistemas de controle", "controle automático", "controle digital",
        "sistemas embarcados", "simulação em tempo real",
        "engenharia elétrica", "mecatrônica", "instrumentação",
        "energia eólica", "energia solar", "fotovoltaica", "células de combustível"
    ],
    "Dutch": [
        "vermogenselektronica", "energiesystemen", "hernieuwbare energie",
        "microgrid", "batterijbeheer", "energieopslag",
        "regelsystemen", "automatische besturing", "digitale regeling",
        "embedded systemen", "realtime simulatie",
        "elektrotechniek", "mechatronica", "instrumentatie",
        "windenergie", "zonne-energie", "fotovoltaïsche", "brandstofcellen"
    ],
    "Polish": [
        "elektronika mocy", "systemy energetyczne", "energia odnawialna",
        "mikrosieć", "zarządzanie bateriami", "magazynowanie energii",
        "systemy sterowania", "automatyka", "sterowanie cyfrowe",
        "systemy wbudowane", "symulacja czasu rzeczywistego",
        "elektrotechnika", "mechatronika", "oprzyrządowanie",
        "energia wiatrowa", "energia słoneczna", "fotowoltaika", "ogniwa paliwowe"
    ],
    "Czech": [
        "výkonová elektronika", "energetické systémy", "obnovitelná energie",
        "mikrosíť", "správa baterií", "ukládání energie",
        "řídicí systémy", "automatické řízení", "digitální řízení",
        "vestavěné systémy", "simulace v reálném čase",
        "elektrotechnika", "mechatronika", "přístrojová technika",
        "větrná energie", "solární energie", "fotovoltaika", "palivové články"
    ],
    "Swedish": [
        "kraftelektronik", "energisystem", "förnybar energi",
        "mikronät", "batterihantering", "energilagring",
        "styrsystem", "automatisk styrning", "digital styrning",
        "inbyggda system", "realtidssimulering",
        "elektroteknik", "mekatronik", "instrumentering",
        "vindenergi", "solenergi", "fotovoltaik", "bränsleceller"
    ],
    "Norwegian": [
        "kraftelektronikk", "energisystemer", "fornybar energi",
        "mikronett", "batteristyring", "energilagring",
        "kontrollsystemer", "automatisk kontroll", "digital kontroll",
        "innebygde systemer", "sanntidssimulering",
        "elektroteknikk", "mekatronikk", "instrumentering",
        "vindenergi", "solenergi", "fotovoltaisk", "brenselceller"
    ],
    "Danish": [
        "effektelektronik", "energisystemer", "vedvarende energi",
        "mikronet", "batteristyring", "energilagring",
        "kontrolsystemer", "automatisk kontrol", "digital kontrol",
        "indlejrede systemer", "realtidssimulering",
        "elektroteknik", "mekatronik", "instrumentering",
        "vindenergi", "solenergi", "fotovoltaisk", "brændselsceller"
    ],
    "Finnish": [
        "tehoelektroniikka", "energiajärjestelmät", "uusiutuva energia",
        "mikroverkko", "akkujen hallinta", "energian varastointi",
        "säätöjärjestelmät", "automaattinen säätö", "digitaalinen säätö",
        "sulautetut järjestelmät", "reaaliaikasimulointi",
        "sähkötekniikka", "mekatroniikka", "mittaustekniikka",
        "tuulienergia", "aurinkoenergia", "aurinkosähkö", "polttokennot"
    ],
    "Greek": [
        "ηλεκτρονικά ισχύος", "ενεργειακά συστήματα", "ανανεώσιμη ενέργεια",
        "μικροδίκτυο", "διαχείριση μπαταριών", "αποθήκευση ενέργειας",
        "συστήματα ελέγχου", "αυτόματος έλεγχος",
        "ενσωματωμένα συστήματα", "προσομοίωση πραγματικού χρόνου",
        "ηλεκτρολογία", "μηχατρονική", "οργανολογία",
        "αιολική ενέργεια", "ηλιακή ενέργεια", "φωτοβολταϊκά", "κυψέλες καυσίμου"
    ],
    "Turkish": [
        "güç elektroniği", "enerji sistemleri", "yenilenebilir enerji",
        "mikro şebeke", "batarya yönetimi", "enerji depolama",
        "kontrol sistemleri", "otomatik kontrol", "dijital kontrol",
        "gömülü sistemler", "gerçek zamanlı simülasyon",
        "elektrik mühendisliği", "mekatronik", "enstrümantasyon",
        "rüzgar enerjisi", "güneş enerjisi", "fotovoltaik", "yakıt hücreleri"
    ],
    "Albanian": [
        "elektronika e fuqisë", "sistemet energjetike", "energji e rinovueshme",
        "rrjet mikro", "menaxhimi i baterive", "ruajtja e energjisë",
        "sistemet e kontrollit", "kontroll automatik", "kontroll dixhital",
        "sistemet e integruara", "simulim në kohë reale",
        "inxhinieri elektrike", "mekatronikë", "instrumentacion",
        "energji e erës", "energji diellore", "fotovoltaike", "qelizat e karburantit"
    ],
    "Armenian": [
        "հզորության էլեկտրոնիկա", "էներգետիկ համակարգեր", "վերականգնվող էներգիա",
        "միկրոցանց", "մարտկոցների կառավարում", "էներգիայի պահպանում",
        "կառավարման համակարգեր", "ավտոմատ կառավարում",
        "ներկառուցված համակարգեր", "իրական ժամանակի մոդելավորում",
        "էլեկտրատեխնիկա", "մեխատրոնիկա",
        "քամու էներգիա", "արևային էներգիա", "ֆոտովոլտային"
    ],
    "Belarusian": [
        "сілавая электроніка", "энергетычныя сістэмы", "аднаўляльная энергія",
        "мікрасетка", "кіраванне батарэямі", "захоўванне энергіі",
        "сістэмы кіравання", "аўтаматычнае кіраванне",
        "убудаваныя сістэмы", "мадэляванне ў рэжыме рэальнага часу",
        "электратэхніка", "мехатроніка",
        "ветраная энергія", "сонечная энергія", "фотавальтаіка"
    ],
    "Bulgarian": [
        "силова електроника", "енергийни системи", "възобновяема енергия",
        "микромрежа", "управление на батерии", "съхранение на енергия",
        "системи за управление", "автоматично управление", "цифрово управление",
        "вградени системи", "симулация в реално време",
        "електротехника", "мехатроника", "инструментация",
        "вятърна енергия", "слънчева енергия", "фотоволтаици", "горивни клетки"
    ],
    "Croatian": [
        "energetska elektronika", "energetski sustavi", "obnovljiva energija",
        "mikromreža", "upravljanje baterijama", "pohrana energije",
        "sustavi upravljanja", "automatsko upravljanje", "digitalno upravljanje",
        "ugrađeni sustavi", "simulacija u stvarnom vremenu",
        "elektrotehnika", "mehatronika", "instrumentacija",
        "energija vjetra", "solarna energija", "fotonaponski", "gorivne ćelije"
    ],
    "Estonian": [
        "võimelektroonika", "energiasüsteemid", "taastuv energia",
        "mikrovõrk", "akude haldamine", "energia salvestamine",
        "juhtimissüsteemid", "automaatjuhtimine", "digitaaljuhtimine",
        "süsteemsed süsteemid", "reaalajas simuleerimine",
        "elektrotehnika", "mehatroonika", "instrumentatsioon",
        "tuuleenergia", "päikeseenergia", "fotovoltaika", "kütuseelemendid"
    ],
    "Georgian": [
        "სიმძლავრის ელექტრონიკა", "ენერგეტიკული სისტემები", "განახლებადი ენერგია",
        "მიკროქსელი", "ბატარეების მართვა", "ენერგიის შენახვა",
        "კონტროლის სისტემები", "ავტომატური კონტროლი",
        "ჩაშენებული სისტემები", "რეალურ დროში სიმულაცია",
        "ელექტროტექნიკა", "მეხატრონიკა",
        "ქარის ენერგია", "მზის ენერგია", "ფოტოელექტრული"
    ],
    "Hungarian": [
        "teljesítményelektronika", "energiarendszerek", "megújuló energia",
        "mikrohálózat", "akkumulátor kezelés", "energiatárolás",
        "vezérlőrendszerek", "automatikus vezérlés", "digitális vezérlés",
        "beágyazott rendszerek", "valós idejű szimuláció",
        "villamosmérnöki", "mechatronika", "műszerezés",
        "szélenergia", "napenergia", "fotovoltaikus", "üzemanyagcellák"
    ],
    "Icelandic": [
        "aflrafeindatækni", "orkukerfi", "endurnýjanleg orka",
        "örnet", "rafhlöðustjórnun", "orkugeymsla",
        "stýrikerfi", "sjálfvirk stýring", "stafræn stýring",
        "innbyggð kerfi", "rauntíma hermir",
        "rafmagnsverkfræði", "véltækni", "mælitækni",
        "vindorka", "sólarorka", "ljósrafafl", "eldsneytiselda"
    ],
    "Latvian": [
        "jaudas elektronika", "enerģijas sistēmas", "atjaunojamā enerģija",
        "mikrotīkls", "akumulatoru pārvaldība", "enerģijas uzglabāšana",
        "vadības sistēmas", "automātiskā vadība", "digitālā vadība",
        "iegultās sistēmas", "reāllaika simulācija",
        "elektrotehnika", "mehatronika", "instrumentācija",
        "vēja enerģija", "saules enerģija", "fotovoltaiskais", "degvielas šūnas"
    ],
    "Lithuanian": [
        "galios elektronika", "energijos sistemos", "atsinaujinanti energija",
        "mikrotinklas", "baterijų valdymas", "energijos saugojimas",
        "valdymo sistemos", "automatinis valdymas", "skaitmeninis valdymas",
        "įterptinės sistemos", "realaus laiko modeliavimas",
        "elektrotechnika", "mechatronika", "prietaisai",
        "vėjo energija", "saulės energija", "fotovoltinis", "kuro elementai"
    ],
    "Romanian": [
        "electronică de putere", "sisteme energetice", "energie regenerabilă",
        "microreţea", "gestionarea bateriilor", "stocare energie",
        "sisteme de control", "control automat", "control digital",
        "sisteme embedded", "simulare în timp real",
        "inginerie electrică", "mecatronică", "instrumentaţie",
        "energie eoliană", "energie solară", "fotovoltaică", "celule combustibil"
    ],
    "Serbian": [
        "elektronika snage", "energetski sistemi", "obnovljiva energija",
        "mikromreža", "upravljanje baterijama", "skladištenje energije",
        "kontrolni sistemi", "automatska kontrola", "digitalna kontrola",
        "ugrađeni sistemi", "simulacija u realnom vremenu",
        "elektrotehnika", "mehatronika", "instrumentacija",
        "energija vetra", "solarna energija", "fotonaponska", "gorivne ćelije"
    ],
    "Slovak": [
        "výkonová elektronika", "energetické systémy", "obnoviteľná energia",
        "mikrosieť", "správa batérií", "skladovanie energie",
        "riadiace systémy", "automatické riadenie", "digitálne riadenie",
        "vstavaný systémy", "simulácia v reálnom čase",
        "elektrotechnika", "mechatronika", "prístrojová technika",
        "veterná energia", "solárna energia", "fotovoltaika", "palivové články"
    ],
    "Slovenian": [
        "močnostna elektronika", "energetski sistemi", "obnovljiva energija",
        "mikromrežo", "upravljanje baterij", "shranjevanje energije",
        "krmilni sistemi", "avtomatsko krmiljenje", "digitalno krmiljenje",
        "vdelani sistemi", "simulacija v realnem času",
        "elektrotehniko", "mehatronika", "instrumentacija",
        "energija vetra", "sončna energija", "fotovoltaika", "gorivne celice"
    ],
    "Ukrainian": [
        "силова електроніка", "енергетичні системи", "відновлювана енергія",
        "мікромережа", "управління батареями", "зберігання енергії",
        "системи керування", "автоматичне керування", "цифрове керування",
        "вбудовані системи", "моделювання в реальному часі",
        "електротехніка", "мехатроніка", "приладобудування",
        "вітрова енергія", "сонячна енергія", "фотовольтаїка", "паливні елементи"
    ],
    "Macedonian": [
        "моќна електроника", "енергетски системи", "обновлива енергија",
        "микромрежа", "управување со батерии", "складирање на енергија",
        "контролни системи", "автоматска контрола", "дигитална контрола",
        "вградени системи", "симулација во реално време",
        "електротехника", "мехатроника", "инструментација",
        "енергија од ветер", "соларна енергија", "фотоволтаика", "горивни ќелии"
    ],
    "English": [
        # Same as KEYWORDS_INCLUDE - for UK/Ireland/Malta
        "power electronics", "energy systems", "renewable energy", "sustainable power",
        "microgrid", "smart grid", "battery management", "energy storage",
        "control systems", "automatic control", "digital control",
        "embedded systems", "real-time simulation", "hardware-in-the-loop",
        "electrical engineering", "mechatronics", "instrumentation",
        "wind energy", "solar energy", "photovoltaics", "fuel cells"
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

# ---------------------------
# SCRAPER CONFIGURATION
# ---------------------------

# Debug mode for verbose output
DEBUG = True

# Staff page detection keywords (for URL and page title matching)
STAFF_PAGE_KEYWORDS = [
    # English - Academic staff specific
    "/staff/", "/people/", "/faculty/", "/researchers/", "/professors/", 
    "/academics/", "/our-staff/", "/our-people/", "/our-team/",
    "/research-staff/", "/academic-staff/", "/members/",
    # German
    "/mitarbeiter/", "/mitarbeitende/", "/personen/", 
    "/wissenschaftler/", "/professoren/", "/forschende/",
    "lehrstuhl", "arbeitsgruppe",
    # French
    "/personnel/", "/équipe/", "/chercheurs/", "/professeurs/",
    # Italian
    "/personale/", "/ricercatori/", "/professori/",
    # Spanish
    "/investigadores/", "/profesores/",
    # Title keywords (English)
    "academic staff", "research staff", "faculty members", "our researchers",
    "our professors", "team members", "group members",
    "staff", "people", "team", "researchers", "faculty",
    # Title keywords (German)
    "mitarbeiter", "mitarbeitende", "personen", "wissenschaftler", 
    "professoren", "forschende", "team"
]

# URL patterns to exclude from crawling
EXCLUDE_URL_PATTERNS = [
    "/press", "/news", "/events", "/calendar", "/media", "/gallery",
    "/publications", "/papers", "/downloads", "/archive", "/blog",
    "/alumni", "/students", "/courses", "/teaching", "/jobs", "/careers",
    "/contact", "/contacts", "/contact-us", "/get-in-touch",  # Generic contact pages
    "/about/contact", "/general-enquiries", "/enquiries",
    "/admissions", "/apply", "/library", "/accommodation",
    ".pdf", ".jpg", ".png", ".zip", ".doc", ".ppt"
]

# Generic/admin email patterns to exclude (not actual researchers)
# These are substrings that can appear anywhere in the email
EXCLUDE_EMAIL_PATTERNS = [
    "info@", "office@", "admin@", "enquiries@", "enquiry@",
    "press@", "press-office@", "media@", "communications@", "comms@",
    "student@", "students@", "alumni@", "admissions@", "applications@",
    "recruitment@", "hr@", "finance@", "marketing@",
    "library@", "accommodation@", "support@", "help@",
    "general@", "contact@", "reception@", "secretary@", "sec@",
    "events@", "event@", "booking@", "graduation@",
    "internal-", "external-", "public-", "staff-social@"
]

# Crawling limits
MAX_PAGES_PER_DOMAIN = 200  # Maximum pages to crawl per university
MAX_CRAWL_DEPTH = 3  # Maximum recursive depth for crawling

# User agents for rotation (helps avoid blocking)
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
]

# Email obfuscation patterns (regex -> replacement)
EMAIL_OBFUSCATION_PATTERNS = {
    r'\s*\[at\]\s*': '@',
    r'\s*\(at\)\s*': '@',
    r'\s+at\s+': '@',
    r'\s*∂\s*': '@',
    r'\s+dot\s+': '.',
    r'\s*\[dot\]\s*': '.',
    r'\s*\(dot\)\s*': '.',
}

# Comprehensive email regex pattern
EMAIL_REGEX = r'[a-zA-Z0-9][a-zA-Z0-9._%+-]*@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

# CSS selectors for staff/person cards
STAFF_CARD_SELECTORS = [
    ".person", ".staff-member", ".team-member", ".faculty-member",
    ".mitarbeiter", ".employee", ".researcher", ".profile-card",
    ".person-card", ".contact-card", ".vcard", ".staff-card",
    "[itemtype*='Person']", "[data-person]", "[data-staff]"
]

# CSS selectors for job titles/positions
TITLE_HINT_CLASSES = [
    ".title", ".position", ".role", ".job-title", ".designation",
    ".funktion", ".stelle", ".academic-title", ".rank"
]

# Field of study keywords for classification
FIELD_KEYWORDS = {
    "Power Electronics": [
        "power electronics", "power converter", "inverter", "rectifier",
        "dc-dc converter", "ac-dc", "switching power", "pwm"
    ],
    "Electric Drives & Motors": [
        "electric drives", "motor control", "electrical machines",
        "pmsm", "induction motor", "servo drive", "motion control"
    ],
    "Energy Systems": [
        "energy systems", "renewable energy", "smart grid", "microgrid",
        "grid integration", "power systems", "hvdc", "energy storage"
    ],
    "Battery & Storage": [
        "battery", "bms", "battery management", "energy storage",
        "lithium-ion", "battery pack", "cell balancing"
    ],
    "E-Mobility & EVs": [
        "e-mobility", "electric vehicle", "ev", "powertrain",
        "traction drive", "charging", "vehicle electrification"
    ],
    "Embedded & Real-Time": [
        "embedded systems", "real-time", "microcontroller", "firmware",
        "hardware-in-the-loop", "hil", "rapid prototyping", "digital twin"
    ],
    "Control Systems": [
        "control systems", "automatic control", "digital control",
        "model predictive control", "mpc", "robust control", "optimal control"
    ]
}
