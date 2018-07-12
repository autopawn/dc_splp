if (( $# != 0 )); then
    echo "usage: bash solve_problems.sh"
    exit 1
fi

PP="4 8 12 16"
BB="400 140 80 50"

read -p "Delete all problems first [y/n]? " choice
case "$choice" in
  y|Y ) echo "Deleting them." && rm -rf problems;;
  n|N ) echo "Not deleting them.";;
  * ) echo "Invalid answer!" && exit;;
esac

read -p "Delete all results first [y/n]? " choice
case "$choice" in
  y|Y ) echo "Deleting them." && rm -rf results;;
  n|N ) echo "Not deleting them.";;
  * ) echo "Invalid answer!" && exit;;
esac

QSUBPROCS=2
QSUBPROCS_FULLVR=1

LOCALPROCS=2
LOCALPROCS_FULLVR=1

if [ ! -d problems ]; then
    bash _generate_problems.sh "$PP" "$BB"
fi

for pp in $PP; do

    qsub -N pm_lpsolve_p"$pp" _solve_lpsolve.sh -F "$pp $QSUBPROCS pm" || \
        bash _solve_lpsolve.sh "$pp" "$LOCALPROCS" "pm"
    qsub -N splp_lpsolve_p"$pp" _solve_lpsolve.sh -F "$pp $QSUBPROCS splp" || \
        bash _solve_lpsolve.sh "$pp" "$LOCALPROCS" "splp"

    qsub -N pm_dsa50_p"$pp" _solve_dsa.sh -F "$pp $QSUBPROCS_FULLVR pm 50" || \
        bash _solve_dsa.sh "$pp" "$LOCALPROCS_FULLVR" "pm" "50"
    qsub -N splp_dsa50_p"$pp" _solve_dsa.sh -F "$pp $QSUBPROCS_FULLVR splp 50" || \
        bash _solve_dsa.sh "$pp" "$LOCALPROCS_FULLVR" "splp" "50"

    qsub -N pm_dsa200vr400_p"$pp" _solve_dsa.sh -F "$pp $QSUBPROCS pm 200 400" || \
        bash _solve_dsa.sh "$pp" "$LOCALPROCS" "pm" "200" "400"
    qsub -N splp_dsa200vr400_p"$pp" _solve_dsa.sh -F "$pp $QSUBPROCS splp 200 400" || \
        bash _solve_dsa.sh "$pp" "$LOCALPROCS" "splp" "200" "400"

    qsub -N pm_dsa400vr800_p"$pp" _solve_dsa.sh -F "$pp $QSUBPROCS pm 400 800" || \
        bash _solve_dsa.sh "$pp" "$LOCALPROCS" "pm" "400" "800"
    qsub -N splp_dsa400vr800_p"$pp" _solve_dsa.sh -F "$pp $QSUBPROCS splp 400 800" || \
        bash _solve_dsa.sh "$pp" "$LOCALPROCS" "splp" "400" "800"

    # NOTE: ONLY ONE RANDOMHC
    # maxs=$((pp+3))
    # qsub -N pm_randomhc400_p"$pp" _solve_randomhc.sh -F "$pp $QSUBPROCS pm 400 $maxs" || \
    #     bash _solve_randomhc.sh "$pp" "$LOCALPROCS" "pm" "400" "$maxs"
    # qsub -N splp_randomhc400_p"$pp" _solve_randomhc.sh -F "$pp $QSUBPROCS splp 400 $maxs" || \
    #     bash _solve_randomhc.sh "$pp" "$LOCALPROCS" "splp" "400" "$maxs"

done
