# Git과 함께하는 Python 첫 발자국

## 1. 프로젝트 개요

이 프로젝트는 Python으로 만든 콘솔 기반 퀴즈 게임입니다.  
사용자는 메뉴를 통해 퀴즈를 풀고, 새로운 퀴즈를 추가하고, 등록된 퀴즈 목록을 확인하고, 최고 점수를 조회할 수 있습니다.

이번 과제의 핵심 목표는 다음 세 가지를 직접 경험하는 것입니다.

- Python 기본 문법으로 동작하는 프로그램 만들기
- 클래스(`Quiz`, `QuizGame`)로 역할을 나누어 구조화하기
- Git으로 기능 단위 커밋, 브랜치 생성, 병합 기록 남기기

또한 `state.json` 파일을 사용해 퀴즈 데이터, 최고 점수, 게임 기록을 저장하도록 구현해 프로그램을 종료한 뒤 다시 실행해도 이전 상태가 유지되도록 구성했습니다.

---

## 2. 퀴즈 주제 선정 이유

퀴즈 주제는 `영화 상식`입니다.

영화는 평소에도 자주 접하는 분야라 문제를 직접 만들기 좋았고, 감독, 작품, 설정, 시리즈 관련 내용처럼 다양한 방식으로 문제를 확장할 수 있어 퀴즈 게임 주제로 적합하다고 판단했습니다.  
또한 4지선다형 문제를 만들기에도 자연스럽고, 난이도를 조절하기 쉬워 콘솔 기반 퀴즈 게임의 주제로 사용했습니다.

---

## 3. 개발 환경

- Python 3.10 이상
- 표준 라이브러리만 사용
- 실행 환경: 터미널 / 콘솔

---

## 4. 실행 방법

### 1) 저장소 클론

```bash
git clone [본인 저장소 주소]
cd Python_quiz
```

### 2) 프로그램 실행

```bash
python main.py
```

환경에 따라 아래 명령어를 사용할 수도 있습니다.

```bash
python3 main.py
```

---

## 5. 기능 목록

### 필수 기능

- 메뉴 출력 및 번호 선택
- 퀴즈 풀기
- 퀴즈 추가
- 퀴즈 목록 확인
- 최고 점수 확인
- 프로그램 종료
- `state.json` 저장 / 불러오기
- 잘못된 입력 처리
- `Ctrl+C`, `EOFError` 예외 처리

### 보너스 기능

- 퀴즈 출제 순서 랜덤 셔플
- 사용자가 풀 문제 수 선택
- 힌트 출력 기능
- 힌트 사용 시 점수 차감
- 퀴즈 삭제 기능
- 게임 기록(`history`) 저장 기능

---

## 6. 주요 기능 설명

### 1) 퀴즈 풀기

- 저장된 퀴즈를 랜덤 순서로 출제합니다.
- 사용자가 풀 문제 수를 직접 선택할 수 있습니다.
- 각 문제마다 힌트 사용 여부를 선택할 수 있습니다.
- 힌트를 사용하지 않고 맞히면 `1점`, 힌트를 사용하고 맞히면 `0.5점`을 획득합니다.
- 한 게임이 끝나면 총점과 퍼센트를 출력합니다.
- 최고 점수를 갱신하면 즉시 저장합니다.

### 2) 퀴즈 추가

- 문제, 선택지 4개, 정답 번호, 힌트를 입력받아 새 퀴즈를 등록합니다.
- 퀴즈마다 고유한 `id`를 부여합니다.
- 추가한 퀴즈는 즉시 `state.json`에 저장됩니다.

### 3) 퀴즈 목록 확인

- 현재 저장된 퀴즈 목록을 출력합니다.
- 각 퀴즈는 번호와 `id`, 문제 내용이 함께 표시됩니다.

### 4) 퀴즈 삭제

- 등록된 퀴즈 중 하나를 선택해 삭제할 수 있습니다.
- 삭제 후 즉시 `state.json`에 반영됩니다.

### 5) 점수 및 기록 확인

