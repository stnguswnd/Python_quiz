from __future__ import annotations

from datetime import datetime
import json
import random
from pathlib import Path
from typing import Any

from quiz import Quiz


class QuizGame:
    FULL_SCORE = 1.0
    HINT_PENALTY_SCORE = 0.5

    def __init__(self, state_file: str = "state.json") -> None:
        self.state_path = Path(state_file)
        self.quizzes: list[Quiz] = []
        self.best_score: int | None = None
        self.history: list[dict[str, Any]] = []
        self.load_state()

    def get_default_quizzes(self) -> list[Quiz]:
        return [
            Quiz(
                id=1,
                question="영화 '기생충'의 감독은 누구일까요?",
                choices=["박찬욱", "봉준호", "김기덕", "이창동"],
                answer=2,
                hint="아카데미 작품상을 받은 한국 영화의 감독입니다.",
            ),
            Quiz(
                id=2,
                question="마블 시네마틱 유니버스에서 인피니티 스톤은 모두 몇 개일까요?",
                choices=["4개", "5개", "6개", "7개"],
                answer=3,
                hint="한 손에 모두 끼울 수 있는 숫자입니다.",
            ),
            Quiz(
                id=3,
                question="영화 '인셉션'의 감독은 누구일까요?",
                choices=["크리스토퍼 놀란", "스티븐 스필버그", "제임스 카메론", "리들리 스콧"],
                answer=1,
                hint="시간과 구조를 비틀어 보여주는 연출로 유명합니다.",
            ),
            Quiz(
                id=4,
                question="영화 '인터스텔라'에서 주인공이 방문하지 않은 행성은 무엇일까요?",
                choices=["밀러 박사의 행성", "만 박사의 행성", "에드먼즈 행성", "화성"],
                answer=4,
                hint="세 행성은 모두 극 중 탐사 대상이지만 하나는 현실의 행성입니다.",
            ),
            Quiz(
                id=5,
                question="영화 '어벤져스: 엔드게임'에서 시간 여행 작전을 부르는 이름은 무엇일까요?",
                choices=["타임 점프", "타임 하이스트", "타임 워프", "멀티버스 미션"],
                answer=2,
                hint="강탈 작전을 뜻하는 영어 단어가 들어갑니다.",
            ),
        ]

    def show_menu(self) -> None:
        print("\n" + "=" * 38)
        print("영화 상식 퀴즈 게임")
        print("=" * 38)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 퀴즈 삭제")
        print("5. 최고 점수 확인")
        print("6. 종료")
        print("=" * 38)

    def run(self) -> None:
        while True:
            self.show_menu()
            choice = self.get_int_input("선택: ", valid_range=range(1, 7))

            if choice == 1:
                self.play_quiz()
            elif choice == 2:
                self.add_quiz()
            elif choice == 3:
                self.list_quizzes()
            elif choice == 4:
                self.delete_quiz()
            elif choice == 5:
                self.show_best_score()
            elif choice == 6:
                self.safe_exit("프로그램을 종료합니다.")
                break

    def get_int_input(self, prompt: str, valid_range: range | None = None) -> int:
        while True:
            raw = input(prompt).strip()

            if raw == "":
                print("빈 입력은 사용할 수 없습니다. 다시 입력해주세요.")
                continue

            try:
                value = int(raw)
            except ValueError:
                print("숫자를 입력해주세요.")
                continue

            if valid_range is not None and value not in valid_range:
                start = valid_range.start
                end = valid_range.stop - 1
                print(f"{start}~{end} 사이의 숫자를 입력해주세요.")
                continue

            return value

    def get_yes_no_input(self, prompt: str) -> bool:
        while True:
            raw = input(prompt).strip().lower()
            if raw in {"y", "yes"}:
                return True
            if raw in {"n", "no"}:
                return False
            print("y 또는 n으로 입력해주세요.")

    def format_score(self, score: float) -> str:
        if score.is_integer():
            return str(int(score))
        return f"{score:.1f}"

    def play_quiz(self) -> None:
        if not self.quizzes:
            print("\n등록된 퀴즈가 없습니다.")
            return

        total_quiz_count = len(self.quizzes)
        quiz_count = self.get_int_input(
            f"몇 문제를 풀까요? (1~{total_quiz_count}): ",
            valid_range=range(1, total_quiz_count + 1),
        )
        quizzes_to_play = self.quizzes[:]
        random.shuffle(quizzes_to_play)
        selected_quizzes = quizzes_to_play[:quiz_count]

        print(f"\n퀴즈를 시작합니다. (총 {quiz_count}문제)\n")
        score = 0.0
        correct_count = 0
        used_hints = 0

        for number, quiz in enumerate(selected_quizzes, start=1):
            print("-" * 38)
            quiz.display(number)
            used_hint = self.get_yes_no_input("힌트를 볼까요? (y/n): ")
            if used_hint:
                used_hints += 1
                quiz.display_hint()
            user_answer = self.get_int_input("정답 입력 (1~4): ", valid_range=range(1, 5))

            if quiz.is_correct(user_answer):
                correct_count += 1
                earned_score = (
                    self.HINT_PENALTY_SCORE if used_hint else self.FULL_SCORE
                )
                score += earned_score
                print(f"정답입니다. 획득 점수: {self.format_score(earned_score)}점")
            else:
                correct_text = quiz.choices[quiz.answer - 1]
                print(f"오답입니다. 정답은 {quiz.answer}번({correct_text}) 입니다.")

        percent = round((score / quiz_count) * 100, 1)
        self.record_history(
            total_questions=quiz_count,
            correct_count=correct_count,
            used_hints=used_hints,
            score=score,
            percent=percent,
        )
        print("\n" + "=" * 38)
        print(
            f"결과: {quiz_count}문제 중 총점 {self.format_score(score)}점 "
            f"({self.format_score(percent)}점)"
        )

        previous_best = self.best_score
        if previous_best is None or percent > previous_best:
            self.best_score = percent
            print("새로운 최고 점수입니다.")
            self.save_state()
        else:
            print(f"현재 최고 점수는 {self.best_score}점입니다.")
            self.save_state()

        print("=" * 38)

    def add_quiz(self) -> None:
        print("\n새로운 퀴즈를 추가합니다.")

        question = self.get_non_empty_text("문제를 입력하세요: ")
        choices: list[str] = []

        for index in range(1, 5):
            choice = self.get_non_empty_text(f"선택지 {index}: ")
            choices.append(choice)

        answer = self.get_int_input("정답 번호 (1~4): ", valid_range=range(1, 5))
        hint = self.get_non_empty_text("힌트를 입력하세요: ")
        new_quiz = Quiz(
            id=self.get_next_quiz_id(),
            question=question,
            choices=choices,
            answer=answer,
            hint=hint,
        )
        self.quizzes.append(new_quiz)
        self.save_state()

        print("퀴즈가 추가되었습니다.")

    def get_next_quiz_id(self) -> int:
        if not self.quizzes:
            return 1
        return max(quiz.id for quiz in self.quizzes) + 1

    def get_non_empty_text(self, prompt: str) -> str:
        while True:
            text = input(prompt).strip()
            if text == "":
                print("빈 입력은 사용할 수 없습니다. 다시 입력해주세요.")
                continue
            return text

    def list_quizzes(self) -> None:
        if not self.quizzes:
            print("\n등록된 퀴즈가 없습니다.")
            return

        print(f"\n등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        print("-" * 38)
        for index, quiz in enumerate(self.quizzes, start=1):
            print(f"[{index}] (id: {quiz.id}) {quiz.question}")

    def delete_quiz(self) -> None:
        if not self.quizzes:
            print("\n삭제할 퀴즈가 없습니다.")
            return

        print(f"\n삭제할 퀴즈를 선택하세요. (총 {len(self.quizzes)}개)")
        print("-" * 38)
        for index, quiz in enumerate(self.quizzes, start=1):
            print(f"[{index}] (id: {quiz.id}) {quiz.question}")

        delete_index = self.get_int_input(
            "삭제할 퀴즈 번호: ",
            valid_range=range(1, len(self.quizzes) + 1),
        )
        deleted_quiz = self.quizzes.pop(delete_index - 1)
        self.save_state()
        print(f"퀴즈를 삭제했습니다: {deleted_quiz.question}")

    def show_best_score(self) -> None:
        print()
        if self.best_score is None:
            print("아직 기록된 최고 점수가 없습니다.")
        else:
            print(f"최고 점수: {self.best_score}점")

    def record_history(
        self,
        total_questions: int,
        correct_count: int,
        used_hints: int,
        score: float,
        percent: float,
    ) -> None:
        self.history.append(
            {
                "played_at": datetime.now().isoformat(timespec="seconds"),
                "total_questions": total_questions,
                "correct_count": correct_count,
                "used_hints": used_hints,
                "score": score,
                "percent": percent,
            }
        )

    def load_state(self) -> None:
        if not self.state_path.exists():
            self.quizzes = self.get_default_quizzes()
            self.best_score = None
            self.history = []
            print("저장 파일이 없어 기본 퀴즈 데이터를 불러왔습니다.")
            return

        try:
            with self.state_path.open("r", encoding="utf-8") as file:
                data = json.load(file)

            quizzes_data = data.get("quizzes", [])
            self.quizzes = [Quiz.from_dict(item) for item in quizzes_data]

            raw_best_score = data.get("best_score")
            self.best_score = None if raw_best_score is None else int(raw_best_score)
            history_data = data.get("history", [])
            self.history = [self.normalize_history_entry(item) for item in history_data]

            if not self.quizzes:
                self.quizzes = self.get_default_quizzes()
                print("저장된 퀴즈가 없어 기본 퀴즈 데이터를 불러왔습니다.")
            else:
                score_text = f", 최고 점수 {self.best_score}점" if self.best_score is not None else ""
                print(
                    f"저장된 데이터를 불러왔습니다. "
                    f"(퀴즈 {len(self.quizzes)}개, 기록 {len(self.history)}개{score_text})"
                )

        except (json.JSONDecodeError, KeyError, TypeError, ValueError):
            self.quizzes = self.get_default_quizzes()
            self.best_score = None
            self.history = []
            print("state.json 파일이 손상되어 기본 퀴즈 데이터로 시작합니다.")
        except OSError:
            self.quizzes = self.get_default_quizzes()
            self.best_score = None
            self.history = []
            print("파일을 읽는 중 오류가 발생해 기본 퀴즈 데이터로 시작합니다.")

    def save_state(self) -> None:
        data: dict[str, Any] = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
            "history": self.history,
        }

        try:
            with self.state_path.open("w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
        except OSError:
            print("데이터를 저장하지 못했습니다.")

    def normalize_history_entry(self, data: dict[str, Any]) -> dict[str, Any]:
        return {
            "played_at": str(data["played_at"]),
            "total_questions": int(data["total_questions"]),
            "correct_count": int(data["correct_count"]),
            "used_hints": int(data["used_hints"]),
            "score": float(data["score"]),
            "percent": float(data["percent"]),
        }

    def safe_exit(self, message: str) -> None:
        self.save_state()
        print(message)
