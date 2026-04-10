# School Project: Inicjalizacja Asynchronicznego Ekosystemu FinTech

## 1. Opis:
- Przygotowanie szkieletu aplikacji (Boilerplate) opartej na FastAPI, która integruje lokalną bazę danych z zewnętrznymi dostawcami usług finansowych i telekomunikacyjnych (Stripe, Airalo) w sposób bezpieczny i asynchroniczny.

## 2. Zakres działań (setup)

### a) Konfiguracja Serwera i Środowiska
- Stworzenie asynchronicznej instancji FastAPI z zdefiniowanymi metadanymi (tytuł, wersja, opis dla OpenAPI).
- Implementacja zarządzania konfiguracją przy użyciu pydantic-settings (klasa Settings), która wczytuje klucze API z pliku .env.
- Zmienne wymagane w .env:
  * DATABASE_URL (async driver)
  * STRIPE_SECRET_KEY_SANDBOX
  * AIRALO_API_KEY
  * AIRALO_API_SECRET

### b) Architektura bazy danych
- Konfiguracja asynchronicznego silnika (create_asyc_engine) oraz fabryki sesji (async_sessionmaker).
- Stworzenie bazowych modeli tabeli:
  * User (id, email, stripe_customer_id)
  * Transaction (id_ user_id, amount, status: *pending/success/failed*)

### c) Integracja z Dostawcami
- Stworzenie asynchronicznych klientów (używając biblioteki httpx) do komunikacji z:
  * Stripe Sandbox: Endpoint do tworzenia PaymentIntent
  * Airalo API: Endpoint do pobierania listy dostępnych pakietów eSIM (*sandbox/test*)
- Zastosowanie wzorca Dependency Injection w FastAPI do wstrzykiwania sesji bazy danych oraz klientów API do endpointu.

## 3. Punkty Kontrolne 

1. **Swagger UI**(*/docs*): Dokumentacja musi automatycznie wykrywać schematy Pydantic dla żądań do Stripe & Airalo.
2. **Healthcheck Endpoint**: Endpoint */health*, który sprawdza asynchronicznie połącznie z bazą danych oraz dostępność API Stripe (*ping*)
3. **Bezpieczeństwo**: Wykazanie, że klucze API nie są zahardkodowane w kodzie, a jedynie pobierane ze środowiska.
