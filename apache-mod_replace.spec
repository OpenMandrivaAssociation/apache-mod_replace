#Module-Specific definitions
%define mod_name mod_replace
%define mod_conf A45_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Replace text strings based on regular expressions
Name:		apache-%{mod_name}
Version:	0.1.0
Release:	14
Group:		System/Servers
License:	BSD
URL:		http://mod-replace.sourceforge.net/
Source0:	http://prdownloads.sourceforge.net/mod-replace/%{mod_name}-%{version}.tar.bz2
Source1:	%{mod_conf}.bz2
Source2:	docs.html.bz2
Source3:	faq.html.bz2
# http://sourceforge.net/tracker/index.php?func=detail&aid=1110387&group_id=107152&atid=646835
Patch0:		mod_replace.c.diff
Patch1:		mod_replace-0.1.0-apache220.diff
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):  apache-conf >= 2.2.0
Requires(pre):  apache >= 2.2.0
Requires:       apache-conf >= 2.2.0
Requires:       apache >= 2.2.0
BuildRequires:  apache-devel >= 2.2.0
BuildRequires:	file

%description
mod_replace is an Apache 2.0.x filter module that allows you to
replace text strings based on regular expressions. Most commonly
it is used together with mod_proxy to sanitize the behaviour of
ill behaving web applications / servers when using Apache as an
reverse proxy. Other uses are, of course, supported as well. It
has been tested on Solaris 8/Sparc and Linux/i386 with various
versions of Apache 2.0.x (development started with 2.0.44, tested
with all releases up to 2.0.49). Although it has only been tested
on those two platforms, this doesn´t mean it won´t work for
others. Any reports of successfull or unsuccessfull deployment is
more than welcome!

%prep

%setup -q -n %{mod_name}-%{version}
%patch0 -p0
%patch1 -p0

bzcat %{SOURCE2} > docs.html
bzcat %{SOURCE3} > faq.html

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

%build

%{_bindir}/apxs -c mod_replace.c

%install

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
bzcat %{SOURCE1} > %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

install -d %{buildroot}/var/www/html/addon-modules
ln -s ../../../..%{_docdir}/%{name}-%{version} %{buildroot}/var/www/html/addon-modules/%{name}-%{version}

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
    fi
fi

%clean

%files
%doc INSTALL LICENSE README docs.html faq.html
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}
/var/www/html/addon-modules/*




%changelog
* Sat Feb 11 2012 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-14mdv2012.0
+ Revision: 772752
- rebuild

* Tue May 24 2011 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-13
+ Revision: 678406
- mass rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-12mdv2011.0
+ Revision: 588052
- rebuild

* Mon Mar 08 2010 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-11mdv2010.1
+ Revision: 516168
- rebuilt for apache-2.2.15

* Sat Aug 01 2009 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-10mdv2010.0
+ Revision: 406639
- rebuild

* Tue Jan 06 2009 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-9mdv2009.1
+ Revision: 326226
- rebuild

* Mon Jul 14 2008 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-8mdv2009.0
+ Revision: 235074
- rebuild

* Thu Jun 05 2008 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-7mdv2009.0
+ Revision: 215625
- fix rebuild

* Fri Mar 07 2008 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-6mdv2008.1
+ Revision: 181850
- rebuild

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Fri Dec 14 2007 Thierry Vignaud <tv@mandriva.org> 0.1.0-5mdv2008.1
+ Revision: 119822
- rebuild b/c of missing package on ia32

* Sat Sep 08 2007 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-4mdv2008.0
+ Revision: 82664
- rebuild


* Sat Mar 10 2007 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-3mdv2007.1
+ Revision: 140733
- rebuild

* Thu Nov 09 2006 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-2mdv2007.1
+ Revision: 79491
- Import apache-mod_replace

* Mon Aug 07 2006 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-2mdv2007.0
- rebuild

* Wed Dec 21 2005 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-1mdk
- initial Mandriva package
- added P0,P1 to make it compile
- added the docs (S2,S3)

