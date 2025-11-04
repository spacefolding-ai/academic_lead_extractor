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
    echo "   ACADEMIC LEAD EXTRACTOR - WITHOUT AI"
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
            if get_depth; then
                echo ""
                echo -e "${GREEN}Running with universities.csv...${NC}"
                python3 run_without_ai.py $DEPTH_ARG
                break
            fi
            ;;
        2)
            if get_depth; then
                while true; do
                    echo ""
                    read -p "Enter university URL (or 'b' to go back): " url
                    
                    if [ "$url" = "b" ] || [ "$url" = "B" ] || [ "$url" = "back" ] || [ "$url" = "BACK" ]; then
                        break
                    elif [ -z "$url" ]; then
                        echo -e "${RED}Error: URL cannot be empty${NC}"
                    else
                        python3 run_without_ai.py --urls "$url" $DEPTH_ARG
                        break 2
                    fi
                done
            fi
            ;;
        3)
            if get_depth; then
                while true; do
                    echo ""
                    echo "Enter URLs separated by spaces (or 'b' to go back):"
                    read -p "URLs: " urls
                    
                    if [ "$urls" = "b" ] || [ "$urls" = "B" ] || [ "$urls" = "back" ] || [ "$urls" = "BACK" ]; then
                        break
                    elif [ -z "$urls" ]; then
                        echo -e "${RED}Error: URLs cannot be empty${NC}"
                    else
                        python3 run_without_ai.py --urls $urls $DEPTH_ARG
                        break 2
                    fi
                done
            fi
            ;;
        4)
            if get_depth; then
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
                        python3 run_without_ai.py --csv "$csvfile" $DEPTH_ARG
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
