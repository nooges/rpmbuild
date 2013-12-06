# used for CVS snapshots:
%define CVSDATE %{nil}
%define WITH_SELINUX 1
%define desktop_file 1
%if %{desktop_file}
%define desktop_file_utils_version 0.2.93
%endif

%define withnetbeans 0

%define withcvim 0

%define withvimspell 0

%define baseversion 7.4
#used for pre-releases:
%define beta %{nil}
%define vimdir vim74%{?beta}
%define patchlevel 110

Summary: The VIM editor.
Name: vim
Version: %{baseversion}.%{beta}%{patchlevel}
Release: 1%{?dist}
License: freeware
Group: Applications/Editors
#Source0: ftp://ftp.vim.org/pub/vim/unix/vim-%{baseversion}%{?beta}%{?CVSDATE}.tar.bz2
#Source1: ftp://ftp.vim.org/pub/vim/extra/vim-%{baseversion}%{?beta}-lang%{?CVSDATE}.tar.gz
#Source2: ftp://ftp.vim.org/pub/vim/extra/vim-%{baseversion}%{?beta}-extra%{?CVSDATE}.tar.gz
Source3: gvim.desktop
Source4: vimrc
#Source5: ftp://ftp.vim.org/pub/vim/patches/README.patches
#Source6: spec.vim
Source7: gvim16.png
Source8: gvim32.png
Source9: gvim48.png
Source10: gvim64.png
#Source11: Changelog.rpm
#Source12: vi-help.txt
# Source at http://www.vim.org/scripts/script.php?script_id=213 :
#Source12: cvim.zip
#Source13: runtime-update-20060911.tar.bz2
%if %{withvimspell}
Source14: vim-spell-files.tar.bz2
%endif

Buildroot: %{_tmppath}/%{name}-%{version}-root
Buildrequires: python-devel perl libtermcap-devel gettext
Buildrequires: libacl-devel gpm-devel autoconf
%if %{WITH_SELINUX}
Buildrequires: libselinux-devel
%endif
%if %{desktop_file}
Requires: /usr/bin/desktop-file-install
Buildrequires: desktop-file-utils >= %{desktop_file_utils_version}
%endif
Epoch: 2

%description
VIM (VIsual editor iMproved) is an updated and improved version of the
vi editor.  Vi was the first real screen-based editor for UNIX, and is
still very popular.  VIM improves on vi by adding new features:
multiple windows, multi-level undo, block highlighting and more.

%package common
Summary: The common files needed by any version of the VIM editor.
Group: Applications/Editors
Obsoletes: vim7-common
Conflicts: man-pages-fr < 0.9.7-14
Conflicts: man-pages-it < 0.3.0-17
Conflicts: man-pages-pl < 0.24-2

%description common
VIM (VIsual editor iMproved) is an updated and improved version of the
vi editor.  Vi was the first real screen-based editor for UNIX, and is
still very popular.  VIM improves on vi by adding new features:
multiple windows, multi-level undo, block highlighting and more.  The
vim-common package contains files which every VIM binary will need in
order to run.

If you are installing vim-enhanced or vim-X11, you'll also need
to install the vim-common package.

%package spell
Summary: The dictionaries for spell checking. This package is optional.
Group: Applications/Editors
Requires: vim-common = %{epoch}:%{version}-%{release}

%description spell
This subpackage contains dictionaries for vim spell checking in
many different languages.

%package minimal
Summary: A minimal version of the VIM editor.
Group: Applications/Editors
Obsoletes: vim
Obsoletes: vim7-minimal

%description minimal
VIM (VIsual editor iMproved) is an updated and improved version of the
vi editor.  Vi was the first real screen-based editor for UNIX, and is
still very popular.  VIM improves on vi by adding new features:
multiple windows, multi-level undo, block highlighting and more. The
vim-minimal package includes a minimal version of VIM, which is
installed into /bin/vi for use when only the root partition is
present. NOTE: The online help is only available when the vim-common
package is installed.

%package enhanced
Summary: A version of the VIM editor which includes recent enhancements.
Group: Applications/Editors
Requires: vim-common = %{epoch}:%{version}-%{release}
BuildRequires: ncurses-devel
Obsoletes: vim-color
Obsoletes: vim7-enhanced

%description enhanced
VIM (VIsual editor iMproved) is an updated and improved version of the
vi editor.  Vi was the first real screen-based editor for UNIX, and is
still very popular.  VIM improves on vi by adding new features:
multiple windows, multi-level undo, block highlighting and more.  The
vim-enhanced package contains a version of VIM with extra, recently
introduced features like Python and Perl interpreters.

Install the vim-enhanced package if you'd like to use a version of the
VIM editor which includes recently added enhancements like
interpreters for the Python and Perl scripting languages.  You'll also
need to install the vim-common package.

