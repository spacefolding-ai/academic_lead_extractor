"""
AI-powered evaluation for academic contact relevance scoring.
"""

import json
import time
import asyncio
from typing import List, Dict
from collections import defaultdict

from config import (
    KEYWORDS_INCLUDE,
    KEYWORDS_BY_LANGUAGE,
    COUNTRY_LANGUAGE,
    AI_PRICING
)


async def ai_evaluate_contacts(contacts: List[Dict], use_ai: bool, client, ai_model: str, 
                               ai_batch_size: int, ai_min_score: float) -> tuple:
    """Evaluate contacts with AI and add scoring.
    
    Returns:
        tuple: (evaluated_contacts, token_stats) where token_stats is a dict with:
            - total_tokens: total tokens used
            - input_tokens: input tokens used
            - output_tokens: output tokens used
            - estimated_cost: estimated cost in USD
    """
    # Initialize token tracking
    token_stats = {
        "total_tokens": 0,
        "input_tokens": 0,
        "output_tokens": 0,
        "estimated_cost": 0.0
    }
    
    if not use_ai or not contacts:
        # Fallback: multi-language keyword matching
        print(f"🔍 Evaluating {len(contacts)} contacts with keyword matching (multi-language)")
        
        for c in contacts:
            text = (c.get("Title", "") + " " + c.get("Role", "") + " " + c.get("page_text", "")).lower()
            
            # Get keywords for this contact's country/language
            keywords_to_check = list(KEYWORDS_INCLUDE)  # Start with English keywords
            
            # Add language-specific keywords if available
            country = c.get("Country", "")
            if country in COUNTRY_LANGUAGE:
                language = COUNTRY_LANGUAGE[country]
                if language in KEYWORDS_BY_LANGUAGE:
                    keywords_to_check.extend(KEYWORDS_BY_LANGUAGE[language])
            
            # Check if any keyword matches
            matched_keywords = [k for k in keywords_to_check if k.lower() in text]
            relevant = len(matched_keywords) > 0
            
            c["AI_Score"] = 1.0 if relevant else 0.3
            c["AI_Field"] = c.get("Field_of_study", "Unknown")
            if relevant:
                c["AI_Reason"] = f"Keyword match: {', '.join(matched_keywords[:3])}"
            else:
                c["AI_Reason"] = "No ICP keywords found"
        
        # Count matches by language
        by_language = defaultdict(int)
        for c in contacts:
            if c["AI_Score"] >= 0.5:
                country = c.get("Country", "Unknown")
                language = COUNTRY_LANGUAGE.get(country, "English")
                by_language[language] += 1
        
        if by_language:
            print(f"  ✅ Found matches in: {', '.join([f'{lang} ({count})' for lang, count in by_language.items()])}")
        
        return contacts, token_stats

    # Normalize model name (fix common typos for allowed models)
    # Only gpt-4o-mini and gpt-4o are allowed
    model_name_mapping = {
        # Common typos for gpt-4o-mini
        "gpt-4.o-mini": "gpt-4o-mini",
        "gpt-4.1-mini": "gpt-4o-mini",
        "gpt-4o-mini-2024-07-18": "gpt-4o-mini",
        # Common typos for gpt-4o
        "gpt-4.o": "gpt-4o",
        "gpt-4.1": "gpt-4o",
        "gpt-4o-2024-08-06": "gpt-4o",
        "gpt-4o-2024-05-13": "gpt-4o",
        # Current allowed models (pass through unchanged)
        "gpt-4o-mini": "gpt-4o-mini",
        "gpt-4o": "gpt-4o"
    }
    
    # Normalize the model name
    original_model = ai_model
    ai_model_lower = ai_model.lower()
    
    # Check if model name needs normalization
    if ai_model_lower in model_name_mapping:
        normalized_model = model_name_mapping[ai_model_lower]
        if original_model != normalized_model:
            print(f"   ⚠️  Model name corrected: '{original_model}' → '{normalized_model}'")
        ai_model = normalized_model
    
    # Validate model name - only gpt-4o-mini and gpt-4o are allowed
    valid_models = ["gpt-4o-mini", "gpt-4o"]
    if ai_model not in valid_models:
        print(f"❌ Error: Invalid model name '{original_model}'")
        print(f"   Supported models: {', '.join(valid_models)}")
        print(f"   💡 Tip: gpt-4o-mini is recommended (faster, cheaper, works with all API tiers)")
        print(f"   Defaulting to: gpt-4o-mini")
        ai_model = "gpt-4o-mini"
    
    print(f"🤖 Evaluating {len(contacts)} contacts with AI ({ai_model})...")
    
    # Validate client is available
    if not client:
        print("❌ Error: AI client is not available. Cannot evaluate contacts.")
        print("   Check that OPENAI_API_KEY is set in .env file")
        # Return contacts with default scores
        for c in contacts:
            c["AI_Score"] = 0.5
            c["AI_Field"] = c.get("Field_of_study", "Unknown")
            c["AI_Reason"] = "AI client not available"
        return contacts, token_stats
    
    evaluated = []
    total = len(contacts)
    
    for i in range(0, len(contacts), ai_batch_size):
        batch = contacts[i:i + ai_batch_size]
        
        # Build prompt
        items = []
        for idx, c in enumerate(batch):
            page_text = c.get("page_text", "")
            # Include page text up to 10000 chars for better context
            text_snippet = page_text[:10000] if page_text else ""
            
            # Combine Title and Role if available, fallback to Title_role for backward compatibility
            title = c.get("Title", "")
            role = c.get("Role", "")
            title_role_combined = f"{title}, {role}".strip(", ") if title or role else c.get("Title_role", "")
            
            items.append({
                "id": idx,
                "name": c.get("Full_name", "Unknown"),
                "email": c.get("Email", ""),
                "title": title,
                "role": role or title_role_combined,
                "text": text_snippet
            })
            
            # Warn if page text is very short (might affect scoring)
            if len(text_snippet) < 100 and idx == 0:
                print(f"   ⚠️  Warning: First contact has very short page text ({len(text_snippet)} chars)")
                print(f"      This might affect AI scoring quality.")

        prompt = f"""You are an expert at qualifying academic contacts for power electronics and energy systems research.

For each person below, evaluate their relevance. A person is relevant if their field of study or research is in: power electronics, 
energy systems, smart grids, renewable energy, real-time simulation, embedded systems, electrical machines, 
battery systems, EVs, or related domains.

Return a JSON object with a "contacts" array. Each contact should have:
- id (number, same as input)
- relevant (boolean)
- score (number 0.0-1.0, confidence level)
- reason (string, brief explanation)
- field (string, specific technical domain)
- cleaned_name (string, extract and clean the person's name from the input)
- role (string, extract and clean the person's role/position from the text - e.g., "Head of Research Group", "Professor", "Group Leader")

NAME CLEANING RULES:
- Extract only the person's actual name (first and last name)
- Remove contact information: "Tel.", "Telefon", "E-Mail:", "Email:", phone numbers
- Remove German honorifics: "Herr", "Frau" (but keep "Dr.", "Prof.", "Prof. Dr.")
- Remove common words: "Bitte", "für", "und"
- Remove trailing punctuation and separators: ",", ";", ":", "-"
- Remove parenthetical contact info: "(Tel. +49)", "(Email: ...)"
- Keep academic titles: "Dr.", "Prof.", "Prof. Dr."
- Example: "Herr Jörg Barrakling, Tel. +49" → "Jörg Barrakling"
- Example: "Dr. Jörg Matthes, Bitte" → "Dr. Jörg Matthes"
- Example: "Frau Christine Bender, E-Mail:" → "Christine Bender"
- Example: "Dr. Henning Meyerhenke, (Tel." → "Dr. Henning Meyerhenke"

ROLE EXTRACTION RULES:
- Extract detailed position/role information from the provided text
- Include department/institute name if mentioned
- Examples:
  * "Head of Research Group, Institute of Applied Materials – Energy Storage Systems"
  * "Professor and Group Leader"
  * "Scientific Officer, KIT Energy Center"
  * "Researcher, Smart Grids & Energy Markets group"
- If no role is found in text, leave as empty string

IMPORTANT SCORING GUIDELINES:
- Use the FULL 0.0-1.0 scale. Don't be overly conservative.
- 0.9-1.0 = Perfect match (direct researcher/professor in target domains)
- 0.7-0.89 = Strong match (active work in relevant areas)
- 0.5-0.69 = Moderate match (some relevance, related work)
- 0.3-0.49 = Weak match (peripheral connection, possible relevance)
- 0.0-0.29 = Not relevant (no connection to target domains)

Be generous with scores when there's ANY indication of relevance to power electronics, energy systems, or related fields.

Contacts to evaluate:
{json.dumps(items, indent=2)}
"""

        # Debug: Show batch info before API call
        if i == 0:
            print(f"   📋 DEBUG: Batch size: {len(batch)}, Prompt length: {len(prompt)} chars")
            print(f"   📋 DEBUG: Using model: {ai_model}")
        
        # Retry logic with exponential backoff
        max_retries = 3
        retry_delay = 30  # Start with 30 seconds
        response = None
        
        for attempt in range(max_retries):
            try:
                response = client.chat.completions.create(
                    model=ai_model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.2,
                    response_format={"type": "json_object"}  # Force JSON output
                )
                # Success! Break out of retry loop
                break
                
            except Exception as api_error:
                error_msg = str(api_error)
                is_rate_limit = "rate" in error_msg.lower() and "limit" in error_msg.lower()
                is_server_error = "500" in error_msg or "502" in error_msg or "503" in error_msg
                is_timeout = "timeout" in error_msg.lower()
                
                # Only retry on transient errors
                should_retry = is_rate_limit or is_server_error or is_timeout
                
                if attempt < max_retries - 1 and should_retry:
                    wait_time = retry_delay * (attempt + 1)  # 30s, 60s, 90s
                    print(f"   ⚠️  API error (attempt {attempt + 1}/{max_retries}): {type(api_error).__name__}")
                    print(f"   ⏳ Waiting {wait_time} seconds before retry...")
                    time.sleep(wait_time)
                else:
                    # Last attempt or non-retryable error - raise it to be caught by outer try/except
                    raise
        
        try:
            if not response:
                raise Exception("Failed to get response after all retries")
            
            # Track token usage from response
            if hasattr(response, 'usage') and response.usage:
                usage = response.usage
                input_tokens = getattr(usage, 'prompt_tokens', 0)
                output_tokens = getattr(usage, 'completion_tokens', 0)
                total_tokens = getattr(usage, 'total_tokens', input_tokens + output_tokens)
                
                token_stats["input_tokens"] += input_tokens
                token_stats["output_tokens"] += output_tokens
                token_stats["total_tokens"] += total_tokens
                
                # Calculate cost for this batch
                if ai_model in AI_PRICING:
                    pricing = AI_PRICING[ai_model]
                    batch_cost = (input_tokens / 1_000_000 * pricing["input"]) + \
                                 (output_tokens / 1_000_000 * pricing["output"])
                    token_stats["estimated_cost"] += batch_cost
            
            # Parse response (strip markdown if present)
            content = response.choices[0].message.content
            content = content.strip()
            if content.startswith("```json"):
                content = content[7:]
            if content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()
            
            response_data = json.loads(content)
            # Handle both array and object with array
            data = response_data if isinstance(response_data, list) else response_data.get("contacts", response_data.get("results", []))
            
            # Debug: Check if we got the expected number of results
            if len(data) != len(batch):
                print(f"⚠️ Warning: Expected {len(batch)} results, got {len(data)}")
                # Handle mismatch: pad or trim data to match batch size
                if len(data) < len(batch):
                    print(f"   ⚠️ AI returned fewer results. Padding missing contacts with default scores.")
                    # Pad with default entries for missing contacts
                    for missing_idx in range(len(data), len(batch)):
                        data.append({
                            "id": missing_idx,
                            "score": 0.0,
                            "relevant": False,
                            "reason": "AI response missing for this contact",
                            "field": "unknown"
                        })
                elif len(data) > len(batch):
                    print(f"   ⚠️ AI returned more results. Trimming excess results.")
                    data = data[:len(batch)]
            
            # Debug: Show sample of first result in first batch
            if i == 0 and len(data) > 0:
                print(f"   📋 Sample AI response keys: {list(data[0].keys())}")
                print(f"   📋 Sample score: {data[0].get('score', 'MISSING')}")
                print(f"   📋 Sample reason: {data[0].get('reason', 'MISSING')[:100]}")
                print(f"   📋 Sample field: {data[0].get('field', 'MISSING')}")
                # Show sample of what was sent to AI
                if len(items) > 0:
                    original_name = items[0].get('name', 'N/A')
                    cleaned_name = data[0].get('cleaned_name', 'N/A')
                    print(f"   📋 Sample input - Original name: {original_name[:60]}")
                    if cleaned_name and cleaned_name != 'N/A':
                        print(f"   📋 Sample output - Cleaned name: {cleaned_name[:60]}")
                    print(f"   📋 Sample input - Title: {items[0].get('title', 'N/A')[:100]}")
                    print(f"   📋 Sample input - Text length: {len(items[0].get('text', ''))} chars")
            
            # Merge results with improved error handling
            for idx, (contact, ai_data) in enumerate(zip(batch, data)):
                # Try multiple possible score keys
                score = ai_data.get("score")
                if score is None:
                    score = ai_data.get("confidence", ai_data.get("relevance_score", 0.0))
                    if score == 0.0:
                        print(f"⚠️ Contact #{i+idx}: No score in AI response! Keys: {list(ai_data.keys())}")
                
                # Ensure score is a float
                try:
                    score = float(score)
                except (ValueError, TypeError):
                    print(f"⚠️ Contact #{i+idx}: Invalid score '{score}', defaulting to 0.0")
                    score = 0.0
                
                contact["AI_Score"] = score
                contact["AI_Field"] = ai_data.get("field", contact.get("Field_of_study", "Unknown"))
                contact["AI_Reason"] = ai_data.get("reason", "No reason provided")
                
                # Use AI-cleaned name if provided, otherwise keep original
                cleaned_name = ai_data.get("cleaned_name")
                if cleaned_name and cleaned_name.strip():
                    contact["Full_name"] = cleaned_name.strip()
                
                # Use AI-extracted role if provided and better than existing
                ai_role = ai_data.get("role")
                if ai_role and ai_role.strip() and len(ai_role.strip()) > 10:
                    # Only replace if current role is empty or very short
                    current_role = contact.get("Role", "")
                    if not current_role or len(current_role) < 10:
                        contact["Role"] = ai_role.strip()
                
                evaluated.append(contact)
                
        except json.JSONDecodeError as e:
            print(f"⚠️ AI evaluation failed for batch: JSON parsing error")
            print(f"   Error: {e}")
            print(f"   Response content preview: {content[:200] if 'content' in locals() else 'N/A'}")
            # Fallback for this batch
            for c in batch:
                c["AI_Score"] = 0.5
                c["AI_Field"] = c.get("Field_of_study", "Unknown")
                c["AI_Reason"] = "AI evaluation failed: JSON parsing error"
                evaluated.append(c)
        except Exception as e:
            error_type = type(e).__name__
            error_msg = str(e)
            print(f"⚠️ AI evaluation failed for batch: {error_type}: {error_msg}")
            
            # Check for OpenAI APIError and extract error details
            try:
                if hasattr(e, 'response') and e.response:
                    error_data = e.response.json() if hasattr(e.response, 'json') else {}
                    error_info = error_data.get('error', {})
                    error_code = error_info.get('code', '')
                    error_message = error_info.get('message', '')
                    
                    if error_code == 'model_not_found':
                        print(f"   ❌ Model '{ai_model}' not found or you don't have access")
                        print(f"   Error message: {error_message}")
                        print(f"   Valid models: gpt-4o-mini, gpt-4o")
                        print(f"   Check your model name in .env (AI_MODEL) or --ai-model argument")
                    elif error_code == 'invalid_api_key':
                        print(f"   ❌ Invalid API key - check your OPENAI_API_KEY in .env")
                    elif error_code == 'rate_limit_exceeded':
                        print(f"   ⚠️  Rate limit exceeded - wait a moment and try again")
            except:
                pass
            
            # Check for common API errors in error message
            if "authentication" in error_msg.lower() or "api key" in error_msg.lower():
                print(f"   ❌ Authentication error - check your OPENAI_API_KEY in .env")
            elif "rate limit" in error_msg.lower():
                print(f"   ⚠️  Rate limit exceeded - wait a moment and try again")
                print(f"   💡 Tip: Reduce AI_BATCH_SIZE in .env to process fewer contacts at once")
            elif "model" in error_msg.lower() and ("not found" in error_msg.lower() or "does not exist" in error_msg.lower()):
                print(f"   ❌ Model '{ai_model}' not found or not accessible with your API key")
                print(f"   💡 Supported models: gpt-4o-mini (recommended), gpt-4o")
                print(f"   💡 Note: gpt-4o requires higher API tier - use gpt-4o-mini if you see this error")
            elif "invalid" in error_msg.lower() and "model" in error_msg.lower():
                print(f"   ❌ Model '{ai_model}' rejected by OpenAI API")
                print(f"   💡 Possible reasons:")
                print(f"      - Your API key tier doesn't have access to this model")
                print(f"      - Temporary API issue (try again)")
                print(f"   💡 Solution: Use --ai-model gpt-4o-mini (works with all API tiers)")
            
            # Fallback for this batch
            for c in batch:
                c["AI_Score"] = 0.5
                c["AI_Field"] = c.get("Field_of_study", "Unknown")
                c["AI_Reason"] = f"AI evaluation failed: {error_type}"
                evaluated.append(c)
        
        # Progress with percentage and bar
        current = min(i + ai_batch_size, total)
        percentage = (current / total) * 100
        bar_length = 20
        filled = int(bar_length * current / total)
        bar = '█' * filled + '░' * (bar_length - filled)
        print(f"   Evaluated {current}/{total} contacts    [{percentage:5.1f}%] {bar}")
    
    # Final validation: Check score distribution
    if evaluated:
        scores = [c.get("AI_Score", 0.0) for c in evaluated]
        avg_score = sum(scores) / len(scores)
        max_score = max(scores)
        min_score = min(scores)
        above_threshold = sum(1 for s in scores if s >= ai_min_score)
        
        print(f"\n   📊 Score Distribution:")
        print(f"      Average: {avg_score:.3f} | Min: {min_score:.3f} | Max: {max_score:.3f}")
        print(f"      Above threshold ({ai_min_score}): {above_threshold}/{len(evaluated)}")
        
        # Warning if all scores are suspiciously low
        if max_score < 0.3:
            print(f"\n   ⚠️  WARNING: All scores are very low (max={max_score:.3f})!")
            print(f"      This could indicate:")
            print(f"      1. AI model is being too strict")
            print(f"      2. Contacts truly don't match the criteria")
            print(f"      3. Page text doesn't contain enough information")
            print(f"      Check sample AI response above to verify parsing is working correctly.")
        elif max_score < 0.5 and above_threshold == 0:
            print(f"\n   ⚠️  WARNING: No contacts passed threshold, but max score is {max_score:.3f}")
            print(f"      Consider lowering --ai-score threshold or checking if contacts are truly relevant.")
    
    # Display token usage summary
    if token_stats["total_tokens"] > 0:
        print(f"\n   💰 Token Usage & Cost:")
        print(f"      Input tokens:  {token_stats['input_tokens']:,}")
        print(f"      Output tokens: {token_stats['output_tokens']:,}")
        print(f"      Total tokens:  {token_stats['total_tokens']:,}")
        print(f"      Estimated cost: ${token_stats['estimated_cost']:.4f} USD")
        print(f"      Model: {ai_model}")
    
    return evaluated, token_stats

