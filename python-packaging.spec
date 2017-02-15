%global pypi_name packaging

%global build_wheel 1

%global python2_wheelname %{pypi_name}-%{version}-py2.py3-none-any.whl
%global python3_wheelname %python2_wheelname

Name:           python-%{pypi_name}
Version:        16.8
Release:        4%{?dist}
Summary:        Core utilities for Python packages

License:        BSD or ASL 2.0
URL:            https://github.com/pypa/packaging
Source0:        https://files.pythonhosted.org/packages/source/p/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch
 
BuildRequires:  python2-setuptools
BuildRequires:  python2-devel
BuildRequires:  python2-pytest
BuildRequires:  python-pretend
BuildRequires:  python2-pyparsing
BuildRequires:  python-six
 
BuildRequires:  python3-setuptools
BuildRequires:  python3-devel
BuildRequires:  python3-pytest
BuildRequires:  python3-pretend
BuildRequires:  python3-pyparsing
BuildRequires:  python3-six
BuildRequires:  python3-sphinx

%if 0%{?build_wheel}
BuildRequires:  python2-pip
BuildRequires:  python-wheel
BuildRequires:  python%{python3_pkgversion}-pip
BuildRequires:  python%{python3_pkgversion}-wheel
%endif

%description
python-packaging provides core utilities for Python packages like utilities for
dealing with versions, specifiers, markers etc.

%package -n python2-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{pypi_name}}
 
Requires:       python2-pyparsing
Requires:       python-six
%description -n python2-%{pypi_name}
python2-packaging provides core utilities for Python packages like utilities for
dealing with versions, specifiers, markers etc.


%package -n python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}
 
Requires:       python3-pyparsing
Requires:       python3-six
%description -n python3-%{pypi_name}
python3-packaging provides core utilities for Python packages like utilities for
dealing with versions, specifiers, markers etc.

%package -n python-%{pypi_name}-doc
Summary:        python-packaging documentation
Suggests:       python3-%{pypi_name} = %{version}-%{release}
%description -n python-%{pypi_name}-doc
Documentation for python-packaging

%prep
%autosetup -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%if 0%{?build_wheel}
%py2_build_wheel
%else
%py2_build
%endif
%if 0%{?build_wheel}
%py3_build_wheel
%else
%py3_build
%endif
# generate html docs 
sphinx-build-3 docs html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}
# Do not bundle fonts
rm -rf html/_static/fonts/

%install
%if 0%{?build_wheel}
%py2_install_wheel %{python2_wheelname}
%else
%py2_install
%endif
%if 0%{?build_wheel}
%py3_install_wheel %{python3_wheelname}
%else
%py3_install
%endif

%check
%{__python2} -m pytest tests/
%{__python3} -m pytest tests/

%files -n python2-%{pypi_name}
%license LICENSE LICENSE.APACHE LICENSE.BSD
%doc README.rst CHANGELOG.rst CONTRIBUTING.rst
%{python2_sitelib}/%{pypi_name}/
%{python2_sitelib}/%{pypi_name}-*.dist-info/

%files -n python3-%{pypi_name}
%license LICENSE LICENSE.APACHE LICENSE.BSD
%doc README.rst CHANGELOG.rst CONTRIBUTING.rst
%{python3_sitelib}/%{pypi_name}/
%{python3_sitelib}/%{pypi_name}-*.dist-info/

%files -n python-%{pypi_name}-doc
%doc html
%license LICENSE LICENSE.APACHE LICENSE.BSD

%changelog
* Mon Feb 13 2017 Charalampos Stratakis <cstratak@redhat.com> - 16.8-4
- Rebuild as wheel

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 16.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 16.8-2
- Rebuild for Python 3.6

* Wed Nov 02 2016 Lumir Balhar <lbalhar@redhat.com> - 16.8-1
- New upstream version

* Fri Sep 16 2016 Lumir Balhar <lbalhar@redhat.com> - 16.7-1
- Initial package.
