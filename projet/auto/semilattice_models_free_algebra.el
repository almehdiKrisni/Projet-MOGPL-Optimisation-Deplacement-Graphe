(TeX-add-style-hook
 "semilattice_models_free_algebra"
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
    "sec:semilattice_models_free_algebra"
    "def:aml_free_algebra_1"
    "def:aml_free_algebra_2"
    "prop:card_free_algebra"
    "def:natural_homomorphism"
    "the:aml2"
    "eq:freeisterm"
    "the:aml1"
    "not:model"
    "eq:semilattice_M1"
    "fig:M1"
    "fig:M_1"
    "ex:natural_homomorphism"
    "def:duple"))
 :latex)

