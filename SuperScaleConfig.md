Wszystkie ścieżki i ustawienia SuperScaleAI (`@dataclass`) z wartościami domyślnymi. **Na co dzień ustawienia zmieniasz w bloku main, w sekcji INITIALISER** (Refresh → zmiana → Apply). Ten blok dostaje stamtąd wartości i sprawdza je; tutaj zmienia się tylko listę modeli.

Foldery są liczone względem folderu z `SuperScaleAI.catnip`, więc ten sam kod działa w venv, z podfolderu `src/` i w Dockerze (`/app`).

## scale_factor
Mnożnik od 1 do 10, może być ułamkowy (np. 2.5). 1 oznacza tę samą rozdzielczość, ale lepszą jakość. 2 oznacza 2× więcej pikseli, a 10 oznacza 10× więcej pikseli.

## min_factor
Najmniejszy dozwolony mnożnik (1).

## max_factor
Największy dozwolony mnożnik (10).

## factor_mode
`"pixels"` (domyślnie): mnożnik dotyczy liczby pikseli, więc 2 daje bok ×1.41, a 10 daje bok ×3.16. `"side"`: mnożnik dotyczy szerokości i wysokości, więc 2 daje bok ×2 (4× więcej pikseli). W tym trybie mnożnik 10 oznacza dwa przejścia sieci x4 i jest bardzo wolny.

## models
Gotowe modele do wyboru. Domyślnie to Real-ESRGAN x2plus i x4plus (Tencent ARC, licencja BSD-3), oficjalne wagi autorów. Program bierze najmniejszy model, który osiąga potrzebne powiększenie w jednym przejściu. x2plus jest około 4× szybszy, więc obsługuje mnożniki do 4 (`pixels`). Można tu wpisać dowolny model obsługiwany przez `spandrel` (ESRGAN, SwinIR, HAT, DAT…).

## tile_size
Bok kafelka w pikselach (256). Zdjęcie przechodzi przez sieć kafelkami, więc zużycie pamięci nie rośnie z jego rozmiarem. Większy kafelek jest trochę szybszy na GPU, ale zajmuje więcej pamięci.

## tile_overlap
Zakładka kafelków (16 px). Dzięki niej nie widać szwów.

## output_extension
Format wyniku: `.png` (bezstratny). Można ustawić `.jpg`.

## inputs_dir
`Inputs/`: miejsce na kopie zdjęć do uruchomień w Dockerze, gdzie zdjęcie jest szukane po nazwie.

## outputs_dir
`Outputs/`, gdzie trafiają wyniki jako `<nazwa>_x<mnożnik>.png`.

## models_dir
`models/`, gdzie leżą pobrane wagi modeli.

## model_path
Ścieżka do pliku wag danego modelu.

## model_for
`model_for(side_scale)` zwraca najmniejszy model, który osiąga to powiększenie w jednym przejściu, a jeśli żaden nie wystarcza, największy.

## __post_init__
Sprawdza ustawienia: mnożnik musi być w zakresie 1–10, a `factor_mode` musi mieć wartość `pixels` albo `side`. W przeciwnym razie uruchomienie kończy się czytelnym komunikatem.

## ensure_dirs
Tworzy `Inputs/`, `Outputs/` i `models/`, jeśli ich nie ma.

## is_image
Czy plik ma rozszerzenie obrazu.
