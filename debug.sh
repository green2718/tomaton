rsync -e ssh -av --delete-after --exclude="pienv" --exclude="Photomaton_x1x4x9.py" --exclude="requirement.txt" --exclude="debug.sh" . maton:selfmaton/

ssh maton 'killall python3; cd selfmaton; python3 -m debugpy --listen 0.0.0.0:5678 --wait-for-client main.py '