- 최고 점수를 확인할 수 있습니다.
- 게임이 끝날 때마다 플레이 기록이 `history`에 저장됩니다.
- 기록에는 플레이 시각, 푼 문제 수, 정답 수, 사용한 힌트 수, 총점, 퍼센트가 포함됩니다.

---

## 7. 공통 입력 처리 및 예외 처리

다음 입력/예외 상황을 처리하도록 구현했습니다.

- 숫자 입력 전 공백 제거
- 빈 입력 방지
- 숫자 변환 실패 시 재입력 처리
- 허용 범위 밖 숫자 입력 시 재입력 처리
- `KeyboardInterrupt` (`Ctrl+C`) 발생 시 저장 후 안전 종료
- `EOFError` 발생 시 저장 후 안전 종료
- `state.json` 파일이 없으면 기본 퀴즈 데이터로 시작
- `state.json` 파일이 손상되었으면 안내 메시지 출력 후 기본 데이터로 복구

---

## 8. 클래스 구조

### `Quiz`

개별 퀴즈 1개를 표현하는 클래스입니다.

속성:

- `id`
- `question`
- `choices`
- `answer`
- `hint`

주요 메서드:

- `display()`
- `display_hint()`
- `is_correct()`
- `to_dict()`
- `from_dict()`

### `QuizGame`

게임 전체 흐름을 관리하는 클래스입니다.

속성:

- `quizzes`
- `best_score`
- `history`

주요 메서드:

- `show_menu()`
- `run()`
- `play_quiz()`
- `add_quiz()`
- `list_quizzes()`
- `delete_quiz()`
- `show_best_score()`
- `load_state()`
- `save_state()`

---

## 9. 파일 구조

```text
Python_quiz/
├─ main.py
├─ quiz.py
├─ quiz_game.py
├─ state.json
├─ README.md
├─ commit-plan.md
└─ docs/
   └─ screenshots/
      ├─ menu.png
      ├─ play.png
      ├─ add_quiz.png
      ├─ score.png
      ├─ delete.png
      ├─ history.png
      └─ git-log.png
```

### 파일 설명

- `main.py`: 프로그램 시작 파일
- `quiz.py`: `Quiz` 클래스 정의
- `quiz_game.py`: `QuizGame` 클래스 및 전체 게임 로직
- `state.json`: 퀴즈, 최고 점수, 게임 기록 저장 파일
- `README.md`: 프로젝트 설명 문서

---

## 10. 데이터 파일 설명

데이터 파일은 프로젝트 루트의 [`state.json`](C:\Users\guswn\Desktop\코디세이\Python_quiz\state.json) 을 사용합니다.

역할:

- 퀴즈 목록 저장
- 최고 점수 저장
- 플레이 기록 저장

현재 스키마 예시는 다음과 같습니다.

```json
{
  "quizzes": [
    {
      "id": 1,
      "question": "영화 '기생충'의 감독은 누구일까요?",
      "choices": ["박찬욱", "봉준호", "김기덕", "이창동"],
      "answer": 2,
      "hint": "아카데미 작품상을 받은 한국 영화의 감독입니다."
    }
  ],
  "best_score": 60,
  "history": [
    {
      "played_at": "2026-04-03T15:10:00",
      "total_questions": 3,
      "correct_count": 2,
      "used_hints": 1,
      "score": 1.5,
      "percent": 50.0
    }
  ]
}
```

필드 설명:

- `quizzes`: 저장된 퀴즈 목록
- `best_score`: 최고 점수
- `history`: 게임 플레이 기록 목록
- `played_at`: 플레이 시각
- `total_questions`: 푼 문제 수
- `correct_count`: 맞힌 문제 수
- `used_hints`: 사용한 힌트 수
- `score`: 해당 게임의 총점
- `percent`: 해당 게임의 점수 퍼센트

---

## 11. 실행 화면

### 메뉴 화면

![메뉴 화면](./screenshots/게임메뉴.png)

### 퀴즈 풀기 화면

![퀴즈 풀기 화면](./screenshots/퀴즈풀기.png)

### 퀴즈 추가 화면

