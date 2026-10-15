Doprowadza jedno zdjęcie do żądanego rozmiaru. Dobiera model do mnożnika: x2, gdy wystarcza powiększenie boku ×2 (jest około 4× szybszy), x4 powyżej tego, a kilka przejść x4 tylko powyżej ×4 na bok. Wynik sieci jest na końcu dopasowywany do rozmiaru docelowego (INTER_AREA przy zmniejszaniu, Lanczos przy powiększaniu). Zmniejszenie czystszego, większego obrazu zachowuje detale dodane przez sieć, dlatego mnożnik 1 też poprawia zdjęcie.

## config
`SuperScaleConfig`.

## downloader
`ModelDownloader`, który dostarcza pliki wag.

## plan
`plan(image, factor)` zwraca `ScalePlan` i wybrany `ModelSpec`.

## scale
`scale(image, factor)` zwraca parę (wynik, plan).

## upscaler_for
Upscaler dla danego modelu, tworzony raz i używany ponownie dla kolejnych zdjęć.

## resize
Dopasowanie do rozmiaru docelowego.
