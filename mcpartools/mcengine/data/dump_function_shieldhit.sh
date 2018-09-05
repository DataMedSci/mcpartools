function dump_function(){
  echo -e "\n\t##############################\n"
  echo "THIS FUTURE WILL ONLY WORK CORRECTLY WHEN SECOND ARGUMENT OF NSTAT"
  echo "(Step of saving) IN FILE input/beam.dat IS SET TO -1"
  echo -e "\n\t##############################\n"
  sleep 5
  RETRY_MAX=5
  ERR="Will check correctness of directories and files"
  COUNT=1
  echo "$ERR"
  while [[ ! -z "$ERR" && "$RETRY_MAX" -ne "$COUNT" ]]; do
    CORRECT=0
    ERR=""
    sleep $COUNT
    for i in $WORKSPACE_DIR/* ; do  # Goes through all directories job_* in workspace
      if [ -d "$i" ]; then
        CORRECT=$(($CORRECT + 1))
        echo "Checking $i..."
        BDO_NUM=$(ls -l "$i" | grep ".*.bdo" | wc -l 2>ERR)
        DUMP_SUBDIR=$DUMP_DIR`basename $i`
        if [ "$BDO_NUM" -ne 4 ]; then # if number of output files is different than 4 (here 4 .bdo for shieldhit)
          CORRECT=$(($CORRECT - 1))
          LOCAL_ERR="\tInvalid number of .bdo files in $i, should be 4 of them"
          echo -e $LOCAL_ERR
          ERR="$ERR\n$LOCAL_ERR"
        elif [ ! -d "$DUMP_SUBDIR" ]; then         # if number of output files is correct then create subdirectory
          mkdir $DUMP_SUBDIR                       # in dump/<date> with name job_<id_number> with id_number of currently
          echo -e "\tCopying files to dump dir..." # proccess workspace/job_<id> directory and copy output files from that directory
	      find "$i" -name "*bdo" -exec cp -- "{}" $DUMP_SUBDIR \;
        fi
      fi
    done
    COUNT=$(($COUNT + 1))
    if [ "$CORRECT" -ge "$MIN_NUM" ]; then              # if found more than X valid output files where X is given by user as option then
        echo "Found $CORRECT valid jobs for collect"    # return successfully
        return 0
    fi
    if [ ! -z "$ERR" ]; then                        # if did not found satisfying number of valid output files then do a retry
      echo "Found $CORRECT valid jobs for collect"  # or leave if reached maximum number of retries
      echo "Left retries: $(($RETRY_MAX - $COUNT))"
      if [ $RETRY_MAX -eq $COUNT ]; then
        echo "Reached maxium number of retries, leaving..."
        exit 1
      fi
    fi
  done

}