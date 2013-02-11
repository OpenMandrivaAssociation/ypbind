# Rebuild with  '--with dbus' to enbale dbus/Netwrokmanager support
%global nodbus_support %{?_with_dbus: %nil}%{?!_with_dbus: --disable-dbus-nm}

Summary:	The NIS daemon which binds NIS clients to an NIS domain
Name:		ypbind
Version:	1.36
Release:	1
Epoch:		3
License:	GPL
Group:		System/Servers
URL:		http://www.linux-nis.org/nis/ypbind-mt/index.html
Source0:	http://www.linux-nis.org/download/ypbind-mt/ypbind-mt-%version.tar.bz2
Source1:	ypbind.init
Source2:	yp.conf
Patch0:		ypbind-mt-1.32-link-tirpc.patch
Patch1:		ypbind-mt-1.32-automake-1.13.patch
Patch2:		ypbind-1.11-gettextdomain.patch
Requires(post):	rpm-helper
Requires(preun):	rpm-helper
Requires:	rpcbind
Requires:	yp-tools
%if %{?nodbus_support: 0}%{?!nodbus_support: 1}
BuildRequires:	dbus-devel
BuildRequires:	dbus-glib >= 0.60
BuildRequires:	networkmanager-devel
%endif
BuildRequires:	tirpc-devel

%track
prog %name = {
	url = http://www.linux-nis.org/download/ypbind-mt/
	version = %version
	regex = ypbind-mt-(__VER__)\.tar\.bz2
}

%description
The Network Information Service (NIS) is a system which provides
network information (login names, passwords, home directories, group
information) to all of the machines on a network.  NIS can enable
users to login on any machine on the network, as long as the machine
has the NIS client programs running and the user's password is
recorded in the NIS passwd database.  NIS was formerly known as Sun
Yellow Pages (YP).

This package provides the ypbind daemon.  The ypbind daemon binds NIS
clients to an NIS domain.  Ypbind must be running on any machines
which are running NIS client programs.

Install the ypbind package on any machines which are running NIS client
programs (included in the yp-tools package).  If you need an NIS server,
you'll also need to install the ypserv package to a machine on your
network.

%prep
%setup -q -n ypbind-mt-%version
%apply_patches
aclocal -I m4
automake -a
autoconf

%build
%serverbuild
%configure --sbindir=/sbin %{?nodbus_support}
%make

%install
%makeinstall sbindir=$RPM_BUILD_ROOT/sbin

mkdir -p $RPM_BUILD_ROOT%{_initrddir}
install -m 755 %{SOURCE1} $RPM_BUILD_ROOT%{_initrddir}/ypbind
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/yp.conf
mkdir -p $RPM_BUILD_ROOT/var/yp/binding

perl -pi -e "s|/etc/rc.d/init.d|%{_initrddir}|" $RPM_BUILD_ROOT%{_initrddir}/*

%find_lang %{name}

%post
%_post_service ypbind

%preun
%_preun_service ypbind

%files -f %{name}.lang
%defattr(-,root,root)
%attr(755, root, root) /sbin/ypbind
%{_mandir}/*/*
%{_initrddir}/*
%config(noreplace) %{_sysconfdir}/yp.conf
%dir /var/yp/binding
%doc README ChangeLog AUTHORS THANKS NEWS





%changelog
* Sat May 07 2011 Oden Eriksson <oeriksson@mandriva.com> 3:1.29.91-5mdv2011.0
+ Revision: 671948
- mass rebuild

* Sat Dec 04 2010 Oden Eriksson <oeriksson@mandriva.com> 3:1.29.91-4mdv2011.0
+ Revision: 608268
- rebuild

* Mon Nov 30 2009 Olivier Thauvin <nanardon@mandriva.org> 3:1.29.91-3mdv2010.1
+ Revision: 471694
- add usefull files as doc (NEWS, ChangeLog, ...)

* Mon Nov 30 2009 Olivier Thauvin <nanardon@mandriva.org> 3:1.29.91-2mdv2010.1
+ Revision: 471642
- patch0: ensure server list is updated when using broadcast (#56029)

* Mon Nov 23 2009 Olivier Thauvin <nanardon@mandriva.org> 3:1.29.91-1mdv2010.1
+ Revision: 469164
- 1.29.91

* Sat May 09 2009 Olivier Thauvin <nanardon@mandriva.org> 3:1.20.5-2mdv2010.0
+ Revision: 373774
- requires rpcbind instead portmap since portmap has been trashed

* Sun Mar 22 2009 Oden Eriksson <oeriksson@mandriva.com> 3:1.20.5-1mdv2009.1
+ Revision: 360450
- 1.20.5

* Tue Dec 23 2008 Oden Eriksson <oeriksson@mandriva.com> 3:1.20.4-2mdv2009.1
+ Revision: 317953
- rediffed one fuzzy patch

* Sat Aug 16 2008 Olivier Thauvin <nanardon@mandriva.org> 3:1.20.4-1mdv2009.0
+ Revision: 272494
- 1.20.4

* Tue Mar 04 2008 Oden Eriksson <oeriksson@mandriva.com> 3:1.20.2-4mdv2008.1
+ Revision: 178844
- rebuild

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Thu Jun 07 2007 Anssi Hannula <anssi@mandriva.org> 3:1.20.2-3mdv2008.0
+ Revision: 36219
- rebuild with correct optflags

  + Olivier Thauvin <nanardon@mandriva.org>
    - requires portmapper instead portmap


* Fri Feb 16 2007 Olivier Thauvin <nanardon@mandriva.org> 1.20.2-1mdv2007.0
+ Revision: 121971
- 1.20.2
- make dbus support optional and disable by default

* Sat Jul 22 2006 Olivier Thauvin <nanardon@mandriva.org> 3:1.19.1-4mdv2007.0
+ Revision: 41840
- rebuild
- Import ypbind

* Mon Jan 09 2006 Olivier Blin <oblin@mandriva.com> 1.19.1-3mdk
- add LSB comments in initscript
- fix Requires post/preun

* Mon Jul 18 2005 Olivier Thauvin <nanardon@mandriva.org> 1.19-2mdk
- rpmlint fix

* Mon Jul 18 2005 Olivier Thauvin <nanardon@mandriva.org> 1.19-1mdk
- 1.19.1
- fix wrong conrestart check
- remove patch3, not need anymore

* Fri Aug 27 2004 Frederic Lepied <flepied@mandrakesoft.com> 1.17.3-1mdk
- new version

