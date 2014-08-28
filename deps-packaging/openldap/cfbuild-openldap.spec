Summary: CFEngine Build Automation -- openldap
Name: cfbuild-openldap
Version: %{version}
Release: 1
Source0: openldap-2.4.23.tgz
License: MIT
Group: Other
Url: http://example.com/
BuildRoot: %{_topdir}/BUILD/%{name}-%{version}-%{release}-buildroot

AutoReqProv: no

%define prefix /var/cfengine

%prep
mkdir -p %{_builddir}
%setup -q -n openldap-2.4.23

LDFLAGS=-L/var/cfengine/lib
CPPFLAGS=-I/var/cfengine/include

#
# glibc-2.8 errorneously hides peercred(3) under #ifdef __USE_GNU.
#
# Remove this after decomissioning all glibc-2.8-based distributions
# (e.g. SLES 11).
#
CPPFLAGS="$CPPFLAGS -D_GNU_SOURCE"

./configure --prefix=%{prefix} \
            --enable-shared \
            --disable-slapd \
            --disable-backends \
            --with-tls=openssl \
            --without-gssapi \
            LDFLAGS="$LDFLAGS" \
            CPPFLAGS="$CPPFLAGS"


%build

make -C include
make -C libraries

%install
rm -rf ${RPM_BUILD_ROOT}

make -C include install DESTDIR=${RPM_BUILD_ROOT}
make -C libraries install DESTDIR=${RPM_BUILD_ROOT}

# Removing unused files

rm -rf ${RPM_BUILD_ROOT}%{prefix}/etc
rm -f ${RPM_BUILD_ROOT}%{prefix}/lib/*.a
rm -f ${RPM_BUILD_ROOT}%{prefix}/lib/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%package devel
Summary: CFEngine Build Automation -- openldap -- development files
Group: Other
AutoReqProv: no

%description
CFEngine Build Automation -- openldap

%description devel
CFEngine Build Automation -- openldap -- development files

%files
%defattr(-,root,root)

%dir %{prefix}/lib
%{prefix}/lib/*.so.*

%files devel
%defattr(-,root,root)

%{prefix}/include

%dir %{prefix}/lib
%{prefix}/lib/*.so

%changelog