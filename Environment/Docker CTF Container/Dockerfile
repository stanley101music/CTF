FROM ubuntu:20.04
MAINTAINER stanleymusic

ENV DEBIAN_FRONTEND=noninteractive
ENV LC_ALL=en_US.UTF-8

RUN apt update && \
    apt install -yq gcc && \
    apt install -yq gdb && \
    apt install -yq git && \
    apt install -yq ruby-dev && \
    apt install -yq vim-gtk3 && \
    apt install -yq fish && \
    apt install -yq glibc-source && \
    apt install -yq make && \
    apt install -yq gawk && \
    apt install -yq bison && \
    apt install -yq libseccomp-dev && \
    apt install -yq tmux && \
    apt install -yq wget && \
	apt install -yq locales && \
    locale-gen en_US.UTF-8

# Create symlink for python3 as python
RUN ln -s /usr/bin/python3 /usr/bin/python

# compile glibc-2.31
RUN cd /usr/src/glibc && \
    tar xvf glibc-2.31.tar.xz && \
    mkdir glibc_dbg && \
    cd glibc_dbg && \
    ../glibc-2.31/configure --prefix $PWD --enable-debug && \
    make -j4

# vim theme config
COPY ./vim_config/.vimrc /root/.vimrc

# Pwn
## install pwndbg
RUN git clone https://github.com/pwndbg/pwndbg ~/pwndbg && \
    cd ~/pwndbg && \
    ./setup.sh

## install pwngdb
RUN git clone https://github.com/scwuaptx/Pwngdb.git ~/Pwngdb && \
    cat ~/Pwngdb/.gdbinit >> ~/.gdbinit && \
    sed -i "s/source ~\/peda\/peda.py//g" ~/.gdbinit

## install Peda
RUN git clone https://github.com/longld/peda.git ~/peda

## install GEF
RUN wget -q -O ~/.gdbinit-gef.py https://github.com/hugsy/gef/raw/master/gef.py

## Useful pwn related tools
RUN pip3 install pwntools==4.4.0
RUN gem install seccomp-tools one_gadget
RUN ln -s /usr/local/lib/python3.8/dist-packages/bin/ROPgadget /bin/ROPgadget

## config gdb
COPY ./gdb_config/.gdbinit /root/.gdbinit
COPY ./gdb_config/gdb-peda /usr/bin/gdb-peda
COPY ./gdb_config/gdb-pwndbg /usr/bin/gdb-pwndbg
COPY ./gdb_config/gdb-gef /usr/bin/gdb-gef
RUN chmod +x /usr/bin/gdb-*

# Crypto
RUN mkdir /Crypto

## xortool
RUN pip3 install xortool

## RsaCtfTool
RUN git clone https://github.com/Ganapati/RsaCtfTool.git /Crypto/RsaCtfTool && \
	apt install -yq libgmp3-dev && \
	apt install -yq libmpc-dev && \
	cd /Crypto/RsaCtfTool && \
	pip3 install -r "requirements.txt" && \
	ln -s /Crypto/RsaCtfTool/RsaCtfTool.py /bin/RsaCtfTool

## HashPump
RUN git clone https://github.com/bwall/HashPump.git /Crypto/HashPump && \
	apt install -yq g++ libssl-dev && \
	cd /Crypto/HashPump && \
	make && make install

## hashcat
RUN git clone https://github.com/hashcat/hashcat.git /Crypto/hashcat && \
	cd /Crypto/hashcat && \
	make && make install

## BaseCrack
RUN git clone https://github.com/mufeedvh/basecrack.git /Crypto/basecrack && \
	cd /Crypto/basecrack && \
	pip3 install pillow && \
	pip3 install -r "requirements.txt"

# Web
RUN mkdir /Web

## nmap
RUN apt install -yq nmap

## scrabble
RUN git clone https://github.com/denny0223/scrabble.git /Web/scrabble && \
	ln -s /Web/scrabble/scrabble /bin/scrabble

## sqlmap
RUN git clone --depth 1 https://github.com/sqlmapproject/sqlmap.git /Web/sqlmap-dev && \
	ln -s /Web/sqlmap-dev/sqlmap.py /bin/sqlmap

# Reverse
## ltrace / strace / radare2
RUN apt install -yq ltrace && \
	apt install -yq strace && \
	apt install -yq radare2

# Forensics
Run mkdir /Forensics

## exiftool
RUN wget -q -O /Forensics/Image-ExifTool-12.39.tar.gz https://exiftool.org/Image-ExifTool-12.39.tar.gz && \
	cd /Forensics && \
	gzip -dc Image-ExifTool-12.39.tar.gz | tar -xf - && \
	rm /Forensics/Image-ExifTool-12.39.tar.gz && \
	ln -s /Forensics/Image-ExifTool-12.39/exiftool /bin/exiftool

## binwalk / foremost / fcrackzip / pngcheck
RUN apt install -yq binwalk && \
	apt install -yq foremost && \
	apt install -yq fcrackzip && \
	apt install -yq pngcheck

# Not sure why this folder is created, perhaps due to the different format between windows and linux
RUN rm -rf /'~'

CMD ["/bin/fish"]