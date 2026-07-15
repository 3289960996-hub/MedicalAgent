@echo off
chcp 65001 >nul
title MedicalAgent - 停止服务
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\stop_project.ps1"
if errorlevel 1 pause
