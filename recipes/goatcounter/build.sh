BUILDIR=/tmp/build/debbuild

mkdir -p $BUILDIR

DIRNAME=$BUILDIR/goatcounter_$2_$3
mkdir -p $DIRNAME
mkdir -p $DIRNAME/usr/bin
mkdir -p $DIRNAME/etc/default
mkdir -p $DIRNAME/lib/systemd/system/
mkdir -p $DIRNAME/var/opt/goatcounter
#Get current release
wget -q $1 -O $DIRNAME/usr/bin/file.gz
gunzip -c $DIRNAME/usr/bin/file.gz >$DIRNAME/usr/bin/goatcounter
rm $DIRNAME/usr/bin/file.gz

# Copy systemd file

cp recipes/goatcounter/goatcounter.service $DIRNAME/lib/systemd/system/

# Copy config file

cp recipes/goatcounter/goatcounter $DIRNAME/etc/default/

# Copy postinstall file
mkdir -p $DIRNAME/DEBIAN
cp recipes/goatcounter/postinst $DIRNAME/DEBIAN/
chmod 0775 $DIRNAME/DEBIAN/postinst
# Make control dir and file

CONTROLFILE=$DIRNAME/DEBIAN/control
echo "Package: goatcounter" > $CONTROLFILE
echo Version: $2 >> $CONTROLFILE
echo Architecture: $3 >> $CONTROLFILE
echo "Maintainer: Philipp Wasser <info@philippwasser.de>" >> $CONTROLFILE
echo "Description: User friendly website statistics / analytics" >> $CONTROLFILE

dpkg-deb --build --root-owner-group $DIRNAME
mv $BUILDIR/goatcounter_$2_$3.deb $4
rm -r $DIRNAME
