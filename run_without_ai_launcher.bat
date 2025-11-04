@echo off
title Academic Lead Extractor - Without AI
color 0A

:main_menu
cls
echo ================================================================================
echo    ACADEMIC LEAD EXTRACTOR - WITHOUT AI
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

if "%choice%"=="1" goto option1
if "%choice%"=="2" goto option2
if "%choice%"=="3" goto option3
if "%choice%"=="4" goto option4
goto invalid_choice

:option1
echo.
echo Running with universities.csv...
python run_without_ai.py %depth_arg%
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
python run_without_ai.py --urls %url% %depth_arg%
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
python run_without_ai.py --urls %urls% %depth_arg%
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
python run_without_ai.py --csv "%csvfile%" %depth_arg%
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
