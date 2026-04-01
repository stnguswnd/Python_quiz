from __future__ import annotations

from quiz_game import QuizGame #QuizGame 클래스 가져오기. 


def main() -> None:
    game = QuizGame() #객체를 하나 만들고, 그 객체 네임을 gaim으로 둠. 
    try:
        game.run() #게임을 실행하는 메쏘드, 먼저 메뉴를 보여주고, 사용자가 1번 누르면 퀴즈, 2번 누르면 퀴즈 추가함.
    except KeyboardInterrupt: #Crtl+C를 누른 경우
        game.safe_exit("\n⚠ Ctrl+C가 입력되어 프로그램을 안전하게 종료합니다.")
    except EOFError: #사용자가 키를 잘못눌러서, 컨트롤 + Z/D 등 
        game.safe_exit("\n⚠ 입력이 종료되어 프로그램을 안전하게 종료합니다.")


if __name__ == "__main__":
    main()
