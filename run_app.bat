@echo off
title FalkorDB Universal Memory Mesh - Graph Hacks 2026
echo ==============================================================================
echo   🔱 FalkorDB Universal Memory Mesh (Graph Hacks 2026)
echo   Track 01 (Connected Data), Track 02 (CoW Memory), Track 03 (Company Brain)
echo ==============================================================================
echo.
echo [1/2] Verifying FalkorDB Docker container...
docker ps | findstr falkordb >nul
if errorlevel 1 (
    echo [FalkorDB] Starting container on localhost:6379 / localhost:3000...
    docker run -d -p 6379:6379 -p 3000:3000 --name falkordb falkordb/falkordb:latest
) else (
    echo [FalkorDB] Container is already active and healthy.
)

echo.
echo [2/2] Launching FastAPI Web Service on http://localhost:8000 ...
start http://localhost:8000
python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload
pause
