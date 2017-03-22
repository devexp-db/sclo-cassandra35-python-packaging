%global pypi_name packaging

Name:           python-%{pypi_name}
Version:        16.8
Release:        2%{?dist}
Summary:        Core utilities for Python packages

License:        BSD or ASL 2.0
URL:            https://github.com/pypa/packaging
Source0:        https://files.pythonhosted.org/packages/source/p/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

# Dependencies with different names in Fedora and Epel7
%if 0%{?fedora}
BuildRequires:  python2-setuptools
BuildRequires:  python2-devel
BuildRequires:  python2-pytest
BuildRequires:  python2-pyparsing
%else
BuildRequires:  python-setuptools
BuildRequires:  python-devel
BuildRequires:  pytest
BuildRequires:  pyparsing
BuildRequires:  python-sphinx
%endif

BuildRequires:  python-pretend
BuildRequires:  python-six

# Build Python 3 subpackage only for Fedora
%if 0%{?fedora}
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-pytest
BuildRequires:  python%{python3_pkgversion}-pretend
BuildRequires:  python%{python3_pkgversion}-pyparsing
BuildRequires:  python%{python3_pkgversion}-six
BuildRequires:  python%{python3_pkgversion}-sphinx
%endif

%description
python-packaging provides core utilities for Python packages like utilities for
dealing with versions, specifiers, markers etc.

%package -n python2-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{pypi_name}}

%if 0%{?fedora}
Requires:       python2-pyparsing
%else
Requires:       pyparsing
%endif

Requires:       python-six

%description -n python2-%{pypi_name}
python2-packaging provides core utilities for Python packages like utilities for
dealing with versions, specifiers, markers etc.

%if 0%{?fedora}
%package -n python%{python3_pkgversion}-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{pypi_name}}
 
Requires:       python%{python3_pkgversion}-pyparsing
Requires:       python%{python3_pkgversion}-six
%description -n python%{python3_pkgversion}-%{pypi_name}
python3-packaging provides core utilities for Python packages like utilities for
dealing with versions, specifiers, markers etc.
%endif

%package -n python-%{pypi_name}-doc
Summary:        python-packaging documentation
%description -n python-%{pypi_name}-doc
Documentation for python-packaging

%prep
%autosetup -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py2_build
%if 0%{?fedora}
%py3_build
%endif

# generate html docs
%if 0%{?fedora}
sphinx-build-3 docs html
%else
sphinx-build docs html
%endif

# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}
# Do not bundle fonts
rm -rf html/_static/fonts/

%install
%py2_install
%if 0%{?fedora}
%py3_install
%endif

%check
%if 0%{?fedora}
%{__python2} -m pytest tests/
%{__python3} -m pytest tests/
%else
# Disable non-working tests in Epel7
%{__python2} -m pytest --ignore=tests/test_requirements.py tests/
%endif

%files -n python2-%{pypi_name}
%license LICENSE LICENSE.APACHE LICENSE.BSD
%doc README.rst CHANGELOG.rst CONTRIBUTING.rst
%{python2_sitelib}/%{pypi_name}/
%{python2_sitelib}/%{pypi_name}-%{version}-py%{python2_version}.egg-info

%if 0%{?fedora}
%files -n python%{python3_pkgversion}-%{pypi_name}
%license LICENSE LICENSE.APACHE LICENSE.BSD
%doc README.rst CHANGELOG.rst CONTRIBUTING.rst
%{python3_sitelib}/%{pypi_name}/
%{python3_sitelib}/%{pypi_name}-%{version}-py%{python3_version}.egg-info
%endif

%files -n python-%{pypi_name}-doc
%doc html
%license LICENSE LICENSE.APACHE LICENSE.BSD

%changelog
* Wed Mar 22 2017 Lumir Balhar <lbalhar@redhat.com> - 16.8-2
- Epel7 compatible spec/package

* Wed Nov 02 2016 Lumir Balhar <lbalhar@redhat.com> - 16.8-1
- New upstream version

* Fri Sep 16 2016 Lumir Balhar <lbalhar@redhat.com> - 16.7-1
- Initial package.
