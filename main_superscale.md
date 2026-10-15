**SuperScale AI.** Powiększa zdjęcia wskazane w blokach File content modelem Real-ESRGAN, poprawiając przy tym ich jakość. Wynik zapisuje jako `Outputs/<nazwa>_x<mnożnik>.png`. W zakładce Output pokazuje wynik oraz wycinek 1:1 z porównaniem zwykłego powiększenia i AI.

Jeden blok File content to jedno zdjęcie. Żeby przetworzyć kilka zdjęć, dodaj kolejne bloki File content (połączenie z mainem nie jest wymagane, ale pomaga w czytelności).

**Ustawienia:** zaznacz ten blok, w Inspectorze otwórz sekcję **INITIALISER** i kliknij **Refresh**. Pojawią się parametry `__init__`. Zmień wartości i kliknij **Apply**.

Pakiety: `torch torchvision spandrel numpy opencv-python-headless`.

## scale_factor
Mnożnik od 1 do 10, może być ułamkowy. 1 oznacza tę samą rozdzielczość, ale lepszą jakość. 2 oznacza 2× więcej pikseli, a 10 oznacza 10× więcej pikseli. Wartość spoza zakresu przerywa uruchomienie z komunikatem.

## factor_mode
`"pixels"` (domyślnie): mnożnik dotyczy liczby pikseli, więc 2 daje bok ×1.41. `"side"`: mnożnik dotyczy boku, więc 2 daje bok ×2, czyli 4× więcej pikseli.

## output_extension
`".png"` (bezstratnie) albo `".jpg"`.

## jpeg_quality
Jakość zapisu JPEG (1–100). Działa tylko przy `".jpg"`.

## tile_size
Bok kafelka sieci w pikselach. Większy kafelek jest szybszy na GPU, ale zajmuje więcej pamięci.

## tile_overlap
Zakładka kafelków w pikselach. Dzięki niej nie widać szwów.

## outputs_folder
Folder wyników obok projektu.

## run
Cały przebieg dla wszystkich wskazanych zdjęć.
