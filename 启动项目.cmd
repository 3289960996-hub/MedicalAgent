@echo off
chcp 65001 >nul
title MedicalAgent - 统一启动
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\start_project.ps1"
if errorlevel 1 pause
