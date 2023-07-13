%define _prefix /gem_base/epics/support
%define name sequencer
%define repository gemdev
%define debug_package %{nil}
%define arch %(uname -m)
%define checkout %(git log --pretty=format:'%h' -n 1) 

# These defines need to be adjusted to point to the git ref
# that is to be built

# vendor/upstream git project
## NOTE: HHZ Berlin is down due to a hacker attack! referring to an earlier commit of our
## own repo for now, as I didn't find a mirror with more recent commits
#%%define vendor_project https://www-csr.bessy.de/control/SoftDist/sequencer/repo/branch-2-2.git
%define vendor_project git@gitlab.com:nsf-noirlab/gemini/rtsw/support/sequencer.git
# vendor git ref (tag or commit hash). Please keep in sync with 'Version' below!
%define vendor_ref 00c29dbdfef888c2f32ce9774631b88bd16a06db

#These global defines are added to prevent stripping
# symbols on vxWorks cross-compiled code
# Getting 'strip' to work is probably only needed for
# building a related debug sub-package
#
# But this prevents all the strip warnings
# mrippa 20120202
%global _enable_debug_package 0
%global debug_package %{nil}
%global __os_install_post /usr/lib/rpm/brp-compress %{nil}

Summary: %{name} Package, a module for EPICS base
Name: %{name}
Version: 2.2.9.e5e3615
Release: 4%{?dist}
License: EPICS Open License
Group: Applications/Engineering
Source0: %{name}-%{version}.tar.gz
ExclusiveArch: %{arch}
Prefix: %{_prefix}
## You may specify dependencies here
BuildRequires: epics-base-devel re2c
Requires: epics-base
## Switch dependency checking off
## AutoReqProv: no

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
# get vendor code
git clone %{vendor_project} vendor_project
cd vendor_project

# apply Gemini-specific configuration
cp ../configure/* configure/

make distclean uninstall
make

%install
# cd into the directory containing the vendor sources
cd vendor_project

export DONT_STRIP=1
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_prefix}/%{name}
cp -r dbd $RPM_BUILD_ROOT/%{_prefix}/%{name}
cp -r bin $RPM_BUILD_ROOT/%{_prefix}/%{name}
cp -r lib $RPM_BUILD_ROOT/%{_prefix}/%{name}
cp -r include $RPM_BUILD_ROOT/%{_prefix}/%{name}
cp -r configure $RPM_BUILD_ROOT/%{_prefix}/%{name}
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
