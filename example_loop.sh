#!/bin/bash
for (( c=1; c<=5; c++ ))
do  
	python3 toot_spam.py '<login>' '<passwd>' '<instance>' '<text>' '<url_to_img>'
done
