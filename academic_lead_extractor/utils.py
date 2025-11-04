"""
Utility functions for text processing and validation.
"""

import re
from typing import List


def clean_email(email: str) -> str:
    """Clean and normalize email addresses."""
    return (
        email.replace(" [at] ", "@")
        .replace(" (at) ", "@")
        .replace(" at ", "@")
        .replace("∂", "@")
        .replace(" dot ", ".")
        .replace(" ", "")
        .strip()
    )


def extract_emails_from_mailto(soup) -> List[str]:
    """Extract email addresses from mailto: links in HTML."""
    emails = set()
    
    # Find all <a> tags with href attribute
    for link in soup.find_all('a', href=True):
        href = link.get('href', '').strip()
        
        # Check if it's a mailto: link
        if href.lower().startswith('mailto:'):
            # Extract email from mailto:email or mailto:email?subject=...
            email_part = href[7:]  # Remove 'mailto:' prefix
            
            # Remove query parameters (everything after ?)
            if '?' in email_part:
                email_part = email_part.split('?')[0]
            
            # Remove any remaining URL encoding
            email_part = email_part.strip()
            
            # Validate it looks like an email
            if '@' in email_part and '.' in email_part.split('@')[1]:
                emails.add(email_part.lower())
    
    return list(emails)


def extract_contact_from_mailto(soup, email: str) -> dict:
    """Extract contact information associated with a mailto: link.
    
    Returns dict with 'name', 'title', and 'context' if found near the mailto: link.
    """
    result = {'name': None, 'title': None, 'context': None}
    
    # Find the mailto: link for this email
    mailto_link = soup.find('a', href=lambda x: x and f'mailto:{email}' in x.lower())
    if not mailto_link:
        return result
    
    # Strategy 1: Get text from the link itself (if it's a name, not the email)
    link_text = mailto_link.get_text(strip=True)
    if link_text and '@' not in link_text and len(link_text) > 2:
        # Check if link text contains name-like content
        if is_likely_person(link_text):
            result['name'] = link_text
    
    # Strategy 2: Look at parent elements (often wrapped in list items, divs, etc.)
    parent = mailto_link.parent
    if parent and not result['name']:
        # Look for nearby headings or strong tags within the same parent
        # Search in a limited scope to avoid getting wrong person's name
        for tag in ['h3', 'h4', 'h5', 'strong', 'b']:
            # Only look within close proximity (same parent or direct siblings)
            heading = parent.find(tag)
            if not heading:
                # Look at previous sibling
                prev_sibling = parent.find_previous_sibling()
                if prev_sibling:
                    heading = prev_sibling.find(tag)
            
            if heading:
                heading_text = heading.get_text(strip=True)
                # Make sure it's close to the email and looks like a person name
                if heading_text and '@' not in heading_text and len(heading_text) < 100:
                    if is_likely_person(heading_text):
                        # Check if this heading is reasonably close (within ~200 chars)
                        if parent.get_text().find(heading_text) < 200:
                            result['name'] = heading_text
                            break
        
        # Look for title/position in nearby text (limited scope)
        parent_text = parent.get_text(strip=True)
        if len(parent_text) < 500:  # Only check if parent is reasonably sized
            # Common title patterns
            title_patterns = [
                r'(Prof\.?\s+Dr\.?\s+[A-Za-z\-]+(?:\s+[A-Za-z\-]+)?)',
                r'(Dr\.?\s+[A-Za-z\-]+(?:\s+[A-Za-z\-]+)?)',
                r'(Professor\s+[A-Za-z\-]+(?:\s+[A-Za-z\-]+)?)',
                r'(Lecturer\s+[A-Za-z\-]+(?:\s+[A-Za-z\-]+)?)',
                r'(Senior\s+Researcher)',
            ]
            for pattern in title_patterns:
                match = re.search(pattern, parent_text, re.IGNORECASE)
                if match:
                    result['title'] = match.group(1).strip()
                    break
    
    # Strategy 3: Look for data attributes (data-name, data-title, etc.)
    if not result['name']:
        for attr in ['data-name', 'data-person', 'data-contact']:
            if mailto_link.get(attr):
                result['name'] = mailto_link.get(attr).strip()
                break
    
    # Strategy 4: Capture broader context (for field/role extraction later)
    # Get text from the parent container (but limit to reasonable size)
    context_parent = mailto_link.parent
    for _ in range(3):  # Go up max 3 levels
        if context_parent and context_parent.parent:
            context_parent = context_parent.parent
        else:
            break
    
    if context_parent:
        context_text = context_parent.get_text(strip=True)
        if len(context_text) < 2000:  # Only if not too large
            result['context'] = context_text
    
    return result


