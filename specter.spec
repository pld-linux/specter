Summary:	Userspace logging facility for Linux
Summary(pl.UTF-8):	Demon logujący w trybie użytkownika dla iptables
Name:		specter
Version:	1.4
Release:	1
License:	GPL
Group:		Networking/Daemons
Source0:	http://joker.linuxstuff.pl/specter/%{name}-%{version}.tar.gz
# Source0-md5:	24c93d7539b8d7485848b21430702965
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}.logrotate
Patch0:		%{name}-limits.patch
URL:		http://joker.linuxstuff.pl/specter/
BuildRequires:	mysql-devel
BuildRequires:	postgresql-devel
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post):	fileutils
Requires(post,preun):	/sbin/chkconfig
Requires:	iptables
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
specter is a userspace logging facility for Linux. It uses netfilter
ULOG target for packets gathering, and then passes them to attached
plugins. Modularized structure makes specter very flexible and robust.
It's based on ulogd, but has improved design and wider functionality.

Install it if you want to easily gather and manage your net traffic
logs among different formats (plain text, MySQL/PostgreSQL databases,
etc..).

%description -l pl.UTF-8
specter jest demonem do logowania pakietów. Wykorzystuje cel
netfiltra ULOG do zbierania pakietów, następnie przekazuje je do
załączonych wtyczek. Dzięki modularnej strukturze specter jest
bardzo sprawny i potężny. Bazuje na ulogd, ale ma wiele zmian i
szerszą funkcjonalność.

Zainstaluj jeżeli potrzebujesz prostego zbierania i zarządzania
logami z sieci w różnych formatach (czysty tekst, bazy
MySQL/PostgreSQL, itp).

%package mysql
Summary:	MySQL plugin for specter
Summary(pl.UTF-8):	Wtyczka MySQL dla specter
Group:		Networking/Daemons

%description mysql
MySQL plugin for specter.

%description mysql -l pl.UTF-8
Wtyczka MySQL dla specter. #
%package pgsql
Summary:	PostgreSQL plugin for specter
Summary(pl.UTF-8):	Wtyczka PostgreSQL dla specter
Group:		Networking/Daemons

%description pgsql
PostgreSQL plugin for specter.

%description pgsql -l pl.UTF-8
Wtyczka PostgreSQL dla specter.

%prep
%setup -q
%patch0 -p1

%build
%configure \
	--with-mysql \
	--with-pgsql
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},/etc/{sysconfig,logrotate.d,rc.d/init.d,specter}} \
	$RPM_BUILD_ROOT/var/log

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/specter
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/specter
install %{SOURCE3} $RPM_BUILD_ROOT/etc/logrotate.d/specter

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add specter
%service specter restart "specter daemon"

%preun
if [ "$1" = "0" ]; then
	%service specter stop
	/sbin/chkconfig --del specter
fi

%files
%defattr(644,root,root,755)
%doc README doc/*.{txt,html}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/specter
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/specter.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/specter
%attr(750,root,root) %dir %{_sysconfdir}/specter
%attr(754,root,root) /etc/rc.d/init.d/specter
#
%attr(755,root,root) %{_sbindir}/*
%dir %{_libdir}/specter
%attr(755,root,root) %{_libdir}/specter/specter_[BLOHES]*.so
%attr(755,root,root) %{_libdir}/specter/specter_PCAP*.so
%attr(755,root,root) %{_libdir}/specter/specter_PWSNIFF*.so
#
#%attr(640,root,root) %ghost /var/log/*
%{_mandir}/man?/%{name}.*

%files mysql
%defattr(644,root,root,755)
%doc doc/mysql.table
%attr(755,root,root) %{_libdir}/specter/specter_MYSQL.so
#
%files pgsql
%defattr(644,root,root,755)
%doc doc/pgsql.table
%attr(755,root,root) %{_libdir}/specter/specter_PGSQL.so
#
