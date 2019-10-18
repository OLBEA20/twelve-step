from abc import ABC, abstractmethod


class A(ABC):
    @abstractmethod
    def say_hello(self):
        pass

class D(obejct):
    def say_bye(self):
        print("Bye")
