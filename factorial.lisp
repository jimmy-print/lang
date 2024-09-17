(set "i" 1);
(set "limit" 10000);
(while (< ($ "i") ($ "limit"))
    (print "number:{}" ($ "i"))

    (set "j" 1)
    (set "t" 1)
    (while (! (= ($ "j") (+ ($ "i") 1)))
        (set "t" (* ($ "t") ($ "j")))
        (set "j" (+ ($ "j") 1)))
    (print "factorial-of{}is-{}" ($ "i") ($ "t"))

    (set "i" (+ ($ "i") 1))
);
