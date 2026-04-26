from dataclasses import dataclass


@dataclass(frozen=True)
class Person:
    full_name: str
    age: str
    address: str
    birth_date: str
