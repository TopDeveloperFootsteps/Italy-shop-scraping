@echo off
set /p supermarket="Enter supermarket name (Iperal or carrefour): "
set /p location="Enter town name (for Iperal) or zip code (for carrefour): "

python main.py "%supermarket%" "%location%"

pause