FILE(REMOVE_RECURSE
  "libf1_headers.pdb"
  "libf1_headers.a"
)

# Per-language clean rules from dependency scanning.
FOREACH(lang)
  INCLUDE(CMakeFiles/f1_headers.dir/cmake_clean_${lang}.cmake OPTIONAL)
ENDFOREACH(lang)
