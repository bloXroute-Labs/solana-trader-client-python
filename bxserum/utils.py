from abc import abstractmethod
from types import TracebackType
from typing import TypeVar, AsyncGenerator, Type, overload

T = TypeVar("T")
_T_co = TypeVar("_T_co")
_T_contra = TypeVar("_T_contra")



class ExceptionGenerator(AsyncGenerator["T"]):
    def __aiter__(self):
        raise NotImplementedError()

    async def __anext__(self) -> _T_co:
        pass

    async def asend(self, __value: _T_contra) -> _T_co:
        pass

    @overload
    @abstractmethod
    async def athrow(
        self, __typ: Type[BaseException], __val: BaseException | object = ..., __tb: TracebackType | None = ...
    ) -> _T_co: ...

    @overload
    @abstractmethod
    async def athrow(self, __typ: BaseException, __val: None = ..., __tb: TracebackType | None = ...) -> _T_co: ...

    async def athrow(self, __typ: Type[BaseException], __val: BaseException | object = ...,
                     __tb: TracebackType | None = ...) -> _T_co:
        pass

    async def aclose(self) -> None:
        pass

