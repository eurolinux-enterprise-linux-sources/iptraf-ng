Summary:        A console-based network monitoring utility
Name:           iptraf-ng
Version:        1.1.4
Release:        7%{?dist}
Source0:        https://github.com/iptraf-ng/iptraf-ng/archive/v%{version}.tar.gz
Source1:        %{name}-logrotate.conf
Source2:        %{name}-tmpfiles.conf
URL:            https://github.com/iptraf-ng/iptraf-ng/
License:        GPLv2+
Group:          Applications/System
BuildRequires:  gcc
BuildRequires:  ncurses-devel
Obsoletes:      iptraf < 3.1
Provides:       iptraf = 3.1
Patch01:        0001-BUGFIX-fix-Floating-point-exception-in-tcplog_flowra.patch
Patch02:        0002-Makefile-add-Werror-format-security.patch
Patch03:        0003-fix-segfault-in-adding-interface.patch

%description
IPTraf-ng is a console-based network monitoring utility.  IPTraf gathers
data like TCP connection packet and byte counts, interface statistics
and activity indicators, TCP/UDP traffic breakdowns, and LAN station
packet and byte counts.  IPTraf-ng features include an IP traffic monitor
which shows TCP flag information, packet and byte counts, ICMP
details, OSPF packet types, and oversized IP packet warnings;
interface statistics showing IP, TCP, UDP, ICMP, non-IP and other IP
packet counts, IP checksum errors, interface activity and packet size
counts; a TCP and UDP service monitor showing counts of incoming and
outgoing packets for common TCP and UDP application ports, a LAN
statistics module that discovers active hosts and displays statistics
about their activity; TCP, UDP and other protocol display filters so
you can view just the traffic you want; logging; support for Ethernet,
FDDI, ISDN, SLIP, PPP, and loopback interfaces; and utilization of the
built-in raw socket interface of the Linux kernel, so it can be used
on a wide variety of supported network cards.

%prep
%setup -q
%patch01 -p1
%patch02 -p1
%patch03 -p1

%build
make %{?_smp_mflags} V=1 CFLAGS="-g -O2 -Wall -W -std=gnu99 -Werror=format-security %{optflags}"

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} prefix=%{_prefix}

# remove everything besides the html and pictures in Documentation
find Documentation -type f | grep -v '\.html$\|\.png$\|/stylesheet' | \
     xargs rm -f

install -D -m 0644 -p %{SOURCE1} %{buildroot}%{_sysconfdir}/logrotate.d/iptraf-ng

install -d -m 0755 %{buildroot}%{_localstatedir}/{log,lib}/iptraf-ng

mkdir -p %{buildroot}%{_prefix}/lib/tmpfiles.d
install -m 0644 %{SOURCE2} %{buildroot}%{_prefix}/lib/tmpfiles.d/%{name}.conf

mkdir -p %{buildroot}/run
install -d -m 0755 %{buildroot}/run/%{name}/

%files
%defattr(-,root,root,-)
%doc CHANGES FAQ LICENSE README* RELEASE-NOTES
%doc Documentation
%{_sbindir}/iptraf-ng
%{_sbindir}/rvnamed-ng
%{_mandir}/man8/iptraf-ng.8*
%{_mandir}/man8/rvnamed-ng.8*
%{_localstatedir}/log/iptraf-ng
%{_localstatedir}/lib/iptraf-ng
%config(noreplace) %{_sysconfdir}/logrotate.d/iptraf-ng
%dir /run/%{name}/
%{_prefix}/lib/tmpfiles.d/%{name}.conf

%changelog
* Mon Apr 09 2018 Phil Cameron <pcameron@redhat.com> - 1.1.4-7
- Fixes error in patch Patch03 - this fixes 1283773 and 1539081
  1501821 - Upstream moved to https://github.com/iptraf-ng/iptraf-ng/
  1020552, 1372679 - fix missing /var/lock/iptraf-ng file
  Add BuildRequires:  gcc to spec file.
  1109768 - bad configuration logrotate

* Fri Apr 15 2016 Phil Cameron <pcameron@redhat.com> - 1.1.4-6
- fix 1283773 - segfault in rate_add_rate

  Jun 17 2014 Alejandro Pérez  <aeperezt@fedoraproject.org>
  fix 1109768 bad configuration logrotate
  Mar 02 2014 Alejandro Pérez  <aeperezt@fedoraproject.org>
  fix bug 1020552 - rpm report /var/lock/ipraf-ng is missing
  added missing file iptraf-nf-tmpfiles.conf
  Dec 03 2013 Nikola Pajkovsky <npajkovs@redhat.com>
  Fedora start using -Werror=format-security and iptraf-ng had some
  parts where error compilation was trigged.
  202b2e7b27a1 Makefile: add -Werror=format-security
  Resolved: #1037133

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 1.1.4-4
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.1.4-3
- Mass rebuild 2013-12-27

* Mon Sep 02 2013 Nikola Pajkovsky <npajkovs@redhat.com> - 1.1.4-2
- 9b32013 BUGFIX: fix "Floating point exception" in tcplog_flowrate_msg() (Vitezslav Samel)

* Tue Jul 23 2013 Nikola Pajkovsky <npajkovs@redhat.com> - 1.1.4
- new upstream iptraf-ng-1.1.4

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu May 24 2012 Nikola Pajkovsky <npajkovs@redhat.com> - 1.1.3.1-2
- append standard CFLAGS

* Wed May 23 2012 Nikola Pajkovsky <npajkovs@redhat.com> - 1.1.3.1-1
- new upstream iptraf-ng-1.1.3.1-1

* Fri May 04 2012 Nikola Pajkovsky <npajkovs@redhat.com> - 1.1.2-1
- new upstream iptraf-ng-1.1.2-1

* Fri Apr 27 2012 Nikola Pajkovsky <npajkovs@redhat.com> - 1.1.2.rc0-1
- new upstream iptraf-ng-1.1.2.rc0-1

* Thu Feb 02 2012 Nikola Pajkovsky <npajkovs@redhat.com> - 1.1.1-1
- new upstream iptraf-ng-1.1.1

* Sun Jan 16 2011 Nikola Pajkovsky <npajkovs@redhat.com> - 1.1.0-2
- fix wrongly used execl

* Tue Jan 11 2011 Nikola Pajkovsky <npajkovs@redhat.com> - 1.1.0-1
- Initialization build