%package X11
Summary: The VIM version of the vi editor for the X Window System.
Group: Applications/Editors
Requires: vim-common = %{epoch}:%{version}-%{release} libattr
BuildRequires: gtk2-devel libSM-devel libXt-devel libXpm-devel
Requires(pre): gtk2 >= 2.6
Obsoletes: vim7-X11

%description X11
VIM (VIsual editor iMproved) is an updated and improved version of the
vi editor.  Vi was the first real screen-based editor for UNIX, and is
still very popular.  VIM improves on vi by adding new features:
multiple windows, multi-level undo, block highlighting and
more. VIM-X11 is a version of the VIM editor which will run within the
X Window System.  If you install this package, you can run VIM as an X
application with a full GUI interface and mouse support.

Install the vim-X11 package if you'd like to try out a version of vi
with graphics and mouse capabilities.  You'll also need to install the
vim-common package.

%prep
cp -vR ~/proj/vim/* ./
#cp -f %{SOURCE6} runtime/ftplugin/spec.vim
# fix rogue dependencies from sample code
chmod -x runtime/tools/mve.awk
perl -pi -e "s,bin/nawk,bin/awk,g" runtime/tools/mve.awk


# install spell files
%if %{withvimspell}
%{__tar} xjf %{SOURCE14}
%endif

%if "%{withcvim}" == "1"
mkdir cvim
( cd cvim; unzip %{SOURCE12}; )
patch -p1 < %{PATCH3005}
%endif


%build
cd src
autoconf

export CFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -D_FORTIFY_SOURCE=2"
export CXXFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -D_FORTIFY_SOURCE=2"

%configure --with-features=huge --enable-pythoninterp --enable-perlinterp \
  --disable-tclinterp --with-x=yes \
  --enable-xim --enable-multibyte \
  --enable-gtk2-check --enable-gui=gtk2 \
  --with-compiledby="<bugzilla@redhat.com>" --enable-cscope \
  --with-modified-by="<bugzilla@redhat.com>" \
%if "%{withnetbeans}" == "1"
  --enable-netbeans \
%else
  --disable-netbeans \
%endif

make -j
cp vim gvim
make clean

%configure --prefix=/usr --with-features=huge --enable-pythoninterp \
 --enable-perlinterp --disable-tclinterp --with-x=no \
 --enable-gui=no --exec-prefix=/usr --enable-multibyte \
 --enable-cscope --with-modified-by="<bugzilla@redhat.com>" \
 --with-compiledby="<bugzilla@redhat.com>" \
%if "%{withnetbeans}" == "1"
  --enable-netbeans \
%else
  --disable-netbeans \
%endif

make -j
cp vim enhanced-vim
make clean

#perl -pi -e "s/help.txt/vi-help.txt/"  os_unix.h ex_cmds.c
perl -pi -e "s/\/etc\/vimrc/\/etc\/virc/"  os_unix.h
%configure --prefix='${DEST}'/usr --with-features=tiny --with-x=no \
  --enable-multibyte \
  --disable-netbeans \
  --disable-pythoninterp --disable-perlinterp --disable-tclinterp \
  --with-tlib=termcap --enable-gui=no --disable-gpm --exec-prefix=/ --with-compiledby="<bugzilla@redhat.com>"

make -j

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/bin
mkdir -p $RPM_BUILD_ROOT/usr/{bin,share/vim}
#cp -f %{SOURCE5} .

%if "%{withcvim}" == "1"
# cvim plugin stuff:
mkdir -p $RPM_BUILD_ROOT%{_datadir}/vim/%{vimdir}/codesnippets-c
mkdir -p $RPM_BUILD_ROOT%{_datadir}/vim/%{vimdir}/plugin/templates
mkdir -p $RPM_BUILD_ROOT%{_datadir}/vim/%{vimdir}/wordlists
mkdir -p $RPM_BUILD_ROOT%{_datadir}/vim/%{vimdir}/rc
mkdir -p $RPM_BUILD_ROOT%{_datadir}/vim/%{vimdir}/ftplugin
   install -m644 cvim/codesnippets-c/*  $RPM_BUILD_ROOT%{_datadir}/vim/%{vimdir}/codesnippets-c/
   install -m644 cvim/plugin/templates/*  $RPM_BUILD_ROOT/%{_datadir}/vim/%{vimdir}/plugin/templates/
   install -m644 cvim/plugin/wrapper.sh  $RPM_BUILD_ROOT/%{_datadir}/vim/%{vimdir}/plugin/
   install -m644 cvim/plugin/c.vim  $RPM_BUILD_ROOT/%{_datadir}/vim/%{vimdir}/plugin/
   install -m644 cvim/plugin/templates/*  $RPM_BUILD_ROOT/%{_datadir}/vim/%{vimdir}/plugin/templates/
   install -m644 cvim/rc/*  $RPM_BUILD_ROOT/%{_datadir}/vim/%{vimdir}/rc/
   install -m644 cvim/wordlists/*  $RPM_BUILD_ROOT/%{_datadir}/vim/%{vimdir}/wordlists/
   install -m644 cvim/ftplugin/*  $RPM_BUILD_ROOT/%{_datadir}/vim/%{vimdir}/ftplugin/
   cp cvim/doc/* runtime/doc
   cp cvim/README.csupport .
%endif

cd src
%makeinstall BINDIR=/bin DESTDIR=$RPM_BUILD_ROOT
mv $RPM_BUILD_ROOT/bin/xxd $RPM_BUILD_ROOT/usr/bin/xxd
make installmacros DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/{16x16,32x32,48x48,64x64}/apps
install -m755 gvim $RPM_BUILD_ROOT/usr/bin/gvim
install -m644 %{SOURCE7} \
   $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/16x16/apps/gvim.png
install -m644 %{SOURCE8} \
   $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/32x32/apps/gvim.png
install -m644 %{SOURCE9} \
   $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/48x48/apps/gvim.png
install -m644 %{SOURCE10} \
   $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/64x64/apps/gvim.png
install -m755 enhanced-vim $RPM_BUILD_ROOT/usr/bin/vim

( cd $RPM_BUILD_ROOT
  mv ./bin/vimtutor ./usr/bin/vimtutor
  mv ./bin/vim ./bin/vi
  rm -f ./bin/rvim
  ln -sf vi ./bin/ex
  ln -sf vi ./bin/rvi
  ln -sf vi ./bin/rview
  ln -sf vi ./bin/view
  ln -sf vim ./usr/bin/ex
  ln -sf vim ./usr/bin/rvim
  ln -sf vim ./usr/bin/vimdiff
  perl -pi -e "s,$RPM_BUILD_ROOT,," .%{_mandir}/man1/vim.1 .%{_mandir}/man1/vimtutor.1
  rm -f .%{_mandir}/man1/rvim.1
  ln -sf vim.1.gz .%{_mandir}/man1/vi.1.gz
  ln -sf vim.1.gz .%{_mandir}/man1/rvi.1.gz
  ln -sf vim.1.gz .%{_mandir}/man1/rvim.1.gz
  ln -sf vim.1.gz .%{_mandir}/man1/vimdiff.1.gz
  ln -sf gvim ./usr/bin/gview
  ln -sf gvim ./usr/bin/gex
  ln -sf gvim ./usr/bin/evim
  ln -sf gvim ./usr/bin/gvimdiff
  ln -sf vim.1.gz .%{_mandir}/man1/gvim.1.gz
  ln -sf vim.1.gz .%{_mandir}/man1/gvimdiff.1.gz
  ln -sf gvim ./usr/bin/vimx
  %if "%{desktop_file}" == "1"
    mkdir -p $RPM_BUILD_ROOT/usr/share/applications
    desktop-file-install --vendor net \
        --dir $RPM_BUILD_ROOT/usr/share/applications \
        --add-category "Application;Utility;TextEditor;X-Red-Hat-Base" \
        %{SOURCE3}
  %else
    mkdir -p ./etc/X11/applnk/Applications
    cp %{SOURCE3} ./etc/X11/applnk/Applications/gvim.desktop
  %endif
  # ja_JP.ujis is obsolete, ja_JP.eucJP is recommended.
  ( cd ./usr/share/vim/%{vimdir}/lang; \
    ln -sf menu_ja_jp.ujis.vim menu_ja_jp.eucjp.vim )
)

pushd $RPM_BUILD_ROOT/usr/share/vim/%{vimdir}/tutor
mkdir conv
   iconv -f CP1252 -t UTF8 tutor.ca > conv/tutor.ca
   iconv -f CP1252 -t UTF8 tutor.it > conv/tutor.it
   #iconv -f CP1253 -t UTF8 tutor.gr > conv/tutor.gr
   iconv -f CP1252 -t UTF8 tutor.fr > conv/tutor.fr
   iconv -f CP1252 -t UTF8 tutor.es > conv/tutor.es
   iconv -f CP1252 -t UTF8 tutor.de > conv/tutor.de
   #iconv -f CP737 -t UTF8 tutor.gr.cp737 > conv/tutor.gr.cp737
   #iconv -f EUC-JP -t UTF8 tutor.ja.euc > conv/tutor.ja.euc
   #iconv -f SJIS -t UTF8 tutor.ja.sjis > conv/tutor.ja.sjis
   iconv -f UTF8 -t UTF8 tutor.ja.utf-8 > conv/tutor.ja.utf-8
   iconv -f UTF8 -t UTF8 tutor.ko.utf-8 > conv/tutor.ko.utf-8
   iconv -f CP1252 -t UTF8 tutor.no > conv/tutor.no
   iconv -f ISO-8859-2 -t UTF8 tutor.pl > conv/tutor.pl
   iconv -f ISO-8859-2 -t UTF8 tutor.sk > conv/tutor.sk
   iconv -f KOI8R -t UTF8 tutor.ru > conv/tutor.ru
   iconv -f CP1252 -t UTF8 tutor.sv > conv/tutor.sv
   mv -f tutor.ja.euc tutor.ja.sjis tutor.ko.euc tutor.pl.cp1250 tutor.zh.big5 tutor.ru.cp1251 tutor.zh.euc conv/
   rm -f tutor.ca tutor.de tutor.es tutor.fr tutor.gr tutor.it tutor.ja.utf-8 tutor.ko.utf-8 tutor.no tutor.pl tutor.sk tutor.ru tutor.sv
mv -f conv/* .
rmdir conv
popd

# Dependency cleanups
chmod 644 $RPM_BUILD_ROOT/usr/share/vim/%{vimdir}/doc/vim2html.pl \
 $RPM_BUILD_ROOT/usr/share/vim/%{vimdir}/tools/*.pl \
 $RPM_BUILD_ROOT/usr/share/vim/%{vimdir}/tools/vim132
chmod 644 ../runtime/doc/vim2html.pl

mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/profile.d
cat >$RPM_BUILD_ROOT/%{_sysconfdir}/profile.d/vim.sh <<EOF
if [ -n "\$BASH_VERSION" -o -n "\$KSH_VERSION" -o -n "\$ZSH_VERSION" ]; then
  [ -x /usr/bin/id ] || return
  tmpid=\$(/usr/bin/id -u)
  [ "\$tmpid" = "" ] && tmpid=0
  [ \$tmpid -le 100 ] && return
  # for bash and zsh, only if no alias is already set
  alias vi >/dev/null 2>&1 || alias vi=vim
fi
EOF
cat >$RPM_BUILD_ROOT/%{_sysconfdir}/profile.d/vim.csh <<EOF
if ( -x /usr/bin/id ) then
  if ( "\`/usr/bin/id -u\`" > 100 ) then
    alias vi vim
  endif
endif
EOF
chmod 0755 $RPM_BUILD_ROOT/%{_sysconfdir}/profile.d/*
install -m644 %{SOURCE4} $RPM_BUILD_ROOT/%{_sysconfdir}/vimrc
install -m644 %{SOURCE4} $RPM_BUILD_ROOT/%{_sysconfdir}/virc
(cd $RPM_BUILD_ROOT/usr/share/vim/%{vimdir}/doc;
 gzip -9n *.txt
 gzip -d help.txt.gz
 cat tags | sed -e 's/\t\(.*.txt\)\t/\t\1.gz\t/;s/\thelp.txt.gz\t/\thelp.txt\t/' > tags.new; mv -f tags.new tags
# cp %{SOURCE12} . 
 )
(cd ../runtime; rm -rf doc; ln -svf ../../vim/%{vimdir}/doc docs;) 

%post X11
touch --no-create %{_datadir}/icons/hicolor
if [ -x /usr/bin/gtk-update-icon-cache ]; then
  gtk-update-icon-cache --ignore-theme-index -q %{_datadir}/icons/hicolor
fi

%postun X11
touch --no-create %{_datadir}/icons/hicolor
if [ -x /usr/bin/gtk-update-icon-cache ]; then
  gtk-update-icon-cache --ignore-theme-index -q %{_datadir}/icons/hicolor
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files common
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/vimrc
%doc README*
%doc runtime/docs
#%doc $RPM_SOURCE_DIR/Changelog.rpm
%dir /usr/share/vim
%dir /usr/share/vim/%{vimdir}
/usr/share/vim/%{vimdir}/autoload
/usr/share/vim/%{vimdir}/colors
/usr/share/vim/%{vimdir}/compiler
/usr/share/vim/%{vimdir}/doc
#exclude /usr/share/vim/%{vimdir}/doc/vi-help.txt
/usr/share/vim/%{vimdir}/*.vim
/usr/share/vim/%{vimdir}/ftplugin
/usr/share/vim/%{vimdir}/indent
/usr/share/vim/%{vimdir}/keymap
/usr/share/vim/%{vimdir}/lang/*.vim
/usr/share/vim/%{vimdir}/lang/*.txt
%dir /usr/share/vim/%{vimdir}/lang
/usr/share/vim/%{vimdir}/macros
/usr/share/vim/%{vimdir}/plugin
/usr/share/vim/%{vimdir}/print
/usr/share/vim/%{vimdir}/syntax
/usr/share/vim/%{vimdir}/tools
/usr/share/vim/%{vimdir}/tutor
%if ! %{withvimspell}
/usr/share/vim/%{vimdir}/spell
%endif
%lang(af) /usr/share/vim/%{vimdir}/lang/af
%lang(ca) /usr/share/vim/%{vimdir}/lang/ca
%lang(cs) /usr/share/vim/%{vimdir}/lang/cs
%lang(cs.cp1250) /usr/share/vim/%{vimdir}/lang/cs.cp1250
%lang(de) /usr/share/vim/%{vimdir}/lang/de
%lang(en_GB) /usr/share/vim/%{vimdir}/lang/en_GB
%lang(es) /usr/share/vim/%{vimdir}/lang/es
%lang(eo) /usr/share/vim/%{vimdir}/lang/eo
%lang(fr) /usr/share/vim/%{vimdir}/lang/fr
%lang(fi) /usr/share/vim/%{vimdir}/lang/fi
%lang(ga) /usr/share/vim/%{vimdir}/lang/ga
%lang(it) /usr/share/vim/%{vimdir}/lang/it
%lang(ja) /usr/share/vim/%{vimdir}/lang/ja
%lang(ja.euc-jp) /usr/share/vim/%{vimdir}/lang/ja.euc-jp
%lang(ja.sjis) /usr/share/vim/%{vimdir}/lang/ja.sjis
%lang(ko) /usr/share/vim/%{vimdir}/lang/ko
%lang(ko.UTF-8) /usr/share/vim/%{vimdir}/lang/ko.UTF-8
%lang(no) /usr/share/vim/%{vimdir}/lang/no
%lang(nb) /usr/share/vim/%{vimdir}/lang/nb
%lang(nl) /usr/share/vim/%{vimdir}/lang/nl
%lang(pl) /usr/share/vim/%{vimdir}/lang/pl
%lang(pl.UTF-8) /usr/share/vim/%{vimdir}/lang/pl.UTF-8
%lang(pl.cp1250) /usr/share/vim/%{vimdir}/lang/pl.cp1250
%lang(pt_BR) /usr/share/vim/%{vimdir}/lang/pt_BR
%lang(ru) /usr/share/vim/%{vimdir}/lang/ru
%lang(ru.cp1251) /usr/share/vim/%{vimdir}/lang/ru.cp1251
%lang(sk) /usr/share/vim/%{vimdir}/lang/sk
%lang(sk.cp1250) /usr/share/vim/%{vimdir}/lang/sk.cp1250
%lang(sv) /usr/share/vim/%{vimdir}/lang/sv
%lang(uk) /usr/share/vim/%{vimdir}/lang/uk
%lang(uk.cp1251) /usr/share/vim/%{vimdir}/lang/uk.cp1251
%lang(vi) /usr/share/vim/%{vimdir}/lang/vi
%lang(zh_CN) /usr/share/vim/%{vimdir}/lang/zh_CN
%lang(zh_CN.cp936) /usr/share/vim/%{vimdir}/lang/zh_CN.cp936
%lang(zh_TW) /usr/share/vim/%{vimdir}/lang/zh_TW
%lang(zh_CN.UTF-8) /usr/share/vim/%{vimdir}/lang/zh_CN.UTF-8
%lang(zh_TW.UTF-8) /usr/share/vim/%{vimdir}/lang/zh_TW.UTF-8
/usr/bin/xxd
%{_mandir}/man1/vim.*
%{_mandir}/man1/ex.*
%{_mandir}/man1/vi.*
%{_mandir}/man1/view.*
%{_mandir}/man1/rvi.*
%{_mandir}/man1/rview.*
%{_mandir}/man1/xxd.*
%lang(fr) %{_mandir}/fr*
%lang(ja) %{_mandir}/ja*
%lang(it) %{_mandir}/it*
%lang(ru) %{_mandir}/ru*
%lang(pl) %{_mandir}/pl*

%if %{withvimspell}
%files spell
%dir /usr/share/vim/%{vimdir}/spell
/usr/share/vim/vim70/spell/cleanadd.vim
%lang(af) /usr/share/vim/%{vimdir}/spell/af.*
%lang(am) /usr/share/vim/%{vimdir}/spell/am.*
%lang(bg) /usr/share/vim/%{vimdir}/spell/bg.*
%lang(ca) /usr/share/vim/%{vimdir}/spell/ca.*
%lang(cs) /usr/share/vim/%{vimdir}/spell/cs.*
%lang(cy) /usr/share/vim/%{vimdir}/spell/cy.*
%lang(da) /usr/share/vim/%{vimdir}/spell/da.*
%lang(de) /usr/share/vim/%{vimdir}/spell/de.*
%lang(el) /usr/share/vim/%{vimdir}/spell/el.*
%lang(en) /usr/share/vim/%{vimdir}/spell/en.*
%lang(eo) /usr/share/vim/%{vimdir}/spell/eo.*
%lang(es) /usr/share/vim/%{vimdir}/spell/es.*
%lang(fo) /usr/share/vim/%{vimdir}/spell/fo.*
%lang(fr) /usr/share/vim/%{vimdir}/spell/fr.*
%lang(ga) /usr/share/vim/%{vimdir}/spell/ga.*
%lang(gd) /usr/share/vim/%{vimdir}/spell/gd.*
%lang(gl) /usr/share/vim/%{vimdir}/spell/gl.*
%lang(he) /usr/share/vim/%{vimdir}/spell/he.*
%lang(hr) /usr/share/vim/%{vimdir}/spell/hr.*
%lang(hu) /usr/share/vim/%{vimdir}/spell/hu.*
%lang(id) /usr/share/vim/%{vimdir}/spell/id.*
%lang(it) /usr/share/vim/%{vimdir}/spell/it.*
%lang(ku) /usr/share/vim/%{vimdir}/spell/ku.*
%lang(la) /usr/share/vim/%{vimdir}/spell/la.*
%lang(lt) /usr/share/vim/%{vimdir}/spell/lt.*
%lang(lv) /usr/share/vim/%{vimdir}/spell/lv.*
%lang(mg) /usr/share/vim/%{vimdir}/spell/mg.*
%lang(mi) /usr/share/vim/%{vimdir}/spell/mi.*
%lang(ms) /usr/share/vim/%{vimdir}/spell/ms.*
%lang(nb) /usr/share/vim/%{vimdir}/spell/nb.*
%lang(nl) /usr/share/vim/%{vimdir}/spell/nl.*
%lang(nn) /usr/share/vim/%{vimdir}/spell/nn.*
%lang(ny) /usr/share/vim/%{vimdir}/spell/ny.*
%lang(pl) /usr/share/vim/%{vimdir}/spell/pl.*
%lang(pt) /usr/share/vim/%{vimdir}/spell/pt.*
%lang(ro) /usr/share/vim/%{vimdir}/spell/ro.*
%lang(ru) /usr/share/vim/%{vimdir}/spell/ru.*
%lang(rw) /usr/share/vim/%{vimdir}/spell/rw.*
%lang(sk) /usr/share/vim/%{vimdir}/spell/sk.*
%lang(sl) /usr/share/vim/%{vimdir}/spell/sl.*
%lang(sv) /usr/share/vim/%{vimdir}/spell/sv.*
%lang(sw) /usr/share/vim/%{vimdir}/spell/sw.*
%lang(tet) /usr/share/vim/%{vimdir}/spell/tet.*
%lang(th) /usr/share/vim/%{vimdir}/spell/th.*
%lang(tl) /usr/share/vim/%{vimdir}/spell/tl.*
%lang(tn) /usr/share/vim/%{vimdir}/spell/tn.*
%lang(uk) /usr/share/vim/%{vimdir}/spell/uk.*
%lang(yi) /usr/share/vim/%{vimdir}/spell/yi.*
%lang(yi-tr) /usr/share/vim/%{vimdir}/spell/yi-tr.*
%lang(zu) /usr/share/vim/%{vimdir}/spell/zu.*
%endif

%files minimal
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/virc
/bin/ex
/bin/vi
/bin/view
/bin/rvi
/bin/rview
#/usr/share/vim/%{vimdir}/doc/vi-help.txt

%files enhanced
%defattr(-,root,root)
/usr/bin/vim
/usr/bin/rvim
/usr/bin/vimdiff
/usr/bin/ex
/usr/bin/vimtutor
%config %{_sysconfdir}/profile.d/vim.*
%{_mandir}/man1/rvim.*
%{_mandir}/man1/vimdiff.*
%{_mandir}/man1/vimtutor.*

%files X11
%defattr(-,root,root)
%if "%{desktop_file}" == "1"
/usr/share/applications/*
%else
/etc/X11/applnk/*/gvim.desktop
%endif
/usr/bin/gvim
/usr/bin/gvimdiff
/usr/bin/gview
/usr/bin/gex
/usr/bin/vimx
/usr/bin/evim
%{_mandir}/man1/evim.*
%{_mandir}/man1/gvim*
%{_datadir}/icons/hicolor/*/apps/*

%changelog
* Tue Jul 10 2012 Karsten Hopp <karsten@redhat.com> 7.0.109-7.2
- remove obsolete 'e' in front of filenames (netrw.vim)
  rhbz #591578
- fix recursive function call when doing completion
  rhbz #681108

* Tue Jul 03 2012 Karsten Hopp <karsten@redhat.com> 7.0.109-7.1
- fix directory listing (vim ..) (rhbz #652610)

* Wed Aug 04 2010 Karsten Hopp <karsten@redhat.com> 7.0.109-7
- move gvim desktop entry to Accessories (#506442)
- redo several patches so that they apply with fuzz=0
- fix syntax error when a script contains \c (#512265)
- fix end of line error in ex mode comments (#572157)

* Fri Jun 12 2009 Karsten Hopp <karsten@redhat.com> 7.0.109-6
- fix release
- fix file delete in netrw (#505344)

* Wed Jun 10 2009 Karsten Hopp <karsten@redhat.com> 7.0.109-5.6
- fix vim.sh profile

* Thu May 14 2009 Karsten Hopp <karsten@redhat.com> 7.0.109-5.4
- fix vim.csh profile
- link with libncurses instead of libtermcap
- provide correct number of parameters to [ builtin when 'id -u' returns
  an empty string
- group autocmds provided by Red Hat into a redhat augroup so that they 
  can be cleanly removed


* Thu Apr 09 2009 Karsten Hopp <karsten@redhat.com> 7.0.109-5.3
- add patch 7.0.236 to fix memory calculation

* Mon Oct 27 2008 Karsten Hopp <karsten@redhat.com> 7.0.109-5.1
- fixes CVE-2008-3074 (tar plugin)
- fixes CVE-2008-3075 (zip plugin)
- fixes CVE-2008-3076 (netrw plugin)
- fixes CVE-2008-4101 (keyword and tag lookup)

* Fri Jul 25 2008 Karsten Hopp <karsten@redhat.com> 7.0.109-5.1
- another fix for CVE-2008-2712

* Tue Jul 22 2008 Karsten Hopp <karsten@redhat.com> 7.0.109-5
- fix release

* Mon Jul 14 2008 Karsten Hopp <karsten@redhat.com> 7.0.109-3.6
- re-enable debuginfo

* Thu Jul 10 2008 Karsten Hopp <karsten@redhat.com> 7.0.109-3.5
- update netrw files for CVE-2008-2712

* Thu Jul 02 2008 Karsten Hopp <karsten@redhat.de> 7.0.109-3.4
- add fixes for CVE-2007-2953 and CVE-2008-2712

* Fri May 04 2007 Karsten Hopp <karsten@redhat.de> 7.0.109-3.3
- use gzip -9n to avoid multilib fileconflicts

* Wed May 02 2007 Karsten Hopp <karsten@redhat.com> 7.0.109-3.2
- Let 'modeline' default to off for root
- Resolves: bz#238259

* Wed May 02 2007 Karsten Hopp <karsten@redhat.com> 7.0.109-3.1
- fix modeline issues
- Resolves: bz#238259

* Thu Sep 28 2006 Jeremy Katz <katzj@redhat.com> - 7.0.109-3
- disable vim-spell subpackage as it pushes us over CD boundaries

* Tue Sep 28 2006 Karsten Hopp <karsten@redhat.com> 7.0.109-2
- fix typo in vimspell.sh (#203178)

* Tue Sep 19 2006 Karsten Hopp <karsten@redhat.com> 7.0.109-1
- update to patchlevel 109 to fix some redraw problems
- fix invisible comments in diff mode (#204042)

* Tue Sep 12 2006 Karsten Hopp <karsten@redhat.com> 7.0.100-1
- Patchlevel 100
- replace runtime files with newer ones

* Mon Sep 11 2006 Karsten Hopp <karsten@redhat.de> 7.0.099-1
- Patchlevel 99

* Mon Sep 05 2006 Karsten Hopp <karsten@redhat.de> 7.0.086-1
- Patchlevel 86

* Mon Sep 04 2006 Karsten Hopp <karsten@redhat.de> 7.0.083-1
- Patchlevel 83

* Wed Aug 30 2006 Karsten Hopp <karsten@redhat.de> 7.0.076-1
- Patchlevel 76

* Thu Aug 25 2006 Karsten Hopp <karsten@redhat.de> 7.0.066-2
- fix vimdiff colors (#204042)

* Thu Aug 24 2006 Karsten Hopp <karsten@redhat.de> 7.0.066-1
- fix syntax patch (#203798)
- patchlevel 66

* Wed Aug 17 2006 Karsten Hopp <karsten@redhat.de> 7.0.063-1
- Patchlevel 63

* Wed Aug 15 2006 Karsten Hopp <karsten@redhat.de> 7.0.053-1
- Patchlevel 53
- Buildrequires libXpm-devel

* Wed Aug 09 2006 Karsten Hopp <karsten@redhat.de> 7.0.050-1
- Patchlevel 50

* Thu Aug 03 2006  Karsten Hopp <karsten@redhat.de> 7.0.042-2
- clean up spec file

* Mon Jul 24 2006 Karsten Hopp <karsten@redhat.de> 7.0.042-1
- patchlevel 42

* Wed Jul 20 2006 Karsten Hopp <karsten@redhat.de> 7.0.039-1
- patchlevel 39
- allow usage of $VIM variable (#199465)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2:7.0.035-1.1
- rebuild

* Tue Jun 27 2006 Karsten Hopp <karsten@redhat.de> 7.0.035-1
- patchlevel 35

* Wed Jun 21 2006 Karsten Hopp <karsten@redhat.de> 7.0.022-2
- add binfmt_misc rpc_pipefs to fstypes for better mtab highlighting

* Tue Jun 20 2006 Karsten Hopp <karsten@redhat.de> 7.0.022-1
- patchlevel 22

* Tue Jun 20 2006 Karsten Hopp <karsten@redhat.de> 7.0.020-1
- patchlevel 20

* Tue Jun 20 2006 Karsten Hopp <karsten@redhat.de> 7.0.019-1
- patchlevel 19
- buildrequire autoconf

* Tue May 30 2006 Karsten Hopp <karsten@redhat.de> 7.0.017-1
- patchlevel 17, although it affects just the Motif version
- own some directories (#192787)

* Sat May 13 2006 Karsten Hopp <karsten@redhat.de> 7.0.016-1
- patchlevel 016

* Fri May 12 2006 Karsten Hopp <karsten@redhat.de> 7.0.012-1
- patchlevel 012

* Thu May 11 2006 Karsten Hopp <karsten@redhat.de> 7.0.010-1
- patchlevel 010

* Wed May 10 2006 Karsten Hopp <karsten@redhat.de> 7.0.005-2
- patchlevel 005
- move older changelogs (<7.0) into a file, no need to keep them 
  in the rpm database

* Tue May 09 2006 Karsten Hopp <karsten@redhat.de> 7.0.000-2
- bump epoch, the buildsystem thinks 7.0.000-2 is older than 7.0.g001-1
  although rpm is quite happy with it.

* Mon May 08 2006 Karsten Hopp <karsten@redhat.de> 7.0.000-1
- vim-7.0 
- Spell checking support for about 50 languages
- Intelligent completion for C, HTML, Ruby, Python, PHP, etc.
- Tab pages, each containing multiple windows
- Undo branches: never accidentally lose text again
- Vim script supports Lists and Dictionaries (similar to Python)
- Vim script profiling
- Improved Unicode support
- Highlighting of cursor line, cursor column and matching braces
- Translated manual pages support.
- Internal grep; works on all platforms, searches compressed files
- Browsing remote directories, zip and tar archives
- Printing multi-byte text
- find details about the changes since vim-6.4 with :help version7

- fix SE Linux context of temporary (.swp) files (#189968)
- /bin/vi /vim-minimal is now using /etc/virc to avoid .rpmnew files
  when updating

* Tue May 02 2006 Karsten Hopp <karsten@redhat.de> 7.0.g001-1
- vim-7.0g BETA

* Fri Apr 28 2006 Karsten Hopp <karsten@redhat.de> 7.0.f001-1
- vim-7.0f3 BETA

* Thu Apr 20 2006 Karsten Hopp <karsten@redhat.de> 7.0.e001-1
- vim-7.0e BETA

* Tue Apr 11 2006 Karsten Hopp <karsten@redhat.de> 7.0.d001-1
- vim-7.0d BETA

* Fri Apr 07 2006 Karsten Hopp <karsten@redhat.de> 7.0c.000-3
- fix vimrc filename

* Thu Apr 06 2006 Karsten Hopp <karsten@redhat.de> 7.0c.000-2
- new snapshot

* Tue Apr 04 2006 Karsten Hopp <karsten@redhat.de> 7.0c.000-1
- vim-7.0c BETA

* Wed Mar 22 2006 Karsten Hopp <karsten@redhat.de> 7.0aa.000-3
- Rawhide build as vim, opposed to vim7 (prerelease)
- conflict with older man-pages-{it,fr} packages
- cleanup lang stuff

* Thu Mar 16 2006 Karsten Hopp <karsten@redhat.de> 7.0aa.000-2
- make it coexist with vim-6 (temporarily)
- new CVS snapshot

* Tue Mar 14 2006 Karsten Hopp <karsten@redhat.de> 7.0aa.000-1
- vim7 pre Release
- older changelogs available in Changelog.rpm

# vim:nrformats-=octal
