# To-Do List

Aplicație web simplă pentru gestionarea sarcinilor. Sarcinile sunt salvate în
fișierul `tasks.json` din directorul proiectului.

## Funcționalități

- Adăugarea și ștergerea sarcinilor
- Marcarea unei sarcini ca finalizată sau revenirea la starea nefinalizată
- Validarea titlurilor goale
- Salvarea sarcinilor între pornirile aplicației

## Tehnologii

- Python 3
- Flask și Jinja2
- HTML și CSS
- JSON pentru stocarea datelor
- pytest pentru testele unitare

## Instalare

Din directorul proiectului, creează și activează un mediu virtual PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Instalează dependențele:

```powershell
python -m pip install Flask pytest
```

## Rulare

Pornește serverul local:

```powershell
python app.py
```

Deschide apoi adresa afișată în terminal (implicit, `http://127.0.0.1:5000`).
Modul debug este activ la rularea directă a aplicației și este destinat
dezvoltării locale.

## Teste

Rulează testele unitare din directorul proiectului:

```powershell
python -m pytest -q
```

Testele din `test_todo.py` folosesc fișiere temporare și nu modifică
`tasks.json`.
