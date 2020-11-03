# Solvro - Backend

[![N|Solid](https://process.filestackapi.com/cache=expiry:max/resize=width:1050/7WnZWlR7TgafdDesB5ow)]

Projekt zawiera backend do aplikacji JakDojadę, którego głównym zadaniem jest określenie oraz zwrócenie optymalnej trasy na podstawie dwóch podanych przystanków. API ma też wbudowaną funkcję rejestracji oraz logowania. 
Do sprawdzenia poszczególnych funkcji napisałem kilka skryptów testujących (folder testy).

# Dostępne funkcje

  - rejestracja
  - logowanie
  - generowanie tokena autoryzacyjnego
  - zwracanie listy wszystkich przystanków
  - ustalanie oraz zwracanie optymalnej trasy

# Wykorzystane technologie
  - Flask API
  - SQL
  - JSON
  - Password encryption
  
# Zawartość
  - api.py, czyli rdzeń projektu
  - find_path.py zawierający algorytm Dijkstry zmodyfikowany do potrzeb i specyfikacji
  - niewielkie aplikacje testujące niektóre funkcje
  - full_test.py przedstawiający pełne działanie aplikacji wraz z obsługą wyjątków

### Todos

 - rozbudowanie aplikacji testującej
 - swagger
