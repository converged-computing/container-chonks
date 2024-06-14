# Top Layer Contents

These are the top 100 digests, from most to least (where "References" is the number of times there are used across just under 3 million layers). We can look at a particular image we found the layer / number in to try and figure out what it is. Note that this is problematic because the most commonly used layer (the top) seems to be 32 bytes of nothing, and registries seem to filter it out. This means that the lookup below is wrong, but we can try to look them up on our own.

## My Lookup

### sha256:4f4fb700ef54461cfa02571ae0db9a0dc1e0cdb5577484a6d75e68dc38e8acc1

Is an empty 32 bytes.  Here is an example manifest (see last layer)

```console
$ docker manifest inspect kaldiasr/kaldi:cpu-debian10-2022-08-18
{
	"mediaType": "application/vnd.docker.distribution.manifest.v2+json",
	"schemaVersion": 2,
	"config": {
		"mediaType": "application/vnd.docker.container.image.v1+json",
		"digest": "sha256:fffdf0321036771a84c85a9601568d5c955330f7ff6a31d5c93c02f8102c7992",
		"size": 3184
	},
	"layers": [
		{
			"mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
			"digest": "sha256:7e6a53d1988fa8e19db6bcfc96ee6783afb079c38dbe047528e691815d19a9fa",
			"size": 50440980
		},
		{
			"mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
			"digest": "sha256:768ecfb0ddc73413705602b980b73d3bf93e9733c02febc82faf6255c24d278e",
			"size": 264830520
		},
		{
			"mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
			"digest": "sha256:a53b7f1011ac9b13c9656a00f4fcfa93b083bfdb2a1173e09427ef776a82eb9f",
			"size": 156
		},
		{
			"mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
			"digest": "sha256:aadaf5d34d0b7753e058c7c2af5ddb6c60fb20600b0e10369d5707ae054f0884",
			"size": 26052659
		},
		{
			"mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
			"digest": "sha256:d657859482f8ce46cf55bd850f541b3991276b6de579a09d3e07dacbcaee9a03",
			"size": 1050690172
		},
		{
			"mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
			"digest": "sha256:4f4fb700ef54461cfa02571ae0db9a0dc1e0cdb5577484a6d75e68dc38e8acc1",
			"size": 32
		}
	]
}
```

