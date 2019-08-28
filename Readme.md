This repository is referenced by the COPR build system for
[rpraab/Polybar](https://copr.fedorainfracloud.org/coprs/rpraab/Polybar/),
which packages [polybar](https://polybar.github.io/) as an RPM.

This exercise was intended to introduce me to the RPM ecosytem. Polybar was a
good target since multiple spec files already exist on COPR for this software.

This being said, I do believe I made some improvements over existing packages 
(such as downloading sources from the github archives rather than the tarball 
release, which in theory need not match the original sources). I also compiled
the source with all optional modules enabled, included the documentation in the
install.

At present, I have only enabled Fedora version 30 on x86_64 machines as a build
target.

# Making the package

The most helpful resource I found was 
"[RPM Packaging Guide](https://rpm-packaging-guide.github.io/)", produced by
the Redhat Developer Program.

Besides documentation for the `.spec` file format, the most helpful element of
the documentation was at the begining of the document: steps for local testing.

## Building from your local environment

1. Install the rpm devtools

`sudo dnf install rpmdevtools rpm-build`

2. Set up the build directories expected by the tool (they will be placed in
your home directory. This only needs to be done once.)

`rpmdev-setuptree`

3. Prep the spec file (downloads sources):

`spectool -g -R <spec_file>`

4. Try the build on your local architecture
(note, build dependencies must be manually met first)

`rpmbuild -ba <spec_file>`

## Mimicking COPR builds

These instructions are referenced from 
[fedoraproject.org](https://fedoraproject.org/wiki/Using_Mock_to_test_package_builds).

1. Install [mock](https://github.com/rpm-software-management/mock/wiki) and
add yourself to the mock group.

```
sudo dnf install mock fedpkg
sudo usermod -a -G mock $USER
```

2. Build the source RPM with rpmbuild (install and setup in steps 1 and 2 above)
and lint it for errors. Replace "f30" with your target release.

```
rpmbuild -bs <specfile>
cp <specfile> ~/rpmbuild/SRPMS
fedpkg --path ~/rpmbuild/SRPMS --release f30 lint
```

3. "rebuild" from the source-rpm using mock, where the package name will
have been assigned (and printed in the stdout message) by rpmbuild in the last
step. Mock will default to your current distro version and architecture as the
build target unless given an alternative with the `-r` flag. Enabling the ccache
plugin will speed up the debug cycle of repeatedly rebuilding after the first 
run.

```
cd ~/rpmbuild/SRPMS
mock --enable-plugin ccache <package-name.src.rpm>
```

4. If you make it here without errors, you should be good to go for using the
COPR build system.

# Building on COPR

The online 
[tutorial](https://docs.pagure.org/copr.copr/user_documentation.html#tutorial)
was straightforward, and in particular the
[screenshot tutorial](https://docs.pagure.org/copr.copr/screenshots_tutorial.html#screenshots-tutorial) was very easy
to follow.

In the future, I want to remember that using webhooks is 
[possible](https://hobo.house/2017/09/03/automate-rpm-builds-from-git-sources-using-copr/)
for triggering automatic builds.
