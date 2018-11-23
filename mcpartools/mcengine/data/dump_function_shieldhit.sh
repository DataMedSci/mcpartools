function dump_function(){
    echo -e "\n\t##############################\n"
    echo "THIS FEATURE WILL ONLY WORK CORRECTLY WHEN SECOND ARGUMENT OF NSTAT"
    echo "(Step of saving) IN FILE input/beam.dat IS SET TO -1"
    echo -e "\n\t##############################\n"
    echo "Waiting for results..."
    sleep 10 # waiting 10 sec for results to dump and meantime user can read information

    for i in $WORKSPACE_DIR/* ; do  # Goes through all directories job_* in workspace
      if [ -d "$i" ]; then
        DUMP_SUBDIR=$DUMP_DIR`basename $i`
        mkdir -p $DUMP_SUBDIR
        find "$i" -name "*bdo" -exec cp -- "{}" $DUMP_SUBDIR \; # copy output files to dump directory
        BDO_NUM=$(ls -l "$DUMP_SUBDIR" | grep ".*.bdo" | wc -l 2>/dev/null) # check number of bdo files copied
        if [[ $BDO_NUM -eq 0 ]]; then
            echo "Did not copied any files from `basename $i`. Most probably job has not started yet"
        else
            echo "Copied $BDO_NUM .bdo files from `basename $i` to dump dir..."
        fi
      fi
    done
}