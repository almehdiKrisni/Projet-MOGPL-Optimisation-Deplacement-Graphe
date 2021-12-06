(TeX-add-style-hook
 "algos"
 (lambda ()
   (add-to-list 'LaTeX-verbatim-environments-local "lstlisting")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "lstinline")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "path")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "url")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "nolinkurl")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperbaseurl")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperimage")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperref")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "href")
   (add-to-list 'LaTeX-verbatim-macros-with-delims-local "lstinline")
   (add-to-list 'LaTeX-verbatim-macros-with-delims-local "path")
   (LaTeX-add-labels
    "sec:algos"
    "sec:transfo"
    "eq:8"
    "eq:9"
    "alg:transfo"
    "sec:plus-tot"
    "alg:plus-tot"
    "eq:10"
    "sec:plus-tard"
    "alg:plus-tard"
    "sec:plus-rapide"
    "alg:plus-rapide"
    "sec:plus-court"
    "alg:plus-court"
    "sec:plus-court-pl"
    "sec:algos-sans-transfo"
    "sec:tests"))
 :latex)

