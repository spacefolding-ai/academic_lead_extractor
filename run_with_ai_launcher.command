#!/bin/bash

# Change to script directory
cd "$(dirname "$0")"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to show main menu
show_menu() {
    clear
    echo "================================================================================"
    echo "   ACADEMIC LEAD EXTRACTOR - WITH AI FILTERING"
    echo "================================================================================"
    echo ""
    echo "Options:"
    echo "  1. Process ALL universities from universities.csv (default)"
    echo "  2. Process SINGLE university URL"
    echo "  3. Process MULTIPLE universities (space-separated URLs)"
    echo "  4. Use CUSTOM CSV file"
    echo "  0. EXIT"
    echo ""
}

# Function to get AI score
get_ai_score() {
    while true; do
        echo ""
        read -p "AI Score threshold (0.0-1.0) or 'b' to go back [default: 0.5]: " ai_score_input
        
        case "$ai_score_input" in
            b|B|back|BACK)
                return 1
                ;;
            "")
                AI_SCORE_ARG=""
                return 0
                ;;
            *)
                # Check if valid number between 0 and 1
                if [[ "$ai_score_input" =~ ^[0-9]*\.?[0-9]+$ ]] && (( $(echo "$ai_score_input >= 0 && $ai_score_input <= 1" | bc -l) )); then
                    AI_SCORE_ARG="--ai-score $ai_score_input"
                    return 0
                else
                    echo -e "${RED}Invalid input. Please enter a number between 0.0 and 1.0, or 'b' to go back.${NC}"
                fi
                ;;
        esac
    done
}

# Function to get AI model
get_ai_model() {
    while true; do
        echo ""
        echo "AI Model Selection:"
        echo "  1. gpt-4o-mini - Fast + cost-efficient (filter 500-10,000 contacts) [default]"
        echo "  2. gpt-4o - Stronger understanding, fewer false positives"
        echo ""
        read -p "Enter model (1-2) or 'b' to go back [default: 1]: " model_input
        
        case "$model_input" in
            b|B|back|BACK)
                return 1
                ;;
            ""|1)
                AI_MODEL_ARG=""
                return 0
                ;;
            2)
                AI_MODEL_ARG="--ai-model gpt-4o"
                return 0
                ;;
            *)
                echo -e "${RED}Invalid input. Please enter 1, 2, or 'b' to go back.${NC}"
                ;;
        esac
    done
}

# Function to get depth setting
get_depth() {
    while true; do
        echo ""
        echo "Exploration depth:"
        echo "  1 = Shallow (fast, ~20-30 contacts per university)"
        echo "  2 = Normal (balanced, ~35-60 contacts) [default]"
        echo "  3 = Deep (thorough, ~60-100 contacts)"
        echo ""
        read -p "Enter depth (1-3) or 'b' to go back [default: 2]: " depth_input
        
        case "$depth_input" in
            b|B|back|BACK)
                return 1
                ;;
            ""|2)
                DEPTH_ARG=""
                return 0
                ;;
            1|3)
                DEPTH_ARG="--depth $depth_input"
                return 0
                ;;
            *)
                echo -e "${RED}Invalid input. Please enter 1, 2, 3, or 'b' to go back.${NC}"
                ;;
        esac
    done
}

# Function to get AI profile detection setting
get_ai_profile_detection() {
    while true; do
        echo ""
        echo -e "${YELLOW}⚡ AI Profile Detection (Advanced):${NC}"
        echo "  Uses AI to detect individual researcher profiles"
        echo ""
        echo "  1. Disabled = FAST (60-80% faster, recommended) [default]"
        echo "  2. Enabled  = SLOW (may catch edge cases, 4-6x slower)"
        echo ""
        echo -e "${BLUE}💡 TIP: Keep disabled unless you need maximum completeness${NC}"
        echo ""
        read -p "Select option (1-2) or 'b' to go back [default: 1]: " profile_input
        
        case "$profile_input" in
            b|B|back|BACK)
                return 1
                ;;
            ""|1)
                PROFILE_DETECTION_ARG=""
                return 0
                ;;
            2)
                PROFILE_DETECTION_ARG="--use-ai-profile-detection"
                echo -e "${YELLOW}⚠️  Warning: This will make extraction 4-6x slower!${NC}"
                sleep 1
                return 0
                ;;
            *)
                echo -e "${RED}Invalid input. Please enter 1, 2, or 'b' to go back.${NC}"
                ;;
        esac
    done
}

