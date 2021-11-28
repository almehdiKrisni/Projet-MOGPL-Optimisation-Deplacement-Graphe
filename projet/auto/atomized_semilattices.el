(TeX-add-style-hook
 "atomized_semilattices"
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
    "sec:atomized_semilattices"
    "fig:asl_fc0"
    "fig:asl_M1"
    "def:atomized_semilattice"
    "lemma:tautology"
    "lemma:1.2"
    "lemma:1.3"
    "lemma:1.4"
    "thm:asl_order"
    "thm:asl1"
    "eq:extandedAS4"
    "thm:asl2"
    "prop:terms"
    "thm:mine"
    "def:ext"
    "fig:hypergraph"))
 :latex)

