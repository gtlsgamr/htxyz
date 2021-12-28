#!/bin/sh
 for i in *;
 do 
	cwebp "$i" -o "${i%.*}.webp"
 done

