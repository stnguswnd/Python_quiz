from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class Quiz:
    id: int
    question: str
    choices: list[str]
    answer: int
    hint: str

    def __post_init__(self) -> None:
        if self.id < 1:
            raise ValueError("퀴즈 id는 1 이상이어야 합니다.")
        if len(self.choices) != 4:
            raise ValueError("선택지는 반드시 4개여야 합니다.")
        if not 1 <= self.answer <= 4:
            raise ValueError("정답 번호는 1~4 사이여야 합니다.")
        if self.hint.strip() == "":
            raise ValueError("힌트는 비어 있을 수 없습니다.")

    def display(self, number: int | None = None) -> None:
        prefix = f"[문제 {number}] " if number is not None else ""
        print(f"{prefix}{self.question}")
        for index, choice in enumerate(self.choices, start=1):
            print(f"{index}. {choice}")

    def display_hint(self) -> None:
        print(f"힌트: {self.hint}")

    def is_correct(self, user_answer: int) -> bool:
        return self.answer == user_answer

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
            "hint": self.hint,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Quiz":
        return cls(
            id=int(data["id"]),
            question=str(data["question"]),
            choices=[str(choice) for choice in data["choices"]],
            answer=int(data["answer"]),
            hint=str(data["hint"]),
        )
