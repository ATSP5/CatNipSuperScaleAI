"""The photos picked in the project's File content blocks.

CatNip writes a File content block's path into main only on Generate
Blueprint, so the picks are read straight out of SuperScaleAI.catnip (plain
JSON): every File content node (nodeCategory 1) holds its path in codeText.
One block is one photo - add more File content blocks to scale several.

In a Docker run the Windows path does not exist - the container sees /app,
not C: - so the file is then looked up by name next to the project and in
Inputs/ (where "Copy to source" or a manual copy puts it).
"""

import json
from pathlib import Path
from typing import List, Optional

from SuperScaleConfig import SuperScaleConfig


class PhotoPicker:
	FILE_CONTENT = 1

	def __init__(self, config: SuperScaleConfig):
		self.config = config

	def picked_photos(self) -> List[Path]:
		photos = []
		for picked in self.paths_from_blocks():
			found = self.resolve(picked)
			if found is None:
				print("[Zdjecia] Nie znaleziono: %s" % picked)
			elif not self.config.is_image(found):
				print("[Zdjecia] To nie jest obraz, pomijam: %s" % found)
			elif found not in photos:
				photos.append(found)
		return photos

	def paths_from_blocks(self) -> List[str]:
		project = self.find_project()
		if project is None:
			return []
		try:
			data = json.loads(project.read_text(encoding="utf-8-sig"))
		except (OSError, ValueError):
			return []
		nodes = [n.get("nodeData", {}) for n in data.get("nodes", [])]
		nodes = [n for n in nodes if n.get("nodeCategory", n.get("nodeCathegory")) == self.FILE_CONTENT]
		paths = [(n.get("codeText") or "").strip().strip('"') for n in sorted(nodes, key=lambda n: n.get("id", 0))]
		return [p for p in paths if p]

	def resolve(self, picked: str) -> Optional[Path]:
		path = Path(picked)
		if path.is_file():
			return path
		name = picked.replace("\\", "/").rsplit("/", 1)[-1]
		for folder in (self.config.project_dir, self.config.inputs_dir):
			candidate = folder / name
			if candidate.is_file():
				print("[Zdjecia] %s nie istnieje tutaj - uzywam %s" % (picked, candidate))
				return candidate
		return None

	def find_project(self) -> Optional[Path]:
		projects = sorted(self.config.project_dir.glob("*.catnip"))
		return projects[0] if projects else None
