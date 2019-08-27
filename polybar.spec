################################################################################
# Preamble
# The preamble section contains information about the package being built and
# define any dependencies to the package. In general, the preamble consists of
# entries, one per line, that start with a tag followed by a colon, and then
# some information.

# The base name of the package, which should match the SPEC file name.
Name: polybar

# The upstream version number of the software.
Version: 3.4.0

# The number of times this version of the software was released. Normally, set
# the initial value to 1%{?dist}, and increment it with each new release of the
# package. Reset to 1 when a new Version of the software is built. 
Release: 1%{?dist}

# A brief, one-line summary of the package.
Summary: A fast and easy to use tool for creating status bars

# The license of the software being packaged.
License: MIT

Group: System/GUI/Other

# The full URL for more information about the program. Most often this is the
# upstream project website for the software being packaged. 
URL: https://polybar.github.io/

# Path or URL to the compressed archive of the upstream source code (unpatched,
# patches are handled elsewhere). This should point to an accessible and
# reliable storage of the archive, for example, the upstream page and not the
# packager’s local storage. If needed, more SourceX directives can be added,
# incrementing the number each time, for example: Source1, Source2, Source3,
# and so on. 
Source0: https://github.com/polybar/polybar/archive/%{version}.tar.gz

# The name of the first patch to apply to the source code if necessary. If
# needed, more PatchX directives can be added, incrementing the number each
# time, for example: Patch1, Patch2, Patch3, and so on.
# Patch0:

# If the package is not architecture dependent, for example, if written
# entirely in an interpreted programming language, set this to BuildArch:
# noarch. If not set, the package automatically inherits the Architecture
# of the machine on which it is built, for example x86_64. 
# BuildArch:

# A comma- or whitespace-separated list of packages required for building the
# program written in a compiled language. There can be multiple entries of
# BuildRequires, each on its own line in the SPEC file.
# BuildRequires:

# From https://github.com/polybar/polybar/wiki/Compiling

# The following dependencies are only needed during compilation, you can remove
# them, if you don't need them, after you built polybar
BuildRequires: clang
BuildRequires: cmake
BuildRequires: @development-tools
BuildRequires: python3-sphinx

# These are the hard dependencies, you cannot build or run polybar without them
BuildRequires: cairo-devel
BuildRequires: xcb-util-devel
BuildRequires: libxcb-devel
BuildRequires: xcb-proto
BuildRequires: xcb-util-image-devel
BuildRequires: xcb-util-wm-devel

# These dependencies enable optional features in polybar, if they are installed
# during compilation:
BuildRequires: xcb-util-xrm-devel
BuildRequires: xcb-util-cursor-devel
BuildRequires: alsa-lib-devel
BuildRequires: pulseaudio-libs-devel
BuildRequires: i3
BuildRequires: jsoncpp-devel
BuildRequires: libmpdclient-devel
BuildRequires: libcurl-devel
BuildRequires: libnl3-devel

# A comma- or whitespace-separated list of packages required by the software to
# run once installed. There can be multiple entries of Requires, each on its own
# line in the SPEC file.
# Requires:

# These are the hard dependencies, you cannot build or run polybar without them
Requires: cairo
Requires: xcb-util
Requires: libxcb
Requires: xcb-proto
Requires: xcb-util-image
Requires: xcb-util-wm

# If a piece of software can not operate on a specific processor architecture,
# you can exclude that architecture here.
# ExcludeArch: 

################################################################################
# Description

# A full description of the software packaged in the RPM. This description can
# span multiple lines and can be broken into paragraphs. 

%description
Polybar aims to help users build beautiful and highly customizable status
bars for their desktop environment, without the need of having a black belt in
shellscripting.

The main purpose of Polybar is to help users create awesome status bars. It
has built-in functionality to display information about the most commonly
used services.

################################################################################
# Prep

# Command or series of commands to prepare the software to be built, for
# example, unpacking the archive in Source0. This directive can contain a shell
# script. 
%prep

# The setup macro ensures that we are working in the right directory, removes
# residues of previous builds, unpacks the source tarball, and sets up some
# default privileges.
%setup

################################################################################
# Build

# Command or series of commands for actually building the software into machine
# code (for compiled languages) or byte code (for some interpreted languages).
%build

mkdir build
cd build

# options come from https://github.com/polybar/polybar/blob/master/include/settings.hpp.cmake
# just set everythong to on
cmake .. \
      -DCMAKE_INSTALL_PREFIX=/usr \
      -DCMAKE_BUILD_TYPE=Release \
      -DCMAKE_C_COMPILER="clang" \
      -DCMAKE_CXX_COMPILER="clang++" \
      -DENABLE_ALSA:BOOL="ON" \
      -DENABLE_MPD:BOOL="ON" \
      -DENABLE_NETWORK:BOOL="ON" \
      -DWITH_LIBNL:BOOL="ON" \
      -DENABLE_I3:BOOL="ON" \
      -DENABLE_CURL:BOOL="ON" \
      -DENABLE_PULSEAUDIO:BOOL="ON" \
      -DWITH_XRANDR:BOOL="ON" \
      -DWITH_XCOMPOSITE:BOOL="ON" \
      -DWITH_XKB:BOOL="ON" \
      -DWITH_XRM:BOOL="ON" \
      -DWITH_XCURSOR:BOOL="ON"

%make_build

################################################################################
# Install

# Command or series of commands for copying the desired build artifacts from the
# builddir (where the build happens) to the %buildroot directory (which
# contains the directory structure with the files to be packaged). This usually
# means copying files from ~/rpmbuild/BUILD to ~/rpmbuild/BUILDROOT and creating
# the necessary directories in ~/rpmbuild/BUILDROOT. This is only run when
# creating a package, not when the end-user installs the package. See Section
# 5.1.7, “Working with SPEC files” for details.
%install

%make_install

################################################################################
# Check

# Command or series of commands to test the software. This normally includes
# things such as unit tests. 
%check

################################################################################
# Files

# The list of files that will be installed in the end user’s system.
# Copied from original source (see changelog)

%files
%{_bindir}/%{name}
%{_bindir}/%{name}-msg
%{_mandir}/man1/%{name}.1.gz
%{_datadir}/bash-completion/completions/%{name}
%{_datadir}/zsh/site-functions/_%{name}
%{_datadir}/zsh/site-functions/_%{name}_msg
%config(noreplace) %{_datadir}/doc/%{name}/config/

################################################################################
# Changelog

# A record of changes that have happened to the package between different
# Version or Release builds. 
%changelog
* Tue Aug 17 2019 - Reilly Raab <rraab@ucsc.edu>
- Copied spec file from https://copr-dist-git.fedorainfracloud.org/cgit/mhartgring/polybar/polybar.git/tree/?h=f30
- Added verbose comments documenting purpose of spec file copied from https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html-single/rpm_packaging_guide/index
- Set upstream version to 3.4.0

* Tue May 9 2019 - Marco Hartgring <marco.hartgring@gmail.com>
- Initial version
