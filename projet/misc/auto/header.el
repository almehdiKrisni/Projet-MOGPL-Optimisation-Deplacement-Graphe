(TeX-add-style-hook
 "header"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-package-options
                     '(("geometry" "margin=1.2in") ("babel" "english") ("natbib" "numbers")))
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
   (TeX-run-style-hooks
    "latex2e"
    "article"
    "art10"
    "geometry"
    "babel"
    "amsthm"
    "amsmath"
    "amssymb"
    "amsfonts"
    "mathtools"
    "bm"
    "proof-at-the-end"
    "pict2e"
    "picture"
    "graphicx"
    "tikz"
    "subcaption"
    "xcolor"
    "wrapfig"
    "float"
    "comment"
    "enumitem"
    "epigraph"
    "environ"
    "listings"
    "lipsum"
    "mwe"
    "abstract"
    "multicol"
    "refcount"
    "hyperref"
    "censor"
    "natbib")
   (TeX-add-symbols
    '("highlight" 1)
    "coveringA"
    "coveringB"
    "pictcoveringB"
    "equivclass")
   (LaTeX-add-environments
    "reponse"
    "dedication")
   (LaTeX-add-amsthm-newtheorems
    "theorem"
    "corollary"
    "lemma"
    "prop"
    "definition"
    "example"
    "property"
    "notation"
    "convention"
    "interpretation"
    "remark"
    "note"
    "question"
    "assertion"
    "sptheorem"
    "spcorollary"
    "splemma"
    "spprop"
    "spdefinition"
    "spproperty")
   (LaTeX-add-amsthm-newtheoremstyles
    "specialthm"
    "specialdef"))
 :latex)

