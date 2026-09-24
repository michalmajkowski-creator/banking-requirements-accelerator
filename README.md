# Banking Requirements Accelerator — skeleton

Minimalny, uruchamialny szkielet platformy do prowadzenia wymagań bankowych przez kompozycyjne skillsy. Rdzeń nie zależy od konkretnego LLM ani systemu docelowego.

## Stan rozwiązania

Wersja 0.2 zawiera formularz WWW, API i deterministyczny pipeline z jawnymi zaślepkami. Nie zawiera jeszcze konwersacyjnego Studio ani rzeczywistej integracji z modelem AI.

Docelowy zakres opisuje [specyfikacja Conversational Requirements Studio](SPEC-Conversational-Requirements-Studio.md).

Aplikację uruchamiaj lokalnie. Obecny szkielet nie ma logowania ani kontroli dostępu, a wyniki przechowuje w pamięci procesu i traci je po restarcie. Repozytorium udostępnia kod, nie hostuje działającej usługi.

Wymagania: Python 3.11 lub nowszy. Komendy wykonuj z głównego katalogu projektu.

## Start

```bash
python -m venv .venv
. .venv/bin/activate
pip install -e '.[dev]'
uvicorn bra.api:app --reload
```

Następnie otwórz `http://localhost:8000`. Dane do analizy wprowadza się w formularzu; ręczne przygotowanie JSON nie jest potrzebne. Dokumentacja technicznego API pozostaje pod `http://localhost:8000/docs`.

Opcjonalne wywołanie API dla integratorów:

```bash
curl -X POST http://localhost:8000/v1/runs \
  -H 'content-type: application/json' \
  -d '{"pipeline":"mvp","initiative":{"title":"Zmiana limitu przelewów","problem":"Klient nie może samodzielnie kontrolować limitu przelewu.","desired_outcome":"Bezpieczna zmiana limitu w bankowości mobilnej.","sources":["notatka warsztatowa"]}}'
```

Smoke test bez dodatkowego runnera:

```bash
PYTHONPATH=src python scripts/smoke_test.py
```

Bez skonfigurowanego LLM pipeline działa deterministycznie: wykonuje reguły lokalne, a kroki wymagające wiedzy lub generowania zwracają `needs_input` albo `stubbed`. Szczegóły: [ARCHITECTURE.md](docs/ARCHITECTURE.md) i [BACKLOG.md](docs/BACKLOG.md).

## Windows PowerShell

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
.\.venv\Scripts\python.exe -m uvicorn bra.api:app --reload
```

## Testy

Po zainstalowaniu zależności deweloperskich uruchom `python -m pytest -q`.
