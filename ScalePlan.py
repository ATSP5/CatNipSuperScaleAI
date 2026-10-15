"""What one photo turns into: its size now, the size it must reach, and which
model gets it there in how many passes."""

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class ScalePlan:
	width: int
	height: int
	factor: float
	side_scale: float
	target_width: int
	target_height: int
	model_scale: int
	passes: int

	@staticmethod
	def side_scale_for(factor: float, factor_mode: str) -> float:
		if factor_mode == "pixels":
			return math.sqrt(factor)
		if factor_mode == "side":
			return float(factor)
		raise ValueError("factor_mode musi byc 'pixels' albo 'side', jest '%s'" % factor_mode)

	@classmethod
	def build(cls, width: int, height: int, factor: float, factor_mode: str, model_scale: int) -> "ScalePlan":
		side_scale = cls.side_scale_for(factor, factor_mode)
		# Always at least one pass: even at factor 1 the network cleans the
		# photo up, and the result is then brought back to the original size.
		passes = max(1, math.ceil(math.log(side_scale, model_scale) - 1e-9)) if side_scale > 1 else 1
		return cls(
			width=width,
			height=height,
			factor=factor,
			side_scale=side_scale,
			target_width=max(1, round(width * side_scale)),
			target_height=max(1, round(height * side_scale)),
			model_scale=model_scale,
			passes=passes,
		)

	@property
	def pixel_gain(self) -> float:
		return (self.target_width * self.target_height) / float(self.width * self.height)

	def describe(self) -> str:
		return "%dx%d -> %dx%d  (bok x%.2f, pikseli x%.2f; model x%d, przejscia: %d)" % (
			self.width, self.height, self.target_width, self.target_height,
			self.side_scale, self.pixel_gain, self.model_scale, self.passes)
