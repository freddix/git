%include	/usr/lib/rpm/macros.perl

Summary:	Distributed version control system
Name:		git
Version:	1.8.5
Release:	1
License:	GPL v2
Group:		Development/Tools
Source0:	http://git-core.googlecode.com/files/%{name}-%{version}.tar.gz
# Source0-md5:	16448b1cfd62fcbe738729edc6279e14
URL:		http://git-scm.com/
BuildRequires:	asciidoc
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	curl-devel
BuildRequires:	docbook-dtd45-xml
BuildRequires:	expat-devel
BuildRequires:	openssl-devel
BuildRequires:	perl-base
BuildRequires:	python
BuildRequires:	rpm-perlprov
BuildRequires:	xmlto
BuildRequires:	zlib-devel
Requires:	coreutils
Requires:	curl
Requires:	diffutils
Requires:	findutils
Requires:	grep
Requires:	sed
Suggests:	openssh-clients
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Git is a free & open source, distributed version control system
designed to handle everything from small to very large projects
with speed and efficiency.

%package devel
Summary:	Header files for git
Group:		Development/Libraries

%description devel
Header files for git.

%package doc
Summary:	Documentation for git
Group:		Documentation

%description doc
Documentation for git.

%package gitk
Summary:	Tcl/Tk interface to the Git version control system
Group:		Development/Tools
Requires:	%{name} = %{version}-%{release}
Requires:	tk

%description gitk
gitk displays changes in a repository or a selected set of commits.
This includes visualizing the commit graph, showing information
related to each commit, and the files in the trees of each revision.

%package gitview
Summary:	A GTK+ based repository browser for git
Group:		Development/Tools
Requires:	%{name} = %{version}-%{release}
Requires:	python-pygtk-gtk
Requires:	python-pygtksourceview

%description gitview
A GTK+ based repository browser for git.

%package gui
Summary:	Tcl/Tk interface to the Git version control system
Group:		Development/Tools
Requires:	%{name} = %{version}-%{release}
Requires:	tk
Requires:	xdg-utils
Suggests:	meld

%description gui
Displays changes in a repository or a selected set of commits. This
includes visualizing the commit graph, showing information related to
each commit, and the files in the trees of each revision.

%package svn
Summary:	Subversion support for Git
Group:		Development/Tools
Requires:	%{name} = %{version}-%{release}

%description svn
Subversion support for Git.

%package cvs
Summary:	CVS support for Git
Group:		Development/Tools
Requires:	%{name} = %{version}-%{release}
Requires:	cvsps
Requires:	rcs

%description cvs
CVS support for Git.

%package email
Summary:	Git tools for sending email
Group:		Development/Tools
Requires:	%{name} = %{version}-%{release}

%description email
Git tools for sending email.

%package -n perl-Git
Summary:	Perl interface to the Git version control system
Group:		Development/Languages/Perl

%description -n perl-Git
This module provides Perl scripts easy way to interface the Git
version control system. The modules have an easy and well-tested way
to call arbitrary Git commands; in the future, the interface will also
provide specialized methods for doing easily operations which are not
totally trivial to do over the generic command interface.

%package -n python-Git
Summary:	Python interface to the Git version control system
Group:		Development/Languages/Python

%description -n python-Git
This module provides Python scripts easy way to interface the Git
version control system.

%prep
%setup -q

%build
%{__aclocal}
%{__autoconf}
%configure \
	--with-openssl

%{__make} INSTALLDIRS=vendor V=1
%{__make} -C Documentation man V=1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_includedir}/%{name}/xdiff

%{__make} install \
	INSTALLDIRS=vendor \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} -C Documentation install \
	DESTDIR=$RPM_BUILD_ROOT

