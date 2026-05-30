#!/usr/bin/env bash

# Takes a file with currency-formatted numbers and adds them together

awk '{
        # print "# " $1

        val = $1

        # 1. Check if the value is parenthesized (accounting negative format)
        is_neg = (val ~ /\(|\)/)

        # 2. Strip currency symbols: $, commas, and parentheses
        gsub(/[$,()]/, "", val)

        # 3. Convert to a numeric value and negate if it was parenthesized
        num = val + 0
        if (is_neg) {
            num = -num
        }

        # 4. Add to sum
        sum += num
    }
    END {
        # Output format with 2 decimal places
        printf "%.2f\n", sum
    }' $1
