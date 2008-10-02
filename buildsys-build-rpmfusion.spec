%define repo rpmfusion

Name:           buildsys-build-%{repo}
Epoch:          9
Version:        9.1
Release:        14
Summary:        Tools and files used by the %{repo} buildsys 

Group:          Development/Tools
License:        MIT
URL:            http://rpmfusion.org
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source2:        %{name}-list-kernels.sh
Source5:        %{name}-README
Source11:       %{name}-kerneldevpkgs-current
Source12:       %{name}-kerneldevpkgs-newest
Source20:       %{name}-filterfile_i586
Source21:       %{name}-filterfile_i686
Source22:       %{name}-filterfile_x86_64
Source23:       %{name}-filterfile_ppc
Source24:       %{name}-filterfile_ppc64

# provide this to avoid a error when generating akmods packages
Provides:       buildsys-build-rpmfusion-kerneldevpkgs-akmod-%{_target_cpu}

# rpmlint will complain this should be a noarch package; but for
#  proper builddeps deps it needs to be a non-noarch package
ExclusiveArch:  i586 i686 x86_64 ppc ppc64

# unneeded
%define debug_package %{nil}

%description
This package contains tools and lists of recent kernels that get used when
building kmod-packages.

%package        kerneldevpkgs-newest
Summary:        Meta-package to get newly released kernel-devel packages into the buildroot
Group:          Development/Tools
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      buildsys-build-newest-kernels-livna < 17
Provides:       %{name}-kerneldevpkgs-newest-%{_target_cpu} = %{?epoch:%{epoch}:}%{version}-%{release}

Requires:       %{_bindir}/kmodtool
BuildRequires:  %{_bindir}/kmodtool

# we use our own magic here to safe ourself to cut'n'paste the BR
%{expand:%(bash %{SOURCE2} --newest --requires --prefix %{_sourcedir}/%{name}- 2>/dev/null)}

%description kerneldevpkgs-newest
This is a meta-package used by the buildsystem to track the kernel-devel
packages for newly released kernels into the buildroot to build
kmods against them.

%files kerneldevpkgs-newest
%defattr(-,root,root,-)
%doc .tmp/newest/README


%package        kerneldevpkgs-current
Summary:        Meta-package to get all current kernel-devel packages into the buildroot
Group:          Development/Tools
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       %{name}-kerneldevpkgs-%{_target_cpu} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       %{name}-kerneldevpkgs-current-%{_target_cpu} = %{?epoch:%{epoch}:}%{version}-%{release}

Requires:       %{_bindir}/kmodtool
BuildRequires:  %{_bindir}/kmodtool

# we use our own magic here to safe ourself to cut'n'paste the BR
%{expand:%(bash %{SOURCE2} --current --requires --prefix %{_sourcedir}/%{name}- 2>/dev/null)}

%description kerneldevpkgs-current
This is a meta-package used by the buildsystem to track the kernel-devel
packages for all current up-to-date kernels into the buildroot to build
kmods against them.

%files kerneldevpkgs-current
%defattr(-,root,root,-)
%doc .tmp/current/README

%prep
# for debugging purposes output the stuff we use during the rpm generation
bash %{SOURCE2} --newest --requires --prefix %{_sourcedir}/%{name}-
sleep 2
bash %{SOURCE2} --current --requires --prefix %{_sourcedir}/%{name}-
sleep 2


%build
echo nothing to build


%install
rm -rf $RPM_BUILD_ROOT .tmp/
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/%{name} $RPM_BUILD_ROOT/%{_bindir} .tmp/newest .tmp/current

# install the stuff we need
install -p -m 0755 %{SOURCE2}  $RPM_BUILD_ROOT/%{_bindir}/%{name}-kerneldevpkgs
install -p -m 0644 %{SOURCE5}  .tmp/newest/README
install -p -m 0644 %{SOURCE5}  .tmp/current/README
install -p -m 0644 %{SOURCE11} $RPM_BUILD_ROOT/%{_datadir}/%{name}/kerneldevpkgs-current
install -p -m 0644 %{SOURCE12} $RPM_BUILD_ROOT/%{_datadir}/%{name}/kerneldevpkgs-newest
install -p -m 0644 %{SOURCE20} $RPM_BUILD_ROOT/%{_datadir}/%{name}/filterfile_i586
install -p -m 0644 %{SOURCE21} $RPM_BUILD_ROOT/%{_datadir}/%{name}/filterfile_i686
install -p -m 0644 %{SOURCE22} $RPM_BUILD_ROOT/%{_datadir}/%{name}/filterfile_x86_64
install -p -m 0644 %{SOURCE23} $RPM_BUILD_ROOT/%{_datadir}/%{name}/filterfile_ppc
install -p -m 0644 %{SOURCE24} $RPM_BUILD_ROOT/%{_datadir}/%{name}/filterfile_ppc64


# adjust default-path
sed -i 's|^default_prefix=.*|default_prefix=%{_datadir}/%{name}/|'  \
 $RPM_BUILD_ROOT/%{_bindir}/%{name}-kerneldevpkgs


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_datadir}/%{name}/



%changelog
* Thu Oct 02 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 9.1-14
- install filterfile for ppc64

* Thu Oct 02 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 9.1-13
- Rebuild for RPM Fusion

* Sun Sep 21 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 9.1-12
- Update to latest kernels 2.6.26.5-45.fc9 2.6.25.3-2.fc9xen

