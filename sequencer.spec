%define _prefix /gem_base/epics/support
%define name sequencer
%define repository gemdev
%define debug_package %{nil}
%define arch %(uname -m)
%define checkout %(git log --pretty=format:'%h' -n 1)

# These defines need to be adjusted to point to the git ref
# that is to be built

# Tip 1: git remote add vendor https://github.com/epics-modules/sequencer.git
# to your development sandbox to easily track both vendor/upstream and
# origin/gemini.

# Tip 2: git ls-remote --tags vendor to see sha and refs/tags side-by-side

# vendor/upstream git project
%define vendor_project https://github.com/epics-modules/sequencer.git
# vendor git ref (tag or commit hash). Please keep in sync with 'Version' below!
%define vendor_ref R2-2-9

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
# version follows SemVer release tagging; vendor_ref pins the exact upstream snapshot
Version: 2.2.9
Release: 0.4.rc4
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
git checkout %{vendor_ref}

# apply Gemini-specific configuration
cp ../configure/* configure/
rm -f configure/RELEASE.local
rm -f configure/RELEASE.linux-x86_64.Common
rm -f configure/RELEASE.local.linux-x86_64

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
* Fri Apr 24 2026 Matt Rippa <matt.rippa@noirlab.edu> 2.2.9-0.4.rc4
- RTEMS-858: Bootstrap branch snapshot metadata
- RTEMS-858: Pin sequencer vendor source to upstream R2-2-9
- RTEMS-858: Fix support-layer CI base container
- RTEMS-858: Prepare sequencer v2.2.9-rc.2 from corrected branch anchor
- SYSCO-876: Rebuild New Testing Release

* Fri Apr 24 2026 Matt Rippa <matt.rippa@noirlab.edu> 2.2.9-0.2.rc2
- RTEMS-858: Bootstrap branch snapshot metadata
- RTEMS-858: Bootstrap branch snapshot metadata
- RTEMS-858: Align sequencer release prep with vendor rc.2 packaging
- SYSCO-876: Rebuild New Testing Release

* Fri Apr 24 2026 Matt Rippa <matt.rippa@noirlab.edu> 2.2.9-0.2.rc2
- 

* Fri Apr 24 2026 Matt Rippa <matt.rippa@noirlab.edu> 2.2.9-0.2.rc2
- move release metadata from rc.1 to rc.2
- switch sequencer packaging to vendor-style checkout from epics-modules
