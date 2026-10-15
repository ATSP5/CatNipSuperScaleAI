"""Brings one photo to the requested size with the network's help.

The model is picked per factor: x2 when 2x per side is enough (it is ~4x
faster), x4 above that, and several x4 passes only beyond 4x per side. The
requested size is rarely exactly what the network produces, so the last pass
is brought to the target with a high-quality resample (INTER_AREA going down,
Lanczos going up). Going down from a cleaner, larger image keeps the network's
detail - which is also why factor 1 still improves a photo.
"""

import time
from typing import Dict, Tuple

import cv2
import numpy as np

from ModelDownloader import ModelDownloader
from ModelSpec import ModelSpec
from RealESRGANUpscaler import RealESRGANUpscaler
from ScalePlan import ScalePlan
from SuperScaleConfig import SuperScaleConfig


class SuperScaler:
	def __init__(self, config: SuperScaleConfig, downloader: ModelDownloader):
		self.config = config
		self.downloader = downloader
		self._upscalers: Dict[str, RealESRGANUpscaler] = {}

	def plan(self, image_bgr: np.ndarray, factor: float) -> Tuple[ScalePlan, ModelSpec]:
		height, width = image_bgr.shape[:2]
		side_scale = ScalePlan.side_scale_for(factor, self.config.factor_mode)
		spec = self.config.model_for(side_scale)
		return ScalePlan.build(width, height, factor, self.config.factor_mode, spec.scale), spec

	def scale(self, image_bgr: np.ndarray, factor: float) -> Tuple[np.ndarray, ScalePlan]:
		plan, spec = self.plan(image_bgr, factor)
		print("[Skala] %s" % plan.describe())
		upscaler = self.upscaler_for(spec)

		started = time.time()
		current = image_bgr
		for number in range(1, plan.passes + 1):
			print("[Skala] Przejscie %d/%d (%s): %dx%d" % (number, plan.passes, spec.name, current.shape[1], current.shape[0]))
			current = upscaler.upscale(current)

		result = self.resize(current, plan.target_width, plan.target_height)
		print("[Skala] Gotowe w %.1f s" % (time.time() - started))
		return result, plan

	def upscaler_for(self, spec: ModelSpec) -> RealESRGANUpscaler:
		if spec.name not in self._upscalers:
			path = self.downloader.ensure_model(spec)
			self._upscalers[spec.name] = RealESRGANUpscaler(self.config, path)
		return self._upscalers[spec.name]

	@staticmethod
	def resize(image: np.ndarray, width: int, height: int) -> np.ndarray:
		if image.shape[1] == width and image.shape[0] == height:
			return image
		shrinking = width < image.shape[1]
		interpolation = cv2.INTER_AREA if shrinking else cv2.INTER_LANCZOS4
		return cv2.resize(image, (width, height), interpolation=interpolation)
