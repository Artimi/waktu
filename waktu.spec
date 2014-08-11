Name:		waktu
Version:	0.1
Release:	alpha1
Summary:	Waktu is time tracking application that automatically watch application you have focus on

License:	MIT
URL:		http://github.com/Artimi/waktu
Source0:	dist/%{name}-%{version}-%{release}.tar.gz

BuildArch:  noarch

BuildRequires:	python2-devel

Requires: gobject-introspection
Requires: gtk3
Requires: libwnck3
Requires: pygobject3-base
Requires: libnotify
Requires: python-matplotlib


%description
Waktu is time tracking application that automatically watch application you have focus on

%prep
%setup -q -n %{name}-%{version}-%{release}


%build
python2 ./setup.py build


%install
rm -rf $RPM_BUILD_ROOT
python ./setup.py install -O2 --root=$RPM_BUILD_ROOT --record=%{name}.files
rm -rf $RPM_BUILD_ROOT/%{_docdir}/waktu
desktop-file-install $RPM_BUILD_ROOT/%{_datadir}/applications/waktu.desktop \
  --dir=$RPM_BUILD_ROOT/%{_datadir}/applications \
  --add-category X-Fedora \
  --delete-original


%clean
rm -rf $RPM_BUILD_ROOT

%files
#%defattr(-,root,root,-)
%{_bindir}/*
%{python2_sitelib}/waktu/
%{python2_sitelib}/waktu*.egg-info
%{_datadir}/applications/*
%{_datadir}/waktu/
%{_datadir}/icons/hicolor/*
%doc README.md
%doc LICENSE
%doc AUTHORS
%doc waktu.spec


%changelog
* Sun Aug 10 2014 Martin Simon <martiin.siimon@gmail.com> - 0.1-alpha
- Reorganized infrastructure
