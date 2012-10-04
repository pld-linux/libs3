# $Revision: 1.21 $, $Date: 2011/07/16 18:25:43 $
#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
#
Summary:	C library and tools for Amazon S3 access
Summary(pl.UTF-8):	Biblioteka C i narzędzia do dostępu do Amazon S3
Name:		libs3
Version:	2.0
Release:	1
License:	GPL v3 with OpenSSL exception
Group:		Libraries
Source0:	http://libs3.ischo.com.s3.amazonaws.com/%{name}-%{version}.tar.gz
# Source0-md5:	e52da69ddc11019e98cf8246fc55b4e1
URL:		http://libs3.ischo.com.s3.amazonaws.com/index.html
BuildRequires:	curl-devel
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	libxml2-devel
BuildRequires:	openssl-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package includes the libs3 shared library needed to run
applications using libs3 and additionally contains the s3 utility
for accessing Amazon S3.

%description -l pl.UTF-8
Ten pakiet zawiera bibliotekę współdzieloną libs3 niezbędną do
uruchamiania aplikacji wykorzystujących libs3 oraz dodatkowo
narzędzie s3 pozwalające na dostęp do Amazon S3.

%package devel
Summary:	Header files for libs3 library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libs3
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	curl-devel
Requires:	libxml2-devel
Requires:	openssl-devel

%description devel
Header files for libs3 library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libs3.

%package static
Summary:	Static libs3 library
Summary(pl.UTF-8):	Statyczna biblioteka libs3
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libs3 library.

%description static -l pl.UTF-8
Statyczna biblioteka libs3.

%package apidocs
Summary:	libs3 API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki libs3
Group:		Documentation

%description apidocs
API and internal documentation for libs3 library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libs3.

%prep
%setup -q

%build
CFLAGS="%{rpmcflags}" \
%{__make} exported \
	VERBOSE=1

%{?with_apidocs:doxygen}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT%{_prefix}

%if "%{_lib}" != "lib"
mv -f $RPM_BUILD_ROOT%{_prefix}/{lib,%{_lib}}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog LICENSE README TODO
%attr(755,root,root) %{_bindir}/s3
%attr(755,root,root) %{_libdir}/libs3.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libs3.so.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libs3.so
%{_includedir}/libs3.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libs3.a

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc dox/html/*
%endif
