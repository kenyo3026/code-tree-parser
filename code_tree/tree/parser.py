import os
import sys
import importlib
import subprocess
import charset_normalizer
from dataclasses import dataclass
from importlib.metadata import version
from typing import Union

import tree_sitter
from tree_sitter import Language, Parser

from .utils import remove_comments_and_docstrings
from .traverser import DFSTraverser

MIN_SYSTEM_RECURSION_LIMIT = 20000


def install_library(lib:str):
    try:
        if lib not in sys.modules:
            importlib.import_module(lib)
    except ModuleNotFoundError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", lib])

        try:
            importlib.import_module(lib)
        except ModuleNotFoundError:
            raise ImportError(f"Failed to install {lib}. Please install it manually.")


@dataclass
class SupportedLanguages:
    c:str = 'tree_sitter_c'
    h:str = 'tree_sitter_cpp'
    python:str = 'tree_sitter_python'


class CodeParser:

    def __init__(
        self,
        lang:str='c',
        auto_install_packages:bool=True
    ):
        if sys.getrecursionlimit() < MIN_SYSTEM_RECURSION_LIMIT:
            sys.setrecursionlimit(MIN_SYSTEM_RECURSION_LIMIT)

        lib = getattr(SupportedLanguages, lang)
        if lib in sys.modules:
            mod = sys.modules[lib]
        else:
            try:
                mod = importlib.import_module(lib)
            except ModuleNotFoundError:
                if auto_install_packages:
                    tree_sitter_version = version(tree_sitter.__name__)
                    subprocess.check_call([
                        sys.executable, "-m", "pip", "install", f"{lib}"#=={tree_sitter_version}"
                    ])
                    try:
                        mod = importlib.import_module(lib)
                    except ModuleNotFoundError:
                        raise ImportError(f"Failed to install {lib}. Please install it manually.")
                else:
                    raise ModuleNotFoundError(f"No module named '{lib}'. Please install it manually.")

        language = Language(mod.language())
        self.parser = Parser(language)


    def parse_code(self, code:Union[str, bytes]):

        if isinstance(code, str) and os.path.isfile(code):
            result = charset_normalizer.from_path(code).best()
            detected_encoding = result.encoding or 'utf-8'

            with open(code, 'r', encoding=detected_encoding) as f:
                code = f.read()

        if isinstance(code, str):
            code = bytes(code, 'utf8')

        tree = self.parser.parse(code)
        return tree.walk()


    def traverse_nodes(
        self,
        code,
        remove_comments:bool=False,
        trace_strategy=None,
        store_strategy=None
    ):
        if remove_comments:
            code = remove_comments_and_docstrings(code, self.lang)
        cursor = self.parse_code(code)

        traversal = DFSTraverser(trace_strategy=trace_strategy, store_strategy=store_strategy)
        return traversal.traverse(cursor)