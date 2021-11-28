(TeX-add-style-hook
 "univ-algebra"
 (lambda ()
   (TeX-run-style-hooks
    "sections/subsections/ordered_sets-lattices-abstract_algebra"
    "sections/subsections/congruences-quotient_algebra-morphisms"
    "sections/subsections/term_algebra-free_algebra")
   (LaTeX-add-labels
    "sec:univ_algebra"))
 :latex)

