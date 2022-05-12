# Crawler Magazinevoce

## Requirements

- [Python 3.x.x](https://www.python.org/downloads/)
- [Anaconda 4.x.x](https://docs.anaconda.com/anaconda/install/)
- [Selenium 4.1.3](https://www.selenium.dev/)

Note: need a correct webdrive to your environment. https://www.selenium.dev/downloads/

## Site

https://www.magazinevoce.com.br/{store name}

### Update requirements.txt

```
 pip3 freeze > requirements.txt
```

### Create env

```
conda create --name <env_name> python=3.8
```

### Active env

```
conda activate fiappy
```

### Deactivate env

```
conda deactivate
```

### Usage

```
python main.py search --store="magazinerayanefreitas" --query="iphone" --browser=false --zipcode=58013130
```
