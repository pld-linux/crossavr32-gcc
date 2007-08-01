# $RevOCision: 1.31 $, $Date: 2007-08-01 20:42:29 $
#
# Conditional build:
%bcond_with	bootstrap	# for bootstraping
#
Summary:	Cross AVR32 GNU binary utility development utilities - gcc
Summary(es.UTF-8):	Utilitarios para desarrollo de binarios de la GNU - AVR32 gcc
Summary(fr.UTF-8):	Utilitaires de développement binaire de GNU - AVR32 gcc
Summary(pl.UTF-8):	Skrośne narzędzia programistyczne GNU dla AVR32 - gcc
Summary(pt_BR.UTF-8):	Utilitários para desenvolvimento de binários da GNU - AVR32 gcc
Summary(tr.UTF-8):	GNU geliştirme araçları - AVR32 gcc
Name:		crossavr32-gcc
Version:	4.2.1
Release:	0.6%{?with_bootstrap:.bootstrap}
Epoch:		1
License:	GPL
Group:		Development/Languages
Source0:	ftp://gcc.gnu.org/pub/gcc/releases/gcc-%{version}/gcc-%{version}.tar.bz2
# Source0-md5:	cba410e6ff70f7d7f4be7a0267707fd0
Patch0:		%{name}.patch
Patch1:		%{name}-configure.patch
BuildRequires:	/bin/bash
BuildRequires:	autoconf
BuildRequires:	bison
BuildRequires:	crossavr32-binutils
BuildRequires:	flex
Requires:	crossavr32-binutils >= 2.17
%{!?with_boostrap:Requires:	crossavr32-uClibc}
Requires:	gcc-dirs
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		target		avr32-pld-linux
%define		arch		%{_prefix}/%{target}
%define		gccarch		%{_libdir}/gcc/%{target}
%define		gcclib		%{_libdir}/gcc/%{target}/%{version}
%define		_noautostrip	.*%{arch}/lib/.*
%define		_noautochrpath	.*%{arch}/lib/.*

%description
This package contains a cross-gcc which allows the creation of
binaries to be run on Atmel AVR32 on other machines.

%description -l de.UTF-8
Dieses Paket enthält einen Cross-gcc, der es erlaubt, auf einem
anderem Rechner Code für Atmel AVR32 zu generieren.

%description -l pl.UTF-8
Ten pakiet zawiera skrośny gcc pozwalający na robienie na innych
maszynach binariów do uruchamiania na Atmel AVR.

%package c++
Summary:	C++ support for avr32-gcc
Summary(pl.UTF-8):	Obsługa C++ dla avr32-gcc
Group:		Development/Languages
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description c++
This package adds C++ support to the GNU Compiler Collection for
AVR32.

%description c++ -l pl.UTF-8
Ten pakiet dodaje obsługę C++ do kompilatora gcc dla AVR32.

%package -n crossavr32-libgomp
Summary:	GNU OpenMP library
Summary(pl.UTF-8):	Biblioteka GNU OpenMP
License:	GPL v2+ with unlimited link permission
Group:		Libraries

%description -n crossavr32-libgomp
GNU OpenMP library.

%description -n crossavr32-libgomp -l pl.UTF-8
Biblioteka GNU OpenMP.

%package -n crossavr32-libstdc++
Summary:	GNU C++ library
Summary(pl.UTF-8):	Biblioteki GNU C++
License:	GPL v2+ with free software exception
Group:		Libraries

%description -n crossavr32-libstdc++
This is the GNU implementation of the standard C++ libraries, along
with additional GNU tools. This package includes the shared libraries
necessary to run C++ applications.

%prep
%setup -q -n gcc-%{version}
%patch0 -p1
%patch1 -p0

%build
%{__autoconf}

rm -rf obj-%{target}
install -d obj-%{target}
cd obj-%{target}

