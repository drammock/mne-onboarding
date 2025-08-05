default:
	echo No default recipe. Current recipes are: clean

clean:
	rm -rf .ipynb_checkpoints
	rm -rf _build
	rm -rf __pycache__
	rm -f optimization/profile_output.lprof
	rm -f optimization/profile_output*.txt
	rm -f optimization/mprofile_*.dat
	killall -q jupyter-server || true
