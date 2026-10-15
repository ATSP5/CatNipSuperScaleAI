"""Runs the super-resolution network over a photo, locally, tile by tile.

The model (Real-ESRGAN x4plus by default) is loaded with spandrel, the
loader chaiNNer uses, so any ESRGAN / SwinIR / HAT / DAT checkpoint works
without writing its architecture by hand.

Tiles overlap by a few pixels and only their centres are kept, so the seams
do not show; memory use depends on the tile size, not on the photo.
"""

import time
from pathlib import Path

import numpy as np

from SuperScaleConfig import SuperScaleConfig


class RealESRGANUpscaler:
	def __init__(self, config: SuperScaleConfig, model_path: Path):
		self.config = config
		self.model_path = model_path
		self._model = None
		self._device = None

	@property
	def scale(self) -> int:
		return int(self.load().scale)

	def load(self):
		if self._model is not None:
			return self._model
		import torch
		from spandrel import ImageModelDescriptor, ModelLoader

		path = self.model_path
		model = ModelLoader().load_from_file(str(path))
		if not isinstance(model, ImageModelDescriptor):
			raise TypeError("%s nie jest modelem obraz -> obraz" % path.name)
		self._device = self.pick_device(torch)
		model.to(self._device).eval()
		print("[Model] %s (%s, x%d) na %s" % (path.name, model.architecture.name, model.scale, self._device))
		self._model = model
		return model

	def upscale(self, image_bgr: np.ndarray) -> np.ndarray:
		"""One pass of the network: BGR uint8 in, BGR uint8 `scale` times larger out."""
		import torch

		model = self.load()
		try:
			return self._run_tiles(torch, model, image_bgr)
		except RuntimeError as error:
			# Some cards still run out of memory; the CPU always finishes.
			if "out of memory" not in str(error).lower() or self._device.type != "cuda":
				raise
			print("[Model] Za malo pamieci GPU - licze dalej na CPU")
			torch.cuda.empty_cache()
			self._device = torch.device("cpu")
			model.to(self._device)
			return self._run_tiles(torch, model, image_bgr)

	def _run_tiles(self, torch, model, image_bgr: np.ndarray) -> np.ndarray:
		scale = int(model.scale)
		tile, pad = self.config.tile_size, self.config.tile_overlap
		height, width = image_bgr.shape[:2]

		rgb = np.ascontiguousarray(image_bgr[:, :, ::-1])
		source = torch.from_numpy(rgb).permute(2, 0, 1).unsqueeze(0).float().div_(255.0)
		result = np.empty((height * scale, width * scale, 3), dtype=np.uint8)

		boxes = [(x, y) for y in range(0, height, tile) for x in range(0, width, tile)]
		started, last_print = time.time(), 0.0
		with torch.inference_mode():
			for done, (x, y) in enumerate(boxes, 1):
				x1, y1 = min(x + tile, width), min(y + tile, height)
				# The tile plus a margin of context on every side that has any.
				px, py = max(x - pad, 0), max(y - pad, 0)
				px1, py1 = min(x1 + pad, width), min(y1 + pad, height)

				chunk = source[:, :, py:py1, px:px1].to(self._device)
				out = model(chunk).clamp_(0, 1).mul_(255.0).round_().byte()
				out = out[0].permute(1, 2, 0).cpu().numpy()

				ox, oy = (x - px) * scale, (y - py) * scale
				result[y * scale:y1 * scale, x * scale:x1 * scale] = \
					out[oy:oy + (y1 - y) * scale, ox:ox + (x1 - x) * scale]

				now = time.time()
				if now - last_print >= 5 or done == len(boxes):
					last_print = now
					print("[Model]   kafelki %d/%d  (%.0f s)" % (done, len(boxes), now - started), flush=True)

		return np.ascontiguousarray(result[:, :, ::-1])

	@staticmethod
	def pick_device(torch):
		"""CUDA only if this PyTorch build has kernels for the card, else CPU.

		New PyTorch wheels dropped older cards (a GTX 1050 Ti is sm_61); on such
		a card CUDA looks available but every kernel launch fails.
		"""
		if not torch.cuda.is_available():
			return torch.device("cpu")
		major, minor = torch.cuda.get_device_capability(0)
		name = torch.cuda.get_device_name(0)
		if "sm_%d%d" % (major, minor) not in torch.cuda.get_arch_list():
			print("[Model] %s (sm_%d%d) nie jest wspierany przez ta wersje PyTorch - licze na CPU" % (name, major, minor))
			return torch.device("cpu")
		print("[Model] GPU: %s" % name)
		return torch.device("cuda")
