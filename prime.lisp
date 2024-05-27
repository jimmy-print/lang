(set "n" 3);

(while (< ($ "n") 10000)
    (set "i" 2)

    (set "prime" "none")

    (while (< ($ "i") ($ "n"))
        (if (= (% ($ "n") ($ "i")) 0)
            (set "prime" "no"))
        (set "i" (+ ($ "i") 1)))

    (if (= ($ "prime") "none")
        (set "prime" "yes"))

    (print "{}{}" ($ "n") ($ "prime"))
    (set "n" (+ ($ "n") 1)));