Name:                HdrHistogram
Version:             2.1.12
Release:             1
Summary:             A High Dynamic Range (HDR) Histogram
License:             Public Domain and BSD and CC0
URL:                 http://hdrhistogram.github.io/%{name}/
Source0:             https://github.com/%{name}/%{name}/archive/%{name}-%{version}.tar.gz
Source1:             xmvn-reactor
BuildRequires:       maven-local 
BuildRequires:       java-1.8.0-openjdk-devel maven
Requires:            javapackages-tools
Requires:            java-1.8.0-openjdk
BuildArch:           noarch
%description
HdrHistogram supports the recording and analyzing sampled data value
counts across a configurable integer value range with configurable value
precision within the range. Value precision is expressed as the number of
significant digits in the value recording, and provides control over value
quantization behavior across the value range and the subsequent value
resolution at any given level.

%package javadoc
Summary:             Javadoc for %{name}
%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n %{name}-%{name}-%{version}
find  -name "*.class"  -print -delete
find  -name "*.jar"  -print -delete
sed -i 's/1.4.0/1.5.0/g' pom.xml
cp %{SOURCE1} ./.xmvn-reactor
echo `pwd` > absolute_prefix.log
sed -i 's/\//\\\//g' absolute_prefix.log
absolute_prefix=`head -n 1 absolute_prefix.log`
sed -i 's/absolute-prefix/'"$absolute_prefix"'/g' .xmvn-reactor
%pom_remove_plugin :maven-dependency-plugin
%pom_remove_plugin :maven-release-plugin
%pom_remove_plugin :maven-source-plugin
%pom_remove_plugin :nexus-staging-maven-plugin
%pom_remove_plugin :maven-gpg-plugin

%pom_xpath_set "pom:plugin[pom:groupId = 'com.google.code.maven-replacer-plugin' ]/pom:artifactId" replacer
%mvn_file :%{name} %{name}

%build
mvn -DskipTests -DskipIT package

%install
%mvn_install
install -d -m 0755 %{buildroot}/%{_javadocdir}/HdrHistogram
install -m 0755 target/HdrHistogram-2.1.12-javadoc.jar %{buildroot}/%{_javadocdir}/HdrHistogram
%jpackage_script org.%{name}.HistogramLogProcessor "" "" %{name} HistogramLogProcessor true

%files -f .mfiles
%{_bindir}/HistogramLogProcessor
%doc README.md
%license COPYING.txt LICENSE.txt

%files javadoc 
%{_javadocdir}/HdrHistogram
%license COPYING.txt LICENSE.txt

%changelog
* Wed Dec 29 2021 Ge Wang <wangge20@huawei.com> - 2.1.12-1
- update to version 2.1.12

* Thu Jul 30 2020 wangyue <wangyue92@huawei.com> - 2.1.11-1
- package init
