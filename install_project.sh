#!/bin/bash

# Устанавливаем виртуальное окружение под python3 для запуска
# Устанавливаем виртуальное окружение для разработки.
# Настраиваем pre-commit

VENV_NAME=".venv"

INSTALL=\
`echo "Install virtualenv in $VENV_NAME"
python3 -m venv $VENV_NAME
$VENV_NAME/bin/pip install -r requirements.txt


VENV_DEV_NAME=".venv-dev"`

INSTALL_FOR_DEV=\
`echo "Install dev virtualenv in $VENV_DEV_NAME"
python3 -m venv $VENV_DEV_NAME
$VENV_DEV_NAME/bin/pip install pytest flake8 pre-commit
$VENV_DEV_NAME/bin/pip install -r requirements.txt
$VENV_DEV_NAME/bin/pip install -r requirements-dev.txt

echo "Install .pre-commit"
pre-commit install

echo "Check project"
pre-commit run --all-files`



MENU=(
    "Install Project"
    "Install Project for development"
)
select menu in "${MENU[@]}" ; do
    case $REPLY in
        1) echo $INSTALL;;
        2) echo $INSTALL_FOR_DEV;;
    esac
done

echo "Comleted!"

echo "You may start project by uvicorn: uvicorn main:app --reload"