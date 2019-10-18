from typing import List

from package_1.A import A


class C(A):
    def say_hello(self):
        print("Hello world, I am C")

    def say_hello_using_typing(self, names: List) -> None:
        pass