# header files and lib
cp -a *.h $RPM_BUILD_ROOT%{_includedir}/%{name}
cp -a compat $RPM_BUILD_ROOT%{_includedir}/%{name}
cp -a xdiff/*.h $RPM_BUILD_ROOT%{_includedir}/%{name}/xdiff
cp -a libgit.a $RPM_BUILD_ROOT%{_libdir}
cp -a xdiff/lib.a $RPM_BUILD_ROOT%{_libdir}/libgit_xdiff.a

rm -f $RPM_BUILD_ROOT%{perl_archlib}/perllocal.pod
rm -f $RPM_BUILD_ROOT%{perl_vendorarch}/auto/Git/.packlist

# gitview
install -p contrib/gitview/gitview $RPM_BUILD_ROOT%{_bindir}

%py_postclean

mv $RPM_BUILD_ROOT%{_localedir}/pt{_PT,}
%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README contrib
%attr(755,root,root) %{_bindir}/git
%attr(755,root,root) %{_bindir}/git-receive-pack
%attr(755,root,root) %{_bindir}/git-shell
%attr(755,root,root) %{_bindir}/git-upload-archive
%attr(755,root,root) %{_bindir}/git-upload-pack

%{_mandir}/man1/git-*.1*
%{_mandir}/man1/git.1*
%{_mandir}/man5/gitattributes.5*
%{_mandir}/man5/githooks.5*
%{_mandir}/man5/gitignore.5*
%{_mandir}/man5/gitmodules.5*
%{_mandir}/man5/gitrepository-layout.5*
%{_mandir}/man7/gitcli.7*
%{_mandir}/man7/gitcore-tutorial.7*
%{_mandir}/man7/gitdiffcore.7*
%{_mandir}/man7/gitglossary.7*
%{_mandir}/man7/gitrevisions.7*
%{_mandir}/man7/gittutorial-2.7*
%{_mandir}/man7/gittutorial.7*
%{_mandir}/man7/gitworkflows.7*
%exclude %{_mandir}/man1/git-cvs*.1*
%exclude %{_mandir}/man1/git-svn.1*

%dir %{_libdir}/git-core
%attr(755,root,root) %{_libdir}/git-core/git-*
%attr(755,root,root) %{_libdir}/git-core/git
%attr(755,root,root) %{_libdir}/git-core/mergetools

%exclude %{_libdir}/git-core/git-gui
%exclude %{_libdir}/git-core/git-svn
%exclude %{_libdir}/git-core/git-archimport
%exclude %{_libdir}/git-core/git-cvs*
%exclude %{_libdir}/git-core/*email*

%{_datadir}/git-core

%files doc
%defattr(644,root,root,755)
%doc Documentation/RelNotes*
%doc Documentation/howto Documentation/technical

%files devel
%defattr(644,root,root,755)
%{_includedir}/git
%{_libdir}/libgit.a
%{_libdir}/libgit_xdiff.a

%files gitk
%defattr(644,root,root,755)
%{_mandir}/man1/gitk.1*
%attr(755,root,root) %{_bindir}/gitk
%dir %{_datadir}/gitk
%dir %{_datadir}/gitk/lib
%dir %{_datadir}/gitk/lib/msgs
%lang(de) %{_datadir}/gitk/lib/msgs/de.msg
%lang(es) %{_datadir}/gitk/lib/msgs/es.msg
%lang(fr) %{_datadir}/gitk/lib/msgs/fr.msg
%lang(hu) %{_datadir}/gitk/lib/msgs/hu.msg
%lang(it) %{_datadir}/gitk/lib/msgs/it.msg
%lang(ja) %{_datadir}/gitk/lib/msgs/ja.msg
%lang(pt_BR) %{_datadir}/gitk/lib/msgs/pt_br.msg
%lang(ru) %{_datadir}/gitk/lib/msgs/ru.msg
%lang(sv) %{_datadir}/gitk/lib/msgs/sv.msg

%files gitview
%defattr(644,root,root,755)
%doc contrib/gitview/gitview.txt
%attr(755,root,root) %{_bindir}/gitview

%files gui
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/git-core/git-gui
%dir %{_datadir}/git-gui
%dir %{_datadir}/git-gui/lib
%dir %{_datadir}/git-gui/lib/msgs
%{_datadir}/git-gui/lib/*.js
%{_datadir}/git-gui/lib/*.tcl
%{_datadir}/git-gui/lib/git-gui.ico
%{_datadir}/git-gui/lib/tclIndex
%lang(de) %{_datadir}/git-gui/lib/msgs/de.msg
%lang(el) %{_datadir}/git-gui/lib/msgs/el.msg
%lang(fr) %{_datadir}/git-gui/lib/msgs/fr.msg
%lang(hu) %{_datadir}/git-gui/lib/msgs/hu.msg
%lang(it) %{_datadir}/git-gui/lib/msgs/it.msg
%lang(ja) %{_datadir}/git-gui/lib/msgs/ja.msg
%lang(nb) %{_datadir}/git-gui/lib/msgs/nb.msg
%lang(ru) %{_datadir}/git-gui/lib/msgs/ru.msg
%lang(sv) %{_datadir}/git-gui/lib/msgs/sv.msg
%lang(zh_CN) %{_datadir}/git-gui/lib/msgs/zh_cn.msg

%files svn
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/git-core/git-svn
%{_mandir}/man1/git-svn.1*

%files cvs
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/git-cvsserver
%attr(755,root,root) %{_libdir}/git-core/git-cvs*
%{_mandir}/man1/git-cvs*.1*
%{_mandir}/man7/gitcvs-migration.7*

%files email
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/git-core/*email*
%{_mandir}/man1/*email*.1*

%files -n perl-Git
%defattr(644,root,root,755)
%{perl_vendorlib}/Git.pm
%dir %{perl_vendorlib}/Git
%{perl_vendorlib}/Git/I18N.pm
%{perl_vendorlib}/Git/IndexInfo.pm

%{_mandir}/man3/Git.3pm*

%files -n python-Git
%defattr(644,root,root,755)
%dir %{py_sitescriptdir}/git_remote_helpers
%dir %{py_sitescriptdir}/git_remote_helpers/git
%{py_sitescriptdir}/git_remote_helpers/*.py[co]
%{py_sitescriptdir}/git_remote_helpers/git/*.py[co]

