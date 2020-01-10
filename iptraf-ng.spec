Summary:        A console-based network monitoring utility
Name:           iptraf-ng
Version:        1.1.4
Release:        4%{?dist}
Source0:        https://fedorahosted.org/releases/i/p/iptraf-ng/%{name}-%{version}.tar.gz
Source1:        iptraf-ng-logrotate.conf
URL:            https://fedorahosted.org/iptraf-ng/
License:        GPLv2+
Group:          Applications/System
BuildRequires:  ncurses-devel
Obsoletes:      iptraf < 3.1
Provides:       iptraf = 3.1
Patch01:        0001-BUGFIX-fix-Floating-point-exception-in-tcplog_flowra.patch

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

%build
make %{?_smp_mflags} V=1 CFLAGS="-g -O2 -Wall -W -std=gnu99 %{optflags}"

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} prefix=%{_prefix}

# remove everything besides the html and pictures in Documentation
find Documentation -type f | grep -v '\.html$\|\.png$\|/stylesheet' | \
     xargs rm -f

install -D -m 0644 -p %{SOURCE1} %{buildroot}%{_sysconfdir}/logrotate.d/iptraf-ng

install -d -m 0755 %{buildroot}%{_localstatedir}/{lock,log,lib}/iptraf-ng

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc CHANGES FAQ LICENSE README* RELEASE-NOTES
%doc Documentation
%{_sbindir}/iptraf-ng
%{_sbindir}/rvnamed-ng
%{_mandir}/man8/iptraf-ng.8*
%{_mandir}/man8/rvnamed-ng.8*
%{_localstatedir}/lock/iptraf-ng
%{_localstatedir}/log/iptraf-ng
%{_localstatedir}/lib/iptraf-ng
%config(noreplace) %{_sysconfdir}/logrotate.d/iptraf-ng

%changelog
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

* Mon Jan 16 2011 Nikola Pajkovsky <npajkovs@redhat.com> - 1.1.0-2
- fix wrongly used execl

* Wed Jan 11 2011 Nikola Pajkovsky <npajkovs@redhat.com> - 1.1.0-1
- Initialization build