![퀴즈 추가 화면](./screenshots/퀴즈추가.png)

### 점수 확인 화면

![점수 확인 화면](./screenshots/점수확인.png)

### 퀴즈 삭제 화면

![퀴즈 삭제 화면](./screenshots/퀴즈삭제.png)

### 게임 기록 화면 또는 state.json 확인 화면

![게임 기록 화면](./screenshots/게임기록화면.png)

## 12. Git 작업 내용

기능 단위로 커밋을 나누어 작업했고, 브랜치를 생성해 병합하는 흐름도 실습했습니다.

예시 커밋:

- `feat: Quiz 모델에 hint, id 필드 추가`
- `feat: 퀴즈 출제 랜덤 셔플 및 문제 수 선택 기능 추가`
- `feat: Quiz hint 출력 및 힌트 감점 로직 추가`
- `feat: 퀴즈 삭제 및 상태 저장 반영`
- `feat: 게임 기록 저장 기능 추가`

---

## 13. 브랜치 활용 흔적

아래는 실제 브랜치 생성 및 병합 기록입니다.

```bash
guswn@DESKTOP-CNJJNL7 MINGW64 ~/Desktop/코디세이/Python_quiz (main)
$ git switch -c feature/quiz-delete
Switched to a new branch 'feature/quiz-delete'

guswn@DESKTOP-CNJJNL7 MINGW64 ~/Desktop/코디세이/Python_quiz (feature/quiz-delete)
$ git add quiz_game.py
warning: in the working copy of 'quiz_game.py', LF will be replaced by CRLF the next time Git touches it

guswn@DESKTOP-CNJJNL7 MINGW64 ~/Desktop/코디세이/Python_quiz (feature/quiz-delete)
$ git commit -m "feat: 퀴즈 삭제 및 상태 저장 반영"
[feature/quiz-delete e930bf8] feat: 퀴즈 삭제 및 상태 저장 반영
1 file changed, 25 insertions(+), 4 deletions(-)

guswn@DESKTOP-CNJJNL7 MINGW64 ~/Desktop/코디세이/Python_quiz (feature/quiz-delete)
$ git switch main
Switched to branch 'main'
Your branch is ahead of 'origin/main' by 3 commits.
(use "git push" to publish your local commits)

guswn@DESKTOP-CNJJNL7 MINGW64 ~/Desktop/코디세이/Python_quiz (main)
$ git merge feature/quiz-delete
Updating dd0a929..e930bf8
Fast-forward
quiz_game.py | 29 +++++++++++++++++++++++++----
1 file changed, 25 insertions(+), 4 deletions(-)
```

## 14. clone / pull 실습 기록

![깃헙사용1]](./screenshots/깃헙사용.png)
![깃헙사용22](./screenshots/깃헙사용2.png)

---

## 15. 느낀 점

이번 과제를 통해 Python 문법을 아는 것과 실제로 동작하는 프로그램을 끝까지 완성하는 것은 다르다는 점을 체감했습니다.  
특히 클래스 분리, 파일 저장, 예외 처리, 입력 검증을 직접 구현하면서 프로그램 구조를 생각하는 연습이 많이 되었습니다.

또한 Git으로 기능 단위 커밋을 남기고, 브랜치를 나누어 작업한 뒤 병합하는 과정을 직접 경험하면서 버전 관리 흐름도 함께 익힐 수 있었습니다.

---

## 16. 제출 체크리스트

- [x] 프로젝트 개요 작성
- [x] 퀴즈 주제 선정 이유 작성
- [x] 실행 방법 작성
- [x] 기능 목록 작성
- [x] 파일 구조 작성
- [x] 데이터 파일 설명 작성
- [x] 브랜치 활용 기록 추가
- [x] 실행 화면 스크린샷 첨부
- [x] `git log --oneline --graph` 스크린샷 첨부
- [x] `clone`, `pull` 기록 추가
- [x] GitHub 저장소 URL 기입

---

## 17. GitHub 저장소 URL

- 저장소 URL: `[https://github.com/stnguswnd/Python_quiz]`
