"""Downloads the upscaling model into models/ once, and checks it is intact.

Only the standard library is used. A broken transfer resumes where it stopped
(HTTP Range), data goes to *.part until every byte is there, and the finished
file must match the SHA-256 in the config before it is used.
"""

import hashlib
import http.client
import time
import urllib.error
import urllib.request
from pathlib import Path

from ModelSpec import ModelSpec
from SuperScaleConfig import SuperScaleConfig


class ModelDownloader:
	CHUNK = 1024 * 1024
	ATTEMPTS = 20
	USER_AGENT = "SuperScaleAI-CatNip/1.0"

	def __init__(self, config: SuperScaleConfig):
		self.config = config

	def ensure_model(self, spec: ModelSpec) -> Path:
		"""The model file, downloaded first if it is missing or damaged."""
		target = self.config.model_path(spec)
		if target.is_file():
			if self.verify(target, spec.sha256):
				return target
			print("[Model] %s jest uszkodzony - pobieram od nowa" % target.name)
			target.unlink()
		self.fetch_file(spec.url, target)
		if not self.verify(target, spec.sha256):
			target.unlink()
			raise IOError("Pobrany plik %s ma niewlasciwa sume SHA-256." % target.name)
		return target

	def verify(self, path: Path, sha256: str) -> bool:
		expected = (sha256 or "").lower()
		if not expected:
			return True
		digest = hashlib.sha256()
		with open(path, "rb") as source:
			for block in iter(lambda: source.read(self.CHUNK), b""):
				digest.update(block)
		return digest.hexdigest() == expected

	def fetch_file(self, url: str, target: Path) -> Path:
		target.parent.mkdir(parents=True, exist_ok=True)
		part = target.with_name(target.name + ".part")
		for attempt in range(1, self.ATTEMPTS + 1):
			have = part.stat().st_size if part.is_file() else 0
			request = urllib.request.Request(url, headers={"User-Agent": self.USER_AGENT})
			if have:
				request.add_header("Range", "bytes=%d-" % have)
			try:
				with urllib.request.urlopen(request, timeout=60) as response:
					resumed = have > 0 and response.status == 206
					if not resumed:
						have = 0
					total = have + int(response.headers.get("Content-Length") or 0)
					if resumed:
						print("[Model] Wznawiam %s od %s" % (target.name, self.size(have)))
					else:
						print("[Model] Pobieram %s  (%s)" % (url, self.size(total) if total else "rozmiar nieznany"))
					self.stream(response, part, have, total)
			except urllib.error.HTTPError as error:
				if error.code != 416:
					raise
				part.unlink()
				continue
			except (OSError, http.client.HTTPException) as error:
				print("[Model] Polaczenie przerwane (%s), proba %d/%d" % (error, attempt, self.ATTEMPTS))
				time.sleep(min(2 * attempt, 10))
				continue

			if total and part.stat().st_size != total:
				continue
			part.replace(target)
			print("[Model] -> %s" % target)
			return target
		raise IOError("Nie udalo sie pobrac %s po %d probach." % (target.name, self.ATTEMPTS))

	def stream(self, response, part: Path, done: int, total: int) -> None:
		last_print, started, start_bytes = 0.0, time.time(), done
		with open(part, "ab" if done else "wb") as out:
			for chunk in iter(lambda: response.read(self.CHUNK), b""):
				out.write(chunk)
				done += len(chunk)
				now = time.time()
				if now - last_print >= 2 or (total and done == total):
					last_print = now
					speed = (done - start_bytes) / max(now - started, 1e-6)
					share = " %5.1f%%" % (100.0 * done / total) if total else ""
					print("[Model]%s  %s  %s/s" % (share, self.size(done), self.size(speed)), flush=True)

	@staticmethod
	def size(n: float) -> str:
		for unit in ("B", "KB", "MB"):
			if n < 1024:
				return "%.1f %s" % (n, unit)
			n /= 1024.0
		return "%.1f GB" % n
