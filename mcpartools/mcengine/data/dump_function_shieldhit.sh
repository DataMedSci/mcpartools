function dump_function(){
  RETRY_MAX=5
  ERR="Will check correctness of directories and files"
  COUNT=1
  echo "$ERR"
  while [[ ! -z "$ERR" && "$RETRY_MAX" -ne "$COUNT" ]]; do
    CORRECT=0
    ERR=""
    sleep $COUNT
    for i in $WORKSPACE_DIR/* ; do
      if [ -d "$i" ]; then
        CORRECT=$(($CORRECT + 1))
        echo "Checking $i..."
        BDO_NUM=$(ls -l "$i" | grep ".*.bdo" | wc -l 2>ERR)
        DUMP_SUBDIR=$DUMP_DIR`basename $i`
        if [ "$BDO_NUM" -ne 4 ]; then
          CORRECT=$(($CORRECT - 1))
          LOCAL_ERR="\tInvalid number of .bdo files in $i, should be 4 of them"
          echo -e $LOCAL_ERR
          ERR="$ERR\n$LOCAL_ERR"
        elif [ ! -d "$DUMP_SUBDIR" ]; then
          mkdir $DUMP_SUBDIR
          echo -e "\tCopying files to dump dir..."
	      find "$i" -name "*bdo" -exec cp -- "{}" $DUMP_SUBDIR \;
        fi
      fi
    done
    COUNT=$(($COUNT + 1))
    if [ "$CORRECT" -ge "$MIN_NUM" ]; then
        echo "Found $CORRECT valid jobs for collect"
        return 0
    fi
    if [ ! -z "$ERR" ]; then
      echo "Found $CORRECT valid jobs for collect"
      echo "Left retries: $(($RETRY_MAX - $COUNT))"
      if [ $RETRY_MAX -eq $COUNT ]; then
        echo "Reached maxium number of retries, leaving..."
        exit 1
      fi
    fi
  done

}