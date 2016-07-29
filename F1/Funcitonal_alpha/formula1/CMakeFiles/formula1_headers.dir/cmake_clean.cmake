FILE(REMOVE_RECURSE
  "libformula1_headers.pdb"
  "libformula1_headers.a"
)

# Per-language clean rules from dependency scanning.
FOREACH(lang)
  INCLUDE(CMakeFiles/formula1_headers.dir/cmake_clean_${lang}.cmake OPTIONAL)
ENDFOREACH(lang)
