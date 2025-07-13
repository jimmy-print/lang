(set "exp" 2);

(while (< $exp 100)
  (set "val" 1)
  (set "base" 2)
  (set "i" 0)
  (while (< $i $exp)
    (set "val" (* $val $base))
    (set "i" (+ $i 1)))

  (set "totest" (- $val 1))

  (set "ii" 2)
  (set "prime" "none")
  (while (< $ii $totest)
    (if (= (% $totest $ii) 0)
        (set "prime" "no"))
    (set "ii" (+ $ii 1)))

  (if (= $prime "none")
      (set "prime" "yes"))

  (if (= $prime "yes")
      (print "2**{}={}mersenneprime" $exp $totest))
  (set "exp" (+ $exp 1)));
