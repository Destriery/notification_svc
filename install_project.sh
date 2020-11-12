#!/bin/bash

# Устанавливаем виртуальное окружение под python3 для запуска
# Устанавливаем виртуальное окружение для разработки.
# Настраиваем pre-commit

VENV_NAME=".venv"
VENV_DEV_NAME=".venv-dev"

echo ""
MENU=(
    "Install Project"
    "Install Project for development"
)
select menu in "${MENU[@]}" ; do
    case $REPLY in
        1)
            break
            ;;
        2)
            echo "Install dev virtualenv in $VENV_DEV_NAME"
            python3 -m venv $VENV_DEV_NAME
            $VENV_DEV_NAME/bin/pip install pytest flake8 pre-commit
            $VENV_DEV_NAME/bin/pip install -r requirements.txt
            $VENV_DEV_NAME/bin/pip install -r requirements-dev.txt

            echo "Install pre-commit"
            $VENV_DEV_NAME/bin/pre-commit install

            echo "Check project"
            $VENV_DEV_NAME/bin/pre-commit run --all-files

            break
            ;;
    esac
done

# В любом случае устанавливаем основное окружение

echo ""
echo "Install virtualenv in $VENV_NAME"
echo ""
python3 -m venv $VENV_NAME
$VENV_NAME/bin/pip install -r requirements.txt

echo ""
echo "Comleted!"
echo ""
echo "Start project?"

MENU=(
    "Yes"
    "No"
)
select menu in "${MENU[@]}" ; do
    case $REPLY in
        1)
            .venv/bin/uvicorn main:app --reload
            break
            ;;
        2)
            echo ""
            echo "You may start project by uvicorn: .venv/bin/uvicorn main:app --reload"
            break
            ;;
    esac
done