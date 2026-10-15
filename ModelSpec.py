"""One ready-made super-resolution model: where to get it and how much it enlarges."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ModelSpec:
	name: str
	scale: int
	url: str
	sha256: str

	@property
	def file_name(self) -> str:
		return self.url.rsplit("/", 1)[-1]
