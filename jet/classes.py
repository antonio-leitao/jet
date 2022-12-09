from dataclasses import dataclass
from rich.console import Console
from typing import Any


class JetError(Exception):
    pass


@dataclass(frozen=True)
class JetConfig:
    foreground: str  # "134"
    background: str
    pass_color: str
    failed_color: str
    error_color: str
    warning_color: str
    second_color: str


@dataclass(frozen=True)
class RunConfig(JetConfig):
    run_all: bool
    path: str
    files: list[str]
    n_jobs: int
    quiet: bool
    show_percentage: bool


@dataclass(frozen=True)
class SeeConfig(JetConfig):
    doc_width: int
    text_width: int
    pad: int
    buffer: int
    path: str
    console: Console


@dataclass(frozen=True)
class Module:
    name: str
    doc: str
    path: str
    module: Any | None = None


@dataclass(frozen=True)
class Test:
    name: str
    doc: str
    module: Module
    routine: Any | None = None


@dataclass(frozen=True)
class Error:
    type: str  # pass/fail/error/warning
    name: str  # alias
    description: str
    line: int
    variables: dict
    out: str
    test: Test
