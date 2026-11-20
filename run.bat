@echo off
title Aplikasi Kasir Python OOP
echo ========================================================
echo Membuka Aplikasi Kasir Modern (Python OOP + GUI)...
echo ========================================================

:: Coba jalankan dengan python di PATH terlebih dahulu
where python >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    python kasir_app.py
    goto end
)

:: Coba jalankan dengan py launcher
where py >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    py kasir_app.py
    goto end
)

:: Gunakan path instalasi Python spesifik jika belum terdaftar di PATH
if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
    "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" kasir_app.py
    goto end
)

echo [ERROR] Python tidak ditemukan! Pastikan Python telah terinstall.
pause

:end
