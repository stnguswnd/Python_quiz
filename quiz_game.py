from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from quiz import Quiz


class QuizGame: 
    def __init__(self, state_file: str = "state.json") -> None: #객체가 생성될떄 자동 실행됨
        self.state_path = Path(state_file) #json 파일 경로 저장
        self.quizzes: list[Quiz] = [] #퀴즈 목록을 저장할 리스트 
        self.best_score: int | None = None #최고 점수를 저장하는 변수
        self.load_state() #시작하마자 파일에서 기존 데이터를 읽음.

    def get_default_quizzes(self) -> list[Quiz]: #만약 처음 시작 시 state.json이 없거나 손상되었으면 이걸로 시작됨
        return [
            Quiz(
                question="영화 '기생충'의 감독은 누구인가?",
                choices=["박찬욱", "봉준호", "김기덕", "이창동"],
                answer=2,
            ),
            Quiz(
                question="마블 시네마틱 유니버스에서 타노스가 모은 인피니티 스톤의 개수는?",
                choices=["4개", "5개", "6개", "7개"],
                answer=3,
            ),
            Quiz(
                question="영화 '인셉션'의 감독은 누구인가?",
                choices=["크리스토퍼 놀란", "스티븐 스필버그", "제임스 카메론", "리들리 스콧"],
                answer=1,
            ),
            Quiz(
                question="영화 '인터스텔라'에서 주인공이 방문하지 않은 행성은?",
                choices=["밀러 행성", "만 박사의 행성", "에드먼즈 행성", "판도라 행성"],
                answer=4,
            ),
            Quiz(
                question="영화 '어벤져스: 엔드게임'에서 시간여행 작전을 부르는 이름은?",
                choices=["타임 워프", "타임 하이스트", "퀀텀 런", "멀티버스 미션"],
                answer=2,
            ),
        ]

    def show_menu(self) -> None: #메뉴 화면 출력  
        print("\n" + "=" * 38)
        print("🎬 나만의 영화 퀴즈 게임 🎬")
        print("=" * 38)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")
        print("=" * 38) #38번 반복해서 출력해라.

    def run(self) -> None: #무한 반복을 돌며 계속 메뉴를 보여줌. 
        while True:
            self.show_menu()
            choice = self.get_int_input("선택: ", valid_range=range(1, 6))

            if choice == 1:
                self.play_quiz()
            elif choice == 2:
                self.add_quiz()
            elif choice == 3:
                self.list_quizzes()
            elif choice == 4:
                self.show_best_score()
            elif choice == 5:
                self.safe_exit("프로그램을 종료합니다.")
                break

    #숫자 입력 받을 때 
    def get_int_input(self, prompt: str, valid_range: range | None = None) -> int:
        while True:
            raw = input(prompt).strip()

            if raw == "":
                print("⚠ 빈 입력은 사용할 수 없습니다. 다시 입력해주세요.")
                continue

            try:
                value = int(raw)
            except ValueError:
                print("⚠ 숫자를 입력해주세요.")
                continue

            if valid_range is not None and value not in valid_range:
                start = valid_range.start
                end = valid_range.stop - 1
                print(f"⚠ {start}~{end} 사이의 숫자를 입력해주세요.")
                continue

            return value
        
    #퀴즈 입력 
    def play_quiz(self) -> None:
        if not self.quizzes:
            print("\n등록된 퀴즈가 없습니다.")
            return

        print(f"\n🎯 퀴즈를 시작합니다! (총 {len(self.quizzes)}문제)\n")
        score = 0

        for number, quiz in enumerate(self.quizzes, start=1):
            print("-" * 38)
            quiz.display(number) #퀴즈 내부의 함수 
            user_answer = self.get_int_input("정답 입력 (1~4): ", valid_range=range(1, 5))

            if quiz.is_correct(user_answer): #퀴즈 내부의 함수 
                score += 1
                print("✅ 정답입니다!")
            else:
                correct_text = quiz.choices[quiz.answer - 1]
                print(f"❌ 오답입니다. 정답은 {quiz.answer}번 ({correct_text}) 입니다.")

        percent = int((score / len(self.quizzes)) * 100) #맞춘 문제 수를 백분율로 바꿈
        print("\n" + "=" * 38)
        print(f"🏆 결과: {len(self.quizzes)}문제 중 {score}문제 정답! ({percent}점)")

        previous_best = self.best_score
        if previous_best is None or percent > previous_best:
            self.best_score = percent
            print("🎉 새로운 최고 점수입니다!")
            self.save_state()
        else:
            print(f"📌 현재 최고 점수는 {self.best_score}점입니다.")

        print("=" * 38)

    def add_quiz(self) -> None: #새로운 퀴즈를 추가함. 
        print("\n✨ 새로운 퀴즈를 추가합니다.")

        question = self.get_non_empty_text("문제를 입력하세요: ") #먼저 문제 내용을 입력받고
        choices: list[str] = []

        for index in range(1, 5): #선택지 4개를 반복해서 입력받음.
            choice = self.get_non_empty_text(f"선택지 {index}: ")
            choices.append(choice)

        answer = self.get_int_input("정답 번호 (1~4): ", valid_range=range(1, 5))
        new_quiz = Quiz(question=question, choices=choices, answer=answer) #새로운 퀴즈 객체를 만들고, 리스트에 추가 및 저장
        self.quizzes.append(new_quiz) #리스트 추가 
        self.save_state() #json에 저장 

        print("✅ 퀴즈가 추가되었습니다!")

    def get_non_empty_text(self, prompt: str) -> str:
        while True:
            text = input(prompt).strip() #문자열 입력용 공통함수, 빈문자열 입력 못하게 막음. 
            if text == "":
                print("⚠ 빈 입력은 사용할 수 없습니다. 다시 입력해주세요.")
                continue
            return text

    def list_quizzes(self) -> None: #저장된 문제 목록 보여주기 
        if not self.quizzes:
            print("\n등록된 퀴즈가 없습니다.")
            return

        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        print("-" * 38)
        for index, quiz in enumerate(self.quizzes, start=1):
            print(f"[{index}] {quiz.question}")

    def show_best_score(self) -> None: #최고 점수 출력하기 
        print()
        if self.best_score is None:
            print("📌 아직 기록된 최고 점수가 없습니다.")
        else:
            print(f"🏅 최고 점수: {self.best_score}점")

    def load_state(self) -> None: #파일에서 데이터를 불러오는 함수 
        if not self.state_path.exists(): #파일이 없는 경우, 
            self.quizzes = self.get_default_quizzes() #이떄는 기본 퀴즈를 넣음
            self.best_score = None
            print("📂 저장 파일이 없어 기본 퀴즈 데이터를 불러왔습니다.")
            return

        try:
            with self.state_path.open("r", encoding="utf-8") as file: #json읽기
                data = json.load(file)

            quizzes_data = data.get("quizzes", []) #이 딕셔너리 리스트를 받고
            self.quizzes = [Quiz.from_dict(item) for item in quizzes_data] #다시 quiz 객체 리스트로 만듬.

            raw_best_score = data.get("best_score") #최고 점수 복원
            if raw_best_score is None:
                self.best_score = None
            else:
                self.best_score = int(raw_best_score)

            if not self.quizzes: #파일은 있는데 퀴즈가 비어있는 경우
                self.quizzes = self.get_default_quizzes()
                print("📂 저장된 퀴즈가 없어 기본 퀴즈 데이터를 불러왔습니다.")
            else: #파일도 있고, 퀴즈도 있는 경우 
                score_text = f", 최고점수 {self.best_score}점" if self.best_score is not None else ""
                print(f"📂 저장된 데이터를 불러왔습니다. (퀴즈 {len(self.quizzes)}개{score_text})")

        except (json.JSONDecodeError, KeyError, TypeError, ValueError): #파일 손상 예외 처리 
            self.quizzes = self.get_default_quizzes()
            self.best_score = None
            print("⚠ state.json 파일이 손상되어 기본 퀴즈 데이터로 시작합니다.")
        except OSError:
            self.quizzes = self.get_default_quizzes()
            self.best_score = None
            print("⚠ 파일을 읽는 중 오류가 발생해 기본 퀴즈 데이터로 시작합니다.")

    def save_state(self) -> None: #현재 상태를 파일에 저장하는 함수 
        data: dict[str, Any] = { #현재 목록과 최고 점수를 딕셔너리로 만듬 
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
        }

        try:
            with self.state_path.open("w", encoding="utf-8") as file: #json파일로 저장함.
                json.dump(data, file, ensure_ascii=False, indent=2) #ensure_ascil는 한글이 안깨지게 저장, indent는 띄어쓰기를 의미 
        except OSError:
            print("⚠ 데이터를 저장하지 못했습니다.")

    def safe_exit(self, message: str) -> None: #종료 직전에 저장하고 메시지를 출력한느 함수 
        self.save_state()
        print(message)
