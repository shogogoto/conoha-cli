"""template repository."""
from functools import cached_property
from pathlib import Path
from string import Template
from typing import Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T", bound=BaseModel)


class TemplateRepo(BaseModel, Generic[T], frozen=True):
    """template IO."""

    read_from: Path
    map_to: dict = Field(default={})

    @cached_property
    def text(self) -> str:
        """Read template."""
        return self.read_from.read_text()

    @cached_property
    def template(self) -> Template:
        """Template object."""
        return Template(self.text)

    def apply(self, model: T) -> str:
        """Write from template."""
        d = model.model_dump(mode="json") | self.map_to
        return self.template.safe_substitute(d)

    def write(self, model: T, write_to: Path) -> None:
        """Write applied template."""
        write_to.write_text(self.apply(model))
