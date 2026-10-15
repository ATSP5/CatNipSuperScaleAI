"""SuperScaleAI - powieksz zdjecia modelem AI (Real-ESRGAN).

Zdjecia wskazuja bloki File content (jeden blok = jedno zdjecie; dodaj
kolejne bloki, zeby przetworzyc kilka). Wynik trafia do
Outputs/<nazwa>_x<mnoznik>.png i jest pokazywany w zakladce Output.

USTAWIENIA: Inspector tego bloku -> sekcja INITIALISER -> Refresh. Pojawia sie
parametry __init__ ponizej; zmien wartosci i kliknij Apply.

  scale_factor      1-10, moze byc ulamkowy: 1 = ta sama rozdzielczosc
                    (tylko lepsza jakosc), 2 = 2x wiecej pikseli, 10 = 10x
  factor_mode       "pixels" - mnoznik liczby pikseli (2 -> bok x1.41)
                    "side"   - mnoznik boku (2 -> bok x2, 4x wiecej pikseli)
  output_extension  ".png" (bez strat) albo ".jpg"
  jpeg_quality      jakosc dla ".jpg", 1-100
  tile_size         bok kafelka sieci; wiekszy = szybciej na GPU, wiecej pamieci
  tile_overlap      zakladka kafelkow (bez widocznych szwow)
  outputs_folder    folder wynikow obok projektu

Model pobiera sie sam przy pierwszym uruchomieniu (~64 MB, do models/):
Real-ESRGAN x2plus do mnoznika 4, x4plus powyzej.
"""

from ImageFiles import ImageFiles
from ModelDownloader import ModelDownloader
from PhotoPicker import PhotoPicker
from SuperScaleConfig import SuperScaleConfig
from SuperScaler import SuperScaler


class SuperScaleApp:
	def __init__(self, scale_factor: float=10.0, factor_mode: str="pixels", output_extension: str=".png", jpeg_quality: int=95, tile_size: int=256, tile_overlap: int=16, outputs_folder: str="Outputs"):
		self.config = SuperScaleConfig(
			scale_factor=float(scale_factor),
			factor_mode=factor_mode,
			output_extension=output_extension,
			jpeg_quality=int(jpeg_quality),
			tile_size=int(tile_size),
			tile_overlap=int(tile_overlap),
			outputs_folder=outputs_folder,
		).ensure_dirs()

	def run(self) -> None:
		config = self.config
		print("=" * 72)
		print("SUPERSCALE AI  (Real-ESRGAN)")
		print("=" * 72)
		print("[Ustawienia] mnoznik %g (%s), wynik %s" % (config.scale_factor,
			"pikseli" if config.factor_mode == "pixels" else "boku", config.output_extension))

		photos = PhotoPicker(config).picked_photos()
		if not photos:
			print("[Zdjecia] Zaden blok File content nie wskazuje istniejacego zdjecia - wybierz plik w bloku 'Zdjecie'.")
			return

		scaler = SuperScaler(config, ModelDownloader(config))
		files = ImageFiles(config.jpeg_quality)

		saved = []
		for number, photo in enumerate(photos, 1):
			print("")
			print("[%d/%d] %s" % (number, len(photos), photo.name))
			try:
				image = files.read(photo)
			except ValueError as error:
				print("[Pominiete] %s" % error)
				continue

			result, plan = scaler.scale(image, config.scale_factor)
			target = config.outputs_dir / ("%s_x%g%s" % (photo.stem, config.scale_factor, config.output_extension))
			files.write(result, target)
			print("[Wynik] -> %s  (%dx%d)" % (target, plan.target_width, plan.target_height))
			saved.append(target)

			files.show("%s (%dx%d)" % (target.name, plan.target_width, plan.target_height), result)
			files.compare_detail("%s - detal 1:1: zwykle powiekszenie | AI" % photo.name, image, result)

		print("")
		print("Zapisano %d z %d zdjec w %s" % (len(saved), len(photos), config.outputs_dir))


def main():
	photo = r"Inputs/t3_color.jpg"
	SuperScaleApp().run()


if __name__ == "__main__":
	main()
