@echo off
setlocal

title ASTRA AI

cd /d "%~dp0"

echo.
echo ============================================================
echo                    STARTING ASTRA
echo ============================================================
echo.

if not exist ".venv\Scripts\activate.bat" (

```
echo ERROR: Virtual environment not found.
echo.
echo Please run setup.bat first.
echo.

pause

exit /b 1
```

)

call ".venv\Scripts\activate.bat"

streamlit run web.py

pause

endlocal
