from abc import ABC, abstractmethod
from pathlib import Path
from typing import Generic, Iterator, Union

from storage.base.type import IOType


class IFileReader(ABC, Generic[IOType]):
    """FileReader Interface."""

    @abstractmethod
    def read_lines(self, path: Path) -> Iterator[IOType]:
        """
        Reads file lines from specified path.

        :param str path: File path
        :return: Algorithm input
        :rtype: AlgorithmInput
        """
        pass
