#!/bin/bash
echo "Getting File"
wget $1 -q -O  /tmp/android-studio.deb > /dev/null
echo "Making temp dir"
mkdir /tmp/debbuild
echo "unpacking deb"
dpkg-deb -R /tmp/android-studio.deb /tmp/debbuild

echo "Making changes"
#cat /tmp/debbuild/DEBIAN/preinstall
rm /tmp/debbuild/DEBIAN/preinst
echo "ln -sf /opt/android-studio/bin/studio.sh /usr/bin/android-studio" > /tmp/debbuild/DEBIAN/postinst
chmod 775 /tmp/debbuild/DEBIAN/postinst 
echo "Package: android-studio" > /tmp/debbuild/DEBIAN/control
echo "Version: ${2}" >> /tmp/debbuild/DEBIAN/control
echo "Architecture: amd64" >> /tmp/debbuild/DEBIAN/control
echo "Maintainer: Phiwatec <mail@philippwasser.de>" >> /tmp/debbuild/DEBIAN/control
echo "Description: Android-Studio neu gepackt aus ChromeOS Version" >> /tmp/debbuild/DEBIAN/control 
echo "Packing deb"
name=/tmp/android-studio_${2}_amd64.deb
dpkg-deb -b /tmp/debbuild $name
echo "Copying.."
mv $name $3
rm -r /tmp/debbuild
echo "Done :)"
