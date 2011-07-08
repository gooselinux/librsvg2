%define __libtoolize :

%define libxml2_version 2.4.12
%define gtk2_version 2.9.0
%define glib2_version 2.15.4
%define freetype_version 2.0.1
%define cairo_version 1.1.2
%define libcroco_version 0.6.1
%define libgnomeui_version 2.5.0
%define libgsf_version 1.6.0
%define gnome_vfs_version 1.9.16

Name: 	 librsvg2
Summary: An SVG library based on cairo
Version: 2.26.0
Release: 5%{?dist}

License: 	LGPLv2+
Group: 		System Environment/Libraries
Source: 	http://download.gnome.org/sources/librsvg/2.26/librsvg-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:	gtk2 >= %{gtk2_version}
Requires:	libxml2 >= %{libxml2_version}
Requires:	freetype >= %{freetype_version}
Requires:       cairo >= %{cairo_version}
Requires:	libgsf >= %{libgsf_version}
Requires(post):		gtk2 >= %{gtk2_version}
Requires(postun):	gtk2 >= %{gtk2_version}
BuildRequires:  libpng-devel
BuildRequires:	glib2-devel >= %{glib2_version}
BuildRequires:	gtk2-devel >= %{gtk2_version}
BuildRequires:	libxml2-devel >= %{libxml2_version}
BuildRequires:	freetype-devel >= %{freetype_version}
BuildRequires:  cairo-devel >= %{cairo_version}
BuildRequires:  libgsf-devel, libcroco-devel
BuildRequires:  libcroco >= %{libcroco_version}
BuildRequires:  libgnomeui >= %{libgnomeui_version}
BuildRequires:  libgnomeui-devel
BuildRequires:  libgsf-devel >= %{libgsf_version}
# grr, librsvg does not install api docs if --disable-gtk-doc
BuildRequires:  gtk-doc

# https://bugzilla.redhat.com/show_bug.cgi?id=578568
Patch0: no-xml-cleanup.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=539315
Patch1: librsvg-python-env.patch

%description
An SVG library based on cairo.


%package devel
Summary: 	Libraries and include files for developing with librsvg
Group: 		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	gtk2-devel >= %{gtk2_version}
Requires:	libxml2-devel >= %{libxml2_version}
Requires:	freetype-devel >= %{freetype_version}
Requires:       libgsf-devel >= %{libgsf_version}
Requires:       libcroco-devel >=  %{libcroco_version}
Requires:       pkgconfig

%description devel
This package provides the necessary development libraries and include
files to allow you to develop with librsvg.

%prep
%setup -q -n librsvg-%{version}
%patch0 -p1 -b .no-xml-cleanup
%patch1 -p1 -b .python-env

%build
%configure --with-svgz \
	--disable-gtk-doc \
	--enable-gtk-theme \
	--enable-gnome-vfs \
	--with-croco \

make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/*/engines/libsvg.a
rm -f $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/*/engines/libsvg.la
rm -f $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/*/loaders/svg_loader.a
rm -f $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/*/loaders/svg_loader.la
rm -f $RPM_BUILD_ROOT%{_libdir}/mozilla/plugins/libmozsvgdec.a
rm -f $RPM_BUILD_ROOT%{_libdir}/mozilla/plugins/libmozsvgdec.la
rm -f $RPM_BUILD_ROOT%{_libdir}/mozilla/plugins/libmozsvgdec.so
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/gtk-2.0/gdk-pixbuf.loaders
rm -f $RPM_BUILD_ROOT%{_datadir}/pixmaps/svg-viewer.svg

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%{_bindir}/update-gdk-pixbuf-loaders %{_host} || :

%postun
/sbin/ldconfig
%{_bindir}/update-gdk-pixbuf-loaders %{_host} || :

