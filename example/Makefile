run:
	python main.py
	zip run_manually -@ < not_scored.txt
	@echo "Notebooks that could not run are in run_manually.zip"

md:
	python get_md.py
	words=`wc -l ppl_wo_FR.txt  | cut -f1 -d" "`
		if [ $words -eq 0 ]
	then
		@echo "All students were given a score!"
	else
		zip missing_md -@ < ppl_wo_FR.txt
		@echo "Notebooks that didn't have the correct amount of answers\n are in missing_md.zip"
	fi