CFLAGS="%{rpmcflags}" \
CXXFLAGS="%{rpmcflags}" \
TEXCONFIG=false \
../configure \
	--prefix=%{_prefix} \
	--infodir=%{_infodir} \
	--mandir=%{_mandir} \
	--bindir=%{_bindir} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libdir} \
	--enable-shared \
%if %{with bootstrap}
	--enable-languages="c" \
	--disable-libssp \
	--disable-threads \
	--disable-libmudflap \
	--disable-nls \
	--disable-libgomp \
%else
	--enable-languages="c,c++" \
	--enable-threads=posix \
	--enable-libssp \
	--disable-libstdcxx-pch \
	--enable-__cxa_atexit \
	--enable-libstdcxx-allocator=new \
%endif
	--with-dwarf2 \
	--with-gnu-as \
	--with-gnu-ld \
	--with-system-zlib \
	--with-multilib \
	--without-x \
	--build=%{_target_platform} \
	--host=%{_target_platform} \
	--target=%{target}


CXXFLAGS_FOR_TARGET="-Os"
export CXXFLAGS_FOR_TARGET
%{__make} CFLAGS_FOR_TARGET="-Os" CXXFLAGS_FOR_TARGET="-Os"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C obj-%{target} install \
	DESTDIR=$RPM_BUILD_ROOT

# don't want it here
rm -f $RPM_BUILD_ROOT%{_libdir}/libiberty.a
rm -rf $RPM_BUILD_ROOT%{_infodir}
rm -f $RPM_BUILD_ROOT%{_mandir}/man7/fsf-funding.7
rm -f $RPM_BUILD_ROOT%{_mandir}/man7/gfdl.7
rm -f $RPM_BUILD_ROOT%{_mandir}/man7/gpl.7
rm -f $RPM_BUILD_ROOT%{_datadir}/locale/*/LC_MESSAGES/{gcc,cpplib}.mo
rm -f $RPM_BUILD_ROOT%{gcclib}/include/fixed
rm -f $RPM_BUILD_ROOT%{gcclib}/include/README
rm -rf $RPM_BUILD_ROOT%{gcclib}/install-tools

%if 0%{!?debug:1}
# strip target libraries
%{target}-strip --strip-debug --remove-section=.note --remove-section=.comment \
	$RPM_BUILD_ROOT%{gcclib}{,/uc}/libg*.a \
	$RPM_BUILD_ROOT%{arch}/lib{,/uc}/lib*.a
%{target}-strip --strip-unneeded --remove-section=.note --remove-section=.comment \
	$RPM_BUILD_ROOT%{arch}/lib{,/uc}/lib*.so.*.*
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{target}-gcc*
%attr(755,root,root) %{_bindir}/%{target}-cpp
%attr(755,root,root) %{_bindir}/%{target}-gcov
%dir %{gccarch}
%dir %{gcclib}
%attr(755,root,root) %{gcclib}/cc1
%attr(755,root,root) %{gcclib}/collect2
%{gcclib}/libg*.a
%{gcclib}/crt*.o
%{gcclib}/uc
%dir %{gcclib}/include
%{gcclib}/include/*.h
%{_mandir}/man1/%{target}-cpp.1*
%{_mandir}/man1/%{target}-gcc.1*
%{_mandir}/man1/%{target}-gcov.1*

%if %{without bootstrap}
%files c++
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{target}-g++
%attr(755,root,root) %{_bindir}/%{target}-c++
%attr(755,root,root) %{gcclib}/cc1plus
%{_mandir}/man1/%{target}-g++.1*

%files -n crossavr32-libgomp
%defattr(644,root,root,755)
%{arch}/lib/libgomp*
%{arch}/lib/uc/libgomp*

%files -n crossavr32-libstdc++
%defattr(644,root,root,755)
%{arch}/lib/libstdc*
%{arch}/lib/libsupc*
%{arch}/lib/uc/libstdc*
%{arch}/lib/uc/libsupc*
%{arch}/include/c++

%endif
