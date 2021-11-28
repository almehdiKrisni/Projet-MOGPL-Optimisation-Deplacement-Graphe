(TeX-add-style-hook
 "aml"
 (lambda ()
   (TeX-run-style-hooks
    "sections/subsections/semilattices_knowledge_representation"
    "sections/subsections/semilattice_models_free_algebra"
    "sections/subsections/atomized_semilattices"
    "sections/subsections/full_crossing"
    "sections/subsections/learning")
   (LaTeX-add-labels
    "sec:aml_theory"))
 :latex)

