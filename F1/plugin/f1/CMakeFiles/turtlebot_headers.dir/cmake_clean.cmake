FILE(REMOVE_RECURSE
  "libturtlebot_headers.pdb"
  "libturtlebot_headers.a"
)

# Per-language clean rules from dependency scanning.
FOREACH(lang)
  INCLUDE(CMakeFiles/turtlebot_headers.dir/cmake_clean_${lang}.cmake OPTIONAL)
ENDFOREACH(lang)
