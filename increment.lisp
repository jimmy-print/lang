(print "thisProgramShouldPrintAllNumbersFrom0to999.");
(input "pressEnterToContinue...");
(set "i" 0);
(while (< ($ "i") 1000)
    (print "{}" ($ "i"))
    (set "i" (+ ($ "i") 1)))
