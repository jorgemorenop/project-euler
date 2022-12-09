from pathlib import Path
import argparse

from traitlets.config import Config
from nbconvert import MarkdownExporter


argparse = argparse.ArgumentParser()
argparse.add_argument("-n", "--notebooks", nargs='+', default=[])


def main(notebooks: list[str]):
    # c = MarkdownExporter.default_config
    c = Config()
    c.NbConvertApp.output_base = 'Readme'
    md_exporter = MarkdownExporter(config=c)
    notebook_paths = [Path(n) for n in notebooks] or Path().rglob('solution.ipynb')
    for notebook_path in notebook_paths:
        print(f"Processing {notebook_path}...")
        with (notebook_path.parent / "Readme.md").open('w') as f:
            f.write(md_exporter.from_filename(notebook_path.as_posix())[0])


if __name__ == '__main__':
    args = argparse.parse_args()
    main(notebooks=args.notebooks)


