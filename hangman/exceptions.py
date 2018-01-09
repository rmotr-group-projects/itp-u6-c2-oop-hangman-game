class InvalidListOfWordsException(Exception):
    print("Not a valid list of words")


class InvalidWordException(Exception):
    print("Not a valid word")


class GameWonException(Exception):
    print("Game is won!")


class GameLostException(Exception):
    print("Game is lost!")


class GameFinishedException(Exception):
    print("Game is finished!")


class InvalidGuessedLetterException(Exception):
    print("Not a valid guess")


class InvalidGuessAttempt(Exception):
    print("Not a valid guess")
