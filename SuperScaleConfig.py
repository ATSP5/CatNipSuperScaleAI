"""Every path and setting of SuperScaleAI.

Folders are resolved against the project folder - the one holding
SuperScaleAI.catnip - so the same code works in a venv on C:, from a src/
folder of generated sources, and in a Docker run, where the project sits in /app.

Defaults live here; the user changes them in the main block's Initialiser section
(Refresh, edit, Apply), which passes them to this config.
"""

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Tuple

from ModelSpec import ModelSpec


def _project_dir() -> Path:
	"""The folder with the .catnip: this file's own, or the one above it."""
	here = Path(os.path.dirname(os.path.abspath(__file__)))
	if not any(here.glob("*.catnip")) and here.parent != here and any(here.parent.glob("*.catnip")):
		return here.parent
	return here


# Real-ESRGAN (Xintao Wang et al., Tencent ARC): the authors' general models
# for real photos - they remove noise, blur and JPEG artefacts while enlarging.
# x2plus works on a quarter of the pixels internally, so it is ~4x faster and
# is used whenever 2x per side is enough. Any model spandrel can load
# (ESRGAN, SwinIR, HAT, DAT ...) can be listed here instead.
REAL_ESRGAN_MODELS = (
	ModelSpec(
		name="Real-ESRGAN x2plus",
		scale=2,
		url="https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.1/RealESRGAN_x2plus.pth",
		sha256="49fafd45f8fd7aa8d31ab2a22d14d91b536c34494a5cfe31eb5d89c2fa266abb",
	),
	ModelSpec(
		name="Real-ESRGAN x4plus",
		scale=4,
		url="https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth",
		sha256="4fa0d38905f75ac06eb49a7951b426670021be3018265fd191d2125df9d682f1",
	),
)


@dataclass
class SuperScaleConfig:
	project_dir: Path = field(default_factory=_project_dir)

	inputs_folder: str = "Inputs"
	outputs_folder: str = "Outputs"
	models_folder: str = "models"

	# How much bigger the result is, from 1 (same size, only cleaner) to 10.
	scale_factor: float = 2.0
	min_factor: float = 1.0
	max_factor: float = 10.0
	# "pixels": the factor multiplies the pixel count - 2 means twice as many
	#           pixels, so each side grows by sqrt(2) = 1.41.
	# "side":   the factor multiplies width and height - 2 means 2x wider and
	#           2x taller, i.e. 4x the pixels.
	factor_mode: str = "pixels"

	models: Tuple[ModelSpec, ...] = REAL_ESRGAN_MODELS

	# The image goes through the network in tiles, so memory use does not grow
	# with the photo: 4 GB of GPU or a few GB of RAM is enough for any size.
	tile_size: int = 256
	tile_overlap: int = 16

	output_extension: str = ".png"
	jpeg_quality: int = 95
	image_extensions: Tuple[str, ...] = (".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp")

	def __post_init__(self) -> None:
		if not self.min_factor <= self.scale_factor <= self.max_factor:
			raise ValueError("scale_factor %g jest poza zakresem %g-%g." % (
				self.scale_factor, self.min_factor, self.max_factor))
		if self.factor_mode not in ("pixels", "side"):
			raise ValueError("factor_mode musi byc 'pixels' albo 'side', jest '%s'." % self.factor_mode)
		if not self.output_extension.startswith("."):
			self.output_extension = "." + self.output_extension
		self.project_dir = Path(self.project_dir)

	@property
	def inputs_dir(self) -> Path:
		return self.project_dir / self.inputs_folder

	@property
	def outputs_dir(self) -> Path:
		return self.project_dir / self.outputs_folder

	@property
	def models_dir(self) -> Path:
		return self.project_dir / self.models_folder

	def model_path(self, spec: ModelSpec) -> Path:
		return self.models_dir / spec.file_name

	def model_for(self, side_scale: float) -> ModelSpec:
		"""The smallest model that reaches side_scale in one pass, else the largest."""
		by_scale = sorted(self.models, key=lambda m: m.scale)
		for spec in by_scale:
			if spec.scale >= side_scale - 1e-9:
				return spec
		return by_scale[-1]

	def is_image(self, path: Path) -> bool:
		return path.suffix.lower() in self.image_extensions

	def ensure_dirs(self) -> "SuperScaleConfig":
		for folder in (self.inputs_dir, self.outputs_dir, self.models_dir):
			folder.mkdir(parents=True, exist_ok=True)
		return self

	def config(self):
		return
