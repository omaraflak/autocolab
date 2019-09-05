# autocolab

Run a colaboratory file in a headless browser. This code is using Selenium & Chrome driver.

# Install Requirements

```
pip install -r requirements.txt
```

# Step 0

Add a cell with the following content at the end of your collab file :

```python
print('--end--')
```

This is a flag that the program will look for when executing your colab file. When reached, the program will exit.

# Step 1

Run `auth.py` to save your cookies.

```
python3 auth.py
```

Cookies are saved in a file names `cookies.pkl`

# Step 2

Run `run.py` which will browse your collab page and run the cells

```
python3 run.py
```
