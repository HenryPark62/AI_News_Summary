from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update(self, summary: str, output_file: str):
        pass

class SummarizerSubject:
    def __init__(self):
        self._observers = []

    def attach(self, observer: Observer):
        self._observers.append(observer)

    def detach(self, observer: Observer):
        self._observers.remove(observer)

    def notify(self, summary: str, output_file: str):
        for observer in self._observers:
            observer.update(summary, output_file)