def extract_emails(text: str) -> List[str]:
    """Extract email addresses from text, including obfuscated ones."""
    emails = set()
    
    # Standard email pattern
    emails.update(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text))
    
    # Obfuscated email pattern (common in German universities)
    # Remove HTML tags first to make pattern matching easier
    text_clean = re.sub(r'<[^>]+>', '', text)
    
    # Pattern: "firstname lastname ∂ domain extension"
    # Example: "niels feldmann ∂ kit edu" -> niels.feldmann@kit.edu
    obfuscated_pattern = r'([a-z][a-z0-9\.\-]+)\s+([a-z][a-z0-9\.\-]+)\s*∂\s*([a-z][a-z0-9\.\-]+)\s+([a-z]{2,})\b'
    obfuscated_matches = re.findall(obfuscated_pattern, text_clean, re.IGNORECASE)
    for match in obfuscated_matches:
        # match = (firstname, lastname, domain, extension)
        domain = match[2]
        extension = match[3]
        
        # Skip anti-spam fake domains
        if 'does-not-exist' in domain.lower() or 'invalid' in domain.lower():
            # Extract real domain from the pattern (usually comes after)
            # Look for the actual domain in the same line
            continue
        
        # Create email as firstname.lastname@domain.extension
        email = f"{match[0]}.{match[1]}@{domain}.{extension}"
        # Validate it's a reasonable email (avoid false positives)
        if len(domain) > 1 and len(extension) >= 2:
            emails.add(email.lower())
    
    # Alternative pattern: extract real domain from spam-protected format
    # "firstname lastname ∂does-not-exist.kit edu" -> firstname.lastname@kit.edu
    spam_protected_pattern = r'([a-z][a-z0-9\.\-]+)\s+([a-z][a-z0-9\.\-]+)\s*∂\s*[^\s]*?\.?([a-z][a-z0-9\.\-]{2,})\s+([a-z]{2,})\b'
    spam_matches = re.findall(spam_protected_pattern, text_clean, re.IGNORECASE)
    for match in spam_matches:
        domain = match[2]
        extension = match[3]
        if len(domain) > 2 and 'does' not in domain.lower():
            email = f"{match[0]}.{match[1]}@{domain}.{extension}"
            emails.add(email.lower())
    
    # Alternative obfuscated pattern with "at" instead of @
    at_pattern = r'([a-z][a-z0-9\.\-\_]+)\s+(?:at|AT|\[at\]|\(at\))\s+([a-z0-9\.\-]+\.[a-z]{2,})'
    at_matches = re.findall(at_pattern, text_clean)
    for match in at_matches:
        email = f"{match[0]}@{match[1]}"
        emails.add(email.lower())
    
    return list(emails)


def clean_text(text: str) -> str:
    """Clean and normalize text by removing extra whitespace."""
    return re.sub(r"\s+", " ", text or "").strip()


