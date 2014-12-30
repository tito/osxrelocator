OSX library relocator
=====================

.. note::

	This tool came originaly from the GStreamer project. It has been extracted
	to works without cerebro, and can be used in multiples situations.
	Documentation cames from the GStreamer's OSX deployment instructions too.
	Thanks a lot to the GStreamer project!

Installation
------------

	pip install osxrelocator

Usage
-----

	osxrelocator.py [options] directory old_prefix new_prefix

Description
-----------

On Darwin operating systems, the dynamic linker doesn't locate dependent
dynamic libraries using their leaf name, but instead it uses full paths, which
makes it harder to relocate them as explained in the DYNAMIC LIBRARY LOADING
section of dyld's man page:

> Unlike many other operating systems, Darwin does not locate dependent dynamic
> libraries via their leaf file name. Instead the full path to each dylib is
> used (e.g. /usr/lib/libSystem.B.dylib). But there are times when a full path
> is not appropriate; for instance, may want your binaries to be installable in
> anywhere on the disk.

We can get the list of paths used by an object file to locate its dependent
dynamic libraries using otool::

	$ otool -L /Library/Frameworks/GStreamer.framework/Commands/gst-launch-0.10 
	/Library/Frameworks/GStreamer.framework/Commands/gst-launch-0.10:
	 /System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation (compatibility version 150.0.0, current version 550.43.0)
	 /Library/Frameworks/GStreamer.framework/Versions/0.10/x86/lib/libgstreamer-0.10.0.dylib (compatibility version 31.0.0, current version 31.0.0)
	 /Library/Frameworks/GStreamer.framework/Versions/0.10/x86/lib/libxml2.2.dylib (compatibility version 10.0.0, current version 10.8.0)

This full path is extracted from the dynamic library *install name*, a path
that is used by the linker to determine its location. The install name of a
library can be retrieved with otool too::

	$ otool -D /Library/Frameworks/GStreamer.framework/Libraries/libgstreamer-0.10.dylib 
	/Library/Frameworks/GStreamer.framework/Libraries/libgstreamer-0.10.dylib:
	/Library/Frameworks/GStreamer.framework/Versions/0.10/x86/lib/libgstreamer-0.10.0.dylib

Any object file that links to the dynamic library `gstreamer-0.10` will use the
path
`/Library/Frameworks/GStreamer.framework/Versions/0.10/x86/lib/libgstreamer-0.10.0.dylib`
to locate it.

Since working exclusively with full paths wouldn't let us install our binaries
anywhere in the path, the linker provides a mechanism of string substitution,
adding three variables that can be used as a path prefix. At runtime the linker
will replace them with the generated path for the prefix. These variables are
`@executable_path`, `@loader_path` and `@rpath`, described in depth in the
DYNAMIC LIBRARY LOADING section of dyld's man page.

For our purpose we will use the `@executable_path  variable, which is replaced
with a fixed path, the path to the directory containing the main executable:
`/Applications/MyApp.app/Contents/MacOS`. The `@loader_path` variable can't be
used in our scope, because it will be replaced with the path to the directory
containing the mach-o binary that loaded the dynamic library, which can vary.

Therefore, in order to relocate the SDK we will need to replace all paths
containing `/Library/Frameworks/GStreamer.framework/` with
`@executable_path/../Frameworks/GStreamer.framework/`, which can be done using
the `install_name_tool` utility
