#SBATCH -J $NAME
#SBATCH --output=fluka_job_%A_%a.out
#SBATCH --error=fluka_job_%A_%a.err
#SBATCH -N 1
#SBATCH --ntasks-per-node 1
#SBATCH --mem 2000
#SBATCH --time=5:00:00
#SBATCH -A ccbemka
#SBATCH -p plgrid
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=magdalena.klodowska@ifj.edu.pl