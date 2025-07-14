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
%define	gitref	f52c14efc88c
%define	snap	20240415
%define	rel	1
Release:	0.%{snap}.%{rel}
License:	WTFPL v2
Group:		Libraries
Source0:	https://bitbucket.org/the-sekrit-twc/libp2p/get/%{gitref}.tar.gz#/%{name}-%{gitref}.tar.gz
# Source0-md5:	12d82bf59fc7408107a21678dff40385
Patch0:		%{name}-shared.patch
URL:		https://bitbucket.org/the-sekrit-twc/libp2p
BuildRequires:	libstdc++-devel >= 6:5
BuildRequires:	libtool >= 2:1.5
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
%setup -q -n the-sekrit-twc-%{name}-%{gitref}
%patch -P0 -p1

%build
%{__make} \
	CXX="%{__cxx}" \
	CXXFLAGS="%{rpmcxxflags}" \
	CPPFLAGS="%{rpmcppflags}" \
	LDFLAGS="%{rpmldflags}" \
%if %{with simd}
	SIMD=1 \
%endif
	libdir=%{_libdir}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	includedir=%{_includedir} \
	libdir=%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

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
