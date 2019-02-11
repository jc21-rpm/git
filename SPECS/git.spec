# Pass --without docs to rpmbuild if you don't want the documentation

Name:       git
Version:    2.20.1
Release:    1
Summary:    Core git tools
License:    GPL
Group:      Development/Tools
URL:        http://kernel.org/pub/software/scm/git/
BuildRequires:  zlib-devel >= 1.2, openssl-devel, curl-devel, expat-devel, gettext  %{!?_without_docs:, xmlto, asciidoc > 6.0.3}
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:   perl-Git = %{version}-%{release}
Requires:   zlib >= 1.2, rsync, less, openssh-clients, expat
Provides:   git-core = %{version}-%{release}
Obsoletes:  git-core <= 1.5.4.2
Obsoletes:  git-p4

%global debug_package %{nil}

%description
Git is a fast, scalable, distributed revision control system with an
unusually rich command set that provides both high-level operations
and full access to internals.

The git rpm installs the core tools with minimal dependencies.  To
install all git packages, including tools for integrating with other
SCMs, install the git-all meta-package.

%package all
Summary:    Meta-package to pull in all git tools
Group:      Development/Tools
Requires:   git = %{version}-%{release}
Requires:   git-svn = %{version}-%{release}
Requires:   git-cvs = %{version}-%{release}
Requires:   git-arch = %{version}-%{release}
Requires:   git-email = %{version}-%{release}
Requires:   gitk = %{version}-%{release}
Requires:   gitweb = %{version}-%{release}
Requires:   git-gui = %{version}-%{release}
Obsoletes:  git <= 1.5.4.2

%description all
Git is a fast, scalable, distributed revision control system with an
unusually rich command set that provides both high-level operations
and full access to internals.

This is a dummy package which brings in all subpackages.

%package svn
Summary:        Git tools for importing Subversion repositories
Group:          Development/Tools
Requires:       git = %{version}-%{release}, subversion
%description svn
Git tools for importing Subversion repositories.

%package cvs
Summary:        Git tools for importing CVS repositories
Group:          Development/Tools
Requires:       git = %{version}-%{release}, cvs, cvsps
%description cvs
Git tools for importing CVS repositories.

%package arch
Summary:        Git tools for importing Arch repositories
Group:          Development/Tools
Requires:       git = %{version}-%{release}, tla
%description arch
Git tools for importing Arch repositories.

%package email
Summary:        Git tools for sending email
Group:          Development/Tools
Requires:   git = %{version}-%{release}
%description email
Git tools for sending email.

%package gui
Summary:        Git GUI tool
Group:          Development/Tools
Requires:       git = %{version}-%{release}, tk >= 8.4
%description gui
Git GUI tool

%package -n gitk
Summary:        Git revision tree visualiser ('gitk')
Group:          Development/Tools
Requires:       git = %{version}-%{release}, tk >= 8.4
%description -n gitk
Git revision tree visualiser ('gitk')

%package -n gitweb
Summary:    Git web interface
Group:          Development/Tools
Requires:       git = %{version}-%{release}
%description -n gitweb
Browsing git repository on the web

%package -n perl-Git
Summary:        Perl interface to Git
Group:          Development/Libraries
Requires:       git = %{version}-%{release}
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildRequires:  perl(Error)
BuildRequires:  perl(ExtUtils::MakeMaker)

%description -n perl-Git
Perl interface to Git

%define path_settings ETC_GITCONFIG=/etc/gitconfig prefix=%{_prefix} mandir=%{_mandir} htmldir=%{_docdir}/%{name}-%{version}
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%prep
wget https://github.com/git/git/archive/v%{version}.tar.gz
tar xzf v%{version}.tar.gz

%build
cd %{name}-%{version}
make %{_smp_mflags} CFLAGS="$RPM_OPT_FLAGS" \
     %{path_settings} \
     all %{!?_without_docs: doc}

%install
rm -rf $RPM_BUILD_ROOT
cd %{name}-%{version}
make %{_smp_mflags} CFLAGS="$RPM_OPT_FLAGS" DESTDIR=$RPM_BUILD_ROOT \
     %{path_settings} \
     INSTALLDIRS=vendor install %{!?_without_docs: install-doc}
test ! -d $RPM_BUILD_ROOT%{python_sitelib} || rm -fr $RPM_BUILD_ROOT%{python_sitelib}
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name '*.bs' -empty -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name perllocal.pod -exec rm -f {} ';'

