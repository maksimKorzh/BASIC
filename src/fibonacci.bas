5 PRINT "How many Fibonacci numbers do you want to print?"
10 LET n = INPUT
15 IF n = 0 THEN GOTO 150
20 LET first = 0
30 LET second = 1
34 PRINT ""
35 PRINT "Here is(are) your ", n, " Fibonacci number(s):"
40 PRINT first
50 IF n = 1 THEN GOTO 150
60 PRINT second
70 IF n = 2 THEN GOTO 150
80 LET count = 3
90 LET next = first + second
100 PRINT next
110 LET first = second
120 LET second = next
130 LET count = count + 1
140 IF count < n + 1 THEN GOTO 90
150 PRINT "All done!"
