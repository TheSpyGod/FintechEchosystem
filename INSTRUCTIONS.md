# Instrukcja weryfikacji projektu

## Wymagania

- Python 3.11+
- `venv` lub globalny pip

---

## 1. Instalacja zależności

```bash
python -m venv venv
source venv/bin/activate        # Linux/macOS
# venv\Scripts\activate         # Windows

pip install fastapi==0.135.3 uvicorn==0.44.0 sqlalchemy==2.0.49 \
            pydantic==2.12.5 pydantic-settings==2.13.1 \
            httpx==0.28.1 aiosqlite==0.22.1 python-dotenv==1.2.2
```

---

## 2. Konfiguracja środowiska

Skopiuj plik przykładowy i uzupełnij klucze:

```bash
cp .env.example .env
```

Minimalna zawartość `.env` wymagana do uruchomienia:

```
DATABASE_URL=sqlite:///./gateway.db
STRIPE_SECRET_KEY_SANDBOX=sk_test_<twoj_klucz>
AIRALO_API_KEY=mock_airalo_key
AIRALO_API_SECRET=mock_airalo_secret
GATEWAY_API_KEY=dev-api-key
USE_MOCK=true
```

> **Bezpieczeństwo:** żaden klucz nie jest zahardkodowany w kodzie —
> wszystkie są wczytywane przez klasę `Settings` z pliku `.env`
> (`src/config.py`). Brak `STRIPE_SECRET_KEY_SANDBOX` w `.env` powoduje
> błąd walidacji Pydantic już przy starcie serwera.

---

## 3. Inicjalizacja bazy danych

```bash
python seed.py
```

Oczekiwany wynik:

```
Seeding database...
Tables created.
Seeded 6 packages.
Seeded 3 orders.
Seeded 3 payments.
Seeded 2 webhook events.
Done.
```

> Skrypt jest idempotentny, bezpieczne wielokrotne uruchomienie.

---

## 4. Uruchomienie serwera

```bash
python server.py
```

Serwer startuje na `http://localhost:8000`.

---

## 5. Punkty kontrolne

### 5.1 Swagger UI,  schematy Pydantic

Otwórz w przeglądarce: **http://localhost:8000/docs**

Sprawdź, że widoczne są następujące schematy w sekcji *Schemas*:

| Schema | Opis |
|---|---|
| `TransactionSchema` | Model transakcji (id, user_id, amount, status) |
| `TransactionCreateRequest` | Żądanie utworzenia transakcji |
| `PaymentIntentRequest` | Żądanie Stripe PaymentIntent |
| `PaymentIntentResponse` | Odpowiedź Stripe |
| `AiraloOrderRequest` | Zamówienie pakietu eSIM |
| `AiraloPackage` | Pakiet eSIM Airalo |

---

### 5.2 Healthcheck: baza danych i Stripe

```bash
curl http://localhost:8000/api/v1/health
```

Oczekiwana odpowiedź:

```json
{
  "status": "ok",
  "database": "ok",
  "stripe": "ok"
}
```

Endpoint asynchronicznie sprawdza:
- połączenie z bazą danych (`SELECT 1` przez `async_sessionmaker`)
- dostępność API Stripe (żądanie `GET /v1/customers` przez `httpx.AsyncClient`)

---

### 5.3 Transakcje: async DB przez Dependency Injection

Utwórz transakcję:

```bash
curl -s -X POST http://localhost:8000/api/v1/transactions \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "amount": 1500, "status": "pending"}' | python -m json.tool
```

Pobierz listę:

```bash
curl -s http://localhost:8000/api/v1/transactions | python -m json.tool
```

---

### 5.4 Airalo: lista pakietów eSIM (mock)

```bash
curl -s http://localhost:8000/api/v1/esims/packages | python -m json.tool
```

Oczekiwana odpowiedź: lista 6 pakietów z polami `id`, `name`, `data_limit_gb`, `validity_days`, `price_usd`.

---

### 5.5 Stripe: PaymentIntent (mock)

```bash
curl -s -X POST http://localhost:8000/api/v1/payments/intent \
  -H "Content-Type: application/json" \
  -d '{"amount": 2000, "currency": "usd", "order_id": "test-order-1"}' | python -m json.tool
```

Oczekiwana odpowiedź:

```json
{
  "intent_id": "pi_...",
  "client_secret": "pi_..._secret_...",
  "status": "requires_payment_method"
}
```

---

## 6. Weryfikacja bezpieczeństwa kluczy

Sprawdź, że żaden klucz API nie występuje bezpośrednio w kodzie źródłowym:

```bash
grep -r "sk_test_" src/
grep -r "sk_live_" src/
```

Oba polecenia powinny zwrócić **brak wyników**.

Klucze są dostępne wyłącznie przez `settings` z `src/config.py`:

```python
from src.config import settings
settings.stripe_secret_key_sandbox  # wczytane z .env
```

---

## 7. Tryb mock

Projekt działa w trybie mock (`USE_MOCK=true`):

- Autentykacja (`X-API-Key`) jest pomijana — wszystkie endpointy dostępne bez nagłówka.
- Airalo i Stripe nie wykonują prawdziwych wywołań API — dane są zapisywane lokalnie w SQLite.
- Zmień `USE_MOCK=false` w `.env` i uzupełnij `GATEWAY_API_KEY`, aby włączyć autentykację.
