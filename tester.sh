#!bin/bash
for k in $(cat strings);do
    echo "-----------String: "$k >> output
    python cyk.py gram2 $k -t >> output
    echo "___________" >> output
done
