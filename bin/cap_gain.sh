#!/usr/bin/env bash

# Exit if input argument is not specified
if [ -z "$1" ]; then
    echo "Error: No directory argument specified." >&2
    echo "Usage: $0 <directory>" >&2
    exit 1
fi

# Exit if the directory is invalid
if [ ! -d "$1" ]; then
    echo "Error: Directory '$1' is invalid or does not exist." >&2
    exit 1
fi

# 1. Given a Schwab Capital Gain Realized file, split the file based on empty lines
#    This will create multiple files
#
find $1 -regex '.*All_Accounts_GainLoss_Realized.*-.......csv' | xargs split_csv.py > /dev/null 


# 2. The files ending with _1.csv and _3.csv are from the two taxable schwab accounts. Extract
#    the long term and short term capital gain  from them and create ltg.txt and stg.txt
#

find $1 -regex '.*All_Accounts_GainLoss_Realized.*_1.csv' | xargs ext_ltg_from_sch.sh >  ltg.txt 
find $1 -regex '.*All_Accounts_GainLoss_Realized.*_3.csv' | xargs ext_ltg_from_sch.sh >> ltg.txt

find $1 -regex '.*All_Accounts_GainLoss_Realized.*_1.csv' | xargs ext_stg_from_sch.sh >  stg.txt 
find $1 -regex '.*All_Accounts_GainLoss_Realized.*_3.csv' | xargs ext_stg_from_sch.sh >> stg.txt

# 3. Handle Etrade Files
find $1 -name 'GainsAndLossesDowload.csv' -exec get_line.py -f {} "^TAXABLE.*SUMMARY" 2 \; > tmp.txt
ext_ltg_from_etrade.sh tmp.txt >> ltg.txt
ext_stg_from_etrade.sh tmp.txt >> stg.txt

# 4. Add them all up and report it
add.sh ltg.txt
add.sh stg.txt

# 5. Cleanup files
rm ltg.txt stg.txt tmp.txt