%files
%defattr(-, root, root)
%doc AUTHORS COPYING COPYING.LIB NEWS README
%{_libdir}/*.so.*
%{_libdir}/gtk-2.0/*/engines/libsvg.so
%{_libdir}/gtk-2.0/*/loaders/svg_loader.so
%{_bindir}/rsvg
%{_bindir}/rsvg-view
%{_bindir}/rsvg-convert
%{_mandir}/man1/*

%files devel
%defattr(-, root, root)
%{_libdir}/*.so
%{_includedir}/librsvg-2
%{_libdir}/pkgconfig/librsvg-2.0.pc
%doc %{_datadir}/gtk-doc/html/rsvg

%changelog
* Mon May 17 2010 Matthias Clasen <mclasen@redhat.com> - 2.16.0-5
- Use /usr/bin/python, not /usr/bin/env python
Resolves: #539315

* Thu Apr  1 2010 Matthias Clasen <mclasen@redhat.com> - 2.16.0-4
- Don't call xmlCleanupParser, it breaks other users of thread-private
  storage
  Resolves: #578568

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 2.26.0-3.1
- Rebuilt for RHEL 6

* Mon Aug 10 2009 Ville Skyttä <ville.skytta@iki.fi> - 2.26.0-3
- Convert specfile to UTF-8.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.26.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Mar 16 2009 Matthias Clasen <mclasen@redhat.com> - 2.26.0-1
- Update to 2.26.0

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.22.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Sep 22 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.3-1
- Update to 2.22.3

* Thu Sep 18 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.2-2
- Plug a memory leak

* Tue Mar  4 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.2-1
- Update to 2.22.2

* Sun Feb 24 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.1-1
- Update to 2.22.1

* Thu Feb 21 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.0-1
- Update to 2.22.0

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.20.0-2
- Autorebuild for GCC 4.3

* Sun Jan 20 2008 Matthias Clasen <mclasen@redhat.com> - 2.20.0-1
- Update to 2.20.0

* Tue Sep 11 2007 Matthias Clasen <mclasen@redhat.com> - 2.18.2-2
- Plug memory leaks

* Mon Sep  3 2007 Matthias Clasen <mclasen@redhat.com> - 2.18.2-1
- Update to 2.18.2

* Mon Sep  3 2007 Matthias Clasen <mclasen@redhat.com> - 2.18.1-1
- Update to 2.18.1

* Thu Aug 23 2007 Adam Jackson <ajax@redhat.com> - 2.18.0-4
- Rebuild for build ID

* Tue Aug  7 2007 Matthias Clasen <mclasen@redhat.com> - 2.18.0-3
- Update license field

* Wed Aug  1 2007 Matthias Clasen <mclasen@redhat.com> - 2.18.0-2
- Don't let scriptlets fail (#243185)

* Fri Jul 27 2007 Matthias Clasen <mclasen@redhat.com> - 2.18.0-1
- Update to 2.18.0

* Sat Nov  4 2006 Matthias Clasen <mclasen@redhat.com> - 2.16.1-1
- Update to 2.16.1

* Tue Sep  5 2006 Matthias Clasen <mclasen@redhat.com> - 2.16.0-2.fc6
- Fix multilib issues

* Thu Aug 31 2006 Matthias Clasen <mclasen@redhat.com> - 2.16.0-1.fc6
- Update to 2.16.0
- Require pkgconfig in the -devel package

* Thu Aug  3 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.90-1.fc6
- Update to 2.15.90

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.15.0-3.1
- rebuild

* Sun Jun 18 2006 Florian La Roche <laroche@redhat.com>
- change to separate Requires(post/postun) lines

* Mon Jun 12 2006 Bill Nottingham <notting@redhat.com> 2.15.0-2
- remove libtool, automake14 buildreqs

* Wed May 10 2006 Matthias Clasen <mclasen@redhat.com> 2.15.0-1
- Update to 2.15.0
- Don't ship static libs

* Fri May  5 2006 Matthias Clasen <mclasen@redhat.com> 2.14.3-3
- Rebuild against new GTK+
- Require GTK+ 2.9.0

* Tue Apr  4 2006 Matthias Clasen <mclasen@redhat.com> 2.14.3-2
- Update to 2.14.3

* Sun Mar 12 2006 Ray Strode <rstrode@redhat.com> 2.14.2-1
- Update to 2.14.2

* Sat Mar 11 2006 Bill Nottingham <notting@redhat.com> 2.14.1-2
- fix bad libart dep

* Tue Feb 28 2006 Matthias Clasen <mclasen@redhat.com> 2.14.1-1
- Update to 2.14.1

* Sat Feb 25 2006 Matthias Clasen <mclasen@redhat.com> 2.14.0-1
- Update to 2.14.0

* Mon Feb 11 2006 Matthias Clasen <mclasen@redhat.com> 2.13.93-1
- Update to 2.13.93

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.13.92-1.1
- bump again for double-long bug on ppc(64)

* Mon Feb  6 2006 Matthias Clasen <mclasen@redhat.com> 2.13.92-1
- Update to 2.13.92

* Fri Jan 13 2006 Matthias Clasen <mclasen@redhat.com> 2.13.5-1
- Update to 2.13.5

* Tue Jan  3 2006 Jesse Keating <jkeating@redhat.com> 2.13.3-4
- Rebuilt on new gcc

* Fri Dec  9 2005 Alexander Larsson <alexl@redhat.com> 2.13.3-3
- Update dependencies (now cairo only, not libart)

* Fri Dec  2 2005 Matthias Clasen <mclasen@redhat.com> - 2.13.3-2
- Compile with svgz support

* Wed Nov 30 2005 Matthias Clasen <mclasen@redhat.com> - 2.13.3-1
- Update to 2.13.3

* Wed Oct 12 2005 Matthias Clasen <mclasen@redhat.com> - 2.12.7-1
- Newer upstream version

* Thu Oct  6 2005 Matthias Clasen <mclasen@redhat.com> - 2.12.5-1
- New upstream version

* Thu Oct  6 2005 Matthias Clasen <mclasen@redhat.com> - 2.12.4-1
- New upstream version

* Thu Sep 29 2005 Matthias Clasen <mclasen@redhat.com> - 2.12.3-1
- New upstream version

* Wed Aug 31 2005 Matthias Clasen <mclasen@redhat.com> - 2.11.1-1
- New upstream version

* Wed Mar  2 2005 Matthias Clasen <mclasen@redhat.com> - 2.9.5-2
- Rebuild with gcc4

* Wed Jan 26 2005 Matthias Clasen <mclasen@redhat.com> - 2.9.5-1
- update to 2.9.5

* Thu Sep 23 2004 Matthias Clasen <mclasen@redhat.com> - 2.8.1-2
- Must use the same rpm macro for the host triplet as the
  gtk2 package, otherwise things can fall apart.  (#137676)

* Thu Sep 23 2004 Alexander Larsson <alexl@redhat.com> - 2.8.1-1
- update to 2.8.1

* Fri Jul 30 2004 Matthias Clasen <mclasen@redhat.com> - 2.7.2-1
- Update to 2.7.2
- Fix up changelog section

* Mon Jun 28 2004 Dan Williams <dcbw@redhat.com> - 2.6.4-7
- Fix usage of "%%{_bindir}/update-gdk-pixbuf-loaders %%{_host}" 
  to point to right place and architecture

* Thu Jun 24 2004 Matthias Clasen <mclasen@redhat.com> 2.6.4-6
- Properly handle updating of arch-dependent config 
  files.  (#124483)

* Wed Jun 23 2004 Matthias Clasen <mclasen@redhat.com> 2.6.4-5
- PreReq gtk2 instead of just requiring it  (#90697)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri May 21 2004 Matthias Clasen <mclasen@redhat.com> 2.6.4-3
- rebuild

* Mon Apr  5 2004 Warren Togami <wtogami@redhat.com> 2.6.4-2
- BuildRequires libtool, libgnomeui-devel, there may be more
- -devel req libcroco-devel

* Thu Apr  1 2004 Alex Larsson <alexl@redhat.com> 2.6.4-1
- update to 2.6.4

* Wed Mar 17 2004 Alex Larsson <alexl@redhat.com> 2.6.1-2
- rebuild to get new gtk bin age

* Mon Mar 15 2004 Alex Larsson <alexl@redhat.com> 2.6.1-1
- update to 2.6.1

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jan 27 2004 Jonathan Blandford <jrb@redhat.com> 2.4.0-3
- update version
- Buildrequire libcroco

* Fri Oct 24 2003 Alexander Larsson <alexl@redhat.com> 2.4.0-3
- Fix libcroco in link line. Fixes #107875.
- Properly require libgsf and libcroco

* Tue Oct 21 2003 Florian La Roche <Florian.LaRoche@redhat.de> 2.4.0-2
- BuildReq libcroco-devel, seems this _can_ get picked up

* Mon Sep  8 2003 Jonathan Blandford <jrb@redhat.com> 2.4.0-1
- bump to 2.4.0

* Thu Sep  4 2003 Alexander Larsson <alexl@redhat.com> 2.3.1-3
- Don't use the epoch, thats implicitly zero and not defined

* Thu Sep  4 2003 Alexander Larsson <alexl@redhat.com> 2.3.1-2
- full version in -devel requires (#102063)

* Wed Aug 13 2003 Jonathan Blandford <jrb@redhat.com> 2.3.1-1
- new version for GNOME 2.4

* Fri Aug  8 2003 Alexander Larsson <alexl@redhat.com> 2.2.3-5
- BuildRequire libgsf-devel

* Wed Aug  6 2003 Elliot Lee <sopwith@redhat.com> 2.2.3-4
- Fix libtool

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Apr  8 2003 Matt Wilson <msw@redhat.com> 2.2.3-2
- use system libtool (#88339)

* Wed Feb  5 2003 Alexander Larsson <alexl@redhat.com> 2.2.3-1
- 2.2.3
- Moved engine and loaders from devel package

* Mon Feb  3 2003 Alexander Larsson <alexl@redhat.com> 2.2.2.1-2
- Move docs to rpm docdir

* Mon Feb  3 2003 Alexander Larsson <alexl@redhat.com> 2.2.2.1-1
- Update to 2.2.2.1, crash fixes

* Fri Jan 31 2003 Alexander Larsson <alexl@redhat.com> 2.2.1-1
- Update to 2.2.1, fixes crash
- Removed temporary manpage hack

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Jan 21 2003 Alexander Larsson <alexl@redhat.com> 2.2.0-3
- Manpage were installed in the wrong place

* Tue Jan 21 2003 Alexander Larsson <alexl@redhat.com> 2.2.0-2
- Add manpage

* Tue Jan 21 2003 Alexander Larsson <alexl@redhat.com> 2.2.0-1
- Update to 2.2.0

* Fri Jan 17 2003 Alexander Larsson <alexl@redhat.com> 2.1.3-3
- Require gtk2 2.2.0 for the pixbuf loader (#80857)

* Thu Jan 16 2003 Alexander Larsson <alexl@redhat.com> 2.1.3-2
- own includedir/librsvg-2

* Thu Jan  9 2003 Alexander Larsson <alexl@redhat.com> 2.1.3-1
- update to 2.1.3

* Tue Dec 17 2002 Owen Taylor <otaylor@redhat.com>
- Don't package gdk-pixbuf.loaders, it gets generated 
  in the %%post

* Mon Dec  9 2002 Alexander Larsson <alexl@redhat.com> 2.1.2-1
- Update to 2.1.2

* Sat Jul 27 2002 Havoc Pennington <hp@redhat.com>
- 2.0.1

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue May 21 2002 Havoc Pennington <hp@redhat.com>
- rebuild in different environment

* Thu May 02 2002 Havoc Pennington <hp@redhat.com>
- rebuild in different environment

* Thu Apr 18 2002 Havoc Pennington <hp@redhat.com>
- 1.1.6

* Mon Feb 11 2002 Alex Larsson <alexl@redhat.com> 1.1.3-1
- Update to 1.1.3

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jan  2 2002 Havoc Pennington <hp@redhat.com>
- new CVS snap 1.1.0.91
- remove automake/autoconf calls

* Mon Nov 26 2001 Havoc Pennington <hp@redhat.com>
- convert to librsvg2 RPM

* Tue Oct 23 2001 Havoc Pennington <hp@redhat.com>
- 1.0.2

* Fri Jul 27 2001 Alexander Larsson <alexl@redhat.com>
- Add a patch that moves the includes to librsvg-1/librsvg
- in preparation for a later librsvg 2 library.

* Tue Jul 24 2001 Havoc Pennington <hp@redhat.com>
- build requires gnome-libs-devel, #49509

* Thu Jul 19 2001 Havoc Pennington <hp@redhat.com>
- own /usr/include/librsvg

* Wed Jul 18 2001 Akira TAGOH <tagoh@redhat.com> 1.0.0-4
- fixed the linefeed problem in multibyte environment. (Bug#49310)

* Mon Jul 09 2001 Havoc Pennington <hp@redhat.com>
- put .la file back in package 

* Fri Jul  6 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Put changelog at the end
- Move .so files to devel subpackage
- Don't mess with ld.so.conf
- Don't use %%{prefix}, this isn't a relocatable package
- Don't define a bad docdir
- Add BuildRequires
- Use %%{_tmppath}
- Don't define name, version etc. on top of the file (why 
  do so many do that?)
- s/Copyright/License/

* Wed May  9 2001 Jonathan Blandford <jrb@redhat.com>
- Put into Red Hat Build system

* Tue Oct 10 2000 Robin Slomkowski <rslomkow@eazel.com>
- removed obsoletes from sub packages and added mozilla and 
  trilobite subpackages

* Wed Apr 26 2000 Ramiro Estrugo <ramiro@eazel.com>
- created this thing

