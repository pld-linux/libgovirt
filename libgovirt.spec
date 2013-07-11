#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
#
Summary:	goVirt library - GLib binding for oVirt REST API
Summary(pl.UTF-8):	Biblioteka goVirt - wiązanie GLib do API REST-owego oVirt
Name:		libgovirt
Version:	0.2.0
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://people.freedesktop.org/~teuf/govirt/%{name}-%{version}.tar.xz
# Source0-md5:	107e814e0196147f6f8573acc6a0a559
URL:		http://cgit.freedesktop.org/~teuf/govirt/
BuildRequires:	glib2-devel >= 1:2.26.0
BuildRequires:	gobject-introspection-devel >= 1.30.0
BuildRequires:	rest-devel >= 0.7.13
Requires:	glib2 >= 1:2.26.0
Requires:	rest >= 0.7.13
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GoVirt is a GObject wrapper for the oVirt REST API. It will only
provide very basic functionality as the goal is to autogenerate a full
wrapper as it is already done for the Python bindings.

%description -l pl.UTF-8
GoVirt to interfejs GObject dla API REST-owego oVirt. Zapewnia
jedynie podstawową funkcjonalność, jako że celem jest automatyczne
generowanie pełnego interfejsu - tak, jak jest to robione w wiązaniach
Pythona.

%package devel
Summary:	Header files for goVirt library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki goVirt
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.26.0
Requires:	rest-devel >= 0.7.13

%description devel
Header files for goVirt library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki goVirt.

%package static
Summary:	Static goVirt library
Summary(pl.UTF-8):	Statyczna biblioteka goVirt
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static goVirt library.

%description static -l pl.UTF-8
Statyczna biblioteka goVirt.

%prep
%setup -q

%build
%configure \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS MAINTAINERS NEWS README
%attr(755,root,root) %{_libdir}/libgovirt.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgovirt.so.2
%{_libdir}/girepository-1.0/GoVirt-1.0.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgovirt.so
%{_includedir}/govirt-1.0
%{_datadir}/gir-1.0/GoVirt-1.0.gir
%{_pkgconfigdir}/govirt-1.0.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libgovirt.a
%endif
