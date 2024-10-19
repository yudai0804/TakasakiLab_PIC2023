# Debian 12以外を使うと今後動かなくなる可能性があるので、latestにはしない
FROM debian:12

RUN apt-get update && apt-get install -y curl procps make python3
RUN dpkg --add-architecture i386 \
    && apt-get update \
    && apt-get install -y libc6:i386 libx11-6:i386 libxext6:i386 libstdc++6:i386 libexpat1:i386
RUN curl -O https://ww1.microchip.com/downloads/en/DeviceDoc/MPLABX-v5.35-linux-installer.tar \
    && tar -xvf MPLABX-v5.35-linux-installer.tar \
    && rm -rf MPLABX-v5.35-linux-installer.tar
RUN USER=root ./MPLABX-v5.35-linux-installer.sh --nox11 -- --unattendedmodeui none --mode unattended \
    && rm -rf MPLABX-v5.35-linux-installer.sh

# Java 8でないと動かないので、Java 8をインストール。
# Java 8は2024年現在でサポート終了しているもののため、今後利用不可、もしくはダウンロードリンクが使えなくなる可能性が高い。
# ダウンロードリンクはhttps://www.java.com/ja/download/のLinux x64をクリックするときのもの
# Oracleのサイトからダウンロードするにはログインする必要があるためやめた。
RUN curl -L -o jre-8u431-linux-x64.tar.gz https://javadl.oracle.com/webapps/download/AutoDL?BundleId=251398_0d8f12bc927a4e2c9f8568ca567db4ee \
    && tar zxvf jre-8u431-linux-x64.tar.gz \
    && rm -rf jre-8u431-linux-x64.tar.gz

ENV IPECMD_JAVA=/jre1.8.0_431/bin/java

WORKDIR /app