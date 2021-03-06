# Rebuild with  '--with dbus' to enable dbus/Networkmanager support
%global nodbus_support %{?_with_dbus: %nil}%{?!_with_dbus: --disable-dbus-nm}

# Location where helper scripts are located
%define scripts_path /usr/lib/%{name}

Summary:	The NIS daemon which binds NIS clients to an NIS domain
Name:		ypbind
Version:	1.37.2
Release:	5
Epoch:		3
License:	GPL
Group:		System/Servers
URL:		http://www.linux-nis.org/nis/ypbind-mt/index.html
Source0:	http://www.linux-nis.org/download/ypbind-mt/ypbind-mt-%{version}.tar.bz2

Source3:	ypbind.service
Source4:	ypbind-pre-setdomain
Source5:	ypbind-post-waitbind

# Needed for autoreconf for patch 3
Patch0:		ypbind-mt-1.37.2-automake-1.13.patch

# Fedora patches
Patch1:		ypbind-1.11-gettextdomain.patch
Patch2:		ypbind-helpman.patch
Patch3:		ypbind-systemdso.patch

Patch4:		ypbind-mt-1.32-link-tirpc.patch

Requires(post):	rpm-helper
Requires(preun): rpm-helper
Requires:	rpcbind
# yp-tools need to be fixed
# with tirpc support
#Requires:	yp-tools
%if %{?nodbus_support: 0}%{?!nodbus_support: 1}
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	dbus-glib
BuildRequires:	pkgconfig(NetworkManager)
%endif
# autoconf, automake, systemd-devel needed for patch 3
# gettext-devel also needed for /usr/bin/autopoint
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	pkgconfig(libsystemd)
BuildRequires:	pkgconfig(libtirpc)

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
%setup -q -n ypbind-mt-%{version}
%autopatch -p1

%build
# autoreconf needed for patch 3
autoreconf -fi
%configure --sbindir=/sbin %{?nodbus_support}
%make

%install
%makeinstall sbindir=%{buildroot}/sbin

mkdir -p %{buildroot}%{_sysconfdir}
install -m 644 etc/yp.conf %{buildroot}%{_sysconfdir}/yp.conf
mkdir -p %{buildroot}/var/yp/binding

mkdir -p %{buildroot}%{_unitdir}
install -m 644 %{SOURCE3} %{buildroot}%{_unitdir}/ypbind.service
mkdir -p %{buildroot}%{scripts_path}
install -m 755 %{SOURCE4} %{buildroot}%{scripts_path}/ypbind-pre-setdomain
install -m 755 %{SOURCE5} %{buildroot}%{scripts_path}/ypbind-post-waitbind

%find_lang %{name}

%post
%_post_service %{name}

%preun
%_preun_service %{name}

%files -f %{name}.lang
%attr(755, root, root) /sbin/%{name}
%{_mandir}/*/*
%{_unitdir}/%{name}.service
%{scripts_path}/*
%config(noreplace) %{_sysconfdir}/yp.conf
%dir /var/yp/binding
%doc README ChangeLog AUTHORS THANKS NEWS
