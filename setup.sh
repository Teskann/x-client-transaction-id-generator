git submodule init
git submodule update
python -mvenv .venv
source ./.venv/bin/activate
pip install -r XClientTransaction/requirements.txt
pip install -r requirements.txt