def is_likely_person(text: str) -> bool:
    """Check if text looks like a person's name."""
    if not text or len(text) < 3:
        return False
    
    # Exclude if it contains email-like patterns
    if '@' in text or '.com' in text or '.edu' in text or '.php' in text:
        return False
    
    # Exclude generic contact labels (case-insensitive)
    generic_labels = [
        'e-mail', 'email', 'mail', 'info', 'contact', 'kontakt',
        'postanschrift', 'anschrift', 'adresse', 'address',
        'team', 'group', 'office', 'büro', 'sekretariat',
        'telefon', 'phone', 'tel', 'fax', 'web', 'website',
        'erreichbar', 'available', 'informationen', 'information',
        'weitere', 'more', 'details', 'verwaltung', 'administration',
        'verwertungsberatung', 'transferprojekte', 'beratung',
        'wir sind erreichbar', 'weitere informationen', 'campusteam',
        'migrants', 'postanschrift'
    ]
    text_lower = text.lower().strip()
    if text_lower in generic_labels:
        return False
    
    # Exclude if it starts with generic prefixes
    generic_prefixes = ['e-mail', 'email', 'mail:', 'info:', 'contact:', 'tel:', 'telefon:', '▶', '►']
    if any(text_lower.startswith(prefix) for prefix in generic_prefixes):
        return False
    
    # Exclude if it contains special symbols
    if any(c in text for c in ['▶', '►', '→', '←', '•', '★', '©', '®', '™']):
        return False
    
    # Good indicators of person names
    has_academic_title = any(title in text for title in ['Dr.', 'Prof.', 'Dr ', 'Prof '])
    
    # If it has an academic title, it's likely a person
    if has_academic_title:
        return True
    
    # Should have at least one space for full names (or be a reasonable single name)
    words = text.split()
    if len(words) == 1:
        # Single word - only accept if it's capitalized and looks like a surname
        if text[0].isupper() and len(text) > 3 and text.isalpha():
            return True
        return False
    
    # Multiple words - check if they look like names
    # Should have at least 2 words, each starting with uppercase
    if len(words) >= 2:
        # Both first and last word should start with capital
        if words[0][0].isupper() and words[-1][0].isupper():
            # Should not be all uppercase (labels)
            if not text.isupper():
                return True
    
    return False


def clean_name(name: str) -> str:
    """Clean extracted name by removing contact info and labels."""
    if not name:
        return ""
    
    # Remove common German honorifics that should be removed (keep Dr., Prof.)
    name = re.sub(r'^(Herr|Frau|Hr\.|Fr\.|Mr\.|Mrs\.|Ms\.)\s+', '', name, flags=re.IGNORECASE)
    
    # Remove contact information patterns
    # Phone numbers
    name = re.sub(r'[Tt]el\.?\s*[:\-]?\s*\+?\d+[\d\s\-\(\)]*', '', name)
    name = re.sub(r'[Tt]elefon\s*[:\-]?\s*\+?\d+[\d\s\-\(\)]*', '', name)
    name = re.sub(r'[Tt]elephone\s*[:\-]?\s*\+?\d+[\d\s\-\(\)]*', '', name)
    name = re.sub(r'\([Tt]el\.?', '', name)
    
    # Email labels
    name = re.sub(r'[Ee]\-?[Mm]ail\s*[:\-]?\s*', '', name)
    name = re.sub(r'[Ee]mail\s*[:\-]?\s*', '', name)
    
    # Common German words that shouldn't be in names
    name = re.sub(r'\b[Bb]itte\b', '', name)
    name = re.sub(r'\b[Ff]ür\b', '', name)
    name = re.sub(r'\b[Uu]nd\b', '', name)
    
    # Remove trailing separators and punctuation
    name = re.sub(r'[,;:\-\.]+$', '', name)
    name = re.sub(r'^[,;:\-\.]+', '', name)
    
    # Remove parenthetical content (often contains contact info)
    name = re.sub(r'\([^)]*\)', '', name)
    
    # Remove multiple spaces and clean
    name = re.sub(r'\s+', ' ', name).strip()
    
    # Extract only the name part (typically 2-4 words, stopping at common separators)
    words = name.split()
    cleaned_words = []
    stop_words = ['tel', 'telefon', 'telephone', 'email', 'e-mail', 'bitte', 'für', 'und']
    
    for word in words:
        word_clean = word.strip(',;:.-')
        if word_clean.lower() in stop_words:
            break
        # Stop if we hit a phone number pattern
        if re.match(r'^\+?\d+[\d\s\-\(\)]*$', word_clean):
            break
        # Stop if we hit an email pattern
        if '@' in word_clean:
            break
        cleaned_words.append(word_clean)
    
    name = ' '.join(cleaned_words)
    
    # Final cleanup
    name = re.sub(r'[,;:\-\.]+$', '', name).strip()
    
    return name

