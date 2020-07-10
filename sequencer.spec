%define _prefix /gem_base/epics/support
%define name sequencer
%define version 3.15.8
%define release 2.2.8
%define repository gemdev
%define debug_package %{nil}
%define arch %(uname -m)
%define checkout %(git log --pretty=format:'%h' -n 1) 


Summary: %{name} Package, a module for EPICS base
Name: %{name}
Version: %{version}
Release: %release.%(date +"%Y%m%d")git%{checkout}%{?dist}
License: EPICS Open License
Group: Applications/Engineering
Source0: %{name}-%{version}.tar.gz
ExclusiveArch: %{arch}
Prefix: %{_prefix}
## You may specify dependencies here
#BuildRequires: epics-base-devel
#Requires: epics-base
## Switch dependency checking off
# AutoReqProv: no

%description
This is the module %{name}.

## If you want to have a devel-package to be generated uncomment the following:
%package devel
Summary: %{name}-devel Package
Group: Development/Gemini
Requires: %{name}
%description devel
This is the module %{name}.

%prep
%setup -q 

%build
make distclean uninstall
make

%install
export DONT_STRIP=1
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_prefix}/%{gemopt}/epics/modules/seq
cp -r %{_builddir}/dbd $RPM_BUILD_ROOT/%{_prefix}/%{name}/epics/modules/seq
cp -r %{_builddir}/bin $RPM_BUILD_ROOT/%{_prefix}/%{name}/epics/modules/seq
cp -r %{_builddir}/lib $RPM_BUILD_ROOT/%{_prefix}/%{name}/epics/modules/seq
cp -r %{_builddir}/include $RPM_BUILD_ROOT/%{_prefix}/%{name}/epics/modules/seq
cp -r %{_builddir}/configure $RPM_BUILD_ROOT/%{_prefix}/%{name}/epics/modules/seq/
find $RPM_BUILD_ROOT/%{_prefix}/%{name}/configure -name ".git" -exec rm -rf {} \;


%postun
if [ "$1" = "0" ]; then
	rm -rf %{_prefix}/%{name}
fi


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
   /%{_prefix}/%{name}/bin
   /%{_prefix}/%{name}/lib

%files devel
%defattr(-,root,root)
   /%{_prefix}/%{name}/dbd
   /%{_prefix}/%{name}/include
   /%{_prefix}/%{name}/configure

%changelog
* Fri Jul 10 2020 Matt Rippa <mrippa@gemini.edu> 3.15.8-2.2.8.20200710gitaf3c52b
- new package built with tito

* Fri Mar 9 2012 Mathew Rippa <mrippa@gemini.edu> 2.1.13-0
- r3.14.12.2, rpmlint compliant
* Mon Feb 11 2008 Felix Kraemer <fkraemer@gemini.edu> 2.0.11-0
- changes to be compliant with EPICS build mechanism
* Wed Dec 19 2007 Felix Kraemer <fkraemer@gemini.edu> 2.0.11-0
- initial release