I extracted the image (save) and I don't see it. I don't know what this is. I think for the above it corresponds with a [WORKDIR](https://github.com/docker/buildx/issues/1910) directive that creates an empty layer. I asked OCI:

> There is an "empty layer" flag in the image config. If the tooling decides not to set that for some reason, you must ship a valid tar+gzip, and that, even without any files being packaged, takes up some space for the tar and gzip headers.

Oh wow! So [this is the empty layer](https://github.com/moby/moby/blob/ff5cc18482bea99a9baba27112474eff156df778/layer/empty.go#L12)

If we decompress it, we get that digest / diff_id.

This was implemented before folks realized (and maybe many still don't) that /dev/null is an actual valid empty tar file

Also see https://oci.dag.dev/?repo=tianon/scratch, which is many variations on this theme.


### sha256:0eeab5c200691bd777e227c6eea27f7ca3c8232b67118a76edac2dcde3186aa1

This one [looks correct](https://hub.docker.com/layers/balenalib/ucm-imx93-alpine/3.12/images/sha256-2d5100981c3141a1bbb5d26f9f6d0e9d7f12afb5bd0d61696acce33bb155e694?context=explore)

This is literally just that many images from this organization, balena. They used a common base. That's it.

## Automated Lookup

This is wrong.

```console
    Digest: sha256:4f4fb700ef54461cfa02571ae0db9a0dc1e0cdb5577484a6d75e68dc38e8acc1
  Found In: kaldiasr/kaldi:cpu-debian10-2022-08-18
   Layer #: 5
References: 67897
   Created: 2022-08-18T09:02:59.056123501Z
   Content: RUN /bin/sh -c git clone --depth 1 https://github.com/kaldi-asr/kaldi.git /opt/kaldi #EOL # buildkit

    Digest: sha256:0eeab5c200691bd777e227c6eea27f7ca3c8232b67118a76edac2dcde3186aa1
  Found In: balenalib/ucm-imx93-alpine:3.12
   Layer #: 0
References: 4124
   Created: 2022-04-04T23:39:53.434744204Z
   Content: /bin/sh -c #(nop) ADD file:a2a992b7f6af1e6f8f5648f329f4a4058d8c4377417ac23ae211290c0cdc8f4b in / 

    Digest: sha256:fac132c5d16f670820c8c4ae332bd663c2ff856e9af86b2b23a201db263d851e
  Found In: mcr.microsoft.com/dotnet/core/runtime-deps:2.1.9-stretch-slim-arm32v7
   Layer #: 0
References: 4021
   Created: 2019-03-27T12:07:48.534712403Z
   Content: /bin/sh -c #(nop) ADD file:6bf06125d936ccaf67981470df5ef6b9bd5dee3c0ef0e042a448fc60bb02f191 in / 

    Digest: sha256:a3ed95caeb02ffe68cdd9fd84406680ae93d633cb16422d00e8a7c22955b46d4
  Found In: appsvc/php:5.6.21-apache
   Layer #: 1
References: 3740
   Created: 2016-05-23T22:57:23.255025884Z
   Content: /bin/sh -c #(nop) CMD ["/bin/bash"]

    Digest: sha256:eb64a536420170e45e3cb10ed6afd2f778bd618d4c63e218784492069bf479e0
  Found In: arm32v7/fedora:30
   Layer #: 0
References: 2729
   Created: 2019-01-17T12:59:01.036648364Z
   Content: /bin/sh -c #(nop)  LABEL maintainer=Clement Verna <cverna@fedoraproject.org>

    Digest: sha256:fdaf648994934a9a02d8cd979314e8987ecb57026c10e22ab829c579d96c9eb2
  Found In: balenalib/orangepi-plus2-debian:2
   Layer #: 4
References: 2467
   Created: 2019-04-18T14:46:14.741567813Z
   Content: /bin/sh -c #(nop) COPY file:f41cb8a4ab74a9bbe0a5955b10b7df7bdee3fe93f2677c5faea3399f3ac38623 in /usr/bin 

    Digest: sha256:7082a08caaff30d90ad6a99368cba8d95e689c717fd116fbf86e4081e014f9af
  Found In: balenalib/orangepi-plus2-debian:2
   Layer #: 5
References: 2467
   Created: 2019-04-18T14:48:17.939659768Z
   Content: /bin/sh -c apt-get update && apt-get install -y --no-install-recommends   sudo   ca-certificates   findutils   gnupg   dirmngr   inetutils-ping   netbase   curl   udev   procps   $(       if apt-cache show 'iproute' 2>/dev/null | grep -q '^Version:'; then         echo 'iproute';       else         echo 'iproute2';       fi   )   && rm -rf /var/lib/apt/lists/*   && echo '#!/bin/sh\nset -e\nset -u\nexport DEBIAN_FRONTEND=noninteractive\nn=0\nmax=2\nuntil [ $n -gt $max ]; do\n  set +e\n  (\n    apt-get update -qq &&\n    apt-get install -y --no-install-recommends "$@"\n  )\n  CODE=$?\n  set -e\n  if [ $CODE -eq 0 ]; then\n    break\n  fi\n  if [ $n -eq $max ]; then\n    exit $CODE\n  fi\n  echo "apt failed, retrying"\n  n=$(($n + 1))\ndone\nrm -r /var/lib/apt/lists/*' > /usr/sbin/install_packages   && chmod 0755 "/usr/sbin/install_packages"

    Digest: sha256:5d2bba83464b5fac87e22ad762b0d5ff2ca85aafdfbf1becb50fc6eed30889c1
  Found In: balenalib/orangepi-plus2-debian:2
   Layer #: 7
References: 2467
   Created: 2019-04-18T14:48:21.553932776Z
   Content: /bin/sh -c #(nop)  ENV LC_ALL=C.UTF-8

    Digest: sha256:f8016bc883964f6dc377e4a339ffb1a1c3cc8b34a91de25806ae0d94fbb7fa14
  Found In: balenalib/orangepi-plus2-debian:2
   Layer #: 6
References: 2467
   Created: 2019-04-18T14:48:20.789225597Z
   Content: /bin/sh -c curl -SLO "http://resin-packages.s3.amazonaws.com/resin-xbuild/v1.0.0/resin-xbuild1.0.0.tar.gz"   && echo "1eb099bc3176ed078aa93bd5852dbab9219738d16434c87fc9af499368423437  resin-xbuild1.0.0.tar.gz" | sha256sum -c -   && tar -xzf "resin-xbuild1.0.0.tar.gz"   && rm "resin-xbuild1.0.0.tar.gz"   && chmod +x resin-xbuild   && mv resin-xbuild /usr/bin   && ln -s resin-xbuild /usr/bin/cross-build-start   && ln -s resin-xbuild /usr/bin/cross-build-end

    Digest: sha256:637f15cfe8980595229088a90bca1a76cef0c69729088a15fd21d0ab39c78891
  Found In: balenalib/orangepi-plus2-debian:2
   Layer #: 2
References: 2467
   Created: 2019-04-18T14:46:12.649826649Z
   Content: /bin/sh -c #(nop)  LABEL io.balena.architecture=armv7hf

    Digest: sha256:9fbe265f43e22a7932321da34a54908650ba190fadb7f6a8670602274c5a86f2
  Found In: balenalib/orangepi-plus2-debian:2
   Layer #: 3
References: 2467
   Created: 2019-04-18T14:46:13.41783943Z
   Content: /bin/sh -c #(nop)  LABEL io.balena.qemu.version=3.0.0+resin-arm

    Digest: sha256:9c7f211abc56f597100152789b08412375fab6fe6c7e1f5f747720e8f9de71fc
  Found In: balenalib/orangepi-plus2-debian:2
   Layer #: 1
References: 2467
   Created: 2019-03-27T12:07:49.273308462Z
   Content: /bin/sh -c #(nop)  CMD ["bash"]

    Digest: sha256:2a7570859f039cd926ea723271ed04029f7f9d1984ca02e7860dfb1d0aac16ff
  Found In: balenalib/orangepi-plus2-debian:2
   Layer #: 8
References: 1550
   Created: 2019-04-18T14:48:22.30975686Z
   Content: /bin/sh -c #(nop)  ENV DEBIAN_FRONTEND=noninteractive

    Digest: sha256:25f523f0e93b2b5fa676c15d91b90f08ee4de7a160874e6c52ea452929d5a7cc
  Found In: balenalib/ucm-imx93-alpine:3.13
   Layer #: 0
References: 2364
   Created: 2022-11-10T20:39:56.523308612Z
   Content: /bin/sh -c #(nop) ADD file:f23c059b4312458fbf0fc018d4695f36157a3eb6e5a83167912a39f9a738f4eb in / 

    Digest: sha256:2d473b07cdd5f0912cd6f1a703352c82b512407db6b05b43f2553732b55df3bc
  Found In: nvcr.io/nvidia/rapidsai/rapidsai:0.18-cuda10.1-base-centos7
   Layer #: 0
References: 2016
   Created: 2020-11-14T00:20:04.1030585Z
   Content: /bin/sh -c #(nop) ADD file:b3ebbe8bd304723d43b7b44a6d990cd657b63d93d6a2a9293983a30bfc1dfa53 in / 

    Digest: sha256:69fff380046369a47fbc74b0aa03f61fb243f73dc5795e3ecf69c6577ee84908
  Found In: balenalib/raspberrypi0-2w-64-fedora:20231127
   Layer #: 0
References: 2008
   Created: 2022-11-03T19:58:13.618756383Z
   Content: /bin/sh -c #(nop)  LABEL maintainer=Clement Verna <cverna@fedoraproject.org>

    Digest: sha256:6234d95b30844a1d16ac1f4014e9ab1a04fbfd031f879412b4e255357fa254c9
  Found In: arm32v7/fedora:26
   Layer #: 0
References: 1983
   Created: 2017-09-27T04:18:33.805000734Z
   Content: /bin/sh -c #(nop)  MAINTAINER [Adam Miller <maxamillion@fedoraproject.org>] [Patrick Uiterwijk <patrick@puiterwijk.org>]

    Digest: sha256:3c114d25664dd2c483a35f38b4247d232492c6349140793bb746b2ee75653db3
  Found In: arm32v7/fedora:28
   Layer #: 0
References: 1921
   Created: 2019-01-17T12:59:01.036648364Z
   Content: /bin/sh -c #(nop)  LABEL maintainer=Clement Verna <cverna@fedoraproject.org>

    Digest: sha256:064a9bb4736de1b2446f528e4eb37335378392cf9b95043d3e9970e253861702
  Found In: balenalib/iot-gate-imx8plus-ubuntu:bionic
   Layer #: 0
References: 1911
   Created: 2023-05-30T09:39:04.161612881Z
   Content: /bin/sh -c #(nop)  ARG RELEASE

    Digest: sha256:3c149c5b6c870036b0d1800ab84879687065f2266327798e1c29f0b0ec4432e4
  Found In: arm32v7/fedora:29
   Layer #: 0
References: 1910
   Created: 2019-01-17T12:59:01.036648364Z
   Content: /bin/sh -c #(nop)  LABEL maintainer=Clement Verna <cverna@fedoraproject.org>

    Digest: sha256:7b0c64ecbe73ee7edefed6c711475ee88c27023b230bda8b3477345aef857a2a
  Found In: arm32v7/alpine:3.12
   Layer #: 0
References: 1776
   Created: 2022-04-04T23:58:21.921040626Z
   Content: /bin/sh -c #(nop) ADD file:b3656d70f83984b1a2ae878f101095aecbc33cbb2f984646066fcf27b2b42178 in / 

    Digest: sha256:c4a218912c373bd27b3a8119edad3513643a05070961aca102e5d4b8566a6ce5
  Found In: balenalib/nanopc-t4-fedora:28
   Layer #: 0
References: 1768
   Created: 2019-06-05T22:43:26.440408184Z
   Content: /bin/sh -c #(nop)  LABEL maintainer=Clement Verna <cverna@fedoraproject.org>

    Digest: sha256:d801eef1c54cc60417183fca04b6b683598744bf6b5c45ffee2e5bd1ada2a9be
  Found In: balenalib/nanopc-t4-fedora:26
   Layer #: 0
References: 1733
   Created: 2019-06-05T22:42:44.092487429Z
   Content: /bin/sh -c #(nop)  MAINTAINER [Adam Miller <maxamillion@fedoraproject.org>] [Patrick Uiterwijk <patrick@puiterwijk.org>]

    Digest: sha256:007027d142c80b166a004bc7265c04036b80df438ac408f1a947e05c581b418e
  Found In: mcr.microsoft.com/dotnet/core/runtime-deps:3.0-stretch-slim-arm64v8
   Layer #: 0
References: 1609
   Created: 2019-03-27T08:47:46.944563278Z
   Content: /bin/sh -c #(nop) ADD file:9db7760cb1c28ef0cd3fa9ee9d0f528d2bcfe80b1c3973daa9f87e30b2047102 in / 

    Digest: sha256:90792d4aa5f3da5527ef99e5ffa78cb18d8ec7e89176ff8ea083d1ee0dfc5280
  Found In: balenalib/nanopc-t4-fedora:20190529
   Layer #: 0
References: 1559
   Created: 2019-01-17T09:42:52.931072074Z
   Content: /bin/sh -c #(nop)  LABEL maintainer=Clement Verna <cverna@fedoraproject.org>

    Digest: sha256:c1323e24d83bead6278a9d962e8184fae424d3b184fd8892fcb9fb05b4b7068e
  Found In: balenalib/raspberrypi0-2w-64-fedora:33
   Layer #: 0
References: 1481
   Created: 2021-11-02T21:12:33.695210213Z
   Content: /bin/sh -c #(nop)  LABEL maintainer=Clement Verna <cverna@fedoraproject.org>

    Digest: sha256:9a7dd24a24ec2fb424aa68e1011fe210a137c7cda3c14068c0835dae60c25f3e
  Found In: balenalib/orangepi-plus2-debian:2-build
   Layer #: 4
References: 1333
   Created: 2019-04-18T14:38:24.433551311Z
   Content: /bin/sh -c #(nop) COPY file:f41cb8a4ab74a9bbe0a5955b10b7df7bdee3fe93f2677c5faea3399f3ac38623 in /usr/bin 

    Digest: sha256:786bbb20b518fc39226d9ebf704e20bec9cb5de353dbf542179a379b11783719
  Found In: balenalib/orangepi-plus2-debian:2-build
   Layer #: 1
References: 1333
   Created: 2019-03-27T12:07:49.273308462Z
   Content: /bin/sh -c #(nop)  CMD ["bash"]

    Digest: sha256:ea0c809f582a19799085ba5e1bfad55e0f529df0b297f789f14252ba64caf4c6
  Found In: balenalib/orangepi-plus2-debian:2-build
   Layer #: 6
References: 1333
   Created: 2019-04-18T14:44:07.906205035Z
   Content: /bin/sh -c apt-get update && apt-get install -y --no-install-recommends 		ca-certificates 		curl 		wget bzr 		git 		mercurial 		openssh-client 		subversion 		autoconf 		build-essential 	imagemagick 		libbz2-dev 		libcurl4-openssl-dev 		libevent-dev 		libffi-dev 		libglib2.0-dev 		libjpeg-dev 		libmagickcore-dev 		libmagickwand-dev 		libncurses-dev 		libpq-dev 		libreadline-dev 		libsqlite3-dev 		libssl-dev 		libxml2-dev 		libxslt-dev 		libyaml-dev 		zlib1g-dev 	$( 			if apt-cache show 'default-libmysqlclient-dev' 2>/dev/null | grep -q '^Version:'; then 				echo 'default-libmysqlclient-dev'; 			else 				echo 'libmysqlclient-dev'; 			fi 		) 	&& rm -rf /var/lib/apt/lists/*

    Digest: sha256:bc283eaf2191c7b58215f83f49b9912987b61115cabe6bab3bd9608620bd144e
  Found In: balenalib/orangepi-plus2-debian:2-build
   Layer #: 7
References: 1333
   Created: 2019-04-18T14:44:12.297951844Z
   Content: /bin/sh -c curl -SLO "http://resin-packages.s3.amazonaws.com/resin-xbuild/v1.0.0/resin-xbuild1.0.0.tar.gz"   && echo "1eb099bc3176ed078aa93bd5852dbab9219738d16434c87fc9af499368423437  resin-xbuild1.0.0.tar.gz" | sha256sum -c -   && tar -xzf "resin-xbuild1.0.0.tar.gz"   && rm "resin-xbuild1.0.0.tar.gz"   && chmod +x resin-xbuild   && mv resin-xbuild /usr/bin   && ln -s resin-xbuild /usr/bin/cross-build-start   && ln -s resin-xbuild /usr/bin/cross-build-end

    Digest: sha256:5b2d8772666bf5f0f606d107259091d9b7917627610bf472d296612b9896f742
  Found In: balenalib/orangepi-plus2-debian:2-build
   Layer #: 8
References: 1333
   Created: 2019-04-18T14:44:13.000013476Z
   Content: /bin/sh -c #(nop)  ENV LC_ALL=C.UTF-8

    Digest: sha256:f3e94b28902acc250e92a83398fe67e8448001390b6a2eb50f45ad5575601bcd
  Found In: balenalib/orangepi-plus2-debian:2-build
   Layer #: 3
References: 1333
   Created: 2019-04-18T14:38:23.089849798Z
   Content: /bin/sh -c #(nop)  LABEL io.balena.qemu.version=3.0.0+resin-arm

    Digest: sha256:3b8c860ab4a3477c7684bca9696efb2cc6ee7ae945bdeb54f8cf88d038564cb2
  Found In: balenalib/orangepi-plus2-debian:2-build
   Layer #: 2
References: 1333
   Created: 2019-04-18T14:38:22.109123934Z
   Content: /bin/sh -c #(nop)  LABEL io.balena.architecture=armv7hf

    Digest: sha256:a18b55278b0cd971fab3879e733c995b80a8554c5788ba1e440afbddc8193200
  Found In: balenalib/orangepi-plus2-debian:2-build
   Layer #: 5
References: 1333
   Created: 2019-04-18T14:40:29.703478804Z
   Content: /bin/sh -c apt-get update && apt-get install -y --no-install-recommends   sudo   ca-certificates   findutils   gnupg   dirmngr   inetutils-ping   netbase   curl   udev   procps   $(       if apt-cache show 'iproute' 2>/dev/null | grep -q '^Version:'; then         echo 'iproute';       else         echo 'iproute2';       fi   )   && rm -rf /var/lib/apt/lists/*   && echo '#!/bin/sh\nset -e\nset -u\nexport DEBIAN_FRONTEND=noninteractive\nn=0\nmax=2\nuntil [ $n -gt $max ]; do\n  set +e\n  (\n    apt-get update -qq &&\n    apt-get install -y --no-install-recommends "$@"\n  )\n  CODE=$?\n  set -e\n  if [ $CODE -eq 0 ]; then\n    break\n  fi\n  if [ $n -eq $max ]; then\n    exit $CODE\n  fi\n  echo "apt failed, retrying"\n  n=$(($n + 1))\ndone\nrm -r /var/lib/apt/lists/*' > /usr/sbin/install_packages   && chmod 0755 "/usr/sbin/install_packages"

    Digest: sha256:65dd610a92700dd7d70c7505ece47d6d74123face305e9bb9cf1856ba353de2c
  Found In: balenalib/orangepi-plus2-debian:2-build
   Layer #: 9
References: 804
   Created: 2019-04-18T14:44:13.833321767Z
   Content: /bin/sh -c #(nop)  ENV DEBIAN_FRONTEND=noninteractive

    Digest: sha256:a44ec0c63899958ea0679c5fddbc5304d0711f79b819fcda3e33ed21eb736e6a
  Found In: balenalib/beaglebone-green-fedora:20190301
   Layer #: 2
References: 1319
   Created: 2019-02-20T13:00:13.192440917Z
   Content: /bin/sh -c #(nop) ADD file:75a904dc30a4c870c164e7973d73396fe333b8bb83f5a448eb97a488419cabb4 in / 

    Digest: sha256:2961fce0d12f7ec6e40a857720d1511ecd24281b7c3a69e6ea4a4a6f6ad2ac68
  Found In: balenalib/beaglebone-green-fedora:20190301
   Layer #: 5
References: 1319
   Created: 2019-03-06T02:22:11.155057576Z
   Content: /bin/sh -c #(nop)  LABEL io.balena.qemu.version=3.0.0+resin-arm

    Digest: sha256:1e0b062ce16a6f9bee9397b4cb329bf024e86f0a3dc198b3e863c8c73f667a91
  Found In: balenalib/beaglebone-green-fedora:20190301
   Layer #: 1
References: 1319
   Created: 2019-01-17T12:59:45.6524644Z
   Content: /bin/sh -c #(nop)  ENV DISTTAG=f29container FGC=f29 FBR=f29

    Digest: sha256:81eab41a9a63f99afd0349712a509f92b6c6f374a8e8c07400d1fc432bf5a0ef
  Found In: balenalib/beaglebone-green-fedora:20190301
   Layer #: 3
References: 1319
   Created: 2019-02-20T13:00:15.136545681Z
   Content: /bin/sh -c #(nop)  CMD ["/bin/bash"]

    Digest: sha256:c4a69f4c6be723f11ffc3a8f866527939dfe707e68e212e74db87a3526cacbd3
  Found In: balenalib/beaglebone-green-fedora:20190301
   Layer #: 4
References: 1319
   Created: 2019-03-06T02:22:10.387297769Z
   Content: /bin/sh -c #(nop)  LABEL io.balena.architecture=armv7hf

    Digest: sha256:422ed46b1a92579f7c475c0c19fade6880a8d98f23a2b4ccfb77c265d4f72dfc
  Found In: balenalib/ucm-imx93-alpine:3.14
   Layer #: 0
References: 1305
   Created: 2023-03-29T17:39:25.334983269Z
   Content: /bin/sh -c #(nop) ADD file:c3d52cc254959a9ff493e7347e6b1bc25c0ccfdcf9532dbf43173ddd182d0e4d in / 

    Digest: sha256:0aeb4ade331e503f627cf2d20e48a0e609546d534f31d0ab05e75c8f0a67add4
  Found In: balenalib/raspberrypi0-2w-64-fedora:36
   Layer #: 0
References: 1292
   Created: 2022-11-03T19:58:13.618756383Z
   Content: /bin/sh -c #(nop)  LABEL maintainer=Clement Verna <cverna@fedoraproject.org>

    Digest: sha256:623fc6c8f399e6dde93fc82beed08af10e667fa3896b48d4d41b3f93d652dd0c
  Found In: balenalib/raspberrypi0-2w-64-fedora:20220413
   Layer #: 0
References: 1257
   Created: 2021-11-02T21:12:33.695210213Z
   Content: /bin/sh -c #(nop)  LABEL maintainer=Clement Verna <cverna@fedoraproject.org>

    Digest: sha256:a4f595742a5b0a76289f5927f75d63ef61a88d2ff5aaad78eed16e50c925cc5d
  Found In: docker.elastic.co/logstash/logstash-oss:6.8-SNAPSHOT
   Layer #: 0
References: 1164
   Created: 2021-09-15T18:20:23.417639551Z
   Content: /bin/sh -c #(nop) ADD file:b3ebbe8bd304723d43b7b44a6d990cd657b63d93d6a2a9293983a30bfc1dfa53 in / 

    Digest: sha256:a35d67b9c84802103773c29f779afc1c2111de2829c76b363fc8250d071ac519
  Found In: balenalib/raspberrypi0-2w-64-fedora:34
   Layer #: 0
References: 1038
   Created: 2021-11-02T21:12:33.695210213Z
   Content: /bin/sh -c #(nop)  LABEL maintainer=Clement Verna <cverna@fedoraproject.org>

    Digest: sha256:85affea9197829aaa02fc12f5746dc2ebda2bf5ba7bef4485314e81765acc103
  Found In: balenalib/raspberrypi3-64-debian:2
   Layer #: 1
References: 1025
   Created: 2019-03-27T08:47:47.838380797Z
   Content: /bin/sh -c #(nop)  CMD ["bash"]

    Digest: sha256:10d36aba5a6689df6cea03e2021d3b93c0cf9e3720e2ff413fe2b0dd3c1f65f0
  Found In: balenalib/raspberrypi3-64-debian:2
   Layer #: 5
References: 1025
   Created: 2019-03-27T12:30:04.980085691Z
   Content: /bin/sh -c apt-get update && apt-get install -y --no-install-recommends   sudo   ca-certificates   findutils   gnupg   dirmngr   inetutils-ping   netbase   curl   udev   procps   $(       if apt-cache show 'iproute' 2>/dev/null | grep -q '^Version:'; then         echo 'iproute';       else         echo 'iproute2';       fi   )   && rm -rf /var/lib/apt/lists/*   && echo '#!/bin/sh\nset -e\nset -u\nexport DEBIAN_FRONTEND=noninteractive\nn=0\nmax=2\nuntil [ $n -gt $max ]; do\n  set +e\n  (\n    apt-get update -qq &&\n    apt-get install -y --no-install-recommends "$@"\n  )\n  CODE=$?\n  set -e\n  if [ $CODE -eq 0 ]; then\n    break\n  fi\n  if [ $n -eq $max ]; then\n    exit $CODE\n  fi\n  echo "apt failed, retrying"\n  n=$(($n + 1))\ndone\nrm -r /var/lib/apt/lists/*' > /usr/sbin/install_packages   && chmod 0755 "/usr/sbin/install_packages"

    Digest: sha256:53ee00d764de67092c60e96ad7650e17c53153659ce2e55490e239c4f03fe620
  Found In: balenalib/raspberrypi3-64-debian:2
   Layer #: 3
References: 1025
   Created: 2019-03-27T12:27:21.70411855Z
   Content: /bin/sh -c #(nop)  LABEL io.balena.qemu.version=3.0.0+resin-aarch64

    Digest: sha256:d7887e24d0c5d161dfb2d930413d8c075409a6a90948615cb2d3939fdfbaf5c7
  Found In: balenalib/raspberrypi3-64-debian:2
   Layer #: 6
References: 1025
   Created: 2019-03-27T12:30:07.668532887Z
   Content: /bin/sh -c curl -SLO "http://resin-packages.s3.amazonaws.com/resin-xbuild/v1.0.0/resin-xbuild1.0.0.tar.gz"   && echo "1eb099bc3176ed078aa93bd5852dbab9219738d16434c87fc9af499368423437  resin-xbuild1.0.0.tar.gz" | sha256sum -c -   && tar -xzf "resin-xbuild1.0.0.tar.gz"   && rm "resin-xbuild1.0.0.tar.gz"   && chmod +x resin-xbuild   && mv resin-xbuild /usr/bin   && ln -s resin-xbuild /usr/bin/cross-build-start   && ln -s resin-xbuild /usr/bin/cross-build-end

    Digest: sha256:c0dac7fc3de3320655db45763984313710d7d40c83d5f6d8b2a07a46a8a7b1d3
  Found In: balenalib/raspberrypi3-64-debian:2
   Layer #: 2
References: 1025
   Created: 2019-03-27T12:27:21.015759285Z
   Content: /bin/sh -c #(nop)  LABEL io.balena.architecture=aarch64

    Digest: sha256:9bfed1a6ff5e63bff8a3f287e89c3334c92e1cd596b1bb57c84d702e7bb11044
  Found In: balenalib/raspberrypi3-64-debian:2
   Layer #: 4
References: 1025
   Created: 2019-03-27T12:27:23.031733563Z
   Content: /bin/sh -c #(nop) COPY file:a15b11e3b748898c722c5f7cbf2a64cf4edcfac16374cb0fc005915a5634c261 in /usr/bin 

    Digest: sha256:966651c0f77356773b2ae07970ba45782dbe080325c8f9c72f08ca907f550e38
  Found In: balenalib/raspberrypi3-64-debian:2
   Layer #: 7
References: 1025
   Created: 2019-03-27T12:30:08.633056944Z
   Content: /bin/sh -c #(nop)  ENV LC_ALL=C.UTF-8

    Digest: sha256:d4fa16d874cacbe930b1a3bf2a46bfb3817acdcaf2c7b17fe369e22d7c412d11
  Found In: balenalib/raspberrypi3-64-debian:2
   Layer #: 8
References: 1008
   Created: 2019-03-27T12:30:09.393211724Z
   Content: /bin/sh -c #(nop)  ENV DEBIAN_FRONTEND=noninteractive

    Digest: sha256:6717b8ec66cd6add0272c6391165585613c31314a43ff77d9751b53010e531ec
  Found In: quay.io/pypa/manylinux2014_aarch64:latest
   Layer #: 0
References: 980
   Created: 2022-02-14T19:39:36.951769438Z
   Content: /bin/sh -c #(nop) ADD file:5b1e63a3cb041177b802b501dedcd71a86f1773ea0f69f048f2eb3901097711d in / 

    Digest: sha256:b038bcb63e9c8905cc879c957302f686a9b43f24a18dcfc4186ab236ddf04cad
  Found In: mcr.microsoft.com/dotnet/core/runtime-deps:3.1-alpine3.10-arm64v8
   Layer #: 0
References: 949
   Created: 2020-04-24T00:14:52.324434922Z
   Content: /bin/sh -c #(nop) ADD file:75529f7e83edb6d0457a3b8bbfe33d4e3a12f339c5ace517d0f52dbedd9a146b in / 

    Digest: sha256:ad20c94522902b824bd9ea4e65dc1cba24dca4fdadd5728ed7446c0f4550d1ff
  Found In: arm32v7/python:3-alpine3.10
   Layer #: 0
References: 937
   Created: 2020-04-23T22:04:44.143517322Z
   Content: /bin/sh -c #(nop) ADD file:dabd2c1328a46961a58e93557d1039d6b98775cbdfe48ce875c109bb74615cb1 in / 

    Digest: sha256:3cfb62949d9d8613854db4d5fe502a9219c2b55a153043500078a64e880ae234
  Found In: arm32v7/python:3-alpine3.11
   Layer #: 0
References: 910
   Created: 2020-04-23T22:04:19.452978168Z
   Content: /bin/sh -c #(nop) ADD file:33578d3cacfab86c195d99396dd012ec511796a1d2d8d6f0a02b8a055673c294 in / 

    Digest: sha256:2244706f264b35566276550fbc21ada79613ddfff850e372b8f5113110a67c93
  Found In: balenalib/photon-nano-debian:20240101
   Layer #: 0
References: 890
   Created: 2023-12-19T01:41:25.583042341Z
   Content: /bin/sh -c #(nop) ADD file:4dd1c5e17a5e57644787f37e8ad290baef6c93f4f112b976f19136480a293713 in / 

    Digest: sha256:3889bb8d808bbae6fa5a33e07093e65c31371bcf9e4c38c21be6b9af52ad1548
  Found In: mcr.microsoft.com/powershell:6.0.2-windowsservercore
   Layer #: 0
References: 886
   Created: 2016-12-13T10:53:31Z
   Content: Apply image 10.0.14393.0

    Digest: sha256:c6b39de5b33961661dc939b997cc1d30cda01e38005a6c6625fd9c7e748bab44
  Found In: mcr.microsoft.com/dotnet/sdk:7.0-alpine3.18-arm64v8
   Layer #: 0
References: 861
   Created: 2024-01-26T23:44:55.650290626Z
   Content: /bin/sh -c #(nop) ADD file:6dc287a22d6cc7723b0576dd3a9a644468d133c54d42c8a8eda403e3117648f7 in / 

    Digest: sha256:c78bf262041043d92ff5941c1d129619bd9f70b9ec3037df22ecd407f7e8a2a5
  Found In: balenalib/raspberrypi0-2w-64-fedora:32
   Layer #: 0
References: 839
   Created: 2021-07-23T01:32:26.444557891Z
   Content: /bin/sh -c #(nop)  LABEL maintainer=Clement Verna <cverna@fedoraproject.org>

    Digest: sha256:3c2cba919283a210665e480bcbf943eaaf4ed87a83f02e81bb286b8bdead0e75
  Found In: solsson/kafka:native-kafka-configs
   Layer #: 2
References: 825
   Created: 1970-01-01T00:00:00Z
   Content: bazel build ...

    Digest: sha256:33728956a279755bb5e348de30626ffff0023b589d4fae264c2722ad7c06e207
  Found In: arm32v7/ubuntu:18.04
   Layer #: 0
References: 820
   Created: 2023-05-30T09:52:11.859558654Z
   Content: /bin/sh -c #(nop)  ARG RELEASE

    Digest: sha256:1b7ca6aea1ddfe716f3694edb811ab35114db9e93f3ce38d7dab6b4d9270cb0c
  Found In: amd64/alpine:3.12
   Layer #: 0
References: 802
   Created: 2022-04-05T00:20:19.714863518Z
   Content: /bin/sh -c #(nop) ADD file:c1aa87a3b464fca64d769444b5201bc0426a1f517c91c4a7916270e10f8b300b in / 

    Digest: sha256:29e5d40040c18c692ed73df24511071725b74956ca1a61fe6056a651d86a13bd
  Found In: mcr.microsoft.com/dotnet/runtime-deps:5.0-alpine3.11-arm64v8
   Layer #: 0
References: 749
   Created: 2020-04-24T00:14:18.623777014Z
   Content: /bin/sh -c #(nop) ADD file:85ae77bc1e43353ff14e6fe1658be1ed4ecbf4330212ac3d7ab7462add32dd39 in / 

    Digest: sha256:6064e7e5b6afa4dc711228eddfd250aebac271830dc184c400ce640020bc2cb0
  Found In: mcr.microsoft.com/dotnet/runtime-deps:3.1.31-bullseye-slim-arm64v8
   Layer #: 0
References: 742
   Created: 2022-12-06T01:40:17.07810417Z
   Content: /bin/sh -c #(nop) ADD file:379d6ac56afdb6e02d71fa0faebc13b8a2554fc6ae76c5f5bbdb5b8e475135d6 in / 

    Digest: sha256:9d9c6880d97881f162ecb459d83e29ab18daa14a7bee66ecdcba38761b6a427f
  Found In: balenalib/photon-nano-debian:20221210
   Layer #: 2
References: 723
   Created: 2022-12-13T04:08:44.828091393Z
   Content: /bin/sh -c #(nop)  LABEL io.balena.architecture=aarch64

    Digest: sha256:62e7aab101f2143b55d89813fb308d59e79cc3338c45a481c23445756edf15c2
  Found In: balenalib/photon-nano-debian:20221210
   Layer #: 1
References: 723
   Created: 2022-12-06T01:40:17.376221803Z
   Content: /bin/sh -c #(nop)  CMD ["bash"]

    Digest: sha256:c39ad53a3dc1cd85e49ea5705169326c2b5ad7203e1f9c204a3916f632ce6030
  Found In: balenalib/nanopc-t4-fedora:20200221
   Layer #: 0
References: 716
   Created: 2019-06-05T22:43:26.440408184Z
   Content: /bin/sh -c #(nop)  LABEL maintainer=Clement Verna <cverna@fedoraproject.org>

    Digest: sha256:bb93aca2282a95f8f1f22679075e757bbdb6164204c8af34102864a5b077b7dc
  Found In: balenalib/nanopc-t4-fedora:31
   Layer #: 0
References: 715
   Created: 2019-06-05T22:43:26.440408184Z
   Content: /bin/sh -c #(nop)  LABEL maintainer=Clement Verna <cverna@fedoraproject.org>

    Digest: sha256:52278dd8e57993669c5b72a9620e89bebdc098f2af2379caaa8945f7403f77a2
  Found In: arm32v7/nginx:1.19.2-alpine
   Layer #: 0
References: 714
   Created: 2020-05-29T21:02:07.502756243Z
   Content: /bin/sh -c #(nop) ADD file:e97bf0d217846312b19a9f7264604851aedd125c23b4d291eed4c69b880dce26 in / 

    Digest: sha256:804555ee037604c40de144f9f8da0d826d38db82f15d74cded32790fe279a8f6
  Found In: mcr.microsoft.com/oryx/build:20200106.1
   Layer #: 0
References: 713
   Created: 2019-12-28T04:23:47.4966447Z
   Content: /bin/sh -c #(nop) ADD file:90a2c81769a336bed3f731f44a385f2a65b0916f517a0b77c06c224579bf9a9a in / 

    Digest: sha256:ff3a5c916c92643ff77519ffa742d3ec61b7f591b6b7504599d95a4a41134e28
  Found In: richarvey/nginx-php-fpm:1.5.1
   Layer #: 0
References: 695
   Created: 2018-01-09T21:10:58.365737589Z
   Content: /bin/sh -c #(nop) ADD file:093f0723fa46f6cdbd6f7bd146448bb70ecce54254c35701feeceb956414622f in / 

    Digest: sha256:970251047358aea56ba6db6975b14ff12470b75de0c2477f4445240ddd727fd4
  Found In: mcr.microsoft.com/dotnet/core/runtime-deps:2.1.14-stretch-slim
   Layer #: 1
References: 686
   Created: 2019-12-28T04:23:47.719507596Z
   Content: /bin/sh -c #(nop)  CMD ["bash"]

    Digest: sha256:d4ba87bb7858f0dd4a60003f011338f3a58b87d0add985652856007fe5ca5034
  Found In: nvcr.io/nvidia/l4t-base:r34.1.1
   Layer #: 0
References: 664
   Created: 2022-04-29T22:49:34.992958516Z
   Content: /bin/sh -c #(nop) ADD file:ccdde790bb849fe101367f2b541f1062b3544d21f99a5acc535bf2b0884cc0eb in / 

    Digest: sha256:d7bfe07ed8476565a440c2113cc64d7c0409dba8ef761fb3ec019d7e6b5952df
  Found In: bioconductor/bioconductor_docker:RELEASE_3_15
   Layer #: 0
References: 632
   Created: 2022-06-06T22:21:11.683921179Z
   Content: /bin/sh -c #(nop) ADD file:00dae10e79b05c4e1a3db053a1f85a4f38a39fe85cbbd88d74201a01a7dd59b5 in / 

    Digest: sha256:abd2c048cba46f85ffcdbd38202d0906c11ea93d39d8ac934411570844119d08
  Found In: balenalib/photon-nano-debian:20240227
   Layer #: 0
References: 625
   Created: 2024-02-13T00:41:34.96456205Z
   Content: /bin/sh -c #(nop) ADD file:ef14ef2abd4725ea6056637e44d9261e2b025853230ea45636b67a735b3d4918 in / 

    Digest: sha256:40a322c395ab3df43e27d8be65cc48139c091588ac868643a02567ca247d0c73
  Found In: balenalib/revpi-connect-4-debian:20240508
   Layer #: 0
References: 624
   Created: 2024-04-24T04:10:54.234410656Z
   Content: /bin/sh -c #(nop) ADD file:e8990741de71fcc1884f30fcd1b6c5ea411bfa752419a82e9748fcd378ca100a in / 

    Digest: sha256:ae0859feeaa49c8802f6aff806ff1412894c5b08c3fcf4d1d75b9edff6c8d861
  Found In: balenalib/revpi-connect-4-debian:20240508
   Layer #: 1
References: 598
   Created: 2024-04-24T04:10:54.597136947Z
   Content: /bin/sh -c #(nop)  CMD ["bash"]

    Digest: sha256:ef2fb7c49f69b9eefb25f02b600342129757e69bb130d53b98ba46ddde18effc
  Found In: balenalib/photon-nano-debian:20240401
   Layer #: 0
References: 624
   Created: 2024-03-12T00:45:51.34944398Z
   Content: /bin/sh -c #(nop) ADD file:e5a8bb54381b61b31ee885b2841ecde6315a03685b0e7f33f736889d8e7768a2 in / 

    Digest: sha256:cbdbe7a5bc2a134ca8ec91be58565ec07d037386d1f1d8385412d224deafca08
  Found In: grafana/grafana:7.0.0-beta3
   Layer #: 0
References: 613
   Created: 2020-04-24T01:05:03.608058404Z
   Content: /bin/sh -c #(nop) ADD file:b91adb67b670d3a6ff9463e48b7def903ed516be66fc4282d22c53e41512be49 in / 

    Digest: sha256:012cb44e32533b8e62587fb98d54517182d9723031be8f9e06a9647ad6b46b61
  Found In: mcr.microsoft.com/powershell:6.1.2-fedora-28
   Layer #: 0
References: 603
   Created: 2019-01-16T21:21:55.569693599Z
   Content: /bin/sh -c #(nop)  LABEL maintainer=Clement Verna <cverna@fedoraproject.org>

    Digest: sha256:b538f80385f9b48122e3da068c932a96ea5018afa3c7be79da00437414bd18cd
  Found In: balenalib/cl-som-imx8-alpine:20200604
   Layer #: 0
References: 602
   Created: 2020-05-29T21:43:19.040389267Z
   Content: /bin/sh -c #(nop) ADD file:7574aee4e37a85460ab889212d52912723a9b30dda1c060548f0deb4a05fc398 in / 

    Digest: sha256:ca426296fe928600d0b4b844aee43e2b70a05c6f4032de5f65dcc49f5cedfd82
  Found In: azul/zulu-openjdk-debian:11.0.21-11.68.17-arm64
   Layer #: 0
References: 600
   Created: 2023-11-21T06:27:20.721480513Z
   Content: /bin/sh -c #(nop) ADD file:7b5bbc3b85f671aaf7b38dbe3fc76aae162bbff29c525bcd127f8a26a53bc664 in / 

    Digest: sha256:fef9491d900a9a262ca6afaa20e9fdc784c635f4ef817a6ba38c61e1174f0d99
  Found In: mdsplus/builder:fc26
   Layer #: 0
References: 598
   Created: 2018-09-07T14:42:43.157088411Z
   Content: /bin/sh -c #(nop)  MAINTAINER [Adam Miller <maxamillion@fedoraproject.org>] [Patrick Uiterwijk <patrick@puiterwijk.org>]

    Digest: sha256:a7f8d3c7de4d035216ab5b8f9d69cbbd09f06b9d1fb06113f55bd89670fe4648
  Found In: arm32v7/buildpack-deps:17.10
   Layer #: 1
References: 593
   Created: 2018-07-17T13:21:29.177725222Z
   Content: /bin/sh -c set -xe 		&& echo '#!/bin/sh' > /usr/sbin/policy-rc.d 	&& echo 'exit 101' >> /usr/sbin/policy-rc.d 	&& chmod +x /usr/sbin/policy-rc.d 		&& dpkg-divert --local --rename --add /sbin/initctl 	&& cp -a /usr/sbin/policy-rc.d /sbin/initctl 	&& sed -i 's/^exit.*/exit 0/' /sbin/initctl 		&& echo 'force-unsafe-io' > /etc/dpkg/dpkg.cfg.d/docker-apt-speedup 		&& echo 'DPkg::Post-Invoke { "rm -f /var/cache/apt/archives/*.deb /var/cache/apt/archives/partial/*.deb /var/cache/apt/*.bin || true"; };' > /etc/apt/apt.conf.d/docker-clean 	&& echo 'APT::Update::Post-Invoke { "rm -f /var/cache/apt/archives/*.deb /var/cache/apt/archives/partial/*.deb /var/cache/apt/*.bin || true"; };' >> /etc/apt/apt.conf.d/docker-clean 	&& echo 'Dir::Cache::pkgcache ""; Dir::Cache::srcpkgcache "";' >> /etc/apt/apt.conf.d/docker-clean 		&& echo 'Acquire::Languages "none";' > /etc/apt/apt.conf.d/docker-no-languages 		&& echo 'Acquire::GzipIndexes "true"; Acquire::CompressionTypes::Order:: "gz";' > /etc/apt/apt.conf.d/docker-gzip-indexes 		&& echo 'Apt::AutoRemove::SuggestsImportant "false";' > /etc/apt/apt.conf.d/docker-autoremove-suggests

    Digest: sha256:d4b47d15749e065d0a65f47b434f099fb66423d2022038bc03b966496fba41dd
  Found In: arm32v7/buildpack-deps:17.10
   Layer #: 2
References: 593
   Created: 2018-07-17T13:21:30.414097504Z
   Content: /bin/sh -c rm -rf /var/lib/apt/lists/*

    Digest: sha256:88159cf8386473438935404ae3388b2c64e93f596b56be73b3e4f15b3ffdc46f
  Found In: arm32v7/buildpack-deps:17.10
   Layer #: 3
References: 593
   Created: 2018-07-17T13:21:31.865118208Z
   Content: /bin/sh -c sed -i 's/^#\s*\(deb.*universe\)$/\1/g' /etc/apt/sources.list

    Digest: sha256:806d9892b0b77043e6019471e61b20ca7de7d33c54841abbcb5a4e9123edbc99
  Found In: arm32v7/buildpack-deps:17.10
   Layer #: 0
References: 593
   Created: 2018-07-17T13:21:27.73537233Z
   Content: /bin/sh -c #(nop) ADD file:a4dc99411ab860d329eab0274053cd2fbe7c42c472f8a63467b5d5f771e48634 in / 

    Digest: sha256:315f43869bb429b821bb0f509894fc274eec98cc92e100582e7e6056f467374b
  Found In: arm32v7/buildpack-deps:17.10
   Layer #: 4
References: 593
   Created: 2018-07-17T13:21:32.877153853Z
   Content: /bin/sh -c mkdir -p /run/systemd && echo 'docker' > /run/systemd/container

    Digest: sha256:f4bb4e8dca02be491b4f72d2ef2127a64ce49c48d0d9c0a0fcaffa625067679d
  Found In: nvcr.io/nvidia/tensorrt:24.04-py3-igpu
   Layer #: 0
References: 592
   Created: 2024-02-27T18:53:22.490310908Z
   Content: /bin/sh -c #(nop)  ARG RELEASE

    Digest: sha256:12f07ff20b502b3ae5f2af821a324b91acb408d6790187420cf8a0619ecdbb52
  Found In: balenalib/beaglebone-green-fedora:29-build
   Layer #: 2
References: 590
   Created: 2019-02-20T13:00:13.192440917Z
   Content: /bin/sh -c #(nop) ADD file:75a904dc30a4c870c164e7973d73396fe333b8bb83f5a448eb97a488419cabb4 in / 

    Digest: sha256:23ae8a7a1e39d43d09a9f8446c585a68a29fb7c3476a0edc112fe8093ae64bb8
  Found In: balenalib/beaglebone-green-fedora:29-build
   Layer #: 3
References: 590
   Created: 2019-02-20T13:00:15.136545681Z
   Content: /bin/sh -c #(nop)  CMD ["/bin/bash"]

    Digest: sha256:1eaf9d5524a11ee829de416b918c79cedd8965fa90575c2478541e758fd29a25
  Found In: balenalib/beaglebone-green-fedora:29-build
   Layer #: 5
References: 590
   Created: 2019-03-06T02:08:22.448200163Z
   Content: /bin/sh -c #(nop)  LABEL io.balena.qemu.version=3.0.0+resin-arm

    Digest: sha256:b37c3c7cdc1c18537455beafb98d784a85f03d13cd4f9fcfd394650602f9c1df
  Found In: balenalib/beaglebone-green-fedora:29-build
   Layer #: 1
References: 590
   Created: 2019-01-17T12:59:45.6524644Z
   Content: /bin/sh -c #(nop)  ENV DISTTAG=f29container FGC=f29 FBR=f29

    Digest: sha256:fb6d7dbc81541e7d928f417112e379651781631cb1afb16c2f614db7620d2485
  Found In: balenalib/beaglebone-green-fedora:29-build
   Layer #: 6
References: 590
   Created: 2019-03-06T02:08:23.775715068Z
   Content: /bin/sh -c #(nop) COPY file:f41cb8a4ab74a9bbe0a5955b10b7df7bdee3fe93f2677c5faea3399f3ac38623 in /usr/bin 

    Digest: sha256:3e6e6508da66d975f0d4749a7c643d482563b168491758a990eb1c016396d895
  Found In: balenalib/beaglebone-green-fedora:29-build
   Layer #: 4
References: 590
   Created: 2019-03-06T02:08:21.663648422Z
   Content: /bin/sh -c #(nop)  LABEL io.balena.architecture=armv7hf

    Digest: sha256:20274425734a05472f3772bae7ce7124a9832f5eb168456d6cb53e92d6e718a8
  Found In: azul/zulu-openjdk:11.0.20-11.66.15-arm64
   Layer #: 0
References: 583
   Created: 2023-08-16T06:19:52.511034945Z
   Content: /bin/sh -c #(nop)  ARG RELEASE

    Digest: sha256:d5a2ad729c09fbfdb259ae764f92188efc67a615ffde9bb34a46298d1edf3cd6
  Found In: nvcr.io/nvidia/tritonserver:24.05-py3-igpu-sdk
   Layer #: 0
References: 581
   Created: 2024-04-27T14:32:22.643440355Z
   Content: /bin/sh -c #(nop)  ARG RELEASE

    Digest: sha256:01eb078129a0d03c93822037082860a3fefdc15b0313f07c6e1c2168aef5401b
  Found In: mdsplus/builder:fc29
   Layer #: 0
References: 571
   Created: 2019-01-16T21:21:55.569693599Z
   Content: /bin/sh -c #(nop)  LABEL maintainer=Clement Verna <cverna@fedoraproject.org>
```
