#!/bin/bash
#SBATCH -A jerin
#SBATCH -n 1
#SBATCG --gres=gpu:0
#SBATCH --mem-per-cpu=2048
#SBATCH --time=1-00:00:00
#SBATCH --mail-type=END

python3 index.py enwiki-20170820-pages-articles15.xml
