from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass  #데이터를 담는 클래스를 간단하게 만들도록 도와주는 문법, #원래는 __init__를 직접 써야 하는데, @dataclass를 쓰면 자동으로 만들어줘
class Quiz:
    question: str #문제 내용
    choices: list[str] #보기 4개 
    answer: int #정답 번호 

    def __post_init__(self) -> None:
        if len(self.choices) != 4:
            raise ValueError("선택지는 반드시 4개여야 합니다.")
        if not 1 <= self.answer <= 4:
            raise ValueError("정답 번호는 1~4 사이여야 합니다.")

    def display(self, number: int | None = None) -> None: #문제와 보기를 제공함. 
        prefix = f"[문제 {number}] " if number is not None else ""
        print(f"{prefix}{self.question}")
        for index, choice in enumerate(self.choices, start=1):
            print(f"{index}. {choice}")

    def is_correct(self, user_answer: int) -> bool: #정답인지 아닌지 비교하는 함수 
        return self.answer == user_answer

    def to_dict(self) -> dict[str, Any]: #JSON에 저장하기 위해서 딕셔너리 형태로 바꿈. 
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Quiz": #딕셔너리를 다시 Quiz객체로 바꿈
        return cls( #cls는 뭐지?
            question=str(data["question"]),
            choices=[str(choice) for choice in data["choices"]],
            answer=int(data["answer"]),
        )
