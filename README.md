[EN] Russian Checkers Game

A Checkers game implementing strict Russian draughts rules in Python using Pygame, featuring upgraded, anti-aliased graphics.

Features:

Classic 8x8 board with smooth, anti-aliased piece graphics (pygame.gfxdraw).

Strict Russian Checkers Rules:

Mandatory Maximum Capture: If you can capture, you must. If there are multiple capture paths, you must choose the one that captures the most pieces.

Backward Captures: Regular pieces can capture opponent pieces both forwards and backwards.

Flying Kings: Kings can move and capture across any distance along diagonals.

On-the-fly Promotion: A piece passing through the promotion rank during a multi-jump sequence promotes to a King immediately and continues the jump sequence as a King.

Win or loss and no-valid-moves detection.

Requirements:

- Python 3.x version

- Pygame

Installation:

- Install Pygame: pip install pygame / if Python >3.12 Version then > pip install pygame-ce

- Run the game: python checkers.py

How to Play:

- Click on a piece to select it. Only pieces with valid moves can be selected.

- Click on a highlighted red dot to move.

- White moves first.

- Regular pieces move diagonally forward one square, but can jump/capture in any direction.

- Reach the opposite end of the board to become a King.

Controls:

- Mouse: Select and move pieces.

- Close window: Quit the game.

[DE] "Russische Dame" Spiel

Ein Dame-Spiel, das die Regeln der Russischen Dame in Python mit Pygame und verbesserten, flüssigen Grafiken implementiert.

Funktionen:

Klassisches 8x8-Brett mit geglätteten Anti-Aliasing-Grafiken (pygame.gfxdraw).

Strikte Russische Dame-Regeln:

Zwingendes Schlagen der maximalen Anzahl: Wenn ein Schlagen möglich ist, ist es Pflicht. Gibt es mehrere Möglichkeiten, muss die Sequenz gewählt werden, die die meisten Steine schlägt.

Rückwärtsschlagen: Einfache Steine können gegnerische Steine sowohl vorwärts als auch rückwärts schlagen.

Fliegende Könige: Könige können über jede Distanz entlang der Diagonalen ziehen und schlagen.

Königsumwandlung im Sprung: Erreicht ein Stein während einer Sprungsequenz die letzte Reihe, wird er sofort zum König und setzt den Sprung als König fort.

Gewinn oder Verlust und Zugunfähigkeits-Erkennung.

Anforderungen:

- Python 3.x Version

- Pygame

Installation:

- Pygame installieren: pip install pygame / Falls Python Version >3.12 ist, dann > pip install pygame-ce

- Spiel starten: python checkers.py

Spielanleitung:

- Klicke auf eine Figur, um sie auszuwählen. Es können nur Figuren mit gültigen Zügen ausgewählt werden.

- Klicke auf einen roten Punkt, um zu ziehen.

- Weiß beginnt.

- Einfache Figuren ziehen diagonal ein Feld vorwärts, können aber in jede Richtung schlagen.

- Erreiche das gegenüberliegende Ende, um ein König zu werden.

Steuerung:

- Maus: Figuren auswählen und ziehen.

- Fenster schließen: Spiel beenden.

[RU] "Русские Шашки" Игра

Игра в шашки по правилам русских шашек, реализованная на Python с использованием Pygame с улучшенной, сглаженной графикой.

Особенности:

Классическая доска 8x8 со сглаженной графикой шашек (pygame.gfxdraw).

Строгие правила русских шашек:

Обязательный бой максимального количества: Бить обязательно. Если есть выбор из нескольких вариантов взятия, необходимо выбрать тот, который снимает с доски наибольшее количество шашек противника.

Бой назад: Простые шашки могут бить шашки противника как вперед, так и назад.

Длинные ходы дамок: Дамки могут ходить и бить по диагонали на любое свободное расстояние.

Превращение на лету: Если простая шашка достигает последней горизонтали во время серии прыжков, она сразу становится дамкой и продолжает бой уже по правилам дамы.

Автоматическое определение победы и отсутствия ходов.

Требования:

- Python 3.x версия

- Pygame

Установка:

- Установите Pygame: pip install pygame / Если версия Python > 3.12, то > pip install pygame-ce

- Запустите игру: python checkers.py

Как играть:

- Кликните на шашку, чтобы выбрать её (выбрать можно только ту шашку, у которой есть допустимые ходы).

- Кликните на подсвеченную красную точку, чтобы сделать ход.

- Белые ходят первыми.

- Простые шашки ходят по диагонали вперёд на одну клетку, но могут бить в любом направлении.

- Достигните противоположного края доски, чтобы стать дамкой.

Управление:

- Мышь: Выбор и перемещение фигур.

- Закрыть окно: Выход из игры.
