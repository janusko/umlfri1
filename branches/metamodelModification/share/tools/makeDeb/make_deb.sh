#!/bin/bash
DIR_UML=umlfri
VERSION=1.0.0
PNAME=umlfri
DIR_DEST=$PNAME-$VERSION
AUTHOR_NAME='FRI'
MAIL=umlfri@umlfri.org
function cdumlfri() {
	cd $DIR_DEST/
}
function cdup() {
	cd ..
}
cp -r $DIR_UML temp
#find temp/ - type d | grep . svn | xargs rm -rf

cp required_files/umlfri temp/
cp required_files/umlfri.desktop temp/
mv  temp/ $DIR_DEST
tar cfz $DIR_DEST.tar.gz $DIR_DEST/
tar xfz $DIR_DEST.tar.gz 
mv $DIR_DEST.tar.gz $PNAME'_'$VERSION.orig.tar.gz
cdumlfri
#pwd
export DEBFULLNAME=$AUTHOR_NAME
dh_make -c GPL -e $MAIL -s 
#pwd
rm debian/*.ex debian/*.EX debian/README.Debian debian/control debian/docs
cp ../required_files/control debian/
cp ../required_files/docs debian/
cp ../required_files/umlfri.install debian/
dpkg-buildpackage
cdup
#--------------------------------------------------------
# comment these lines to keep tarballs and other files
rm -rf $DIR_DEST
rm *tar.gz
rm *.changes *.dsc
#-------------------------------------------------------

