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
# the initial value to 1(replace){?dist}, and increment it with each new release
# of the package. Reset to 1 when a new Version of the software is built.
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
%global i3ipcpp_hash 21ce906
%global xpp_hash d2ff2aa

Source0: https://github.com/polybar/polybar/archive/%{version}.tar.gz
# git submodules are not included in root .tar.gz
Source1: https://github.com/polybar/i3ipcpp/tarball/%{i3ipcpp_hash}
Source2: https://github.com/polybar/xpp/tarball/%{xpp_hash}

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
# BuildRequires: git
BuildRequires: cmake
BuildRequires: cmake-data
BuildRequires: python-sphinx

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
shell-scripting.

The main purpose of Polybar is to help users create awesome status bars. It
has built-in functionality to display information about the most commonly
used services.

# stops rpmbuild from complaining about empty debug files.
# this macro should come before the %prep and %setup sections of the spec file.
%global debug_package %{nil}

################################################################################
# Prep

# Command or series of commands to prepare the software to be built, for
# example, unpacking the archive in Source0. This directive can contain a shell
# script.
%prep

# The setup macro ensures that we are working in the right directory, removes
# residues of previous builds, unpacks the source tarball, and sets up some
# default privileges.
%setup -q -a 1 -a 2

# unpack submodules into correct directories
mv %{name}-i3ipcpp-%{i3ipcpp_hash}/* lib/i3ipcpp/
rm -rf %{name}-i3ipcpp-%{i3ipcpp_hash}
mv %{name}-xpp-%{xpp_hash}/* lib/xpp
rm -rf %{name}-xpp-%{xpp_hash}

################################################################################
# Build

# Command or series of commands for actually building the software into machine
# code (for compiled languages) or byte code (for some interpreted languages).
%build

mkdir build
cd build

# options come from inspection of
#   include/settings.hpp.cmake &
#   CMakeLists.txt

# Set everything to on except tests. Tests require internet access to
# googletests git repository, which keeps failing on my local builds with mock.
# (all tests pass when build in my local environment outside of mock's chroot).
# Without tests, we comment out the `make test` section of "check" and we no
# longer need git as a build dependency.
cmake .. \
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
      -DWITH_XCURSOR:BOOL="ON" \
      -DBUILD_DOC:BOOL="ON" \
      -DBUILD_TESTS:BOOL="OFF"

%make_build

################################################################################
# Install

# Command or series of commands for copying the desired build artifacts from the
# builddir (where the build happens) to the 'buildroot' directory (which
# contains the directory structure with the files to be packaged). This usually
# means copying files from ~/rpmbuild/BUILD to ~/rpmbuild/BUILDROOT and creating
# the necessary directories in ~/rpmbuild/BUILDROOT. This is only run when
# creating a package, not when the end-user installs the package. See Section
# 5.1.7, “Working with SPEC files” for details.
%install

cd build

%make_install

################################################################################
# Check

# Command or series of commands to test the software. This normally includes
# things such as unit tests.
%check

cd build

# make test

################################################################################
# Files

# The list of files that will be installed in the end user’s system.
# This list was generated by stdout of `make install`.

%files

# BINDIR:  /usr/local/bin
/usr/local/bin/polybar
/usr/local/bin/polybar-msg
# DATADIR: /usr/local/share
/usr/local/share/bash-completion/completions/polybar
/usr/local/share/zsh/site-functions/_polybar
/usr/local/share/zsh/site-functions/_polybar_msg
# MANDIR:  /usr/local/share/man
/usr/local/share/man/man1/polybar.1
# DOCDIR:  /usr/local/share/doc/polybar
%dir /usr/local/share/doc/polybar
/usr/local/share/doc/polybar
/usr/local/share/doc/polybar/config
%doc /usr/local/share/doc/polybar/index.html
/usr/local/share/doc/polybar/_static
/usr/local/share/doc/polybar/_static/ajax-loader.gif
/usr/local/share/doc/polybar/_static/up-pressed.png
/usr/local/share/doc/polybar/_static/websupport.js
/usr/local/share/doc/polybar/_static/basic.css
/usr/local/share/doc/polybar/_static/jquery-3.2.1.js
/usr/local/share/doc/polybar/_static/comment.png
/usr/local/share/doc/polybar/_static/comment-close.png
/usr/local/share/doc/polybar/_static/plus.png
/usr/local/share/doc/polybar/_static/comment-bright.png
/usr/local/share/doc/polybar/_static/underscore.js
/usr/local/share/doc/polybar/_static/underscore-1.3.1.js
/usr/local/share/doc/polybar/_static/language_data.js
/usr/local/share/doc/polybar/_static/doctools.js
/usr/local/share/doc/polybar/_static/up.png
/usr/local/share/doc/polybar/_static/down-pressed.png
/usr/local/share/doc/polybar/_static/file.png
/usr/local/share/doc/polybar/_static/documentation_options.js
/usr/local/share/doc/polybar/_static/alabaster.css
/usr/local/share/doc/polybar/_static/minus.png
/usr/local/share/doc/polybar/_static/custom.css
/usr/local/share/doc/polybar/_static/down.png
/usr/local/share/doc/polybar/_static/pygments.css
/usr/local/share/doc/polybar/_static/searchtools.js
/usr/local/share/doc/polybar/_static/jquery.js
/usr/local/share/doc/polybar/man
/usr/local/share/doc/polybar/man/polybar.1.html
/usr/local/share/doc/polybar/searchindex.js
/usr/local/share/doc/polybar/search.html
/usr/local/share/doc/polybar/_sources
/usr/local/share/doc/polybar/_sources/index.rst.txt
/usr/local/share/doc/polybar/_sources/man
/usr/local/share/doc/polybar/_sources/man/polybar.1.rst.txt
/usr/local/share/doc/polybar/objects.inv
/usr/local/share/doc/polybar/genindex.html
/usr/local/share/doc/polybar/.buildinfo

################################################################################
# Changelog

# A record of changes that have happened to the package between different
# Version or Release builds.
%changelog
* Tue Aug 27 2019 Reilly Raab <rraab@ucsc.edu> 3.4.0
  - Initial version
