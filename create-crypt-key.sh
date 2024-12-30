#!/bin/bash -e

cd $(dirname "${BASH_SOURCE[0]}")

crypt_key_file="rest/crypt.key"
if [ "$1" = "-f" ]; then
	echo "Overwriting $crypt_key_file"
elif [ -f "$crypt_key_file" ]; then
	echo "$crypt_key_file already exists, skipping"
	exit 0
fi

chars='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
n=16
key=''
for ((i = 0; i < n; ++i)); do
    key+=${chars:RANDOM%${#chars}:1}
done

echo -n "$key" > "$crypt_key_file"
echo "Created $crypt_key_file"
