@echo off
title Academic Lead Extractor - With AI
color 0B

:main_menu
cls
echo ================================================================================
echo    ACADEMIC LEAD EXTRACTOR - WITH AI FILTERING
echo ================================================================================
echo.
echo Options:
echo   1. Process ALL universities from universities.csv (default)
echo   2. Process SINGLE university URL
echo   3. Process MULTIPLE universities (space-separated URLs)
echo   4. Use CUSTOM CSV file
echo   0. EXIT
echo.

set /p choice="Enter your choice (1-4, 0 to exit) [default: 1]: "
if "%choice%"=="" set choice=1

if "%choice%"=="0" goto exit_script

:get_ai_model
echo.
echo AI Model Selection:
echo   1. gpt-4o-mini - Fast + cost-efficient (filter 500-10,000 contacts) [default]
echo   2. gpt-4o - Stronger understanding, fewer false positives
echo.
set /p model="Enter model (1-2) or 'b' to go back [default: 1]: "

if /i "%model%"=="b" goto main_menu
if /i "%model%"=="back" goto main_menu

set ai_model_arg=
if "%model%"=="2" set ai_model_arg=--ai-model gpt-4o

:get_ai_score
echo.
set /p ai_score="AI Score threshold (0.0-1.0) or 'b' to go back [default: 0.5]: "

if /i "%ai_score%"=="b" goto main_menu
if /i "%ai_score%"=="back" goto main_menu

set ai_score_arg=
if not "%ai_score%"=="" set ai_score_arg=--ai-score %ai_score%

:get_depth
echo.
echo Exploration depth:
echo   1 = Shallow (fast, ~20-30 contacts per university)
echo   2 = Normal (balanced, ~35-60 contacts) [default]
echo   3 = Deep (thorough, ~60-100 contacts)
echo.
set /p depth="Enter depth (1-3) or 'b' to go back [default: 2]: "

if /i "%depth%"=="b" goto main_menu
if /i "%depth%"=="back" goto main_menu

set depth_arg=
if "%depth%"=="1" set depth_arg=--depth 1
if "%depth%"=="3" set depth_arg=--depth 3

:get_ai_profile_detection
echo.
color 0E
echo ========================================
echo  AI Profile Detection (Advanced)
echo ========================================
color 0B
echo   Uses AI to detect individual researcher profiles
echo.
echo   1. Disabled = FAST (60-80%% faster, recommended) [default]
echo   2. Enabled  = SLOW (may catch edge cases, 4-6x slower)
echo.
echo   TIP: Keep disabled unless you need maximum completeness
echo.
set /p profile_detection="Select option (1-2) or 'b' to go back [default: 1]: "

if /i "%profile_detection%"=="b" goto main_menu
if /i "%profile_detection%"=="back" goto main_menu

set profile_detection_arg=
if "%profile_detection%"=="" set profile_detection=1
if "%profile_detection%"=="2" (
    set profile_detection_arg=--use-ai-profile-detection
    color 0E
    echo.
    echo WARNING: This will make extraction 4-6x slower!
    timeout /t 2 >nul
    color 0B
)

if "%choice%"=="1" goto option1
if "%choice%"=="2" goto option2
if "%choice%"=="3" goto option3
if "%choice%"=="4" goto option4
goto invalid_choice

:option1
echo.
echo Running with universities.csv...
python run_with_ai.py %ai_model_arg% %ai_score_arg% %depth_arg% %profile_detection_arg%
goto end

:option2
:get_url
echo.
set /p url="Enter university URL (or 'b' to go back): "
if /i "%url%"=="b" goto main_menu
if /i "%url%"=="back" goto main_menu

if "%url%"=="" (
    echo Error: URL cannot be empty
    goto get_url
)
python run_with_ai.py --urls %url% %ai_model_arg% %ai_score_arg% %depth_arg% %profile_detection_arg%
goto end

:option3
:get_urls
echo.
echo Enter URLs separated by spaces (or 'b' to go back):
set /p urls="URLs: "
if /i "%urls%"=="b" goto main_menu
if /i "%urls%"=="back" goto main_menu

if "%urls%"=="" (
    echo Error: URLs cannot be empty
    goto get_urls
)
python run_with_ai.py --urls %urls% %ai_model_arg% %ai_score_arg% %depth_arg% %profile_detection_arg%
goto end

:option4
:get_csv
echo.
set /p csvfile="Enter CSV filename (or 'b' to go back): "
if /i "%csvfile%"=="b" goto main_menu
if /i "%csvfile%"=="back" goto main_menu

if "%csvfile%"=="" (
    echo Error: Filename cannot be empty
    goto get_csv
)
if not exist "%csvfile%" (
    echo Error: File "%csvfile%" not found!
    goto get_csv
)
python run_with_ai.py --csv "%csvfile%" %ai_model_arg% %ai_score_arg% %depth_arg% %profile_detection_arg%
goto end

:invalid_choice
echo Invalid choice! Please enter 1-4 or 0 to exit.
timeout /t 2 >nul
goto main_menu

:exit_script
echo.
echo Exiting...
echo.
exit

:end
echo.
echo ================================================================================
pause
exit
