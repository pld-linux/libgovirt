#
# Conditional build:
%bcond_without	static_libs	# static library
#
Summary:	goVirt library - GLib binding for oVirt REST API
Summary(pl.UTF-8):	Biblioteka goVirt - wiązanie GLib do API REST-owego oVirt
Name:		libgovirt
Version:	0.3.9
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	https://download.gnome.org/sources/libgovirt/0.3/%{name}-%{version}.tar.xz
# Source0-md5:	6ebc2a24f30e456070f8840792793b13
URL:		https://github.com/GNOME/libgovirt
BuildRequires:	gettext-tools >= 0.19.4
BuildRequires:	glib2-devel >= 1:2.66
BuildRequires:	gobject-introspection-devel >= 1.30.0
BuildRequires:	meson >= 0.49.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	rest1-devel >= 0.9
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	glib2 >= 1:2.66
Requires:	rest1 >= 0.9
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
Requires:	glib2-devel >= 1:2.66
Requires:	rest1-devel >= 0.9

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
%meson build \
	%{!?with_static_libs:--default-library=shared}

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%find_lang govirt-1.0

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f govirt-1.0.lang
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
