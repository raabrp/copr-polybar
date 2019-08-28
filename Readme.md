This repository is referenced by the COPR build system for
[rpraab/Polybar](https://copr.fedorainfracloud.org/coprs/rpraab/Polybar/),
which packages [polybar](https://polybar.github.io/) as an RPM.

This exercise was intended to introduce me to the RPM ecosytem. Polybar was a
good target since multiple spec files already exist on COPR for this software.
This being said, I do beleive I made some improvements over existing packages 
(such as downloading sources from the github archives rather than the tarball 
release, which in theory need not match the original sources). I also compiled
the source with all optional modules enabled, included the documentation in the
install, and ran the provided unit tests).

At present, I have only enabled Fedora version 30 on x86_64 machines as a build
target.

# Making the package

The most helpful resource I found was 
"[RPM Packaging Guide](https://rpm-packaging-guide.github.io/)", produced by
the Redhat Developer Program.

Besides documentation for the `.spec` file format, the most helpful element of
the documentation was at the begining of the document: steps for local testing.

1. Install the rpm devtools

`dnf install rpmdevtools rpm-build`

2. Set up the build directories expected by the tool (they will be placed in
your home directory)

`rpmdev-setuptree`

3. Prep the spec file (download sources):

`spectool -g -R <spec_file>`

4. Try the build on your local architecture
(note, build dependencies must be met first)

`rpmbuild -ba <spec_file>`

# Building on COPR

The online 
[tutorial](https://docs.pagure.org/copr.copr/user_documentation.html#tutorial)
was straightforward, and in particular the
[screenshot tutorial](https://docs.pagure.org/copr.copr/screenshots_tutorial.html#screenshots-tutorial) was very easy
to follow.

In the future, I want to remember that using webhooks is 
[possible](https://hobo.house/2017/09/03/automate-rpm-builds-from-git-sources-using-copr/)
for triggering automatic builds.
