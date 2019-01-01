#!/usr/bin/env newlisp

(define (play label num_players num_marbles)
  (set 'marbles '(0))
  (set 'scores (array num_players (list 0)))
  (for (marble 1 num_marbles)
    (if (= (% marble 23) 0) (begin
      ;(rotate marbles 7)
      (for (i 1 7) (push (pop marbles -1) marbles))
      (inc (scores (% marble num_players)) (+ marble (pop marbles)))
    ) (begin
      ;(if (!= marble 2) (rotate marbles -2))
      (if (> marble 2) (for (i 1 2) (push (pop marbles) marbles -1)))
      (push marble marbles)
    ))
    (if
      (= (% marble 10000) 0)
      (println label " done: " marble " (" (round (/ (* 100 marble) num_marbles)) "%)")
    )
  )
  (apply 'max scores)
)

(define (part1 label input)
  (set 'inp (map int (find-all {\d+} input)))
  (set 'players (inp 0))
  (set 'marbles (inp 1))
  (set 'res (play label players marbles))
  (println label ": " res)
)

(define (part2 label input)
  (set 'inp (map int (find-all {\d+} input)))
  (set 'players (inp 0))
  (set 'marbles (* 100 (inp 1)))
  (set 'res (play label players marbles))
  (println label ": " res)
)

(part1 "Test 1a" "9 players; last marble is worth 25 points")
(part1 "Test 1b" "10 players; last marble is worth 1618 points")
(part1 "Test 1c" "13 players; last marble is worth 7999 points")
(part1 "Test 1d" "17 players; last marble is worth 1104 points: high score is")
(part1 "Test 1e" "21 players; last marble is worth 6111 points")
(part1 "Test 1f" "30 players; last marble is worth 5807 points")

(part1 "Part 1" (read-file "day09.in"))
(part2 "Part 2" (read-file "day09.in"))

(exit)
