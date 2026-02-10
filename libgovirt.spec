#
# Conditional build:
%bcond_without	static_libs	# static library
#
Summary:	goVirt library - GLib binding for oVirt REST API
Summary(pl.UTF-8):	Biblioteka goVirt - wiązanie GLib do API REST-owego oVirt
Name:		libgovirt
Version:	0.3.11
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	https://download.gnome.org/sources/libgovirt/0.3/%{name}-%{version}.tar.xz
# Source0-md5:	872c4bc647110ed53a01b4f1882f80a0
URL:		https://github.com/GNOME/libgovirt
BuildRequires:	gcc >= 5:3.2
BuildRequires:	gettext-tools >= 0.19.4
BuildRequires:	glib2-devel >= 1:2.66
BuildRequires:	gobject-introspection-devel >= 1.30.0
BuildRequires:	librest-devel >= 0.10.2
BuildRequires:	meson >= 0.49.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 2.042
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	glib2 >= 1:2.66
Requires:	librest >= 0.10.2
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
Requires:	librest-devel >= 0.10.2

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
%meson \
	%{!?with_static_libs:--default-library=shared}

%meson_build

%install
rm -rf $RPM_BUILD_ROOT

%meson_install

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS MAINTAINERS NEWS README
%{_libdir}/libgovirt.so.*.*.*
%ghost %{_libdir}/libgovirt.so.2
%{_libdir}/girepository-1.0/GoVirt-1.0.typelib

%files devel
%defattr(644,root,root,755)
%{_libdir}/libgovirt.so
%{_includedir}/govirt-1.0
%{_datadir}/gir-1.0/GoVirt-1.0.gir
%{_pkgconfigdir}/govirt-1.0.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libgovirt.a
%endif
