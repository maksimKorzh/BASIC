5 PRINT "Up to which number would you like to calculate the prime numbers?"
10 LET n = INPUT
15 PRINT ""
20 PRINT "Prime numbers up to ", n, ":"
30 IF n < 2 THEN GOTO 200
40 PRINT 2
45 IF n < 3 THEN GOTO 200
50 PRINT 3
60 LET num = 5
70 IF num < n THEN GOTO 80
71 GOTO 200
75 IF num = n THEN GOTO 80
76 GOTO 200
80 LET prime = 1
90 LET d = 3
100 IF d * d > num THEN GOTO 170
110 IF num - ((num / d) * d) = 0 THEN GOTO 120
115 GOTO 140
120 LET prime = 0
130 GOTO 170
140 LET d = d + 2
150 GOTO 100
160 GOTO 70
170 IF prime = 1 THEN PRINT num
180 LET num = num + 2
190 GOTO 70
200 PRINT "All done!"
