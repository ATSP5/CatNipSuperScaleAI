Uruchamia sieć super-rozdzielczości lokalnie, kafelek po kafelku. Model wczytuje biblioteka `spandrel` (ta sama, której używa chaiNNer), więc działa każdy checkpoint ESRGAN, SwinIR, HAT czy DAT bez ręcznego pisania architektury.

Kafelki zachodzą na siebie, a z każdego brany jest tylko środek, więc nie widać szwów. Zużycie pamięci zależy od rozmiaru kafelka, a nie od zdjęcia. Obliczenia idą na GPU, jeśli ta wersja PyTorch obsługuje kartę, a w przeciwnym razie na CPU. Gdy GPU zabraknie pamięci, program przełącza się na CPU.

Wymaga: `torch`, `torchvision`, `spandrel`, `numpy`, `opencv-python-headless`.

## config
`SuperScaleConfig`.

## model_path
Plik wag, który ten upscaler wczytuje.

## scale
Ile razy model powiększa bok.

## load
Wczytuje model raz i go zapamiętuje.

## upscale
`upscale(image_bgr)` wykonuje jedno przejście sieci i zwraca obraz `scale` razy większy (BGR `uint8`).

## pick_device
Wybiera CUDA tylko wtedy, gdy ta wersja PyTorch ma kernele dla karty. Nowe wersje pomijają starsze karty (np. GTX 1050 Ti to sm_61), więc wtedy liczy na CPU.
