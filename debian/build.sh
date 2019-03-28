#!/bin/bash -e

sudo apt-get install -y  wget make devscripts

VERSION=`cat ../version`

# Clean
rm -rf git-${VERSION}

# Download
if [ -e "git_${VERSION}.orig.tar.gz" ]; then
    echo "git_${VERSION}.orig.tar.gz exists, skipping.."
else
    wget https://github.com/git/git/archive/v${VERSION}.tar.gz
    mv -f v${VERSION}.tar.gz git_${VERSION}.orig.tar.gz
fi

# Extract
tar xzf git_${VERSION}.orig.tar.gz

# Copy over debian package info
cp -pr debian git-${VERSION}/

# Build
cd git-${VERSION}
sudo mk-build-deps --install --tool='apt-get --no-install-recommends -y' debian/control
dpkg-buildpackage -k EFD591B218E19AE3376D80D14F9E050D1DFFBB86 --force-sign

rm -rf git-${VERSION}

