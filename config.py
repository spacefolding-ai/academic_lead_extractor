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

# HTTP retry settings
MAX_RETRIES = 3  # number of retry attempts for failed HTTP requests
RETRY_DELAY = 1.0  # initial retry delay in seconds (exponential backoff)

# AI Token Pricing (per 1M tokens) - Updated as of 2024
AI_PRICING = {
    "gpt-4o-mini": {
        "input": 0.150,   # $0.150 per 1M input tokens
        "output": 0.600   # $0.600 per 1M output tokens
    },
    "gpt-4o": {
        "input": 2.50,    # $2.50 per 1M input tokens
        "output": 10.00   # $10.00 per 1M output tokens
    }
}

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

    # Control & Automation
    "control systems", "automatic control", "digital control",
    "droop", "robust control", "sliding mode control", "PLL", "model predictive control", "motion control",

    # Embedded / Real-Time / Simulation
    "embedded systems", "real-time simulation", "hardware-in-the-loop", "Controller‑hardware‑in‑the‑loop", "hil", "c-hil", "p-hil",
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

# Import multilingual keywords from separate file for better maintainability
from keywords_multilingual import KEYWORDS_BY_LANGUAGE, COUNTRY_LANGUAGE

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
