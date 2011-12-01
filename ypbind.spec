# Rebuild with  '--with dbus' to enbale dbus/Netwrokmanager support
%global nodbus_support %{?_with_dbus: %nil}%{?!_with_dbus: --disable-dbus-nm}

Summary: The NIS daemon which binds NIS clients to an NIS domain
Name: ypbind
Version: 1.29.91
Release: %mkrel 5
Epoch: 3
License: GPL
Group: System/Servers
URL: http://www.linux-nis.org/nis/ypbind-mt/index.html
Source0: ftp://ftp.kernel.org/pub/linux/utils/net/NIS/ypbind-mt-%{PACKAGE_VERSION}.tar.gz
Source3: ftp://ftp.kernel.org/pub/linux/utils/net/NIS/ypbind-mt-%{PACKAGE_VERSION}.tar.gz.sign
Source1: ypbind.init
Source2: yp.conf
Patch0: ypbind-broadcast-get-server.patch
Patch2: ypbind-1.11-gettextdomain.patch
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires: rpcbind
Requires: yp-tools
%if %{?nodbus_support: 0}%{?!nodbus_support: 1}
BuildRequires: dbus-devel
BuildRequires: dbus-glib >= 0.60
BuildRequires: networkmanager-devel
%endif
Buildroot: %{_tmppath}/ypbind-root

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
%patch0 -p0 -b .broadcast
%patch2 -p1 -b .fixit

%build
%serverbuild
%configure --sbindir=/sbin %{?nodbus_support}
%make

%install
rm -rf %{buildroot}
%makeinstall sbindir=%{buildroot}/sbin

mkdir -p %{buildroot}%{_initrddir}
install -m 755 %{SOURCE1} %{buildroot}%{_initrddir}/ypbind
install -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/yp.conf
mkdir -p %{buildroot}/var/yp/binding

perl -pi -e "s|/etc/rc.d/init.d|%{_initrddir}|" %{buildroot}%{_initrddir}/*

%find_lang %{name}

%clean
rm -rf %{buildroot}

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



