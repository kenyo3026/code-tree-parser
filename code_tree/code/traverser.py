import os
from pathlib import Path
from pathspec import PathSpec
from typing import List, Union


class CodeBaseTraverser:

    def __init__(self, rules:Union[str, List, Path, PathSpec]):
        self.pathspec = self.setup_pathspec(rules)

    def setup_pathspec(self, rules:Union[str, List, Path, PathSpec]) -> PathSpec:
        if isinstance(rules, str):
            if Path(rules).exists():
                with open(rules, 'r') as file:
                    rules = file.readlines()
            else:
                rules = [rules]

        return PathSpec.from_lines('gitwildmatch', rules)

    def traverse(self, root:str, return_abs:bool=True):
        matching_files = []
        for root_with_dir, _, files in os.walk(root):

            for file in files:
                abs_path = os.path.join(root_with_dir, file)
                rel_path = os.path.relpath(abs_path, root)

                if not self.pathspec.match_file(rel_path):
                    if return_abs:
                        matching_files.append(abs_path)
                    else:
                        matching_files.append(rel_path)

        return matching_files


if __name__ == "__main__":
    codebase_root = None
    rules = [
        '/*',
        '!*.c',
    ]

    traverser = CodeBaseTraverser(rules)
    print(f'Results: {traverser.traverse(codebase_root)}')