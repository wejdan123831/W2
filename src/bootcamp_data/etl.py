from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class Paths:
   
    root: Path
    raw: Path
    cache: Path
    processed: Path
    external: Path

base_path = Path(r'C:\Users\w\Documents\my_csv_project\week2-data-work')

project_paths = Paths(
    root=base_path,
    raw=base_path / "data" / "raw",
    cache=base_path / "data" / "cache",
    processed=base_path / "data" / "processed",
    external=base_path / "data" / "external"
)


print(f"  processed data at  : {project_paths.processed}")