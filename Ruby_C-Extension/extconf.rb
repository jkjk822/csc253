require 'mkmf'
extension_name = 'mychash'
$CPPFLAGS = "-std=c11"
create_makefile(extension_name)