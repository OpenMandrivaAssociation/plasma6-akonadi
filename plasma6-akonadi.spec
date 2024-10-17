# Use mariadb instead of sqlite
%bcond_with mariadb

#define git 20240217
%define gitbranch release/24.02
%define gitbranchd %(echo %{gitbranch} |sed -e 's,/,-,g')

Summary:	An extensible cross-desktop storage service for PIM
Name:		plasma6-akonadi
Version:	24.08.2
Release:	1
License:	LGPLv2+
Group:		Networking/WWW
Url:		https://pim.kde.org/akonadi/
%if 0%{?git:1}
Source0:	https://invent.kde.org/pim/akonadi/-/archive/%{gitbranch}/akonadi-%{gitbranchd}.tar.bz2
%else
%define stable %([ "`echo %{version} |cut -d. -f3`" -ge 70 ] && echo -n un; echo -n stable)
Source0:	http://download.kde.org/%{stable}/release-service/%{version}/src/akonadi-%{version}.tar.xz
%endif
BuildRequires:	libxml2-utils
BuildRequires:	shared-mime-info >= 0.20
BuildRequires:	xsltproc
BuildRequires:	boost-devel
#BuildRequires:	pkgconfig(soprano)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(libxslt)
BuildRequires:	cmake(ECM)
BuildRequires:	cmake(Qt6)
BuildRequires:	cmake(Qt6Core)
BuildRequires:	cmake(Qt6Gui)
BuildRequires:	cmake(Qt6Widgets)
BuildRequires:	cmake(Qt6Sql)
BuildRequires:	cmake(Qt6Network)
BuildRequires:	cmake(Qt6Xml)
BuildRequires:	cmake(Qt6DBus)
BuildRequires:	cmake(Qt6Test)
BuildRequires:	cmake(Qt6UiPlugin)
BuildRequires:	cmake(Qt6Designer)
BuildRequires:	cmake(SharedMimeInfo)
BuildRequires:	cmake(KF6ItemViews)
BuildRequires:	cmake(KF6KIO)
BuildRequires:	cmake(KF6Config)
BuildRequires:	cmake(KF6I18n)
BuildRequires:	cmake(KF6DBusAddons)
BuildRequires:	cmake(KF6ItemModels)
BuildRequires:	cmake(KF6GuiAddons)
BuildRequires:	cmake(KF6IconThemes)
# FIXME why doesn't this have a cmake(KF6IconWidgets) provide?
BuildRequires:	%mklibname KF6IconWidgets -d 
BuildRequires:	cmake(KF6WindowSystem)
BuildRequires:	cmake(KF6Completion)
BuildRequires:	cmake(KF6Crash)
BuildRequires:	cmake(KF6XmlGui)
BuildRequires:	cmake(Backtrace)
BuildRequires:	cmake(LibXml2)
BuildRequires:	cmake(Gettext)
BuildRequires:	cmake(PythonInterp)
BuildRequires:	boost-devel
BuildRequires:	cmake(SharedMimeInfo)
BuildRequires:	cmake(LibXslt)
BuildRequires:	cmake(KAccounts6)
BuildRequires:	pkgconfig(libaccounts-glib)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(mariadb)
BuildRequires:	pkgconfig(libpq)
# Just to make sure CMake can find it
BuildRequires:	postgresql-server
%if %{with mariadb}
Requires:	mariadb-common
# (tpg) needed for mysqld
Requires:	mariadb-server
# Needed for mysqlcheck  which is used in akonadi
Requires:	mariadb-client
Requires:	qt6-qtbase-sql-mysql
%else
Requires:	qt6-qtbase-sql-sqlite
%endif
# For QCH format docs
BuildRequires: doxygen

%description
An extensible cross-desktop storage service for PIM data and meta data
providing concurrent read, write, and query access.

%files -f akonadi.lang
%{_bindir}/*
%{_sysconfdir}/xdg/akonadi
%{_datadir}/dbus-1/services/*
%{_datadir}/mime/packages/akonadi-mime.xml
%{_datadir}/akonadi
%{_datadir}/config.kcfg/resourcebase.kcfg
%{_datadir}/icons/*/*/*/akonadi.*
%{_sysconfdir}/apparmor.d/*
%{_datadir}/qlogging-categories6/akonadi.categories
%{_datadir}/qlogging-categories6/akonadi.renamecategories
%{_datadir}/kf6/akonadi
%{_datadir}/kf6/akonadi_knut_resource
%dir %{_qtdir}/plugins/pim6
%dir %{_qtdir}/plugins/pim6/akonadi
%{_qtdir}/plugins/pim6/akonadi/akonadi_test_searchplugin.so

#------------------------------------------------------
# FIXME why does this fail to build on armv7hnl even though all
# dependencies are there?
%ifnarch %{arm}

%package -n qt6-designer-plugin-akonadiwidgets
Summary: Akonadi Widgets for Qt Designer
Group: Development/KDE and Qt

%description -n qt6-designer-plugin-akonadiwidgets
Akonadi Widgets for Qt Designer

%files -n qt6-designer-plugin-akonadiwidgets
%{_qtdir}/plugins/designer/akonadi6widgets.so
%endif

#------------------------------------------------------

%libpackage KPim6AkonadiAgentBase 6

%libpackage KPim6AkonadiCore 6

%libpackage KPim6AkonadiWidgets 6

%libpackage KPim6AkonadiXml 6

%libpackage KPim6AkonadiPrivate 6

#------------------------------------------------------

%package devel
Summary:	Devel stuff for %{name}
Group:		Development/KDE and Qt
Requires:	%{mklibname KPim6AkonadiAgentBase} = %{EVRD}
Requires:	%{mklibname KPim6AkonadiCore} = %{EVRD}
Requires:	%{mklibname KPim6AkonadiWidgets} = %{EVRD}
Requires:	%{mklibname KPim6AkonadiXml} = %{EVRD}
Requires:	%{mklibname KPim6AkonadiPrivate} = %{EVRD}
Requires:	%{name} = %{EVRD}
Requires:	boost-devel

%description devel
This package contains header files needed if you wish to build applications
based on %{name}

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/cmake/KPim6Akonadi
%{_datadir}/dbus-1/interfaces/*.xml
%{_datadir}/kdevappwizard/templates/*

#--------------------------------------------------------------------

%prep
%autosetup -p1 -n akonadi-%{?git:%{gitbranchd}}%{!?git:%{version}}
%cmake \
%if ! %{with mariadb}
	-DDATABASE_BACKEND=SQLITE \
%endif
	-DMYSQLD_EXECUTABLE=%{_sbindir}/mysqld \
	-DKDE_INSTALL_USE_QT_SYS_PATHS:BOOL=ON \
	-G Ninja

%build
%ninja -v -C build

%install
%ninja_install -C build

%find_lang libakonadi6
%find_lang akonadi_knut_resource
%find_lang akonadi-db-migrator
cat *.lang >akonadi.lang
