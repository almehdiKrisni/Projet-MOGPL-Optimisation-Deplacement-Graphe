(TeX-add-style-hook
 "implementation"
 (lambda ()
   (TeX-run-style-hooks
    "sections/subsections/bitwise_32")
   (LaTeX-add-labels
    "sec:upmem_implementation"))
 :latex)