* Sun Sep 21 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 9.1-11
- Update to latest kernels 2.6.26.3-29.fc9 2.6.25.3-2.fc9xen

* Sat Aug 24 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 9.1-10
- Update to latest kernels 2.6.25.14-108.fc9 2.6.25.3-2.fc9xen

* Thu Jul 24 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 9.1-9
- Update to latest kernels 2.6.25.11-97.fc9 2.6.25.3-2.fc9xen

* Thu Jul 17 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 9.1-8.1
- fix kernel list

* Tue Jul 15 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 9.1-8
- Update to latest kernels 2.6.25.10-86.fc9 2.6.25.3-2.fc9xen

* Wed Jul 02 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 9.1-7
- Update to latest kernels 2.6.25.9-76.fc9 2.6.25.3-2.fc9xen

* Fri Jun 13 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 9.1-1-6
- Update to latest kernels 2.6.25.6-55.fc9 2.6.25.3-1.fc9xen

* Fri Jun 06 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 9:9.1-5
- Update to latest kernels 2.6.25.4-30.fc9 2.6.25.3-1.fc9xen

* Thu May 15 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 9:9.1-4
- Update to latest kernels 2.6-2.6.25.3-1.fc9xen 2.6.25.3-18.fc9

* Sun May 04 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 9:9.0-3
- adjust output for new kernel scheme

* Sun May 04 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 9:9.0-2
- add epoch to provides/requires

* Sun May 04 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 9:9.0-1
- Build for F9 kernel

* Mon Mar 31 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 2-2
- Update to latest kernels 2.6.24.4-64.fc8 2.6.21.7-3.fc8xen

* Sat Jan 26 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 9:1-2
- s/akmods/akmod/

* Wed Jan 09 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 9:1-3
- Build for rawhide
- disable kerneldevpkgs-newest and kerneldevpkgs-current packages, as we
  don't maintain them for rawhide
- add epoch for new versioning scheme

* Thu Dec 20 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 22-1
- Update to latest kernels 2.6.21-2952.fc8xen 2.6.23.9-85.fc8

* Thu Dec 20 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 22-1
- Update to latest kernels 2.6.21-2952.fc8xen 2.6.23.9-85.fc8

* Mon Dec 03 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 21-1
- Update to latest kernels 2.6.23.8-63.fc8 2.6.21-2952.fc8xen

* Sat Nov 10 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 20-1
- Update to latest kernels 2.6.23.1-49.fc8 2.6.21-2950.fc8xen

* Tue Oct 29 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 19-1
- Update to latest kernels 2.6.23.1-41.fc8 2.6.21-2950.fc8xen

* Tue Oct 28 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 18-1
- Update to latest kernels 2.6.23.1-41.fc8 2.6.21-2950.fc8xen

* Sun Oct 28 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 17-3
- don't include file with know variants and instead properly fix the script

* Sun Oct 28 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 17-2
- include file with know variants as it is needed in buildsys

* Sun Oct 28 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 17-1
- split buildsys stuff out into a seperate package
- rename to buildsys-build-rpmfusion
- add proper obsoletes
- give subpackages and files more sane names and places

* Sat Oct 27 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 16-2
- Update to latest kernels 2.6.23.1-35.fc8 2.6.21-2950.fc8xen

* Sat Oct 27 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 16-1
- Update to latest kernels 2.6.23.1-35.fc8 2.6.21-2949.fc8xen

* Thu Oct 18 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 15-1
- rebuilt for latest kernels

* Thu Oct 18 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 14-1
- rebuilt for latest kernels

* Thu Oct 18 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 13-1
- rebuilt for latest kernels

* Thu Oct 18 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 12-1
- rebuilt for latest kernels

* Fri Oct 12 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 11-1
- rebuilt for latest kernels

* Thu Oct 11 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 10-1
- rebuilt for latest kernels

* Wed Oct 10 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 9-2
- fix typo

* Wed Oct 10 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 9-1
- rebuilt for latest kernels

* Sun Oct 07 2007 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 8-1
- update for 2.6.23-0.224.rc9.git6.fc8

* Sun Oct 07 2007 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 7-1
- update for 2.6.23-0.222.rc9.git1.fc8

* Wed Oct 03 2007 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 6-1
- update for 2.6.23-0.217.rc9.git1.fc8 and 2.6.21-2947.fc8xen

* Wed Oct 03 2007 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 5-1
- disable --all-but-latest stuff -- does not work as expected
- rename up2date list of kernels from "latest" to "current" as latest 
  and newest are to similar in wording; asjust script as well
- kmodtool: don't provide kernel-modules, not needed anymore with
  the new stayle and hurts

* Sun Sep 09 2007 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 4-2
- fix typos in spec file and list-kernels script
- interdependencies between the two buildsys-build packages needs to be
  arch specific as well

* Sun Sep 09 2007 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 4-1
- s/latests/latest/
- update kernel lists for rawhide and test2 kernels
- make kmod-helpers-livna-list-kernels print BuildRequires for all kernels
  as well; this is not needed and will slow build a bit as it will track 
  all the kernel-devel packages in, but that way we make sure they are really
  available in the buildsys

* Fri Sep 07 2007 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 3-4
- implement proper arch deps 

* Fri Sep 07 2007 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 3-3
- proper list of todays rawhide-kernels

* Fri Sep 07 2007 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 3-2
- fix typo in kmod-helpers-livna-latests-kernels

* Fri Sep 07 2007 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 3-1
- adjust for devel

* Sat Sep 01 2007 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2-1
- initial package
