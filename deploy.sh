#!/bin/bash
fission spec init
fission env create --spec --name post-custody-env --image nexus.sigame.com.br/python-env-3.8:0.0.5 --builder nexus.sigame.com.br/fission-builder-3.8:0.0.1
fission fn create --spec --name post-custody-fn --env post-custody-env --src "./func/*" --entrypoint main.post_user_ticket --executortype newdeploy --maxscale 1
fission route create --spec --name post-custody-route --method POST --url /support/post-ticket-user-custody-transfer --function post-custody-fn
