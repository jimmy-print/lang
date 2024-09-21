(set "n" 2);
(set "target" 100);

(while (< ($ "n") ($ "target"))
	(set "perf" 0)
	(set "i" 1)
	(set "sum" 0)

	(while (< ($ "i") ($ "n"))
		(if (= (% ($ "n") ($ "i")) 0)
			(set "sum" (+ ($ "sum") ($ "i"))))
		(set "i" (+ ($ "i") 1)))

	(if (= ($ "sum") ($ "n"))
		(set "perf" 1))
	(if (= ($ "perf") 1)
		(print "{}isPerfect" ($ "n")))

	(set "n" (+ ($ "n") 1)));

(print "allIntegersLessThan{}HaveBeenChecked" ($ "target"));
