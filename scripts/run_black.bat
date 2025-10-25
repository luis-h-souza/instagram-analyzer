@echo off
REM Batch helper to run Black using project's .venv if available.
REM Run from repository root: scripts\run_black.bat

SET ROOT=%~dp0..
IF EXIST "%ROOT%\.venv\Scripts\activate.bat" (
    CALL "%ROOT%\.venv\Scripts\activate.bat"
) ELSE (
    ECHO .venv not found, using system Python environment
)

CD /D "%ROOT%"
ECHO Running: black .
black .
IF ERRORLEVEL 1 (
  ECHO Black returned an error & EXIT /B 1
)
ECHO Black finished.
