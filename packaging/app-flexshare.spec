
Name: app-flexshare
Epoch: 1
Version: 2.4.10
Release: 1%{dist}
Summary: Flexshare
License: GPLv3
Group: ClearOS/Apps
Source: %{name}-%{version}.tar.gz
Buildarch: noarch
Requires: %{name}-core = 1:%{version}-%{release}
Requires: app-base
Requires: app-certificate-manager

%description
Flexshares are flexible share resources that allow an administrator to quickly and easily define data sharing, collaboration and access areas via web, file, and FTP.

%package core
Summary: Flexshare - Core
License: LGPLv3
Group: ClearOS/Libraries
Requires: app-base-core
Requires: app-mode-core
Requires: app-network-core
Requires: app-storage-core >= 1:1.4.7
Requires: app-certificate-manager-core >= 1:2.3.25
Requires: app-tasks-core
Requires: clearos-base >= 7.0.1

%description core
Flexshares are flexible share resources that allow an administrator to quickly and easily define data sharing, collaboration and access areas via web, file, and FTP.

This package provides the core API and libraries.

%prep
%setup -q
%build

%install
mkdir -p -m 755 %{buildroot}/usr/clearos/apps/flexshare
cp -r * %{buildroot}/usr/clearos/apps/flexshare/

install -d -m 0755 %{buildroot}/etc/clearos/flexshare.d
install -d -m 0755 %{buildroot}/var/clearos/flexshare
install -d -m 0755 %{buildroot}/var/clearos/flexshare/backup
install -d -m 0755 %{buildroot}/var/flexshare
install -d -m 0755 %{buildroot}/var/flexshare/shares
install -D -m 0644 packaging/app-flexshare.cron %{buildroot}/etc/cron.d/app-flexshare
install -D -m 0755 packaging/flexshare %{buildroot}/usr/sbin/flexshare
install -D -m 0600 packaging/flexshare.conf %{buildroot}/etc/clearos/flexshare.conf
install -D -m 0644 packaging/flexshare_default.conf %{buildroot}/etc/clearos/storage.d/flexshare_default.conf
install -D -m 0755 packaging/network-configuration-event %{buildroot}/var/clearos/events/network_configuration/flexshare
install -D -m 0755 packaging/updateflexperms %{buildroot}/usr/sbin/updateflexperms

%post
logger -p local6.notice -t installer 'app-flexshare - installing'

%post core
logger -p local6.notice -t installer 'app-flexshare-core - installing'

if [ $1 -eq 1 ]; then
    [ -x /usr/clearos/apps/flexshare/deploy/install ] && /usr/clearos/apps/flexshare/deploy/install
fi

[ -x /usr/clearos/apps/flexshare/deploy/upgrade ] && /usr/clearos/apps/flexshare/deploy/upgrade

exit 0

%preun
if [ $1 -eq 0 ]; then
    logger -p local6.notice -t installer 'app-flexshare - uninstalling'
fi

%preun core
if [ $1 -eq 0 ]; then
    logger -p local6.notice -t installer 'app-flexshare-core - uninstalling'
    [ -x /usr/clearos/apps/flexshare/deploy/uninstall ] && /usr/clearos/apps/flexshare/deploy/uninstall
fi

exit 0

%files
%defattr(-,root,root)
/usr/clearos/apps/flexshare/controllers
/usr/clearos/apps/flexshare/htdocs
/usr/clearos/apps/flexshare/views

%files core
%defattr(-,root,root)
%exclude /usr/clearos/apps/flexshare/packaging
%exclude /usr/clearos/apps/flexshare/unify.json
%dir /usr/clearos/apps/flexshare
%dir /etc/clearos/flexshare.d
%dir /var/clearos/flexshare
%dir /var/clearos/flexshare/backup
%dir /var/flexshare
%dir /var/flexshare/shares
/usr/clearos/apps/flexshare/deploy
/usr/clearos/apps/flexshare/language
/usr/clearos/apps/flexshare/libraries
%config(noreplace) /etc/cron.d/app-flexshare
/usr/sbin/flexshare
%config(noreplace) /etc/clearos/flexshare.conf
/etc/clearos/storage.d/flexshare_default.conf
/var/clearos/events/network_configuration/flexshare
/usr/sbin/updateflexperms