# Main loop
while true; do
    show_menu
    read -p "Enter your choice (1-4, 0 to exit) [default: 1]: " choice
    choice=${choice:-1}
    
    case $choice in
        0)
            echo ""
            echo -e "${YELLOW}Exiting...${NC}"
            echo ""
            exit 0
            ;;
        1)
            if get_ai_model && get_ai_score && get_depth && get_ai_profile_detection; then
                echo ""
                echo -e "${GREEN}Running with universities.csv...${NC}"
                python3 run_with_ai.py $AI_MODEL_ARG $AI_SCORE_ARG $DEPTH_ARG $PROFILE_DETECTION_ARG
                break
            fi
            ;;
        2)
            if get_ai_model && get_ai_score && get_depth && get_ai_profile_detection; then
                while true; do
                    echo ""
                    read -p "Enter university URL (or 'b' to go back): " url
                    
                    if [ "$url" = "b" ] || [ "$url" = "B" ] || [ "$url" = "back" ] || [ "$url" = "BACK" ]; then
                        break
                    elif [ -z "$url" ]; then
                        echo -e "${RED}Error: URL cannot be empty${NC}"
                    else
                        python3 run_with_ai.py --urls "$url" $AI_MODEL_ARG $AI_SCORE_ARG $DEPTH_ARG $PROFILE_DETECTION_ARG
                        break 2
                    fi
                done
            fi
            ;;
        3)
            if get_ai_model && get_ai_score && get_depth && get_ai_profile_detection; then
                while true; do
                    echo ""
                    echo "Enter URLs separated by spaces (or 'b' to go back):"
                    read -p "URLs: " urls
                    
                    if [ "$urls" = "b" ] || [ "$urls" = "B" ] || [ "$urls" = "back" ] || [ "$urls" = "BACK" ]; then
                        break
                    elif [ -z "$urls" ]; then
                        echo -e "${RED}Error: URLs cannot be empty${NC}"
                    else
                        python3 run_with_ai.py --urls $urls $AI_MODEL_ARG $AI_SCORE_ARG $DEPTH_ARG $PROFILE_DETECTION_ARG
                        break 2
                    fi
                done
            fi
            ;;
        4)
            if get_ai_model && get_ai_score && get_depth && get_ai_profile_detection; then
                while true; do
                    echo ""
                    read -p "Enter CSV filename (or 'b' to go back): " csvfile
                    
                    if [ "$csvfile" = "b" ] || [ "$csvfile" = "B" ] || [ "$csvfile" = "back" ] || [ "$csvfile" = "BACK" ]; then
                        break
                    elif [ -z "$csvfile" ]; then
                        echo -e "${RED}Error: Filename cannot be empty${NC}"
                    elif [ ! -f "$csvfile" ]; then
                        echo -e "${RED}Error: File '$csvfile' not found!${NC}"
                    else
                        python3 run_with_ai.py --csv "$csvfile" $AI_MODEL_ARG $AI_SCORE_ARG $DEPTH_ARG $PROFILE_DETECTION_ARG
                        break 2
                    fi
                done
            fi
            ;;
        *)
            echo -e "${RED}Invalid choice! Please enter 1-4 or 0 to exit.${NC}"
            sleep 2
            ;;
    esac
done

echo ""
echo "================================================================================"
read -p "Press Enter to exit..."

# Close the terminal window (macOS)
osascript -e 'tell application "Terminal" to close first window' & exit 0
