# RUN: bench --test "bash %s"

r=$((RANDOM % 10))

if [[ $r -lt 9 ]]; then
    sleep 0.5
else
    echo "Aborting"
    exit 1
fi
