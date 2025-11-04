#!/bin/bash
# Quick Test - Validates contact extraction with UK universities
# These universities have simpler structures and will show immediate results

cd "$(dirname "$0")"

echo "=========================================="
echo "🧪 QUICK TEST - Contact Extraction"
echo "=========================================="
echo ""
echo "Testing with UK universities (simple structure)..."
echo "Expected: 20-50 contacts in ~1 minute"
echo ""

python3 main.py \
  --urls https://www.bristol.ac.uk \
  --depth 2 \
  --no-ai

echo ""
echo "=========================================="
echo "✅ Test Complete!"
echo "=========================================="
echo ""
echo "Check results/Custom.csv for extracted contacts"
echo ""
echo "If you see contacts above, the system is working!"
echo "For German universities like KIT, increase depth:"
echo "  Edit config.py: MAX_CRAWL_DEPTH = 5"
echo ""
read -p "Press Enter to exit..."