(find $RPM_BUILD_ROOT%{_bindir} -type f | grep -vE "archimport|svn|cvs|email|gitk|git-gui|git-citool" | sed -e s@^$RPM_BUILD_ROOT@@)               > bin-man-doc-files
(find $RPM_BUILD_ROOT%{_libexecdir}/git-core -type f | grep -vE "archimport|svn|cvs|email|gitk|git-gui|git-citool" | sed -e s@^$RPM_BUILD_ROOT@@)               >> bin-man-doc-files
(find $RPM_BUILD_ROOT%{perl_vendorlib} -type f | sed -e s@^$RPM_BUILD_ROOT@@) >> perl-files
%if %{!?_without_docs:1}0
(find $RPM_BUILD_ROOT%{_mandir} $RPM_BUILD_ROOT/Documentation -type f | grep -vE "archimport|svn|git-cvs|email|gitk|git-gui|git-citool" | sed -e s@^$RPM_BUILD_ROOT@@ -e 's/$/*/' ) >> bin-man-doc-files
%else
rm -rf $RPM_BUILD_ROOT%{_mandir}
%endif
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/bash_completion.d
install -m 644 -T contrib/completion/git-completion.bash $RPM_BUILD_ROOT%{_sysconfdir}/bash_completion.d/git

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}-%{version}/bin-man-doc-files
%defattr(-,root,root)
%{_datadir}/git-core/
%doc %{name}-%{version}/COPYING %{name}-%{version}/Documentation/*.txt
%{!?_without_docs: %doc %{name}-%{version}/Documentation/*.html %{name}-%{version}/Documentation/howto}
%{!?_without_docs: %doc %{name}-%{version}/Documentation/technical}
%{_sysconfdir}/bash_completion.d

%files svn
%defattr(-,root,root)
%{_libexecdir}/git-core/*svn*
%doc %{name}-%{version}/Documentation/*svn*.txt
%{!?_without_docs: %{_mandir}/man1/*svn*.1*}
%{!?_without_docs: %doc %{name}-%{version}/Documentation/*svn*.html }

%files cvs
%defattr(-,root,root)
%doc %{name}-%{version}/Documentation/*git-cvs*.txt
%{_bindir}/git-cvsserver
%{_libexecdir}/git-core/*cvs*
%{!?_without_docs: %{_mandir}/man1/*cvs*.1*}
%{!?_without_docs: %doc %{name}-%{version}/Documentation/*git-cvs*.html }

%files arch
%defattr(-,root,root)
%doc %{name}-%{version}/Documentation/git-archimport.txt
%{_libexecdir}/git-core/git-archimport
%{!?_without_docs: %{_mandir}/man1/git-archimport.1*}
%{!?_without_docs: %doc %{name}-%{version}/Documentation/git-archimport.html }

%files email
%defattr(-,root,root)
%doc %{name}-%{version}/Documentation/*email*.txt
%{_libexecdir}/git-core/*email*
%{!?_without_docs: %{_mandir}/man1/*email*.1*}
%{!?_without_docs: %doc %{name}-%{version}/Documentation/*email*.html }

%files gui
%defattr(-,root,root)
%{_libexecdir}/git-core/git-gui
%{_libexecdir}/git-core/git-citool
%{_libexecdir}/git-core/git-gui--askpass
%{_datadir}/git-gui/
%{!?_without_docs: %{_mandir}/man1/git-gui.1*}
%{!?_without_docs: %doc %{name}-%{version}/Documentation/git-gui.html}
%{!?_without_docs: %{_mandir}/man1/git-citool.1*}
%{!?_without_docs: %doc %{name}-%{version}/Documentation/git-citool.html}

%files -n gitk
%defattr(-,root,root)
%doc %{name}-%{version}/Documentation/*gitk*.txt
%{_bindir}/*gitk*
%{_datadir}/gitk/
%{!?_without_docs: %{_mandir}/man1/*gitk*.1*}
%{!?_without_docs: %doc %{name}-%{version}/Documentation/*gitk*.html }

%files -n gitweb
%defattr(-,root,root)
%doc %{name}-%{version}/gitweb/README %{name}-%{version}/gitweb/INSTALL %{name}-%{version}/Documentation/*gitweb*.txt
%{_datadir}/gitweb
%{!?_without_docs: %{_mandir}/man1/*gitweb*.1*}
%{!?_without_docs: %{_mandir}/man5/*gitweb*.5*}
%{!?_without_docs: %doc %{name}-%{version}/Documentation/*gitweb*.html }

%files -n perl-Git -f %{name}-%{version}/perl-files
%defattr(-,root,root)
%{_datadir}/perl5/

%files all
# No files for you!

%changelog
* Tue Feb 12 2019 Jamie Curnow <jc@jc21.com> - 2.20.1-1
- Updated to v2.20.1

* Wed Nov 14 2018 Jamie Curnow <jc@jc21.com> - 2.19.1-1
- Updated to v2.19.1

* Fri Sep 21 2018 Jamie Curnow <jc@jc21.com> - 2.19.0-1
- Updated to v2.19.0

* Fri Jul 20 2018 Jamie Curnow <jc@jc21.com> - 2.18.0-1
- Updated to v2.18.0

* Mon Apr 16 2018 Jamie Curnow <jc@jc21.com> - 2.17.0-1
- Updated to v2.17.0

* Mon Dec 22 2014 Jamie Curnow <jc@jc21.com> - 2.2.1-1
- Updated to v2.2.1

* Sat Oct 26 2013 Jukka Ojaniemi <jukka.ojaniemi@gmail.com> - 1.8.4.1-1
- Initial RPM release

