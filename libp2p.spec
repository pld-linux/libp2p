# TODO: shared library
#
# Conditional build:
%bcond_with	simd		# SSE4.1 instructions (runtime detected by cpuid)
#
%ifarch i686 pentium4 %{x8664} x32
%define	with_simd	1
%endif
Summary:	Library to pack/unpack pixels
Summary(pl.UTF-8):	Biblioteka do pakowania/rozpakowywania pikseli
Name:		libp2p
Version:	0
%define	gitref	5e65679ae54d0f9fa412ab36289eb2255e341625
%define	snap	20220707
%define	rel	1
Release:	0.%{snap}.%{rel}
License:	WTFPL v2
Group:		Libraries
Source0:	https://github.com/sekrit-twc/libp2p/archive/%{gitref}/%{name}-%{snap}.tar.gz
# Source0-md5:	663e2005ffe0eecea2cc9336e0b789e4
URL:		https://github.com/sekrit-twc/libp2p
BuildRequires:	libstdc++-devel >= 6:5
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The "p2p" library implements conversion between packed and planar
image formats. A packed format is any memory layout that stores more
than one image component ("plane") in a single array. For example, the
common ARGB format stores pixels as an array of DWORDs holding all
components for each pixel. In contrast, a planar format stores each
image component in its own array.

%description -l pl.UTF-8
Biblioteka "p2p" implementuje przekształcenia między formatem obrazu
upakowanym i płaszczyznowym. Format upakowany to układ pamięci, gdzie
więcej niż jedna składowa (warstwa) znajduje się w pojedynczej
tablicy - np. popularny format ARGB przechowuje piksele w tablicy typu
DWORD, przechowując wszystkie składowe każdego piksela. Dla porównania
format płaszczyznowy przechowuje każdą składową w osobnej tablicy.

%package devel
Summary:	Header files for libp2p library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libp2p
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel >= 6:5

%description devel
Header files for libp2p library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libp2p.

%package static
Summary:	Static libp2p library
Summary(pl.UTF-8):	Statyczna biblioteka libp2p
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libp2p library.

%description static -l pl.UTF-8
Statyczna biblioteka libp2p.

%prep
%setup -q -n %{name}-%{gitref}

%build
%{__make} \
	CXX="%{__cxx}" \
	CXXFLAGS="%{rpmcxxflags}" \
	CPPFLAGS="%{rpmcppflags}" \
	LDFLAGS="%{rpmldflags}" \
%if %{with simd}
	SIMD=1
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_includedir}}

%if %{with shared}
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libp2p.la
%else
cp -p libp2p.a $RPM_BUILD_ROOT%{_libdir}
cp -p p2p.h p2p_api.h $RPM_BUILD_ROOT%{_includedir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with shared}

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING README.md
%attr(755,root,root) %{_libdir}/libp2p.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libp2p.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libp2p.so
%{_libdir}/libp2p.la
%{_includedir}/p2p.h
%{_includedir}/p2p_api.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libp2p.a

%else

%files devel
%defattr(644,root,root,755)
%{_libdir}/libp2p.a
%{_includedir}/p2p.h
%{_includedir}/p2p_api.h

%endif
