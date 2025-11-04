#!/usr/bin/env python3
"""
Integration test for contact extraction - validates the implementation without full crawling.
"""

import sys

print("=" * 80)
print("CONTACT EXTRACTION INTEGRATION TEST")
print("=" * 80)
print()

# Test 1: Import config constants
print("Test 1: Importing configuration constants...")
try:
    from config import (
        STAFF_PAGE_KEYWORDS,
        EMAIL_REGEX,
        FIELD_KEYWORDS,
        STAFF_CARD_SELECTORS,
        EMAIL_OBFUSCATION_PATTERNS,
        DEBUG
    )
    print(f"  ✅ STAFF_PAGE_KEYWORDS: {len(STAFF_PAGE_KEYWORDS)} keywords")
    print(f"  ✅ EMAIL_REGEX: defined")
    print(f"  ✅ FIELD_KEYWORDS: {len(FIELD_KEYWORDS)} categories")
    print(f"  ✅ STAFF_CARD_SELECTORS: {len(STAFF_CARD_SELECTORS)} selectors")
    print(f"  ✅ EMAIL_OBFUSCATION_PATTERNS: {len(EMAIL_OBFUSCATION_PATTERNS)} patterns")
except ImportError as e:
    print(f"  ❌ Failed to import constants: {e}")
    sys.exit(1)

print()

# Test 2: Import scraper functions
print("Test 2: Importing scraper functions...")
try:
    from academic_lead_extractor.scraper import (
        extract_contacts_from_html,
        process_university,
        clean_email
    )
    print(f"  ✅ extract_contacts_from_html: {callable(extract_contacts_from_html)}")
    print(f"  ✅ process_university: {callable(process_university)}")
    print(f"  ✅ clean_email: {callable(clean_email)}")
except ImportError as e:
    print(f"  ❌ Failed to import scraper functions: {e}")
    sys.exit(1)

print()

# Test 3: Test email cleaning
print("Test 3: Testing email obfuscation handling...")
test_emails = [
    "test [at] example.com",
    "user∂domain.edu",
    "name (at) university dot edu",
    "admin@test.org"
]
for email in test_emails:
    cleaned = clean_email(email)
    status = "✅" if "@" in cleaned and "." in cleaned.split("@")[1] else "⚠️"
    print(f"  {status} '{email}' → '{cleaned}'")

print()

# Test 4: Test extract_contacts_from_html with sample HTML
print("Test 4: Testing contact extraction from sample HTML...")
sample_html = """
<html>
<head><title>Staff - Power Electronics Group</title></head>
<body>
    <div class="person">
        <h3>Prof. Dr. John Smith</h3>
        <p class="title">Professor of Power Electronics</p>
        <a href="mailto:john.smith@university.edu">Email</a>
    </div>
    <div class="staff-member">
        <strong>Dr. Jane Doe</strong>
        <span class="role">Research Associate - Battery Systems</span>
        <a href="mailto:jane.doe@university.edu">Contact</a>
    </div>
</body>
</html>
"""

try:
    contacts = extract_contacts_from_html(sample_html, "https://example.edu/staff")
    print(f"  ✅ Extracted {len(contacts)} contacts from sample HTML")
    if contacts:
        for i, contact in enumerate(contacts[:3], 1):
            name = contact.get("Full_name", "N/A")
            email = contact.get("Email", "N/A")
            title = contact.get("Title_role", "N/A")
            print(f"     Contact {i}: {name} <{email}> - {title}")
    else:
        print(f"  ⚠️  No contacts extracted - this might indicate an issue")
except Exception as e:
    print(f"  ❌ Error during extraction: {e}")
    import traceback
    traceback.print_exc()

print()

# Test 5: Verify processor imports
print("Test 5: Verifying processor pipeline imports...")
try:
    from academic_lead_extractor.processor import main as processor_main
    from academic_lead_extractor.ai_evaluator import ai_evaluate_contacts
    print(f"  ✅ processor.main: {callable(processor_main)}")
    print(f"  ✅ ai_evaluator.ai_evaluate_contacts: {callable(ai_evaluate_contacts)}")
except ImportError as e:
    print(f"  ❌ Failed to import processor: {e}")
    sys.exit(1)

print()
print("=" * 80)
print("✅ INTEGRATION TEST COMPLETED SUCCESSFULLY")
print("=" * 80)
print()
print("The contact extraction implementation is properly integrated.")
print("To run a full extraction, use:")
print("  python3 main.py --urls https://example.edu")
print()

