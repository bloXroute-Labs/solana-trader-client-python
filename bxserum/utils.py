from abc import abstractmethod
from types import TracebackType
from typing import TypeVar, AsyncGenerator, Type, overload

T = TypeVar("T")


class ExceptionGenerator(AsyncGenerator["T", None]):
    def __aiter__(self):
        raise NotImplementedError()

    async def __anext__(self) -> T:
        pass

    async def asend(self, __value: None) -> T:
        pass

    async def athrow(
        self,
        __typ: Type[BaseException],
        __val: BaseException | object = ...,
        __tb: TracebackType | None = ...,
    ) -> T:
        pass

    async def athrow(
        self,
        __typ: BaseException,
        __val: None = ...,
        __tb: TracebackType | None = ...,
    ) -> T:
        pass

    async def athrow(
        self,
        __typ: Type[BaseException],
        __val: BaseException | object = ...,
        __tb: TracebackType | None = ...,
    ) -> T:
        pass

    async def aclose(self) -> None:
        pass
