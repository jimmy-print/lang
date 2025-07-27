(set "n" 2);
(set "target" 100);

(while (< (get "n") (get "target"))
	(set "perf" 0)
	(set "i" 1)
	(set "sum" 0)

	(while (< (get "i") (get "n"))
		(if (= (% (get "n") (get "i")) 0)
			(set "sum" (+ (get "sum") (get "i"))))
		(set "i" (+ (get "i") 1)))

	(if (= (get "sum") (get "n"))
		(set "perf" 1))
	(if (= (get "perf") 1)
		(print "{}isPerfect" (get "n")))

	(set "n" (+ (get "n") 1)));

(print "allIntegersLessThan{}HaveBeenChecked" (get "target"));
